import os

from extractors.models import Models
from extractors.general_extractors.custom_extractors.kid.kid_extractor import KidExtractor


class WamInsuranceKidModuleExtractor(KidExtractor):

    def __init__(self, doc_path) -> None:
        self.doc_path = doc_path
        super().__init__(doc_path, "it")

        
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
                "target_market": {"function":self.extract_market}
                }
            results = self.threader(functions_parameters)

            tables = results["tables"]
            basic_information = results["basic_information"]
            target_market = results["target_market"]

        except Exception as error:
            print("first stage error" + repr(error))

        # SECOND STAGE: extract RIY, costs, commissions and performances
        try:
            functions_parameters = {
                "riy": {"function":self.extract_riy_small}, 
                "costs": {"function":self.extract_entryexit_costs, "args":{"table":tables["costi_ingresso"]}},
                "management_costs": {"function":self.extract_management_costs, "args": {"table":tables["costi_gestione"]}},
                "performance": {"function":self.extract_performances, "args":{"table":tables["performance"]}}
                }
            results = self.threader(functions_parameters)
            riy = results["riy"]
            exit_entry_costs = results["costs"]
            management_costs = results["management_costs"]
            performance = results["performance"]       

        except Exception as error:
            print("second stage error" + repr(error))

        try:
            
            # REVIEW: what name do they need?
            filename = os.path.splitext(os.path.basename(self.doc_path))[0]

            api_costs = self._process_costs()

            complete = self.create_output(
                "waminsurance",
                "kidmodule",
                {
                    "file_name": filename,
                    **dict(basic_information),
                    **dict(performance),
                    **dict(riy),
                    **dict(exit_entry_costs),
                    **dict(management_costs),
                    **dict(target_market),
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

