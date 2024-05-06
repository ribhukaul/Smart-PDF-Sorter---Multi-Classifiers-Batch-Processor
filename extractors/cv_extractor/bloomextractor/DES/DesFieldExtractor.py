import re

from .des_specific_extractor import *
from ..scraper_finder import get_quadrant, get_text
from .config import FIELDS, VALID_FIELDS_CONVENTION, SPECIFIC_EXTRACTORS
from ..scraper_utils import convert_isin, convert_date, convert_price, is_valid_date, preprocess_image
from extractors.general_extractors.extractor import Extractor
# TODO:
# - Add DOCSTRING
# - Move postprocessing outside
conversion_config = {
        "maturity": convert_date,
        "interest_accrual_date": convert_date,
        "first_settle_date": convert_date,
        "first_coupon_date": convert_date,
        "pricing_date": convert_date,
        #"cpn_freq": lambda x: {"S/A": 2, 'Annual': 1, 'Quarterly':4}.get(x, "NA"),
        #"rank": lambda x: None if  x== None else "Sub" if "sub" in x.lower() else "Sen" if "senior" in x.lower() or "sr" in x.lower() else "NA",
        "coupon": convert_price,
        "isin": convert_isin,
    }


class DesFieldExtractor(Extractor):

    fields_info = FIELDS
    all_fields = list(fields_info.keys())


    def __init__(self, image_path: str) -> None:
        self.image_path = image_path
        self.info = {"ss_type": "DES"}
        self.image = preprocess_image(self.image_path)
        print(self.image)
        print("processed image")
        self.processed_image = self._reduce_image_scope()
        print("GETTING TEXT")
        self.text_d = get_text(self.processed_image)
        print('got text')
        self.text_d_original = get_text(self.image)
      

    def _reduce_image_scope(self):
        "Reduces image size for the desired columns"
        print("Processing...")
        processed_image = preprocess_image(self.image_path)
        print("processed..")
        # Look for key words and trim the image from there
        words = {"Pages":100, "Industry":-8}
        for word in words:
                
                text = get_text(processed_image)
                print("finding ROI..")
                roi = find_roi(text, word)
                print("found ROI..")
                if roi is not None:
                    xmin, _, _, _ = roi
                    processed_image = processed_image[:, xmin+ words[word]:]
                    return processed_image
        print("No ROI found..")
        return None            

    def _get_row_info(self, field):
        "Get value on a key-value paur text value corresponding to a desired key"
        # Get ROI
        width = FIELDS[field].get('widths', 250)
        name = FIELDS[field].get('name', field)
        roi = get_quadrant(self.text_d, name, width)
        if roi is None:
            print(f"Keyword '{field}' not found in image.")
            return "N/A"
        else:
            x, y, w, h = roi
            h = h + 15
            ymin = y- 5
            field_image = self.processed_image[ymin:y+h, x:x+w]
            raw_info = get_text(field_image, mode='string').strip()
            return raw_info
        
    # def background(f):
    #         "Used for parallelization"
    #         def wrapped(*args, **kwargs):
    #             return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)

    #         return wrapped
    
    def isin_extraction(self):
        self.info['isin'] = isin_extraction(self.processed_image, self.text_d)
        print("The isin is: ", self.info['isin'], "on file: ", self.image_path)

    def name_extraction(self):
        width = FIELDS['name'].get("widths", 250)
        roi = get_quadrant(self.text_d, "Name", width)
        processed_image = self.processed_image.copy()
        if roi is None:
            roi_ii = find_roi(self.text_d, 'Issuer Information')
            if roi_ii is None:
                print(f"Keyword 'Name' not found in image.")
                self.info['name'] = "N/A"
            _, _, ymin, ymax = roi_ii
            processed_image = self.processed_image[ymax:, :]

            roi = get_quadrant(get_text(processed_image), "Issuer", width)
            if roi is None:
                print(f"Keyword 'Name' not found in image.")
                self.info['name'] = "N/A"
        
        x, y, w, h = roi
        h = h + 15
        ymin = y- 5
        field_image = processed_image[ymin:y+h, x:x+w]
        raw_info = get_text(field_image, mode='string').strip()
        self.info['name'] = raw_info

    def esg_type_extraction(self):
        self.info['esg_type'] = esg_extraction(self.image_path)
    
    def exchange_extraction(self):
        width = FIELDS['exchange'].get("widths", 250)
        self.info['exchange'] = exchange_extraction(width, self.image_path)
    
    def sinkability_extraction(self):
        self.info['sinkability'] = check_for_word_property(self.processed_image, self.text_d, ['SINK', 'SINKABLE'])

    def amount_issued_extraction(self):
        self.info['amount_issued'], self.info['amount_outstanding'] = amount_issued_extraction(self.processed_image)

    def min_piece_extraction(self):
        self.info['min_piece'] = min_piece_extraction(self.processed_image)

    def callability_extraction(self):
        self.info['callability'] = check_for_word_property(self.processed_image, self.text_d, ['CALL ', 'CALLABLE', 'CALLED', ' CAL ', ' CAL\n'])
        print(self.info['callability'])
    
    def status_extraction(self):
        self.info['status'] = status_extraction(self.image_path)
    
    def description_extraction(self):
        self.info['description'] = description_extraction(self.image, self.text_d_original)

    def make_whole_extraction(self):
        #self.info['make_whole'] = make_whole_extraction(self.processed_image, self.text_d)
        self.info['make_whole'] = check_for_word_property(self.processed_image, self.text_d, ['MAKE WHOLE'])
    
    def maturity_extraction(self):

        extraction = self._get_row_info('maturity')
        self.info['maturity'] = "N/A"
        self.info['perpetual']= 0
        if "PERPE" in extraction:
            self.info['perpetual']= 1
        
        # split extraction with " "
        extractions = extraction.split(" ")
        # check if there is an element which is a valid date
        for extraction in extractions:
            if is_valid_date(extraction):
                self.info['maturity'] = convert_date(extraction)
                break

    def tasso_type_extraction(self):
        self.info['tasso_type'] = type_extraction(self.processed_image, self.text_d)
    
    def note_des_extraction(self):
        self.info['note_des'] = note_des_extraction(self.image)

    def bond_type_extraction(self):
        self.info['bond_type'] = bond_type_extraction(self.processed_image, self.text_d)
    
    def first_coupon_date_extraction(self):
        self.info['first_coupon_date'] = first_coupon_date_extraction(self.processed_image, self.text_d)
    
    def formula_des_extraction(self):
        self.info['formula_des'] = formula_des_extraction(self.processed_image, self.text_d)
    
    def description_extraction(self):
        self.info['description'] = description_extraction(self.image, self.text_d_original)
    
    def general_extractor(self, field):
        """Extractor devised for standard fields.

        Args:
            field (str): string that identifies the field to be extracted
        """
        if field == "formula_des":
            print(8)
        # Get info from the key value asociation
        raw_info = self._get_row_info(field)

        if raw_info == "N/A":
            self.info[field] = "/NA"
        else:
            # Check convetions
            if field in list(VALID_FIELDS_CONVENTION.keys()):
                for valid_count_convention in VALID_FIELDS_CONVENTION[field]:
                    condition1 = re.search(r'\b' + re.escape(valid_count_convention) + r'\b', raw_info)
                    condition2 = re.search(r'\b' + re.escape(valid_count_convention.replace(' ', '')) + r'\b', raw_info.replace(' ', ''))
                    if condition1 or condition2:
                        print(f'Found {raw_info} in {field} convention set to: {valid_count_convention}')
                        raw_info = valid_count_convention
                        break
                else:
                    print(f'No convention for {field} found, setting {field} to {raw_info}')
                    raw_info = ""

            # Convert fields
            if field in conversion_config:
                convert_func = conversion_config[field]
                self.info[field] = convert_func(raw_info)
            else:
                self.info[field] = raw_info

    # @background
    def execute_field(self, field):
        if field in SPECIFIC_EXTRACTORS:
            eval(f"self.{field}_extraction()")

        else:
            self.general_extractor(field)

    
    def extract_all(self):
        """Extract all the possible fields from the DES screenshot

        Returns:
            dict: dictionary containing the extracted information
        """
        # Run specirfic extraction for certain fields or general ones
        for field in FIELDS.keys():
            print(field)
            if field == "description":
                print(8)                
            try:
                if field in SPECIFIC_EXTRACTORS:
                    eval(f"self.{field}_extraction()")
                else:
                    self.general_extractor(field)
            except Exception as ex:
                print(f"ERROR {ex} in {field}")
                continue
        
        return self.info

    def extract_all_parallel(self):
        """Same function as extract_all but with parallelization
        """

        # Run the extraction operations in parallel

        thraded_functions = {}

        for field in self.all_fields:
    
                thraded_functions[field] = {
                    "function": self.execute_field,
                    "args": {"field": field}
                }
        
        results = self.threader(thraded_functions)

        return results

