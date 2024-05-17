
import re

from PyPDF2 import PdfReader, PdfWriter
from ...llm_functions import complex_table_inspection, general_table_inspection, llm_extraction, tag_only
from ...extractor import Extractor
from extractors.models import Models
from extractors.general_extractors.utils import upload_df_as_excel
from ...llm_functions import (
    llm_extraction_and_tag,
)
from .kid_utils import clean_response_regex, clean_response_strips
from math import ceil
from extractors.general_extractors.utils import select_desired_page
from extractors.general_extractors.config.prompt_config import IsDisclaimerThere
from extractors.general_extractors.config.prompt_config import prompts, table_schemas, word_representation
from extractors.configs.extraction_config.prompts.kid_prompts import performance_rhp_2, performance_abs





class KidExtractor(Extractor):

    def __init__(self, doc_path, predefined_language=False) -> None:
        super().__init__(doc_path, predefined_language)


    def get_tables(self):
        """calc table extractor, it extracts the three tables from the document asynchronously

        Returns:
            dict([pandas.dataframe]): tables as dataframe
        """
        try:
            performance_table,_ = self._extract_table("performance")
            costi_ingresso_table,_ = self._extract_table("costi_ingresso", black_list_pages=[0])
            costi_gestione_table,_ = self._extract_table("costi_gestione")
            #riy, _ = self._extract_table("riy", black_list_pages=[0])
            
        except Exception as error:
            print("calc table error" + repr(error))
            error_list = [performance_table, costi_ingresso_table, costi_gestione_table]
            for i, key in enumerate(error_list):
                if not key:
                    error_list[i] = dict([("ERROR", "ERROR")])

        return dict(
            [
                ("costi_ingresso", costi_ingresso_table),
                ("costi_gestione", costi_gestione_table),
                ("performance", performance_table),
            ]
        )

    
    def extract_general_data(self, general_info_schema="general_info"):
        """
        Extract general data from the document. Namely RHP and SRI.


        Returns: dict(): data extracted
        """
        extraction = dict()
        try:
            # extract and clean
            extraction = llm_extraction_and_tag(self.text, self.language, general_info_schema, self.file_id)
            extraction = clean_response_regex("general_info", self.language, extraction)
            extraction = dict(extraction)

            # REVIEW: ISIN EXTRACTION TO BE MOVED OUTSIDE?
            isin = self.extract_isin()
            extraction.update({"isin": isin})
            if (
                "periodo_detenzione_raccomandato" in extraction
                and extraction["periodo_detenzione_raccomandato"] != "-"
                and re.search(r"\d+", extraction["periodo_detenzione_raccomandato"])
            ):

                rhp_temp = extraction["periodo_detenzione_raccomandato"]
                number = re.search(r"\d+", rhp_temp).group(0)
                if re.search(r"(?i)mesi", rhp_temp):
                    extraction["periodo_detenzione_raccomandato"] = "1"
                else:
                    extraction["periodo_detenzione_raccomandato"] = str(int(number))

                self.rhp = extraction["periodo_detenzione_raccomandato"]
            else:
                self.rhp = "multiple"

        except Exception as error:
            print("extract general data error" + repr(error))
            error_list = ["isin", "indicatore_sintetico_rishio"]
            extraction = {key: (extraction[key] if extraction.get(key) is not None else "ERROR") for key in error_list}
            self.rhp = extraction["periodo_detenzione_raccomandato"] = "multiple"

        return extraction

    def extract_isin(self):
        to_search = self.text[0].page_content[20:1600]
        isin = re.search(r"[A-Z]{2}[A-Z0-9]{9}\d", to_search)
        return isin.group(0) if isin else "-"
    
    def is_product_complex(self):
        """extracts if the product is complex

        Returns:
            dict(): extracted data
        """
        try:
            #extraction = llm_extraction_and_tag(self.text, self.language, 'is_product_complex', self.file_id, specific_page=0)
            extraction = Models.tag(self.text[0].page_content[:1800], IsDisclaimerThere, self.file_id)
            #extraction = {'is_product_complex':  extraction.is_disclaimer_there}
            extraction = {'is_product_complex':  'true' if extraction.is_disclaimer_there else 'false'}
            
            return extraction
        except Exception as error:
            print("is_product_complex error" + repr(error))
            return dict([("ERROR", "ERROR")])
    
    def extract_market(self, market_type="target_market"):
        """extracts market from the document

        Args:
            market_type (str, optional): type of market to extract. Defaults to "market".
                Can also be "maket_gkid".

        Returns:
            dict(): market extracted
        """
        market = None
        try:
            market = llm_extraction(self.text[0], market_type, self.file_id, self.language)
            # procedural cleaning
            market = clean_response_strips("market", self.language, market)

        except Exception as error:
            print("market extraction error" + repr(error))
            if not market:
                market = "ERROR"

        market = dict([("target_market", market)])
        return market

    # OLD METHOD
    # def extract_riy(self, page=1):
    #     """extracts riy from the document

    #     Returns:
    #         dict(): riy extracted
    #     """
    #     try:
    #         # Select page with RIY
    #         extraction_riy = tag_only(self.text[page:], "riy", self.language, self.file_id, rhp=self.rhp)
    #         extraction_riy = clean_response_regex("riy", self.language, extraction_riy)
    #     except Exception as error:
    #         print("extract riy error" + repr(error))
    #         error_list = ["incidenza_costo_1", "incidenza_costo_rhp"]

    #         extraction_riy = {
    #             key: (extraction_riy[key] if extraction_riy.get(key) is not None else "ERROR") for key in error_list
    #         }

    #     return extraction_riy
    
    def extract_riy(self):
        """extracts riy from the document

        Returns:
            dict(): riy extracted
        """
        try:
            rhp = int(self.rhp)
            schema = table_schemas['it']['riy']
            # Set starting page & select desired page
            strat_page = 0 if len(self.text) < 3 else 1
            keywords = word_representation['it']['riy']
            reference_text = self.text[strat_page:]
            page = select_desired_page(reference_text, keywords)
            page = reference_text[int(page)]
            
            # If RHP >=10 we also need to get the values at RHP/2
            if rhp is not None and rhp >=10:
                year = ceil(rhp/2)
                prompt = prompts['it']['riy_rhp2']
                schema = table_schemas['it']['riy_rhp2']             
                total_prompt = prompt.format(year, rhp, page.page_content)
                extraction_riy = Models.tag(total_prompt, schema, self.file_id)         
            else:
                prompt = prompts['it']['riy']
                total_prompt = prompt.format(rhp, page.page_content)
                extraction_riy = Models.tag(total_prompt, schema, self.file_id)

            # Clean response
            extraction_riy = clean_response_regex("riy", self.language, extraction_riy)
            
        except Exception as error:
            print("extract riy error" + repr(error))
            error_list = [k for k in schema.schema()['properties'].keys()]
            performance = {
                key: (performance[key] if performance.get(key) is not None else "ERROR") for key in error_list
            }
    
        return extraction_riy
    
    def extract_riy_small(self):
        """extracts riy from the document

        Returns:
            dict(): riy extracted
        """
        try:
            rhp = int(self.rhp)
            
            # Set starting page & select desired page
            strat_page = 0 if len(self.text) < 3 else 1
            keywords = word_representation['it']['riy']
            reference_text = self.text[strat_page:]
            page = select_desired_page(reference_text, keywords)
            page = reference_text[int(page)]

            # Set prompt and extract
            schema = table_schemas['it']['riy_small']
            prompt = prompts['it']['riy_small']
            total_prompt = prompt.format(rhp, page.page_content)
            extraction_riy = Models.tag(total_prompt, schema, self.file_id)         

            # Clean response
            extraction_riy = clean_response_regex("riy", self.language, extraction_riy)
            
        except Exception as error:
            print("extract riy error" + repr(error))
            error_list = [k for k in schema.schema()['properties'].keys()]
            performance = {
                key: (performance[key] if performance.get(key) is not None else "ERROR") for key in error_list
            }
    
        return extraction_riy
    #REVIEW: NEED TO UPLOAD TABLE AS DF
    def extract_entryexit_costs(self, table):

        try:
            extraction = general_table_inspection(
                table,
                "costi_ingresso",
                self.file_id,
                language=self.language,
                add_text="estrai il valore % dopo {} anni".format(self.rhp),
            )
            extraction = clean_response_regex("costi_ingresso", self.language, extraction)
        except Exception as error:
            print("extract entry exit costs error" + repr(error))
            error_list = ["costi_ingresso", "costi_uscita"]
            extraction = {key: (extraction[key] if extraction.get(key) is not None else "ERROR") for key in error_list}

        return extraction
    
    # redefined extract_entryexit_costs in order to extract the first column of costi di ingresso
    def extract_middle_costs(self, table):
        try:
            from extractors.general_extractors.utils import upload_df_as_excel
            table = upload_df_as_excel(table)
            extraction = general_table_inspection(
                table,
                "costi_ingresso",
                self.file_id,
                language=self.language,
                add_text=(
                    "Estrai il valore dei diritti fissi e dei costi una tantum di entrata e di uscita"
                ),
            )
            #xtraction = clean_response_regex("costi_ingresso", self.language, extraction)
        except Exception as error:
            print("extract middle costs error" + repr(error))
            # Initialize a default error structure for the extraction
            extraction = {key: "ERROR" for key in ["costi_ingresso", "costi_uscita", "costi_ingresso_uscita"]}

        return extraction


    # REVIEW: NEED TO UPLOAD TABLE AS DF
    def extract_management_costs(self, table):

        try:
            extraction = dict()
            extraction = general_table_inspection(
                table,
                "costi_gestione",
                self.file_id,
                language=self.language,
                add_text="estrai il valore % dopo {} anni".format(self.rhp),
            )
            extraction = clean_response_regex("costi_gestione", self.language, extraction)
        except Exception as error:
            print("extract management costs error" + repr(error))
            error_list = ["commissione_gestione", "commissione_transazione", "commissione_performance"]
            extraction = {key: (extraction[key] if extraction.get(key) is not None else "ERROR") for key in error_list}

        return extraction
    
    #redefined extract_management_cost in order to extract the first column of costi di gestione
    def extract_management_costs(self, table):

        try:
            extraction = dict()
            extraction = general_table_inspection(
                table,
                "costi_gestione",
                self.file_id,
                language=self.language,
                add_text="estrai il valore % dopo {} anni".format(self.rhp),
            )
            extraction = clean_response_regex("costi_gestione", self.language, extraction)
        except Exception as error:
            print("extract management costs error" + repr(error))
            error_list = ["commissione_gestione", "commissione_transazione", "commissione_performance"]
            extraction = {key: (extraction[key] if extraction.get(key) is not None else "ERROR") for key in error_list}

        return extraction
    

    def extract_transaction_costs(self, table):

        try:
            from extractors.general_extractors.utils import upload_df_as_excel
            table = upload_df_as_excel(table)
            extraction = dict()
            extraction = general_table_inspection(
                table,
                "costi_gestione_%",
                self.file_id,
                language=self.language,
                add_text="estrai il valore % dei costi correnti e dei costi di transazione",
            )
            #extraction = clean_response_regex("costi_gestione", self.language, extraction)
        except Exception as error:
            print("extract management costs error" + repr(error))
            error_list = ["commissione_gestione", "commissione_transazione", "commissione_performance"]
            extraction = {key: (extraction[key] if extraction.get(key) is not None else "ERROR") for key in error_list}

        return extraction





    def extract_performances(self, table):
        """extracts performances from scenarios in the document

        Args:
            table (pandas.dataframe): table containing the performances

        Returns:
            dict(): dict containing the performances
        """
        performance = dict()
        try:
            performance = dict(
                complex_table_inspection(
                    table,
                    self.rhp,
                    "performance",
                    self.file_id,
                    direct_tag=True,
                    language=self.language,
                )
            )

            morte = dict(
                [
                    ("scenario_morte_1", performance.get("scenario_morte_1")),
                    ("scenario_morte_rhp", performance.get("scenario_morte_rhp")),
                ]
            )
            performance = clean_response_regex("performance", self.language, performance)
            morte = clean_response_regex("performance_morte", self.language, morte)
            performance["scenario_morte_1"] = morte.get("scenario_morte_1")
            performance["scenario_morte_rhp"] = morte.get("scenario_morte_rhp")
        except Exception as error:
            print("extract performances error" + repr(error))
            error_list = [
                "scenario_morte_1",
                "scenario_morte_rhp",
                "stress_return",
                "sfavorevole_return",
                "moderato_return",
                "favorable_return",
                "stress_return_rhp",
                "sfavorevole_return_rhp",
                "moderato_return_rhp",
                "favorable_return_rhp",
            ]
            performance = {
                key: (performance[key] if performance.get(key) is not None else "ERROR") for key in error_list
            }

        return performance

    def extract_performances_abs(self, table, rhp):
        """extracts performances from scenarios in the document

        Args:
            table (pandas.dataframe): table containing the performances

        Returns:
            dict(): dict containing the performances
        """
        performance = dict()
        try:
            schema = table_schemas['it']['performance_abs']
            # eliminate the row where 'minimo' is mentioned
            # SOlo per il primo valore in cui minimo è presente
            table = table[~table.iloc[:, 0].str.contains('caso vita', case=False, na=False)]
            table = table[~table.iloc[:, 0].str.contains('importo investito nel tempo', case=False, na=False)]
            table = table.drop(table.iloc[:, 0].str.contains('minimo', case=False, na=False).idxmax())
            table = table[~table.iloc[:, 0].str.contains('scenario di morte', case=False, na=False)]
            table = table[~table.iloc[:, 0].str.contains('decesso dell\'assicurato', case=False, na=False)]

            table = table.reset_index(drop=True)
            # Fill row names where empty
            table = self.__adjust_performance_table(table, 'stress')
            table = self.__adjust_performance_table(table, 'sfavorevole')
            table = self.__adjust_performance_table(table, 'moderato')
            table = self.__adjust_performance_table(table, 'favorevole')

            table_upload = upload_df_as_excel(table)

            if rhp is None:
                adapt_extraction = "CONSIDERA 1 ANNO , EXTRACTION={}".format(table_upload)
            else:
                adapt_extraction = performance_abs.format(rhp=rhp, context=table_upload)

            # Extract performances                        
            performance_abs_res = Models.tag(adapt_extraction, schema, self.file_id)
            performance_abs_res = clean_response_regex("performance_abs", self.language, performance_abs_res)

        except Exception as error:
            print("extract performances error" + repr(error))
            error_list = [k for k in schema.schema()['properties'].keys()]
            performance_abs_res = {
                key: (performance[key] if performance.get(key) is not None else "ERROR") for key in error_list
            }

        return performance_abs_res

    def extract_performances_rhp_2(self, table, rhp):
            """extracts performances from scenarios in the document

            Args:
                table (pandas.dataframe): table containing the performances

            Returns:
                dict(): dict containing the performances
            """
            performance_rhp_2_res = dict()
            try:
                rhp= int(rhp)
                schema = table_schemas['it']['performance_rhp_2']
                if rhp is not None and rhp >=10:
                    year = ceil(rhp/2)
                    
                    # Adjust table
                    table = table[~table.iloc[:, 0].str.contains('caso vita', case=False, na=False)]
                    table = table[~table.iloc[:, 0].str.contains('importo investito nel tempo', case=False, na=False)]
                    # Drop the FIRST row where 'minimo' is mentioned
                    table = table.drop(table.iloc[:, 0].str.contains('minimo', case=False, na=False).idxmax())
                    # Drop last col (used for RHP's values)
                    table = table.iloc[:, :-1]

                    # Fill row names where empty
                    table = table.reset_index(drop=True)
                    table = self.__adjust_performance_table(table, 'stress')
                    table = self.__adjust_performance_table(table, 'sfavorevole')
                    table = self.__adjust_performance_table(table, 'moderato')
                    table = self.__adjust_performance_table(table, 'favorevole')

                    # Get table from excel & create prompt
                    table_upload = upload_df_as_excel(table)
                    adapt_extraction = performance_rhp_2.format(year=year, context=table_upload)
                    # Tagging
                    performance_rhp_2_res = Models.tag(adapt_extraction, schema, self.file_id)
                    performance_rhp_2_res = clean_response_regex("performance_rhp_2", self.language, performance_rhp_2_res)
                else:
                    performance_rhp_2_res = dict()
                    for k in schema.schema()['properties'].keys():
                        performance_rhp_2_res[k] = ""

            except Exception as error:
                print("extract performances error" + repr(error))
                error_list = [k for k in schema.schema()['properties'].keys()]
                performance_rhp_2_res = {
                    key: (performance_rhp_2_res[key] if performance_rhp_2_res.get(key) is not None else "ERROR") for key in error_list
                }

            return performance_rhp_2_res
    
    def __adjust_performance_table(self, table, word_to_adjust):
        """Adjusts the table by filling the row names where empty

        Args:
            table (pd.DataFrame): table to adjust
            word_to_adjust (str): word to adjust in the dataframe cell

        Returns:
            pd.DataFrame: Adjsuted dataframe
        """
        word_mask = table.iloc[:, 0].str.contains(word_to_adjust, case=False, na=False)
        stress_index = word_mask.index[word_mask].tolist()
        for i in stress_index:
            # If the row is empty, fill it with the word to adjust
            if table.iloc[i-1, 0] == '':
                table.iloc[i-1, 0] = word_to_adjust
    
        return table
    

if __name__ == "__main__":
    # testing
    doc_folder = "data\C\MEDIOLANUM\MYLIFEPIC_FR0011660851.pdf"
    kid_extractor = KidExtractor(doc_folder)
