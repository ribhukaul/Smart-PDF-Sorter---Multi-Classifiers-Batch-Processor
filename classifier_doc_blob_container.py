from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta
from azure.ai.documentintelligence.models import SplitMode
import os
from PyPDF2 import PdfWriter, PdfReader



# Generate SAS Token for the blob
def generate_sas_url():
    account_name = 'kidseparatorstorage'
    account_key = 'Cdt0FZ4tkV6OMVKENHBzn90uWEqa3cVP9s87Wc3PWZx02NYqf076RHyFPhDKmDkN2rlkOCiBTdYF+AStOyuzQA=='
    container_name = 'kidseparator'
    blob_name = 'RibhuClassifier/priipkid_IT0000380649_PAC2X'
    sas_token = generate_blob_sas(
        account_name=account_name,
        container_name=container_name,
        blob_name=blob_name,
        account_key=account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1)  # Token valid for 1 hour
    )
    return f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"


#############################################################################
# This code works perfectly, it takes the file from bolb container and classifies it into KID/KIID using custom classifier
# from azure doc intelligence
def save_document_pages(pdf_path, pages, save_path):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    
    for page in pages:
        writer.add_page(reader.pages[page - 1])  # Adjusting for 0-based indexing of the reader.pages list

    with open(save_path, 'wb') as f:
        writer.write(f)
    print(f"Saved document to {save_path}")


def process_documents(documents, original_pdf_path):
    base_path = r'C:\Users\ribhu.kaul\RibhuLLM\KID_Classifier\Separated_Files'
    
    for idx, document in enumerate(documents):
        doc_type = document.doc_type.upper()  # 'doc_type' attribute used from the actual API response
        folder_path = os.path.join(base_path, doc_type)
        os.makedirs(folder_path, exist_ok=True)
        
        file_name = f"Document_{idx + 1}_{doc_type}.pdf"
        save_path = os.path.join(folder_path, file_name)
        
        pages = [region.page_number - 1 for region in document.bounding_regions]
        save_document_pages(original_pdf_path, pages, save_path)

def classify_and_extract_documents(endpoint, key, classifier_id, document_url, original_pdf_path):
    credential = AzureKeyCredential(key)
    client = DocumentIntelligenceClient(endpoint=endpoint, credential=credential, api_version='2024-02-29-preview')

    classify_request = {
        "urlSource": document_url
    }

    try:
        poller = client.begin_classify_document(
            classifier_id=classifier_id,
            classify_request=classify_request,  
            split="auto",
            content_type="application/json"
        )
        result = poller.result()

        if result.documents:
            process_documents(result.documents, original_pdf_path)
        else:
            print("No documents found in response:", result)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Example usage
endpoint = "https://diapplicativotest.cognitiveservices.azure.com/"
key = "7f56a184a6144306a71a71bd9e7b3c30"
classifier_id = "KidClassifierCorrected2"
document_url = generate_sas_url()
original_pdf_path = r'C:\Users\ribhu.kaul\RibhuLLM\KID_Classifier\priipkid\priipkid_IT0000380649_PAC2X.pdf'


  

classify_and_extract_documents(endpoint, key, classifier_id, document_url, original_pdf_path)