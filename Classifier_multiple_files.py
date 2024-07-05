
 # SMART PDF SORTER - MULTI CLASSIFIERS -BATCH PROCESSOR    
########################################################
""" 
This code works parallelly on several files in a floder to run (one of the many) classification algorithms. A list contains 
the names of the classifiers to choose from. Depending upon which classifier has been chosen, you need to select the relevant
folder (must be a local path in the drive, not a URL) path containing the files that need to be classified. For example, if you 
are using a KID-KIID classifier, then your input floder must contain files that have KID/KIID type documents. Otherwise, the 
classification will not perform optimally. So if you see some errors or mis-classification, it is possible that you didn't feed the 
right kind of files into the classifier.  
 """  
########################################################

import os
from PyPDF2 import PdfReader, PdfWriter
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.exceptions import ResourceNotFoundError
from concurrent.futures import ThreadPoolExecutor, as_completed
from AWSInteraction.EnvVarSetter import EnvVarSetter
from extractors.models import Models
from extractors.general_extractors.config.prompt_config import table_schemas
from extractors.general_extractors import utils

# Initialize and set environment variables
env_setter = EnvVarSetter()
env_setter.configure_local_env_vars()

class Classifier_N_File_Saver:
    def __init__(self, classifier_id, original_pdf_path):
        self.classifier_id = classifier_id
        self.original_pdf_path = original_pdf_path
        self.endpoint = os.environ.get("AZURE_FORM_RECOGNIZER_ENPOINT")
        self.key = os.environ.get("AZURE_FORM_RECOGNIZER_KEY")
        print("Initializing Classifier...")
        print("Model ID:", self.classifier_id)
        if not self.key:
            raise ValueError("Azure Form Recognizer API key is missing or invalid.")
    
    def handle_document_workflow(self):
        """Handles the complete workflow from classifying a document to processing and saving relevant pages using local files."""
        if not self.endpoint or not self.key:
            print("Failed to retrieve endpoint or key from environment variables.")
            return
        
        result = self.classify_and_extract_documents()
        if result and result.documents:
            self.process_and_save_documents(result.documents)
        else:
            print("No documents found in response or failed to classify:", result)

    def classify_and_extract_documents(self):
        """Classifies and extracts documents using Azure Document Intelligence."""
        # print(f"API Key: '{self.key}'")  # Check if the key is correctly retrieved and is a non-empty string
        credential = AzureKeyCredential(self.key)
        client = DocumentIntelligenceClient(endpoint=self.endpoint, credential=credential, api_version='2024-02-29-preview')
        
        try:
            with open(self.original_pdf_path, "rb") as pdf_file:
                poller = client.begin_classify_document(
                    classifier_id=self.classifier_id,
                    classify_request=pdf_file,
                    split="auto",
                    content_type="application/octet-stream"
                )
                result = poller.result()
                print("Document classification successful.")
                self.report_classification_result(result)
                # Explicit check of the result structure
                print(f"Result Type: {type(result)}")
                # print(f"Result: {result}")
                return result
        except ResourceNotFoundError as e:
            print("Model not found. Check the model ID and endpoint.")
            print(e.message)
        except Exception as e:
            print("An error occurred during document classification.")
            print(e)


    def report_classification_result(self, result):
        """Reports the classes, their page ranges, and confidence levels."""
        class_pages = {}
        for document in result.documents:
            doc_type = document.doc_type
            confidence = document.confidence
            for region in document.bounding_regions:
                page_number = region.page_number
                if doc_type not in class_pages:
                    class_pages[doc_type] = {'pages': [], 'confidence': confidence}
                class_pages[doc_type]['pages'].append(page_number)
        
        for doc_type, info in class_pages.items():
            pages = info['pages']
            confidence = info['confidence']
            page_ranges = self.get_page_ranges(pages)
            print(f"Class: {doc_type}, Pages: {page_ranges}, Confidence: {confidence}")

    def get_page_ranges(self, pages):
        """Converts a list of pages into a human-readable range string."""
        pages = sorted(pages)
        ranges = []
        start = pages[0]
        end = pages[0]

        for i in range(1, len(pages)):
            if pages[i] == end + 1:
                end = pages[i]
            else:
                if start == end:
                    ranges.append(f"{start}")
                else:
                    ranges.append(f"{start}-{end}")
                start = pages[i]
                end = pages[i]

        if start == end:
            ranges.append(f"{start}")
        else:
            ranges.append(f"{start}-{end}")

        return ', '.join(ranges)

    def process_and_save_documents(self, documents):
        """Processes classified documents and saves relevant pages into new PDF files based on document type."""
        # Check if documents is a list
        if not isinstance(documents, list):
            print("Error: documents is not a list.")
            return

        # Check if each item in documents has doc_type attribute
        for document in documents:
            if not hasattr(document, 'doc_type'):
                print(f"Error: Document does not have 'doc_type' attribute: {document}")
                return
        
        base_path = 'C://Users//ribhu.kaul//RibhuLLM//TestingMultiClassifier//Output'  # This is the path where the output of the whole program will be stored, change this as per your requirement
        reader = PdfReader(self.original_pdf_path)
        base_file_name = os.path.splitext(os.path.basename(self.original_pdf_path))[0]

        if self.classifier_id == 'KidClassifierCorrected2':
            for idx, document in enumerate(documents):
                doc_type = document.doc_type.upper()
                folder_path = os.path.join(base_path, doc_type)
                os.makedirs(folder_path, exist_ok=True)

                pages = [region.page_number - 1 for region in document.bounding_regions]
                self.save_document_pages(reader, folder_path, base_file_name, pages[0] + 1, pages[-1], f"{idx+1}")

        elif self.classifier_id == '3classifier_class1_3parts_3Companies':
            doc_type_pages = {'NoPart': [], 'Part1': [], 'Part2': []}

            for document in documents:
                doc_type = document.doc_type
                for region in document.bounding_regions:
                    page = region.page_number
                    doc_type_pages[doc_type].append(page)

            for doc_type, pages in doc_type_pages.items():
                if pages:
                    # Extract company name for each set of pages
                    text = utils.get_document_text(self.original_pdf_path)
                    tt = [text[page - 1] for page in pages]  # Adjust page index
                    company_name_object = extract_company_name(tt, company_schema, file_id)
                    company_name = company_name_object.company_name if hasattr(company_name_object, 'company_name') else 'DefaultCompanyName'

                    folder_path = os.path.join(base_path, company_name, doc_type)
                    os.makedirs(folder_path, exist_ok=True)

                    # Sort pages and calculate ranges
                    pages = sorted(pages)
                    ranges = []
                    start = pages[0]
                    end = pages[0]
                    for page in pages[1:]:
                        if page == end + 1:
                            end = page
                        else:
                            ranges.append((start, end))
                            start = end = page
                    ranges.append((start, end))  # add the last range

                    # Save documents based on ranges
                    for start_page, end_page in ranges:
                        identifier = f"{doc_type}_{start_page}-{end_page}"
                        self.save_document_pages(reader, folder_path, base_file_name, start_page, end_page, identifier)


    def save_document_pages(self, reader, folder_path, base_file_name, start_page, end_page, identifier):
        """Saves specified page range from a PDF document to a new file."""
        writer = PdfWriter()
        for page in range(start_page - 1, end_page):  # Adjust indexing for 0-based index
            writer.add_page(reader.pages[page])

        new_file_name = f"{base_file_name}_{identifier}.pdf"
        full_save_path = os.path.join(folder_path, new_file_name)

        try:
            with open(full_save_path, 'wb') as f:
                writer.write(f)
            print(f"Saved document to {full_save_path}")
        except Exception as e:
            print(f"Failed to save document: {e}")

classifier = ['KidClassifierCorrected2', '3classifier_class1_3parts_3Companies'] # These classifiers are trained on a training set in the Azure AI-Document Intelligence Studio

input_path = ["C://Users//ribhu.kaul//RibhuLLM//TestingMultiClassifier//InputFiles_KID_KIID", # Change these paths depending upon the location of relevant files in your drive
              "C://Users//ribhu.kaul//RibhuLLM//TestingMultiClassifier//InputFiles_Parts"]

company_schema = "company_name"  # Schema category
file_id = "unique_identifier_for_file_process"  # Example file identifier, we are not using this in the code, so just pass any string

def extract_company_name(text, company_schema, file_id):
    """Extracts company name from the given text using a predefined schema and tagging mechanism."""
    pydantic_class = table_schemas["it"][company_schema]  # "it" is assumed to be the language or schema category
    raw_extraction = Models.tag(text, pydantic_class, file_id)
    return raw_extraction




t_path = r"C:\Users\ribhu.kaul\RibhuLLM\PageFinder\1ARCA\arca\arca_18.pdf"
t =utils.get_document_text(t_path)
t1 = [t[0], t[1]]

t1_object = extract_company_name(t1, company_schema=company_schema, file_id=file_id)
t1_name = t1_object.company_name if hasattr(t1_object, 'company_name') else 'DefaultCompanyName'

# def process_file(classifier_id, pdf_path):
#     classifier = Classifier_N_File_Saver(classifier_id, pdf_path)
#     result = classifier.classify_and_extract_documents()
#     # Debug print to inspect result
#     # print(f"Result in process_file: {result}")
#     if result:
#         classifier.process_and_save_documents(result.documents)  # Ensure only documents are passed
#     return pdf_path


# def process_directory(directory, classifier_id, max_workers=5):
#     """Process all PDF files in a directory concurrently."""
#     with ThreadPoolExecutor(max_workers=max_workers) as executor:
#         futures = []
#         for file_name in os.listdir(directory):
#             if file_name.lower().endswith('.pdf'):
#                 pdf_path = os.path.join(directory, file_name)
#                 futures.append(executor.submit(process_file, classifier_id, pdf_path))
        
#         for future in as_completed(futures):
#             result = future.result()
#             if result:
#                 print(f"Processed and classified {result}")

# if __name__ == "__main__":
#     process_directory(input_path[1], classifier[1])  # Select the input path for the folder containing the files 
#                                                      # to be classified and the classifier to be used
