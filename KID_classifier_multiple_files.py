# The code below serially performs classification (using KidClassifierCorrected2 model in Document Intelligence) on 
# the files given in a folder one by one and seperates each file based on the doument classification inside that file (KID or KIID)
# and goes on to store the seperated files in KID or KIID folders.
import os
from PyPDF2 import PdfReader, PdfWriter
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.exceptions import ResourceNotFoundError
from AWSInteraction.EnvVarSetter import EnvVarSetter

# Setting up environment variables
env_setter = EnvVarSetter()
env_setter.configure_local_env_vars()

class Classifier:
    def __init__(self, classifier_id, original_pdf_path):
        self.classifier_id = classifier_id
        self.original_pdf_path = original_pdf_path
        self.endpoint = os.environ.get("AZURE_FORM_RECOGNIZER_ENPOINT")
        self.key = os.environ.get("AZURE_FORM_RECOGNIZER_KEY")

    def classify_and_extract_documents(self):
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
                return result
        except ResourceNotFoundError as e:
            print("Model not found. Check the model ID and endpoint.")
            print(e.message)
        except Exception as e:
            print("An error occurred during document classification.")
            print(e)

    def save_document_pages(self, pages, save_path):
        reader = PdfReader(self.original_pdf_path)
        writer = PdfWriter()
        for page_number in pages:
            writer.add_page(reader.pages[page_number])
        with open(save_path, 'wb') as f:
            writer.write(f)
        print(f"Saved document to {save_path}")

    def process_documents(self, classification_result):
        base_path = r'C:\Users\ribhu.kaul\RibhuLLM\KID_Classifier\Separated_Files'
        doc_counter = {}  # Dictionary to keep track of document counts

        for document in classification_result.documents:
            doc_type = document.doc_type.upper()
            folder_path = os.path.join(base_path, doc_type)
            os.makedirs(folder_path, exist_ok=True)

            base_file_name = os.path.splitext(os.path.basename(self.original_pdf_path))[0]
            doc_type_key = f"{base_file_name}_{doc_type}"
            doc_counter[doc_type_key] = doc_counter.get(doc_type_key, 0) + 1

            file_name = f"{base_file_name}_{doc_type}_{doc_counter[doc_type_key]}.pdf"
            save_path = os.path.join(folder_path, file_name)

            if not os.path.exists(save_path):
                self.save_document_pages([region.page_number - 1 for region in document.bounding_regions], save_path)

def process_directory(directory, classifier_id):
    for file_name in os.listdir(directory):
        if file_name.lower().endswith('.pdf'):
            pdf_path = os.path.join(directory, file_name)
            classifier = Classifier(classifier_id, pdf_path)
            result = classifier.classify_and_extract_documents()
            if result:
                classifier.process_documents(result)
            else:
                print(f"No classification result for {file_name}")

if __name__ == "__main__":
    process_directory(r"C:\Users\ribhu.kaul\RibhuLLM\KID_Classifier\kid_uniti", "KidClassifierCorrected2")


############################################### Attempting parallel processing of the above code
# import os
# import logging
# from concurrent.futures import ThreadPoolExecutor, as_completed
# from PyPDF2 import PdfReader, PdfWriter
# from azure.core.credentials import AzureKeyCredential
# from azure.ai.documentintelligence import DocumentIntelligenceClient
# from azure.core.exceptions import ResourceNotFoundError
# from AWSInteraction.EnvVarSetter import EnvVarSetter

# # Set up logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# # Initialize and set environment variables
# env_setter = EnvVarSetter()
# env_setter.configure_local_env_vars()

# class Classifier:
#     def __init__(self, classifier_id, original_pdf_path):
#         self.classifier_id = classifier_id
#         self.original_pdf_path = original_pdf_path
#         self.endpoint = os.environ.get("AZURE_FORM_RECOGNIZER_ENPOINT")
#         self.key = os.environ.get("AZURE_FORM_RECOGNIZER_KEY")

#         if not self.endpoint or not self.key:
#             raise ValueError("Azure credentials are not set properly.")
        
#         logging.info(f"Initializing Classifier for file: {original_pdf_path}")
#         logging.info(f"Model ID: {self.classifier_id}, Endpoint: {self.endpoint}, API Key: {self.key}")

#     def classify_and_extract_documents(self):
#         credential = AzureKeyCredential(self.key)
#         client = DocumentIntelligenceClient(endpoint=self.endpoint, credential=credential, api_version='2024-02-29-preview')
        
#         try:
#             with open(self.original_pdf_path, "rb") as pdf_file:
#                 poller = client.begin_classify_document(
#                     classifier_id=self.classifier_id,
#                     classify_request=pdf_file,
#                     split="auto",
#                     content_type="application/octet-stream"
#                 )
#                 result = poller.result()
#                 logging.info("Document classification successful.")
#                 return result
#         except ResourceNotFoundError as e:
#             logging.error("Model not found. Check the model ID and endpoint.")
#             logging.error(e.message)
#         except Exception as e:
#             logging.error("An error occurred during document classification.")
#             logging.error(str(e))

#     def process_and_save_documents(self, classification_result):
#         if not classification_result or not classification_result.documents:
#             logging.info("No documents found or failed to classify.")
#             return
        
#         base_path = r'C:\Users\ribhu.kaul\RibhuLLM\KID_Classifier\Separated_Files'
#         for document in classification_result.documents:
#             doc_type = document.doc_type.upper()
#             folder_path = os.path.join(base_path, doc_type)
#             os.makedirs(folder_path, exist_ok=True)
            
#             pages = [region.page_number - 1 for region in document.bounding_regions]
#             file_name = f"{os.path.splitext(os.path.basename(self.original_pdf_path))[0]}_{document.doc_type}.pdf"
#             save_path = os.path.join(folder_path, file_name)
            
#             if not os.path.exists(save_path):
#                 self.save_document_pages(pages, save_path)
#                 logging.info(f"Saved document to {save_path}")
#             else:
#                 logging.info(f"File already exists: {save_path}")

#     def save_document_pages(self, pages, save_path):
#         reader = PdfReader(self.original_pdf_path)
#         writer = PdfWriter()
#         for page_number in pages:
#             writer.add_page(reader.pages[page_number])
#         with open(save_path, 'wb') as f:
#             writer.write(f)

# def process_directory(directory, classifier_id, max_workers=5):
#     with ThreadPoolExecutor(max_workers=max_workers) as executor:
#         futures = []
#         for file_name in os.listdir(directory):
#             if file_name.lower().endswith('.pdf'):
#                 pdf_path = os.path.join(directory, file_name)
#                 classifier = Classifier(classifier_id, pdf_path)
#                 futures.append(executor.submit(classifier.classify_and_extract_documents))
        
#         for future in as_completed(futures):
#             result = future.result()
#             if result:
#                 classifier.process_and_save_documents(result)

# if __name__ == "__main__":
#     directory_path = r"C:\Users\ribhu.kaul\RibhuLLM\KID_Classifier\kid_uniti"
#     classifier_id = "KidClassifierCorrected2"
#     process_directory(directory_path, classifier_id, max_workers=10)
