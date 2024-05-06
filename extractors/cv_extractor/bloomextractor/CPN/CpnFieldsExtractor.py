import cv2
import numpy as np

from ..scraper_finder import find_roi, get_text, find_roi_refined
from .cpn_specific_extractor import get_field_value, cpn_formula_extractor
from extractors.cv_extractor.bloomextractor.scraper_utils import convert_date

conversion_config = {
        "effective dt_cpn2": convert_date,
    }

class CpnFieldsExtractor():

    fields = [
        "index 1", "index 2", "spread 1","multiplier 1", "multiplier 2", "multiplier 3",
        "structure type", "pay frequency", "refix frequency", "lookback day", "in arrears"
        ]
    
    specific_fields = [
        "formula"
        ]
    
    bottom_fields ={# Fields in bottom table, x and y refers adjustment to value coordinates
        "cap": {"xmin": -30, "xmax":0, "y":3}, 
        "floor":{"xmin": -10, "xmax":0, "y":8}, 
        "spread":{"xmin": -10,'xmax':20, "y":3},
        "effective dt":{"xmin": -10, "xmax":0, "y":3},
        }
    

    def __init__(self, image_path: str) -> None:
        self.image = cv2.imread(str(image_path))
        self.text = get_text(self.image)
        self.info = {"ss_type": "CPN"}


    def recognize_coupon_number(self):
        """
        Recognizes the coupon number of the image based on the color of the background

        Returns:
            int: the coupon the screenshot refers to.
        """
        # take bottom 1/3 of the page
        table_strat_words = ["effective dt", "reset idx"]
     
        for word in table_strat_words:
            roi = find_roi(self.text, word)
            if roi is not None:
                xmin, xmax, ymin, ymax = roi
                word_heigth = ymax - ymin + 15
                start = ymax + 12

                # Find row with lighter coloudrs
                area1 = self.image[start:start+word_heigth, xmin:xmax]
                area2 = self.image[start+word_heigth:start+2*word_heigth, xmin:xmax]
                area3 = self.image[start+2*word_heigth:start+3*word_heigth, xmin:xmax]
                mean_color_1 = area1.mean(axis=(0, 1)).mean()
                mean_color_2 = area2.mean(axis=(0, 1)).mean()
                mean_color_3 = area3.mean(axis=(0, 1)).mean()
                colours = [mean_color_1, mean_color_2, mean_color_3]
                lighter_row = np.argmax(colours)

                return lighter_row
      

    def get_cpn_values(self):
        """
        Extracts coupon information from a Bloomberg Terminal screen image.

        Returns:
        dict: A dictionary containing the extracted coupon information.
        """
        table_strat_words = {
            "coupon information":[40, 40], 
            "index 1":[10, 40], 
            "index 2":[10, 40], 
            "spread 1":[10, 40], 
            "multiplier 1":[10, 40], 
            "multiplier 2":[10, 40], 
            "multiplier 3":[10, 40]
            }

        # Select area of interest
        for word in table_strat_words.keys():
            deltax = table_strat_words[word][0]
            deltay = table_strat_words[word][1]
            roi = find_roi(self.text, word)
            if roi is not None:
                xmin, _, ymin, _ = roi
                table_of_interest =self.image[ymin-deltay:, xmin-deltax:]

                # Get table text
                table_text = get_text(table_of_interest)
                # Extract desired key value pairs
                extraction = {}
                for field in self.fields:
                    extraction[field] = get_field_value(table_text, table_of_interest, field)
                # Extract peculiar key-values
                for specific_field in self.specific_fields:
                    extraction[specific_field]=eval(f"cpn_{specific_field}_extractor(table_text, table_of_interest)")
                
                return extraction


    def get_column_values(self, table_image, text):
        """Extract the values corresponding to the first two rows of predefined columns.

        Args:
            table_image (np.array): image of the table
            text (_type_): text extracted with pytesseract

        Returns:
            dict: dictionary with specific fields extracted
        """
        table_results = {}
        word_heigth = 35

        for bf, bf_values in self.bottom_fields.items():
            # Look for columns region
            roi = find_roi_refined(text, bf, table_image)
            if roi is not None:
                xmin, xmax, _, ymax = roi
                
                # Adjust area of interest
                start_y = ymax +bf_values["y"]
                strart_x = xmin + bf_values["xmin"]
                end_x = xmax + bf_values["xmax"]
                # Select areas of values
                bf_cpn1 = table_image[start_y:start_y+word_heigth, strart_x:end_x]
                bf_cpn2 = table_image[start_y+word_heigth:start_y+2*word_heigth, strart_x:end_x]
                # Extract text and store text
                table_results[f"{bf}_cpn1"]  = get_text(bf_cpn1, "string", psm=3)
                table_results[f"{bf}_cpn2"] = get_text(bf_cpn2, "string", psm=3)
        
        return table_results
            

    def get_table_below_values(self):
        "Extract the values of the bottom table"

        # Reference coordinates for the table stard
        table_strat_words = {"effective dt":[40, 40], "reset idx":[10, 40]}
        for word in table_strat_words.keys():
            roi = find_roi_refined(self.text, word, self.image)
            if roi is not None:

                # Select table area and set color to grey
                xmin, _, ymin, _ = roi
                maxy = int(self.image.shape[0]*0.95)
                bottom_table_img = self.image[ymin-10:maxy, xmin-10:]
                bottom_table_img = cv2.cvtColor(bottom_table_img, cv2.COLOR_BGR2GRAY)
                
                # Get text and extract values corresponding to the desired columsn
                bottom_table_text = get_text(bottom_table_img)
                table_values = self.get_column_values(bottom_table_img, bottom_table_text)

                return table_values

    # REVIEW
    def extract_all(self):
        "Extract all the desired information in the CPN screenshot"

        # Get values of the table at the bottom
        table_values = self.get_table_below_values()
        # Extract all the values of interest
        coupon_values = self.get_cpn_values()
        self.info.update(**coupon_values, **table_values)
        # Get coupon number (NOT NEEDED FOR NOW)
        #self.info["ss_coupon_reference_number"] = self.recognize_coupon_number()

        # Clean ouput
        for key, value in self.info.items():
            if isinstance(value, str):
                value = value.replace("\n", " ")
            if key in conversion_config.keys():
                value = conversion_config[key](value)
            self.info[key] = value

        # TEMPORARY CODE #
        self.info['floor'] = ''
        self.info['cap'] = ''
        # if self.info['floor_cpn1'] or self.info['floor_cpn2'] are different than '' modify self.info['floor'] to
        # their value
        if 'floor_cpn1' in self.info.keys():
            if self.info['floor_cpn1']:
                self.info['floor'] = self.info['floor_cpn1']
            elif self.info['floor_cpn2']:
                self.info['floor'] = self.info['floor_cpn2']
            del self.info['floor_cpn1']
            del self.info['floor_cpn2']
            
        if 'cap_cpn1' in self.info.keys():
            if self.info['cap_cpn1']:
                self.info['cap'] = self.info['cap_cpn1']
            elif self.info['cap_cpn2']:
                self.info['cap'] = self.info['cap_cpn2']
    
                del self.info['cap_cpn1']
                del self.info['cap_cpn2']
        
        if "spread_cpn2" in self.info.keys():
            del self.info["spread_cpn2"]
        if "effective dt_cpn1" in self.info.keys():
            del self.info["effective dt_cpn1"]

        return self.info

