from .configs.waminsurance import gkidgovernance, kidcredem, kidmodule, kidgovernance
from .configs.wamderivati import complexity, bnp
from .configs.wamasset import kidasset
from .configs.wambond import bloombergss

import locale
import datetime

names_of_fields_to_clean_dot=["SMOR RHP (€)", "SMOR 1Y (€)", "RIY 1Y EUR MIN", "RIY 1Y EUR MAX",
                              "RIY RHP/2 EUR MIN", "RIY RHP/2 EUR MAX", "RIY RHP EUR MIN", "RIY RHP EUR MAX"]
code_to_clean_dot = ['cod_stress_scenario_abs_1y', 'cod_stress_scenario_abs_rhp','cod_stress_scenario_abs_rhp2',
                     'cod_unfavorable_scenario_abs_1y', 'cod_unfavorable_scenario_abs_rhp', 'cod_unfavorable_scenario_abs_rhp2',
                     'cod_moderate_scenario_abs_1y', 'cod_moderate_scenario_abs_rhp', 'cod_moderate_scenario_abs_rhp2',
                     'cod_favorable_scenario_abs_1y', 'cod_favorable_scenario_abs_rhp', 'cod_favorable_scenario_abs_rhp2',
                     'cod_death_scenario_abs_1y', 'cod_death_scenario_abs_rhp', 'cod_death_scenario_abs_rhp2',
                     'cod_riy_abs_1y', 'cod_riy_abs_rhp', 'cod_riy_abs_rhp2']
# controlla meglio filename
# change apicostsss in all extractors


class Field:
    def __init__(self, field_config, field_result):
        self.name = field_config.get("renaming", "Unknown Field")
        self.field_code = field_config.get("field_name", "Unknown Field")
        self.value = field_result
        self.metric = field_config.get("model_of", "N/A")
        self.data_type = field_config.get("type_of", "N/A")
        self.range = field_config.get("range_of")
        self.coord = {}
        self.decimals = field_config.get("decimals_of", "N/A")
        self.allownull = field_config.get("allow_null", False)


    def check_validity(self):
        """clean the value"""
        # Temporary double check
        if self.name in names_of_fields_to_clean_dot or self.field_code in code_to_clean_dot:
            self.value = str(self.value).replace(".", "")
        if self.data_type == "Float":
            if isinstance(self.value, str):
                self.value = str(self.value).replace(",", ".")
            if isinstance(self.value, list):
                self.value = [str(value).replace(",", ".") for value in self.value]
        if self.data_type == "Date":
            if isinstance(self.value, str):
                self.value = self.transform_date(self.value)
            if isinstance(self.value, list):
                self.value = [self.transform_date(value) for value in self.value]
 
    def transform_date(self, date_str):
        # Supported date formats
        english_formats = ["%m/%d/%Y", "%B %d, %Y", "%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d"]  
        italian_formats = ["%d/%m/%Y", "%d %B %Y", "%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d"]
 
        # Attempt parsing in both English and Italian
        locale.setlocale(locale.LC_TIME, 'it_IT')
        for fmt in italian_formats :
            try:
                date_object = datetime.datetime.strptime(date_str, fmt)
                return date_object.strftime("%Y-%m-%d")  # Output in YYYY-MM-DD
            except ValueError:
                pass  # Try the next format if it doesn't match
           
        locale.setlocale(locale.LC_TIME, 'en_US')
        for fmt in english_formats :
            try:
                date_object = datetime.datetime.strptime(date_str, fmt)
                return date_object.strftime("%Y-%m-%d")  # Output in YYYY-MM-DD
            except ValueError:
                pass  # Try the next format if it doesn't match
 
        # If all parsing attempts fail
        return date_str # Return the original string

    def to_dict(self):
        """Return the fields as a dictionary

        Returns:
            dict(): Dictionary with the fields
        """
        self.check_validity()
        return {
            "name": self.name,
            "value": self.value,
            "metric": self.metric,
            "data_type": self.data_type,
            "range": self.range,
            "coord": self.coord,
            "decimals": self.decimals,
            "allownull": self.allownull,
        }

class OutputHandler:

    config_selector = {
        "waminsurance": {
            "kidgovernance": kidgovernance.kid,
            "kidcredem": kidcredem.kidcredem,
            "kidmodule": kidmodule.kid,
            "gkidgovernance": gkidgovernance.gkid,
            },
        "wamderivati": {
            "complexity": complexity.complexity,
            "bnp": bnp.bnp
            },
        "wamasset":{
            "kidasset": kidasset.kidasset
        },
        "wambond":{
            "bloombergss": bloombergss.bloombergss
        }
    }
    
    def __init__(self, tenant, extractor_type, results, doc_path):
        self.complete_output = {"file_path": doc_path}
        self.fields_config = self.config_selector[tenant][extractor_type]
        self.results = results
        self.build_fields()
        self.build_additional_info()


    def build_fields(self):
        """creates the fields for the JSON

        Returns:
            dict(): fields for the JSON
        """
        fields = {}

        for f, f_conf in self.fields_config["fields"].items():

            code = f_conf.get("field_name")
            if code is not None:
                field_res = self.results.get(f, "ERROR")
                fields[code] = Field(f_conf, field_res).to_dict()
        self.complete_output["extraction"] = fields
    

    def build_additional_info(self):
        """creates the basic cost info for the JSON
        """
        api_cost = self.results['api_costs']
        total = api_cost.get("total", {})
        # eliminate "total" key from api_costs
        if "total" in api_cost:
            del api_cost["total"]
                
        self.complete_output['extraction_cost'] = {
            "total": total,
            "currency": "EUR",
            "models": api_cost
        }
        self.complete_output['sections'] = self.fields_config["sections"]

