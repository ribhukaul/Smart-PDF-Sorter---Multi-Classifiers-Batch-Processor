

from extractors.models import Models
from extractors.general_extractors.extractor import Extractor
from .complexity_custom.setting.pydantic_schema import PydanticSchema_unicredit_noLangChain
import os
from langchain_core.prompts import PromptTemplate
from .complexity_custom.setting.column_config import column_dict, columns_to_clean, columns_to_date_convert, new_df_renaming

import pandas as pd
from .complexity_custom.setting.functions import get_new_column_name, truncate, clean_value, convert_date
from .complexity_custom.postprocessing.dataintegration import df_dataintegration


class WamDerivatiComplexity(Extractor):

    def __init__(self, doc_path, predefined_language=False):
        super().__init__(doc_path, predefined_language)

    
    def process(self):


        system_message = "You are a helpful extractor of data from document"
        human_message =  """At the beginnig I will tell you some information that will be useful to answer the question I will ask on the document.
        Final barrier:
         - Europea if the final redemption amount is calculated on a value measured on a single final valuation date(final observation date) or on a series of final valuation dates on which an average is calculated;
         - Americana if the final redemption amount is calculated on a value measured in a continuous interval between the initial valuation date and the final valuation date;
         - None if the Certificate has a floor level/ protection of 100%
        From the following certificate's document {input}
        recover the following information:
        - Isin, Description or type of product, Issuer, Specified Currency, Listing, Nominal Amount, Floor Amount or Floor Level(if it is not present is not a problem), Protection, Guaranteed level, Barrier Level, strike level,
        - tell me if the final barrier is europea or americana or None, in order to respond use the info in the document and the context provided an the beginnig of my message, give me your response based on your reasoning.
        - Additional Unconditional Amount, Additional Conditional Amount(m), Additional Conditional Amount (it is the number of EUR in the table) , Additional Conditional Amount Payment Level(the percentage level in the table),
        - the Additional Conditional Amount Payment with Memory, memory effect: yes if there s the phrase 'less all additional conditional amounts (m) paid on the preceding additional conditional amount', memory effect: if in the description there is MEMORY,
        - maximum payment, underlyings of the certificate specifying Bloomberg code and Isin code, issue date, final payment date.
        - tell me if there is an Early Redemption event, do not consider MREL Disqualification Event in order to respond to this question.
        - if there is a callability mechanism, if there is a putability mechanism.
        - Tell me if there is an Early Redemption Amount greater than the Final Redempton Amount (so greater than 1000), if yes give me the first Early Redemption Amount greater than the Final Redempton Amount ((so greater than 1000))"""

        complete_prompt = system_message + human_message

        prompt_kid = PromptTemplate(input_variables=["input"], template=complete_prompt)
        response = Models.general_extract(self.doc_path, "gpt-4-turbo", prompt=prompt_kid, input=self.text)

        tags  = Models.tag(response, PydanticSchema_unicredit_noLangChain, self.file_id, model="gpt-4-turbo")

        df_tags = pd.DataFrame.from_dict([dict(tags)])
        df_guesses = df_tags.rename(columns=lambda x: get_new_column_name(column_dict, x))
        df_guesses = df_guesses.applymap(truncate)
        df_guesses = df_guesses.replace("'", " ", regex=True)

        df_guesses[columns_to_clean] = df_guesses[columns_to_clean].applymap(clean_value)
        df_guesses[columns_to_date_convert] = df_guesses[columns_to_date_convert].applymap(convert_date)

        df_final = df_dataintegration(df_guesses)
        # get list of column names
        # rename df columns 
        df_final_renamed = df_final.rename(columns=new_df_renaming)
        # from df to dict
        tags = df_final_renamed.to_dict(orient="records")[0]
        

        api_costs = self._process_costs()

        filename = os.path.splitext(os.path.basename(self.doc_path))[0]


        complete = self.create_output(
            "wamderivati",
            "complexity",
            {
                "file_name": filename,
                **dict(tags),
                "api_costs": api_costs
            }
        )

        Models.clear_resources_file(filename)
        return complete


# if __name__ == "__main__":
#     isin_list = ['DE000HC6V3N1']

#     path = 'FT_DE000VU2EF14.pdf'
#     extractor = WamDerivatiComplexity(path)
#     extraction = extractor.process()

#     print(extraction)


