import asyncio
import os
import pandas as pd
from extractors.general_extractors.custom_extractors.certificates.derivati_extractor import DerivatiKidExtractor
from extractors.general_extractors.custom_extractors.kid.kid_utils import clean_response_regex
from extractors.general_extractors.llm_functions import llm_extraction_and_tag
from extractors.models import Models


class VontobelDerivatiKidExtractor(DerivatiKidExtractor):

    def __init__(self, doc_path) -> None:
        self.doc_path = doc_path
        super().__init__(doc_path, "en")

        
    async def extract_deductables(self):
        """extracts the callable from the document
        looks if the word is in the document thats it
        bool for some checks for regex in regex in other

        Returns:
            dict(): dictionary containing the callable
        """
        extraction = dict()
        try:
            extraction=llm_extraction_and_tag([self.text[i] for i in range(2, 9)], self.language, "deductables_vontobel", self.file_id)
            
            
            

            # extraction = clean_response_regex( "first_info_bnp", self.language, extraction)
        except Exception as error:
            print("extract_deductable error" + repr(error))
            error_list = ["market","issue_price_perc"]
            extraction = {key: (extraction[key] if extraction.get(key) is not None else "ERROR") for key in error_list}

        return extraction
    

    async def extract_main_info(self):
        """extracts the main info from the main table/tables


        Returns:
            dict(): dictionary containing the main info

        """

        extraction = dict()
        try:
            extraction=llm_extraction_and_tag([self.text[i] for i in range(1, 7)], self.language, "main_info_vontobel", self.file_id)

            # extraction = clean_response_regex( "first_info_bnp", self.language, extraction)
        except Exception as error:
            print("extract_main_info error" + repr(error))
            error_list = [
                "conditional_protection","currency","strike_date","issue_date","expiry_date",
                "final_valuation_date","nominal","autocall_barrier","conditional_coupon_barrier","memory","strike_level","autocallable",
                "barrier_type","observation_coupon_date","payment_coupon_date","unconditional_coupon","conditional_coupon","payment_callable_date",
                "observation_autocall_date","payment_autocall_date","instrument_description","instrument_isin","instrument_bloombergcode",
                ]
            extraction = {key: (extraction[key] if extraction.get(key) is not None else "ERROR") for key in error_list}

        return extraction
    

    async def extract_first_info(self):
        """extracts the first info from the text
        info is in the first page
        
        Returns:
            dict(): dictionary containing the first info
        """
        extraction = dict()
        try:
            extraction=llm_extraction_and_tag([self.text[0]], self.language, "first_info_vontobel", self.file_id)

            # extraction = clean_response_regex( "first_info_bnp", self.language, extraction)
        except Exception as error:
            print("extract_first_info error" + repr(error))
            error_list = ["isin","description","issuer_desc"]
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

    def _write_to_excel(self, complete, api_costs, filename):
        """writes the results to an excel file

        Args:
            args (dict()): all the results
        """
        
        with pd.ExcelWriter(
            "results\\20febbraio\\resultsmarco_{}.xlsx".format(
                os.path.basename(self.file_id)
            ),
            engine="xlsxwriter",
        ) as excel_writer:
            # Write the first DataFrame to Sheet1
            results1 = pd.DataFrame(complete, index=[filename]).T
            results1.to_excel(excel_writer, sheet_name="info_anagrafiche", header=True)

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

        


    async def process(self):
        """main processor in different phases, first phases extracts the tables and general information,
        and target market, second phase extracts the rest of the fields.

        Returns:
            dict(filename,dict()): dictionary containing the results for the file
        """
        # FIRST STAGE: get tables and general information
        try:
            print("REAL START")
            tasks = []
            tasks.append(asyncio.create_task(self.extract_first_info()))
            tasks.append(asyncio.create_task(self.extract_main_info()))
            tasks.append(asyncio.create_task(self.extract_deductables()))

            await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
            
            first_info, main_info, deductables = [task.result() for task in tasks]
            
        except Exception as error:
            print("first stage error" + repr(error))

        # SECOND STAGE: extract RIY, costs, commissions and performances
        """
        try:
            tasks = []

            tasks.append(asyncio.create_task(self.extract_riy(2)))
            tasks.append(asyncio.create_task(self.extract_entryexit_management_costs()))
            tasks.append(asyncio.create_task(self.extract_performances(tables["performance"])))

            await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)

            riy, exit_entry_management_costs, performance = [task.result() for task in tasks]

        except Exception as error:
            print("second stage error" + repr(error))
        """

        try:
            # Merge and orders all the results

            filename = os.path.splitext(os.path.basename(self.doc_path))[0]

            api_costs = self._process_costs()

            # raccordo
            complete = self.raccorda(
                {
                    **dict(deductables),
                    **dict(clean_response_regex("vontobel_main","it", main_info)),
                    **dict(first_info),
                },
                "vontobel",
                keep=True,
            )
            """#if want to add these too careful about self.language, links to wrong tags and prompt
            complete2 = self.raccorda(
                {
                    "file_name": filename,
                    **dict(performance),
                    **dict(riy),
                    **dict(exit_entry_management_costs),
                },
                "kid",
                keep=True,
            )
            """
            
            self._write_to_excel(complete, api_costs, filename)
            
            
            json=self.create_json({
                    "file_name": filename,
                    #**dict(performance),
                    #**dict(riy),
                    #**dict(exit_entry_management_costs),
                    **dict(api_costs),
                    **dict(deductables),
                    **dict(clean_response_regex("vontobel_main","it", main_info)),
                    **dict(first_info),
                }, "vontobel")
            
            return json


        except Exception as error:
            print("dictionary error: " + repr(error))
            filename = os.path.splitext(os.path.basename(self.doc_path))[0]
            complete = None

        Models.clear_resources_file(filename)
        return complete
