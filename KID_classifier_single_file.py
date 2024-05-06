import os
from PyPDF2 import PdfReader, PdfWriter
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.exceptions import ResourceNotFoundError
from AWSInteraction.EnvVarSetter import EnvVarSetter


env_setter = EnvVarSetter()
env_setter.configure_local_env_vars()



class Classifier:
    def __init__(self, classifier_id, original_pdf_path):
        self.classifier_id = classifier_id
        self.original_pdf_path = original_pdf_path
        self.endpoint = os.environ.get("AZURE_FORM_RECOGNIZER_ENPOINT")  # Check this name
        self.key = os.environ.get("AZURE_FORM_RECOGNIZER_KEY")

        # Print diagnostic information to verify the configuration
        print("Initializing Classifier...")
        # print("Endpoint:", self.endpoint)
        # print("API Key:", self.key)
        print("Model ID:", self.classifier_id)

    def handle_document_workflow(self):
        """Handles the complete workflow from classifying a document to processing and saving relevant pages using local files."""
        if not self.endpoint or not self.key:
            print("Failed to retrieve endpoint or key from environment variables.")
            return

        result = self.classify_and_extract_documents()  # No arguments needed here

        if result and result.documents:
            self.process_and_save_documents(result.documents)
        else:
            print("No documents found in response or failed to classify:", result)

    def classify_and_extract_documents(self):
        """Classifies and extracts documents using Azure Document Intelligence."""
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
                # print("Classification result:", result)  # Print the classification result
                return result
        except ResourceNotFoundError as e:
            print("Model not found. Check the model ID and endpoint.")
            print(e.message)
        except Exception as e:
            print("An error occurred during document classification.")
            print(str(e))

    def process_and_save_documents(self, documents):
        """Processes classified documents and saves relevant pages into new PDF files based on document type."""
        base_path = r'C:\Users\ribhu.kaul\RibhuLLM\KID_Classifier\Separated_Files'

        for idx, document in enumerate(documents):
            doc_type = document.doc_type.upper()
            folder_path = os.path.join(base_path, doc_type)
            os.makedirs(folder_path, exist_ok=True)

            pages = [region.page_number - 1 for region in document.bounding_regions]

            # Call save_document_pages with an index to create unique file names
            self.save_document_pages(pages, folder_path, idx+1)  # idx+1 to start numbering from 1

    def save_document_pages(self, pages, folder_path, document_number):
        """Saves specified pages from a PDF document to a new file."""
        reader = PdfReader(self.original_pdf_path)
        writer = PdfWriter()

        for page in pages:
            writer.add_page(reader.pages[page])

        # Extract base file name without extension
        base_file_name = os.path.splitext(os.path.basename(self.original_pdf_path))[0]

        # Construct new file name using the base name and document number
        new_file_name = f"{base_file_name}_{document_number}.pdf"
        full_save_path = os.path.join(folder_path, new_file_name)

        with open(full_save_path, 'wb') as f:
            writer.write(f)
        print(f"Saved document to {full_save_path}")





# Usage of the Classifier class
if __name__ == "__main__":
    # Parameters for the Classifier
    classifier_id = "KidClassifierCorrected2"
    original_pdf_path = "C://Users//ribhu.kaul//RibhuLLM//KID_Classifier//kid_uniti//kidnkiid1.pdf"
   

    # Create an instance of the Classifier
    classifier = Classifier(classifier_id, original_pdf_path)

    # Handle the document workflow
    # classifier.handle_document_workflow()
    classifier.classify_and_extract_documents()










