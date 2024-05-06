import re
import cv2        
import os
import uuid
from ..scraper_finder import find_roi, check_for_word, check_for_symbol, get_quadrant, get_text
from ..scraper_utils import convert_date
from ..azure.document_intelligence import analyze_general_documents

def check_for_word_property(processed_image, text_d, words):
    """General function to check for a word in an image SS. It condider a subset of the image if 
    the word "Industry si found.

    Args:
        processed_image (np.ndarray): image to analyze
        text_d (dict): a dictionary of text extracted from the image
        words (list): list of words to check for.

    Returns:
        int: 1 if the word is found, 0 otherwise.
    """
    
    roi = find_roi(text_d, 'Industry')
    for word in words:
        if roi is None:
            is_property = check_for_word(processed_image, word)
        else:
            x_min, x_max, y_min, _ = roi
            field_image = processed_image[y_min:, x_min:x_max+500]
            is_property = check_for_word(field_image, word)

        if is_property: return 1

    return 0


def status_extraction(image_path):
    """
    Extracts the status of a financial instrument from a Bloomberg Terminal DES page.

    Args:
    image (numpy.ndarray): The processed image to extract the status from.

    Returns:
    str: The status of the financial instrument. Possible values are "CALLED", "EXCHANGED", "MATURED", or "ACTIVE".
    """
    image = cv2.imread(str(image_path))
    #text_d = get_text(image)

    # Params for extraction
    words = ["CALLED", "EXCHANGED", "MATURED"]
    h = int(image.shape[0]*0.25)
    h_min = int(image.shape[0]*0.1)
    w = int(image.shape[1]*0.33)
    field_image = image[h_min:h, :w]

    for word in words:
        if check_for_word(field_image, word):
            return word

    return "ACTIVE"


def isin_extraction(processed_image, text_d):
    """Extracts the ISIN from a Bloomberg Terminal DES page, unig Azure Document Intelligence.

    Args:
        image_path (str): The file path of the image to be processed.
        processed_image (np.array): The processed image of the DES page.
        text_d (): The dictionary containing the text regions of the DES page.

    Returns:
        str: ISIN of the bond.
    """

    roi = get_quadrant(text_d, 'ISIN', 400)
    if roi is not None:
        # Extract the ISIN from the ROI
        x, y, w, h = roi
        h = h + 15
        ymin = y- 5
        field_image = processed_image[ymin:y+h, x:x+w]
        # make the image bigger
        field_image_big = cv2.resize(field_image, None, fx=5, fy=5, interpolation=cv2.INTER_CUBIC)

        # 1) Docuemnt intelligence
        #REVIEW - create unified module to save files
        save_folder = os.environ.get('LOCAL_SAVE_FOLDER', 'tmp')
        saved_file_path =  os.path.join(save_folder,  str(uuid.uuid4()) + '.png')
        cv2.imwrite(saved_file_path, field_image_big)        
        fields = analyze_general_documents(saved_file_path)
        # remove file
        os.remove(saved_file_path)
        text = fields.content.replace('\n', ' ')
        isin_in_text = re.findall(r"[A-Z]{2}[A-Z0-9]{9}\d", text)
        if len(isin_in_text):
            return isin_in_text[0] 
        
        #2) Tesseract
        isin_value = get_text(field_image, mode='string').strip()
        # eliminate symbols and empty spaces
        isin_value = re.sub(r'[^\w\s]','', isin_value).replace(' ', '')
        isin_in_text = re.findall(r"[A-Z]{2}[A-Z0-9]{9}\d", isin_value)
        # IF there is a match return it
        if len(isin_in_text):
            return isin_in_text[0]
    return "NA"        

       
def description_extraction(image, text_d):
    """
    Extracts the raw information from the 'Description' field of a Bloomberg Terminal DES page.

    Args:
        image (numpy.ndarray): The processed image of the DES page.
        text_d (dict): The dictionary containing the text regions of the DES page.

    Returns:
        str: The raw information extracted from the 'Description' field.
    """
    # Find the region of interest (ROI) for the 'Actions' field
    # transform image on only white text everything else black
    
    image = cv2.bitwise_not(image)
    white_text = get_text(image, mode='data')
    roi = find_roi(white_text, 'Actions')
    
    # If the ROI is found, extract the 'Description' field
    if roi is not None:
        x_min, _, y_min, y_max= roi
        field_image = image[y_min-4:y_max+4, :x_min]
        raw_info = get_text(field_image, mode='string').strip()
        return raw_info


def type_extraction(processed_image, text_d):
    roi = find_roi(text_d, 'Industry')
    words = ["fixed to var", "fixed", "variable", "floating", "zero cou"]
    if roi is not None:
        x_min, _, y_min, _ = roi
        w = int(processed_image.shape[1]*0.7)
        h = int(processed_image.shape[0]*0.7)
        field_image = processed_image[y_min:h, x_min:w]

        for word in words:
            if check_for_word(field_image, word):
                return word


def amount_issued_extraction(processed_image):
    # Get text of the second half of the page
    width = processed_image.shape[1]
    half_images = processed_image[:, int(width/3):]
    small_text = get_text(half_images, mode='data')   

    references = ['Aggregated', 'Amt']
    for ref in references:
        roi = find_roi(small_text, ref)
        if roi is not None:
            # Get row text
            x_min, _, y_min, y_max = roi
            h = y_max - y_min
            field_image = half_images[y_max+5:y_max+int(4*h), x_min+50:]
            raw_info = get_text(field_image, mode='string').strip()

            # regex to extract numerical amounts that are            
            #raw_info = re.findall(r'\d{1,3}(?:,\d{3})*(?:\.\d{2})?', raw_info)
            amount_extracted = re.findall(r'\d{1,3}(?:[,.]\d{3})*(?:\.\d{2})?', raw_info)

            # check if SHR or M is in the text
            to_add = ''
            if 'shr' in raw_info.lower():
                to_add = ' SHR'
            elif 'm' in raw_info.lower():
                to_add = '(M)'
            
            if len(amount_extracted)>=2:
                return amount_extracted[0]+to_add, amount_extracted[1]+to_add
            elif len(amount_extracted)==1:
                return amount_extracted[0]+ to_add, 0

            print(f"Found {ref} but no text extracted.")
    return "NA", "NA"


def min_piece_extraction(processed_image):
    # Get text of the second half of the page
    height, width = processed_image.shape

    half_images = processed_image[int(height/3):, int(width/3):]
    small_text = get_text(half_images, mode='data')   

    roi = find_roi(small_text, 'Min Piece')
    if roi is not None:
        x_min, _, y_min, y_max = roi
        h = y_max - y_min
        field_image = half_images[y_max:y_max+int(4*h), x_min:]
        raw_info = get_text(field_image, mode='string').strip()

        # regex to extract numerical amounts that are
        raw_info = re.findall(r'\d{1,3}(?:,\d{3})*(?:\.\d{2})?', raw_info)
        
        if raw_info:
            return raw_info[0]

    return "NA"


def esg_extraction(image_path):
    """
    Extracts ESG (Environmental, Social, and Governance) type from an image.

    Args:
        image_path (str): The file path of the image to be processed.

    Returns:
        str: A comma-separated string of ESG types found in the image, or "NA" if no ESG types were found.
    """
    # Upload original image
    original_image = cv2.imread(image_path, 1)

    # Compare the original image to the ESG symbols
    symbol_folder_path = "extractors\\cv_extractor\\bloomextractor\\config\\esg_symbols"
    symbols = check_for_symbol(original_image, symbol_folder_path)

    if symbols:
        return ', '.join(symbols)
    else:
        print("No symbols found for 'ESG_type'.")
        return "NA"


def exchange_extraction(width, image_path=''):
    """
    Extracts the exchange name from a given image.

    Args:
        width: The width of the image.
        image_path: The path to the image file.

    Returns:
        The extracted exchange name as a string.
    """

    # Read in the image and resize it
    image = cv2.imread(str(image_path))
    image = cv2.resize(image, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
    
    # Convert the image to grayscale and crop it
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    restricted_image = gray[int(h/2):, int(w/2):]

    # Get the text from the image and find the quadrant containing the exchange name
    text_d = get_text(restricted_image)
    roi = get_quadrant(text_d, 'Exchange', width)

    # If the exchange name is not found, check for the keyword 'TRACE' and return 'TRACE' if found
    if roi is None:
        print("EXCHANGE not found in image.")
        if check_for_word(restricted_image, 'TRACE', text_d):
            print("Keyword 'TRACE' found in image. Setting 'Exchange' to 'TRACE'.")
            return "TRACE"
        return "NA"
    
    # Extract the exchange name from the quadrant
    x, y, w, h = roi
    field_image = restricted_image[y:y+h, x:x+w]
    raw_info = get_text(field_image, mode='string').strip()

    return raw_info


def note_des_extraction(processed_image):
    """
    Extracts the note description from a processed image and a dictionary of text.

    Args:
        processed_image (numpy.ndarray): The processed image of the bond.

    Returns:
        str: The note description.
    """
    # Select Bottom Half of Image
    height, _ = processed_image.shape
    bh_image = processed_image[int(height*0.7):, :]
    bh_text = get_text(bh_image, mode='data')
    
    # FIND UPPER BOUNDARY
    up_boundaries = ['exchange', 'Reporting', 'Maturity', '1st Coupon Date']
    for up_b in up_boundaries:
        roi_up = find_roi(bh_text, up_b)
        if roi_up is not None:
            _, _, _, y_max_up = roi_up
            break
    # FIND LEFT BOUNDARY
    left_boundaries = ['Pricing date', 'Interest Accrual Date', '1st Coupon Date', "Cpn Freq", "Calc Type"]
    for left_b in left_boundaries:
        roi_left = find_roi(bh_text, left_b)
        if roi_left is not None:
            x_min_left, _, _, _ = roi_left
            break
    # FIND bottom BOUNDARY
    y_min_bottom = int(bh_image.shape[0] *0.87)
    roi_bottom = find_roi(bh_text, 'suggested functions')
    if roi_bottom is not None:
        _, _, y_min_bottom, _ = roi_bottom
            
    field_image = bh_image[y_max_up:y_min_bottom, x_min_left:]
    # get text from image
    text_d = get_text(field_image, mode='string')

    return text_d


def bond_type_extraction(processed_image, text_d):
    """
    Extracts the bond type from a processed image and a dictionary of text.

    Args:
        processed_image (numpy.ndarray): The processed image of the bond.
        text_d (dict): A dictionary of text extracted from the bond.

    Returns:
        str: The bond type.
    """
    # Find the region of interest (ROI) containing the "Industry" field.

    boundaries = ['Mkt Iss', 'Mkt of Issue']
    for bound in boundaries:

        roi = find_roi(text_d, bound)

        if roi is not None:
            x_min, _, y_min, y_max = roi
            field_image = processed_image[y_min-3:y_max+3, x_min+380:x_min+740]
            raw_info = get_text(field_image, mode='string').strip()
            return raw_info
    return ""
        

def first_coupon_date_extraction(processed_image, text_d):
    """
    Extracts the first coupon date from a processed image and a dictionary of text.

    Args:
        processed_image (numpy.ndarray): The processed image of the bond.
        text_d (dict): A dictionary of text extracted from the bond.

    Returns:
        str: The first coupon date.
    """
    field_keys = ['1st Coupon Date', 'Coupon Date']
    for key in field_keys:
        roi = get_quadrant(text_d, key, 500)
        if roi is not None:
            x, y, w, h = roi
            h = h + 15
            ymin = y- 5
            field_image = processed_image[ymin:y+h, x:x+w]

            raw_info = get_text(field_image, mode='string').strip()
            converted_info = convert_date(raw_info)
            return converted_info
        
    return "NA"


def formula_des_extraction(processed_image, text_d):
    """Extracts the formula from a processed image and a dictionary of text.

    Args:
        processed_image (numpy.array): The processed image of the bond.
        text_d (dict): A dictionary of text extracted from the bond.

    Returns:
        str: The formula of the bond.
    """

    roi = get_quadrant(text_d, "Formula", 450)
    if roi is None:
        print("Keyword 'Formula' not found in image.")
        return "N/A"
    else:
        x, y, w, h = roi
        ymin = y- 5
        field_image = processed_image[ymin:y+h, x:x+w]
        # show image 
        raw_info = get_text(field_image, mode='string').strip()
        return raw_info


def description_extraction(image, text_d):
    """Extracts the raw information from the 'Description' field of a Bloomberg Terminal DES page.

    Args:
        image (numpy.array): The processed image of the DES page.
        text_d (dict): The dictionary containing the text regions of the DES page.

    Returns:
        str: The raw information extracted from the 'Description' field.
    """
    roi = find_roi(text_d, 'Actions')
    if roi is not None:
        x_min, _, y_min, y_max= roi
        field_image = image[y_min-4:y_max+4, :x_min]
        raw_info = get_text(field_image, mode='string').strip()
        return raw_info
    return "NA"

##########
# LEGACY #
##########
# def callability_extraction(processed_image, text_d):
#     """
#     Extracts whether a bond is callable or not from a processed image and a dictionary of text.

#     Args:
#         processed_image (numpy.ndarray): The processed image of the bond.
#         text_d (dict): A dictionary of text extracted from the bond.

#     Returns:
#         int: 1 if the bond is callable, 0 otherwise.
#     """
#     # Find the region of interest (ROI) containing the "Industry" field.
#     roi = find_roi(text_d, 'Industry')
#     if roi is None:
#         # If the "Industry" field is not found, check for the word "CALL" in the whole image.
#         is_callable = check_for_word(processed_image, 'CALL')
#     else:
#         # If the "Industry" field is found, resize the scope and check for the word CALL.
#         x_min, x_max, y_min, y_max = roi
#         field_image = processed_image[y_min:, x_min:x_max+500]
#         is_callable = check_for_word(field_image, 'CALL')
#     # Return 1 if the bond is callable, 0 otherwise.
#     if is_callable:
#         return 1
#     else:
#         return 0

# def make_whole_extraction(processed_image, text_d):
#     roi = find_roi(text_d, 'Industry')
#     if roi is None:
#         is_make_whole = check_for_word(processed_image, 'MAKE WHOLE')
#     else:
#         x_min, x_max, y_min, y_max = roi
#         field_image = processed_image[y_min:, x_min:x_max+500]
#         is_make_whole = check_for_word(field_image, 'MAKE WHOLE')
#     if is_make_whole: return 1
#     else: return 0

# def sincability_extraction(processed_image, text_d):
#     roi = find_roi(text_d, 'Industry')
#     words = ['SINK', 'SINKABLE']
#     for word in words:
#         if roi is None:
#             is_sincable = check_for_word(processed_image, word)
#         else:
#             x_min, x_max, y_min, y_max = roi
#             field_image = processed_image[y_min:, x_min:x_max+500]
#             is_sincable = check_for_word(field_image, word)
#         if is_sincable: return 1

#     else: return 0

    