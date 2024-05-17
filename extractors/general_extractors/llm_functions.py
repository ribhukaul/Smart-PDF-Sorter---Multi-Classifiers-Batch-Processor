from extractors.general_extractors.config.prompt_config import prompts, table_schemas, word_representation
from extractors.general_extractors.utils import select_desired_page
from extractors.general_extractors.utils import num_tokens_from_string
from langchain.prompts import PromptTemplate
#from .config.tags import *
from extractors.configs.extraction_config.tags.general_tags import DocLanguage

from ..models import Models

# Reviw change and swap to simple TAG
def get_doc_language(pages, file_id):
    """Get the language of the document.

    Args:
        pages (lst): list of pages text
        file_id (str): file_id for costs

    Returns:
        str: language of the document
    """
    # Analyze first page
    page = pages[0].page_content[:500]
    language = Models.tag(page, DocLanguage, file_id, model="gpt-3.5-turbo")

    # Check if language is mapped
    # NOTE: need to add more languages
    doc_language = language.language
    if doc_language not in ["it", "en", "fr", "de", "es"]:
        doc_language = "it"

    return doc_language


def llm_extraction(page, type, file_id, language="it", model="gpt-4-turbo", rhp=None):
    """extracts data from a document text

    Args:
        page ([str]): page in which data is found
        type (str): type of data to extract
        file_id (str): file_id for costs
        language (str): language of the document
        model (str, optional): model to use for extraction. Defaults to 'gpt-4'.
        rhp (str, optional): rhp of the document. Defaults to None.

    Returns:
        dict(): data extracted
    """
    template = prompts[language][type]
    if rhp is not None:
        input_variables = ["rhp", "context"]
    else:
        input_variables = ["context"]
    prompt = PromptTemplate(input_variables=input_variables, template=template)
    # Select model size based on context
    if model == "gpt-3.5-turbo":
        total_token = num_tokens_from_string(prompt.template.format(context=page))
        if total_token > 4000:
            model = "gpt-3.5-turbo-16k"
        else:
            model = "gpt-3.5-turbo"
    # Construct chain and extract relevan info
    response = Models.extract(file_id, model, prompt, [page], rhp)
    return response


def general_table_inspection(
    table, table_type, file_id, language="it", add_text=""
):
    """tags data in a table

    Args:
        table (dataframe): dataframe to tag
        table_type (str): type of data to extract
        file_id (str): file_id for costs
        language (str, optional): language of the doc. Defaults to 'it'.
        add_text (str, optional): text to add in case. Defaults to "".

    Returns:
        dict: extracted data
    """
    try:
        schema = table_schemas[language][table_type]

        # First normal extraction, then tagging
        tag_model = "gpt-4-turbo"
        if add_text != "":
            table = f"considera questo quando analizzi la tabella=-> {add_text} TABELLA-> {table}"

        extraction_adapted = Models.tag(table, schema, file_id, model=tag_model)
    except Exception as error:
        print("table extraction error" + repr(error))
        extraction_adapted = {"ERROR": "ERROR"}

    return extraction_adapted


def complex_table_inspection(table, rhp, type, file_id, direct_tag=True, language="it"):
    """
    searches table for information
    saves excel file with table in tmp to get around llm bug with incomplete stringified dataframe
    llm extraction first if direct_tag is false
    Args:
        table (pandas dataframe): dataframe to search
        rhp (str): rhp to insert
        type (str): type of data to extract
        file_id (str): file_id for costs
        direct_tag (bool, optional): if skip llm extraction. Defaults to True.
        language (str, optional): language of the doc. Defaults to 'it'.

    Returns:
        dict: extracted data
    """

    try:
        #table = table.to_string()
        from extractors.general_extractors.utils import upload_df_as_excel
        table = upload_df_as_excel(table)
        schema = table_schemas[language][type]

        # First normal extraction, then tagging
        tag_model = "gpt-4-turbo"
        if not direct_tag:
            table = llm_extraction(table, type, file_id, language=language, model=tag_model, rhp=rhp)

        if rhp is None:
            adapt_extraction = "CONSIDERA 1 ANNO , EXTRACTION={}".format(table)
        else:
            adapt_extraction = "RHP={} EXTRACTION={}".format(rhp, table)
        extraction_adapted = Models.tag(adapt_extraction, schema, file_id, model=tag_model)
    except Exception as error:
        print("table extraction error" + repr(error))
        extraction_adapted = {"ERROR": "ERROR"}
        
    return extraction_adapted


def tag_only(pages, type, language, file_id, rhp="multiple"):
    """
    Extracts basic information from a document, the basic information are the ones contained
    in the InformazioniBase class.

    Args:
        pages (): The text of the document to extract information from.
        lan (str, optional): The language of the document. Defaults to 'it'.
        file_id (str): file_id for costs

    Returns:
        str: The extracted basic information.
    """
    # Select page with RIY
    keywords = word_representation[language][type]
    page = select_desired_page(pages, keywords)
    page = pages[int(page)]

    pydantic_class = table_schemas[language][type]

    # To ensure optimal data standardization
    total_prompt = "RHP={} EXTRACTION={}".format(rhp, page.page_content)
    extraction = Models.tag(total_prompt, pydantic_class, file_id)

    return extraction


def llm_extraction_and_tag(pages, language, type, file_id, specific_page=None):
    """
    extracts information from pages using a language model and tags it using a schema
    creates prompt and schema based on language and type

    Args:
        pages (): The text of the document to extract information from.
        language (str, optional): The language of the document. Defaults to 'it'.
        type (str): type of data to extract
        file_id (str): file_id for costs

    Returns:
        str: The extracted basic information.
    """
    # Create template
    template = prompts[language][type]
    pydantic_class = table_schemas[language][type]
    prompt = PromptTemplate(input_variables=["context"], template=template)
    if specific_page is not None:
        pages = [pages[specific_page]]
    # Select model size based on context
    total_token = num_tokens_from_string(prompt.template.format(context=pages))
    if total_token > 4000:
        model = "gpt-3.5-turbo-16k"
    else:
        model = "gpt-3.5-turbo"
    # Construct chain and extract relevan info
    extraction = Models.extract(file_id, model, prompt, pages)

    # To ensure optimal data standardization
    tagged = Models.tag(extraction, pydantic_class, file_id)

    return tagged
