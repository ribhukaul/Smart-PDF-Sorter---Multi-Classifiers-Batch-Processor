
from langchain_core.pydantic_v1 import BaseModel, Field


class DocLanguage(BaseModel):
    language: str = Field(..., description="language of the document", enum=["it", "en", "fr", "de", "es"])


class IsFirstPage(BaseModel):
    is_first_page: bool = Field(..., description="True if the page is the first one, False otherwise")
