import os

from extractors.general_extractors.config.prompt_config import prompts, table_schemas, word_representation
from extractors.general_extractors.utils import select_desired_page
from extractors.models import Models
from extractors.general_extractors.custom_extractors.kid.kid_extractor import KidExtractor
from extractors.general_extractors.llm_functions import complex_table_inspection
from extractors.general_extractors.custom_extractors.kid.kid_utils import clean_response_regex

class WamInsuranceKidCredemExtractor(KidExtractor):

    def __init__(self, doc_path) -> None:
        self.doc_path = doc_path
        super().__init__(doc_path, "it")

    def get_tables(self):
        """calc table extractor, it extracts the three tables from the document asynchronously

        Returns:
            dict([pandas.dataframe]): tables as dataframe
        """
        try:
            performance_table,_ = self._extract_table("performance")

        except Exception as error:
            print("calc table error" + repr(error))
            error_list = [performance_table]
            for i, key in enumerate(error_list):
                if not key:
                    error_list[i] = dict([("ERROR", "ERROR")])

        return dict(
            [
                ("performance", performance_table),
            ]
        )

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
                    "performance_credem",
                    self.file_id,
                    direct_tag=True,
                    language=self.language,
                )
            )

            performance = clean_response_regex("performance", self.language, performance)
        except Exception as error:
            print("extract performances error" + repr(error))
            error_list = [
                "moderato_return_rhp",
                "favorable_return_rhp",
            ]
            performance = {
                key: (performance[key] if performance.get(key) is not None else "ERROR") for key in error_list
            }

        return performance
    

    def process(self):
        """main processor in different phases, first phases extracts the tables and general information,
        and target market, second phase extracts the rest of the fields.

        Returns:
            dict(filename,dict()): dictionary containing the results for the file
        """
        # FIRST STAGE: get tables and general information
        try:
      
            functions_parameters = {
                "tables": {"function":self.get_tables}, 
                "basic_information": {"function":self.extract_general_data},
                }
            results = self.threader(functions_parameters)

            tables = results["tables"]
            basic_information = results["basic_information"]

        except Exception as error:
            print("first stage error" + repr(error))

        # SECOND STAGE: extract RIY, costs, commissions and performances
        try:
            functions_parameters = {
                "riy": {"function":self.extract_riy_small}, 
                "performance": {"function":self.extract_performances, "args":{"table":tables["performance"]}}
                }
            results = self.threader(functions_parameters)
            riy = results["riy"]
            performance = results["performance"]       

        except Exception as error:
            print("second stage error" + repr(error))

        try:
            
            # REVIEW: what name do they need?
            filename = os.path.splitext(os.path.basename(self.doc_path))[0]

            api_costs = self._process_costs()

            complete = self.create_output(
                "waminsurance",
                "kidcredem",
                {
                    "file_name": filename,
                    **dict(basic_information),
                    **dict(performance),
                    **dict(riy),
                    "api_costs": api_costs,
                }
   
            )

        except Exception as error:
            print("dictionary error" + repr(error))
            filename = os.path.splitext(os.path.basename(self.doc_path))[0]
            complete = dict([(filename), dict()])

        print(complete)
        Models.clear_resources_file(filename)

        return complete

