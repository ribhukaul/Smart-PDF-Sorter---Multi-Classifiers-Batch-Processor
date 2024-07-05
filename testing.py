from typing import Optional
from pydantic import BaseModel, Field
from langchain.chains.openai_functions.tagging import create_tagging_chain_pydantic
from extractors.general_extractors import utils

NF = "not found"
NA = "N/A"
companies = ["Anima", "Arca", "Eurizon", "Euromobiliare"]

class CompanyNameSchema(BaseModel):
    company_name: str = Field(NF, description="dal documento, estrarre il nome dell'azienda", enum=companies)

table_schemas1 = {
    "it": {
        "company_name": CompanyNameSchema
    }
}

class Models:
    @staticmethod
    def tag(text, schema, file_id):
        # Assuming llm_tag is defined somewhere in your context
        llm_tag = None  # Replace with actual LLM tagging logic if applicable

        # Debug print statements
        print(f"Schema being used: {schema}")
        print(f"Schema is a subclass of BaseModel: {issubclass(schema, BaseModel)}")

        # Create the tagging chain
        chain = create_tagging_chain_pydantic(pydantic_schema=schema, llm_tag=llm_tag)
        return chain.run(text)

def extract_company_name(text, company_schema, file_id):
    """Extracts company name from the given text using a predefined schema and tagging mechanism."""
    pydantic_class = table_schemas1["it"][company_schema]

    # Debug print statement
    print(f"Extracted schema class: {pydantic_class}")
    
    if not issubclass(pydantic_class, BaseModel):
        raise TypeError(f"{pydantic_class} is not a subclass of BaseModel")

    raw_extraction = Models.tag(text, pydantic_class, file_id)
    return raw_extraction

# Example usage
t_path = r"C:\Users\ribhu.kaul\RibhuLLM\PageFinder\1ARCA\arca\arca_18.pdf"
t = utils.get_document_text(t_path)
t1 = [t[0], t[1]]

t1_object = extract_company_name(t1, company_schema="company_name", file_id="unique_identifier_for_file_process")
t1_name = t1_object.company_name if hasattr(t1_object, 'company_name') else 'DefaultCompanyName'
print(t1_name)
