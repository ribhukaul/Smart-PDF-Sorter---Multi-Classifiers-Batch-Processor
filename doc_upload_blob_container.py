#################### This code works perfectly to reach out the KidClassifierCorrected2 method in Azure Doc Intel
from azure.core.credentials import AzureKeyCredential
# from azure.ai.formrecognizer import DocumentAnalysisClient
# from azure.ai.formrecognizer import DocumentModelAdministrationClient
# import requests
# # Replace with your actual endpoint and key
# endpoint = "https://diapplicativotest.cognitiveservices.azure.com/"
# key = "7f56a184a6144306a71a71bd9e7b3c30"
# credential = AzureKeyCredential(key)

# # Replace with your custom model ID
# model_id = "KidClassifierCorrected2"

# # Local file path
# file_path = "C://Users//ribhu.kaul//RibhuLLM//KID_Classifier//priipkid//priipkid_IE0004GRNWK7.pdf"

# # Create a client
# # document_analysis_client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))


# # Construct the URL for the GET request
# url = f"{endpoint}/documentintelligence/documentClassifiers/{model_id}?api-version=2024-02-29-preview"

# # Set up the header with your API key
# headers = {
#     "Ocp-Apim-Subscription-Key": key
# }

# # Make the GET request
# response = requests.get(url, headers=headers)

# # Check if the request was successful
# if response.status_code == 200:
#     # Print classifier details
#     classifier_details = response.json()
#     print(classifier_details)
# else:
#     # Print error details
#     print(f"Error: {response.status_code}")
#     print(response.json())






########################### The code given below is the 1st step in KID/KIID classification. This code uploads the document 
# into the blob-container given in the Azure Document Intelligence
import os
import pandas as pd
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence.models import ClassifyDocumentRequest
from extractors.general_extractors.utils import format_pages_num


from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

def upload_file_to_blob(file_path, container_name, blob_name, connection_string):
    try:
        # Create a blob service client to interact with the blob storage
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Get a client to interact with the specific container
        container_client = blob_service_client.get_container_client(container_name)
        
        # Create the container if it does not exist
        try:
            container_client.create_container()
            print(f"Container '{container_name}' created.")
        except Exception as e:
            print(f"Container '{container_name}' already exists or cannot be created: {str(e)}")

        # Get a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

        # Upload the file
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
            print(f"File {file_path} uploaded to {container_name}/{blob_name}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Variables for the upload
connection_string = "DefaultEndpointsProtocol=https;AccountName=kidseparatorstorage;AccountKey=Cdt0FZ4tkV6OMVKENHBzn90uWEqa3cVP9s87Wc3PWZx02NYqf076RHyFPhDKmDkN2rlkOCiBTdYF+AStOyuzQA==;EndpointSuffix=core.windows.net"
container_name = "kidseparator"
file_path = r'C:\Users\ribhu.kaul\RibhuLLM\KID_Classifier\priipkid\priipkid_IT0000380649_PAC2X.pdf'
blob_name = "RibhuClassifier/priipkid_IT0000380649_PAC2X"

# Upload the file
upload_file_to_blob(file_path, container_name, blob_name, connection_string)




