from extractors.general_extractors.extractor import Extractor
from extractors.cv_extractor.bloomextractor.scraper import extract_data_from_ss

class WamBondBloombergSS(Extractor):

    def __init__(self, doc_path, predefined_language="en"):
        
        if not isinstance(doc_path, list):
            doc_path = [doc_path]
        self.doc_path = doc_path
        self.predefined_language = predefined_language
        self.img_extr = []

    def join_results(self, results):
        """join the results of the extraction

        Args:
            results (dict): results of the extraction

        Returns:
            dict: joined results
        """
        # # Flatten the dictionary
        # cpn_counter = 0
        # des_counter = 0
        # for key, value in results.items():
        #     if isinstance(value, dict):
        #         ss_type = results[key][["ss_type"]]
        #         if ss_type == "DES":
        #             des_counter += 1
        #         else:
        #             cpn_counter += 1
            
        # INSERT CODE TO CONSIDER MAXIMUM 1 DES and 1 CPN
        flattened_dict = {}
        for key, value in results.items():
            if isinstance(value, dict):
                results[key].pop("ss_type", None)
                flattened_dict.update(value)
        
        # Convert each value to a string
        new_flattened_dict = {}
        for key, value in flattened_dict.items():
            if value != '':
                value = str(value)
                value = value.replace("'", '"')
                if value.endswith(' '):
                    value = value.rstrip()

                new_flattened_dict[key] = value
            
        # If isin not there, add a "NOT FOUND" value
        if "isin" not in new_flattened_dict:
            new_flattened_dict["isin"] = "NOT FOUND"
        return flattened_dict['info']

    def process(self):
        file_estr = {}
        
        for img_path in self.doc_path:
            
            x = extract_data_from_ss(img_path)

            file_estr[img_path] = {
                "function": extract_data_from_ss, "args": {"image_path": img_path}
            }

        results = x#self.threader(file_estr)
        

        # clean the results

        complete = self.join_results(results)

        filename = self.doc_path[0].split("/")[-1]

        complete = self.create_output(
            "wambond",
            "bloombergss",
            {
                "file_name": filename,
                **dict(complete),
                "api_costs": {
                    "total": 0.01*len(self.doc_path)
                }
            }
        )

        return complete


# if __name__ == "__main__":
#     isin_list = ['DE000HC6V3N1']

#     path = 'FT_DE000VU2EF14.pdf'
#     extractor = WamDerivatiComplexity(path)
#     extraction = extractor.process()

#     print(extraction)


