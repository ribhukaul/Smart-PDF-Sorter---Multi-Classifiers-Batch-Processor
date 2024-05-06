import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence.models import DocumentAnalysisFeature

# Will need authentication for prod app
# https://medium.com/@tophamcherie/using-python-to-programmatically-authenticate-to-azure-use-resources-6997ff326fb6


def analyze_general_documents(doc_path, specific_pages=None, queries=None):
    """Analyze a document with the Azure Form Recognizer API.

    Args:
        doc_path (str): path to the document to analyze.
        specific_pages (str, optional): specific pages to analyze, indexing starts from 1, can be multiple pages e.g. 2-7.
            Defaults to None.
        language (str, optional): language to help the model to analize, t the moment supported 'en' and 'it'. Defaults to "it".
        

    Returns:
        _type_: _description_
    """


    # Get variables form environment
    endpoint = os.environ.get("AZURE_FORM_RECOGNIZER_ENPOINT")
    key = os.environ.get("AZURE_FORM_RECOGNIZER_KEY")

    # create your `DocumentAnalysisClient` instance and `AzureKeyCredential` variable
    document_analysis_client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    add_args = {}
    if queries is not None:
        add_args = {
            "features": [DocumentAnalysisFeature.QUERY_FIELDS],
            "query_fields": queries
        }


    with open(doc_path, "rb") as pdf_file:
        # Analyze full document or specific pages
        if specific_pages is None:
            poller = document_analysis_client.begin_analyze_document(
                "prebuilt-layout", analyze_request=pdf_file, content_type='application/octet-stream', **add_args)
            
        else:
            poller = document_analysis_client.begin_analyze_document(
                "prebuilt-layout",
                pdf_file,
                content_type='application/octet-stream',
                pages=specific_pages, **add_args
            )

        result = poller.result()

    return result




if __name__ == "__main__":
    path = "data\\Called\\US21036PAL22 des.png"
    analyze_general_documents(path)

