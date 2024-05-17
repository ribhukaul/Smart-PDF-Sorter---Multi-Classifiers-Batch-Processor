import os
import re
import pandas as pd
from extractors.general_extractors.config.json_config import NA
from extractors.general_extractors.custom_extractors.certificates.derivati_extractor import DerivatiKidExtractor
from extractors.general_extractors.custom_extractors.kid.kid_utils import clean_response_regex
from extractors.general_extractors.llm_functions import general_table_inspection, llm_extraction_and_tag
from extractors.general_extractors.utils import is_in_text
from extractors.models import Models
from extractors.general_extractors.utils import extract_between
# REVIEW
from ....config.json_config import renaming
kid_renaming = renaming["kid"]
renaming = renaming["bnp"]



class BNPDerivatiKidExtractor(DerivatiKidExtractor):

    def __init__(self, doc_path) -> None:
        self.doc_path = doc_path
        super().__init__(doc_path, "it")

    def get_tables(self):
        """calc table extractor, it extracts the necessary tables from the document

        Returns:
            dict([pandas.dataframe]): tables as dataframe
        """
        performance_table = None
        try:
            
            self.fill_tables([i for i in range(1,min(len(self.text) + 1, 6))])

            performance_table,_ = self._extract_table("performance", black_list_pages=[0])

        except Exception as error:
            print("get_tables error" + repr(error))
            tables = [ performance_table]
            for i, table in enumerate(tables):
                if not table:
                    tables[i] = None

        return dict(
            [
                ("performance", performance_table),
            ]
        )

    def extract_general_data(self):
        """
        Extract general data from the document (ISIN, RHP...ecc...).

        Returns: dict(): data extracted
        """
        try:
            extraction = {"description": extract_between(self.text[0].page_content[:800], "Prodotto", "codice")}
            extraction.update(
                dict(llm_extraction_and_tag([self.text[1]], self.language, "general_info_bnp", self.file_id))
            )
            extraction = dict(extraction)
            if extraction.get("description") and is_in_text("airbag", (extraction.get("description"))):
                extraction["airbag"] = 1
            else:
                extraction["airbag"] = 0

            if "periodo_detenzione_raccomandato" in extraction:
                self.rhp = extraction["periodo_detenzione_raccomandato"]
            else:
                self.rhp = "multiple"

        except Exception as error:
            print("extract general data error" + repr(error))
            error_list = ["description", "airbag", "indicatore_sintetico_rishio"]
            extraction = {key: (extraction[key] if extraction.get(key) is not None else "ERROR") for key in error_list}
            self.rhp = extraction["periodo_detenzione_raccomandato"] = "multiple"

        return extraction

    def extract_deductables(self):
        """extracts the callable from the document
        looks if the word is in the document thats it
        bool for some checks for regex in regex in other

        Returns:
            dict(): dictionary containing the callable
        """
        try:
            booleans_to_check = {
                "callable": 0,
                "autocall": 0,
                "unconditional_protection": 0,
                "memory": 0,
                "barrier_type": 0,
            }
            str_to_check = {
                "importo_minimo": NA,
                "leva_cedolare": NA,
                "cap": NA,
                "leva_airbag": NA,
            }
            ret = self.extract_regex_text("bnp", 0, booleans_to_check, str_to_check)

            if ret.get("barrier_type") == 1:
                ret["barrier_type"] = "Europea"
            else:
                ret["barrier_type"] = "N/A"

        except Exception as error:
            ret = {**booleans_to_check, **str_to_check}
            print("extract_deductable error" + repr(error))

        return ret

    def extract_main_info(self):
        """extracts the main info from the main table/tables


        Returns:
            dict(): dictionary containing the main info

        """

        pages_for_main = [0, 1]

        extraction = self.extract_from_multiple_tables(pages_for_main, ["main_info_bnp"], complex=True)
        # extraction = clean_response_regex( "main_info", self.language, extraction)
        error_list = [
            "currency","strike_date","issue_date","expiry_date","final_valuation_date","nominal",
            "market","barrier","conditional_coupon_barrier","issue_price_perc","observation_coupon_date",
            "payment_coupon_date","unconditional_coupon","conditional_coupon","payment_callable_date",
            "observation_autocall_date","barrier_autocall","payment_autocall_date","value_autocall"]

        extraction = {key: (extraction[key] if extraction.get(key) is not None else "ERROR") for key in error_list}

        return extraction

    def extract_allegato(self):
        """Extracts info from the allegato table/s
        allegati are from pages 4+


        Returns:
            dict: Dictionary containing the main info

        """                
        error_list = [
            "observation_coupon_date", "payment_coupon_date", "conditional_coupon_barrier", "unconditional_coupon",
            "conditional_coupon", "payment_callable_date", "observation_autocall_date", "barrier_autocall",
            "payment_autocall_date", "value_autocall"
        ]
        
        extraction = {}

        try:
            if len(self.di_tables_pages) > 3:
                
                # Extract tables with specified black list pages
                extraction= self.extract_from_multiple_tables(list(range(3, len(self.di_tables_pages))), ["allegato_bnp_premio", "allegato_bnp_scadenza"], complex=True)
                # Define error list

                # Update extraction with '-' if value is ['not found']
            extraction = {
                key: (
                    extraction[key] 
                    if extraction.get(key) != ["not found"] and extraction.get(key) is not None 
                    else ["-"]
                    ) 
                for key in error_list
            }

        except Exception as error:
            print(f"extract_allegato error: {error}")
            
            # Handle error by setting extraction values to "ERROR" if key is not found
            extraction = {key: (extraction[key] if extraction.get(key) is not None else "ERROR") for key in error_list}

        return extraction

    def extract_sottostanti(self):
        """extracts info from the sottostante table
        sottostante can be in the first /second page or n.4+, so we need to check all

        Args:
            table (pd.DataFrame): table containing the main info

        Returns:
            dict(): dictionary containing the main info
        """
        #TODO: make better
        sottostante = None
        sottostante,_ = self._extract_table_only_header("sottostante_bnp", pages_to_check=[0,1])
        extraction = general_table_inspection(sottostante, "sottostante_bnp", self.file_id, language=self.language)
        
        extraction= dict(extraction)
        if len(self.di_tables_pages) > 3 and (
            extraction.get("instrument_bloombergcode") == ['not found'] 
            or re.search("allegat",extraction.get("instrument_isin")[0], re.IGNORECASE)
        ):
            sottostante,_ = self._extract_table_only_header("sottostante_bnp", list(range(3, len(self.di_tables_pages))))

            extraction = general_table_inspection(sottostante, "sottostante_bnp", self.file_id, language=self.language)
        # extraction = clean_response_regex( "main_info", self.language, extraction)

        error_list = ["instrument_description", "instrument_bloombergcode", "instrument_isin"]
        extraction = dict(extraction)
        extraction = {key: (extraction[key] if extraction.get(key) is not None else "ERROR") for key in error_list}

        return extraction

    def extract_entryexit_management_costs(self):
        """extracts the entry exit management costs from the document
        is multiple tables in page 2 or 3

        Returns:
            dict|object: found values
        """

        extraction = self.extract_from_multiple_tables([1, 2], ["costi_gestione", "costi_ingresso"])
        # extraction = clean_response_regex( "main_info", self.language, extraction)

        error_list = [
            "commissione_gestione",
            "commissione_transazione",
            "commissione_performance",
            "costi_ingresso",
            "costi_uscita",
        ]
        extraction = {key: (extraction[key] if extraction.get(key) is not None else "ERROR") for key in error_list}

        return extraction

    def extract_first_info(self):
        """extracts the first info from the text
        info is in the first page
        
        Returns:
            dict(): dictionary containing the first info
        """
        extraction = dict()
        try:
            extraction = llm_extraction_and_tag([self.text[0]], self.language, "first_info_bnp", self.file_id)

            # extraction = clean_response_regex( "first_info_bnp", self.language, extraction)
        except Exception as error:
            print("extract_first_info error" + repr(error))
            error_list = ["isin", "issuer_desc"]
            extraction = {key: (extraction[key] if extraction.get(key) is not None else "ERROR") for key in error_list}

        return extraction
    
    def fill_array(self, dictionary):
        """fills the arrays in the dictionary with '-'
        to have the same length for excel

        Args:
            dictionary (_type_): _description_

        Returns:
            _type_: _description_
        """
        max_length = max((len(value) for value in dictionary.values() if isinstance(value, list)), default=0)
        # Iterate through the dictionary and fill the arrays with '-'
        for key, value in dictionary.items():
            if isinstance(value, list):
                # If the array is shorter than max_length, fill with '-'
                dictionary[key] = value + ["-"] * (max_length - len(value))

        return dictionary

    # @MARCO MENON qua non so perchè ti salva un excel con tuo nome.
    def _write_to_excel(self, complete, complete2, allegato, sottostanti, api_costs, filename):
        """writes the results to an excel file

        Args:
            args (dict()): all the results
        """
        
        with pd.ExcelWriter(
            "resultsmarco_{}.xlsx".format(
                os.path.basename(self.file_id)
            ),
            engine="xlsxwriter",
        ) as excel_writer:
            # Write the first DataFrame to Sheet1
            results1 = pd.DataFrame(complete, index=[filename]).T
            results1.to_excel(excel_writer, sheet_name="info_anagrafiche", header=True)

            results2 = pd.DataFrame(complete2, index=[filename]).T
            results2.to_excel(excel_writer, sheet_name="performance", header=True)

            results3 = pd.DataFrame(self.raccorda(dict(sottostanti), renaming, keep=True)).T
            results3.to_excel(excel_writer, sheet_name="sottostanti", header=True)

            if allegato:
                results5 = pd.DataFrame(self.raccorda(dict(allegato), renaming, keep=True)).T
                results5.to_excel(excel_writer, sheet_name="allegati", header=True)

            # Write the second DataFrame to Sheet2
            results4 = pd.DataFrame.from_dict(api_costs, orient="index")
            results4 = pd.concat(
                [
                    pd.DataFrame([results4.columns], columns=results4.columns),
                    results4,
                ]
            )
            results4.reset_index(inplace=True)
            results4.columns = ["API"] + list(results4.columns)[1:]
            results4.to_excel(excel_writer, sheet_name="api costs", header=True, index=False)
        

    def process(self):
        """main processor in different phases, first phases extracts the tables and general information,
        and target market, second phase extracts the rest of the fields.

        Returns:
            dict(filename,dict()): dictionary containing the results for the file
        """
        # FIRST STAGE: get tables and general information
        try:
            print("REAL START")
            functions_parameters = {
                "tables": {"function": self.get_tables},
                "basic_information": {"function": self.extract_general_data},
                "deductables": {"function": self.extract_deductables},
            }
            result = self.threader(functions_parameters)

            tables, basic_information, deductables = [result[key] for key in result]
        except Exception as error:
            print("first stage error" + repr(error))

        # SECOND STAGE: extract RIY, costs, commissions and performances
        try:
            functions_parameters = {
                "allegato": {"function": self.extract_allegato},
                "sottostanti": {"function": self.extract_sottostanti},
                "main_info": {"function": self.extract_main_info},
                "first_info": {"function": self.extract_first_info},
                "riy": {"function": self.extract_riy, "args": {"page": 2}},
                "exit_entry_management_costs": {"function": self.extract_entryexit_management_costs},
                "performance": {"function": self.extract_performances, "args": {"table": tables["performance"]}},
            }
            result = self.threader(functions_parameters)

            allegato, sottostanti, main_info, first_info, riy, exit_entry_management_costs, performance = [
                result[key] for key in result
            ]
        except Exception as error:
            print("second stage error" + repr(error))

        try:
            # Merge and orders all the results
            
            allegato = self.fill_array(dict(allegato))

            sottostanti = self.fill_array(dict(sottostanti))

            filename = os.path.splitext(os.path.basename(self.doc_path))[0]

            api_costs = self._process_costs()

            #####################################
            # TEMPORANEAMENTE IN FASE DI TESTING #
            #####################################
            complete = self.raccorda(
                {
                    **dict(deductables),
                    **dict(basic_information),
                    **dict(clean_response_regex("bnp_main","it", main_info)),
                    **dict(first_info),
                },
                renaming,
                keep=True,
            )
            
            complete2 = self.raccorda(
                {
                    "file_name": filename,
                    **dict(performance),
                    **dict(riy),
                    **dict(exit_entry_management_costs),
                },
                kid_renaming,
                keep=True,
            )

            # REVIEW
            response = self.create_output(
                tenant = "wamderivati",
                extractor_type = "bnp",
                results = {
                    "file_name": filename,
                    **dict(basic_information),
                    **dict(performance),
                    **dict(riy),
                    **dict(exit_entry_management_costs),
                    **dict(allegato),
                    **dict(sottostanti),
                    **dict(deductables),
                    **dict(basic_information),
                    **dict(clean_response_regex("bnp_main","it", main_info)),
                    **dict(first_info),
                    "api_costs": api_costs
                    }
                )
            
            # uncomment for local testing
            #self._write_to_excel(complete, complete2, allegato, sottostanti, api_costs, filename)

        except Exception as error:
            print("dictionary error: " + repr(error))
            filename = os.path.splitext(os.path.basename(self.doc_path))[0]
            response = None

        Models.clear_resources_file(filename)
        return response
