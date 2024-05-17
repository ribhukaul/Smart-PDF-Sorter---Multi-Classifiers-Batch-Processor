import os
import pandas as pd
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from PyPDF2 import PdfReader, PdfWriter
from extractors.general_extractors.utils import format_pages_num
 #from azure.ai.formrecognizer import DocumentAnalysisClient

# Will need authentication for prod app
# https://medium.com/@tophamcherie/using-python-to-programmatically-authenticate-to-azure-use-resources-6997ff326fb6


def analyze_general_documents(
    doc_path, specific_pages=None, language="it", api_version="2024-02-29-preview", query_list=None
):
    """Analyze a document with the Azure Form Recognizer API.

    Args:
        doc_path (str): path to the document to analyze.
        specific_pages (str, optional): specific pages to analyze, indexing starts from 1, can be multiple pages e.g. 2-7.
            Defaults to None.
        language (str, optional): language to help the model to analize, t the moment supported 'en' and 'it'. Defaults to "it".

    Returns:
        _type_: _description_
    """
    language_locale_config = {
        "it": "it-IT",
        "en": "en-US",
    }
    language_locale = language_locale_config[language]

    # Get variables form environment
    endpoint = os.environ.get("AZURE_FORM_RECOGNIZER_ENPOINT")
    key = os.environ.get("AZURE_FORM_RECOGNIZER_KEY")

    # create your `DocumentIntelligenceClient` instance and `AzureKeyCredential` variable
    document_analysis_client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key), api_version=api_version
    )
    #document_analysis_client = DocumentAnalysisClient(endpoint, AzureKeyCredential(key), api_version=api_version)
    features_chosen = ["ocrHighResolution"]
    if query_list is not None:
        features_chosen.append("queryFields")

    specific_pages = format_pages_num(specific_pages)

    with open(doc_path, "rb") as pdf_file:
        # Analyze full document or specific pages
        poller = document_analysis_client.begin_analyze_document(
            analyze_request=pdf_file,
            content_type="application/octet-stream",
            model_id="prebuilt-layout",
            locale=language_locale,
            features=features_chosen,
            query_fields=query_list,
            pages=specific_pages,
        )
        result = poller.result()
    return result


def table_json_to_df(json_data):
    """Converts a table json to a pandas dataframe

    Args:
        json_data (_type_): _description_
    """

    # Transform to dict
    rows_data = {}

    # Iterate over cells and group them by row index
    for cell in json_data.cells:
        row_index = cell.row_index
        if row_index not in rows_data:
            rows_data[row_index] = []
        rows_data[row_index].append(cell.content)

    # Convert the dictionary to a sorted list of rows
    rows = [rows_data[row_index] for row_index in sorted(rows_data)]

    # Create DataFrame from rows
    df = pd.DataFrame(rows)

    return df


def get_tables_from_doc(
    doc_path, specific_pages=None, language="it", api_version="2024-02-29-preview", query_list=None
):
    """Get tables from a document, can be used generally to save, or directly for query_list, in that case, return query_list also

    Args:
        doc_path (str): path to the document to analyze.
        specific_pages (str, optional): specific pages to analyze, indexing starts from 1, can be multiple pages e.g. 2-7.
            Defaults to None.
        language (str, optional): language to help the model to analize, t the moment supported 'en' and 'it'. Defaults to "it".

    Returns:
        dataframe[]: tables
    """
    # Analyze document
    result = analyze_general_documents(
        doc_path, specific_pages=specific_pages, language=language, api_version=api_version, query_list=query_list
    )
    # Get tables
    df_tables = []
    for table in result.tables:
        df_tab = table_json_to_df_v2(table)
        df_tables.append(df_tab)

    if query_list:
        return df_tables, result.documents[0].fields

    return df_tables, result



def table_json_to_df_v2(tab):

    num_rows = tab.row_count
    num_columns = tab.column_count
    columns = [""] * num_columns
    df = pd.DataFrame(columns=columns, index=range(0, num_rows))

    # Set headers
    for cell in tab.cells:
        row = cell.row_index
        col = cell.column_index
        col_span = cell.column_span
        row_span = cell.row_span

        content = cell.content
        # convert None to 0
        col_span = 0 if col_span is  None else col_span
        row_span = 0 if row_span is  None else row_span
        df.iloc[row : row + row_span+1, col : col + col_span+1] = content

    return df


