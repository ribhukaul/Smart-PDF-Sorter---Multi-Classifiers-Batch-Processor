import cv2
import os
from typing import Tuple, Optional, List
import pytesseract
import numpy as np
#

#'/extractors/cv_extractor/tesseract/tesseract.exe'

# path of this script
# import os
# dir_name_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # tesseract_path
# tesseract_path = os.path.join(dir_name_path, 'tesseract', 'tesseract.exe')
# pytesseract.pytesseract.tesseract_cmd = tesseract_path



def get_text(image, mode='data', psm=6):
    """
    Extracts text from an image using Tesseract OCR.

    Args:
        image (numpy.ndarray): The image to extract text from.
        mode (str): The mode to use for Tesseract OCR. Can be 'data', 'boxes' or 'string'. Defaults to 'data'.
        psm: (int): from 0 to 13. Defaults to 6. refers to the "page segmentation mode" opiton of pytesseract model.

    Returns:
        dict or str: The extracted text. If mode is 'data', returns a dictionary with information about each word. If mode is 'string', returns a string with the extracted text.
    """
    #pytesseract.pytesseract.tesseract_cmd =os.environ['TESSERACT_CMD']
    retries = 0
    while retries < 5:
        try:
            if mode=='data':
                x = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
                print(x)
                return x
            elif mode=='string':
                x = pytesseract.image_to_string(image, config=f'--psm {psm}')
                print(x)
                return x
            elif mode=='boxes':
                x = pytesseract.image_to_boxes(image)
                print(x)
                return x#pytesseract.image_to_boxes(image)
        except Exception as ex:
            print(ex)
            retries += 1
            print(f"Retrying ({retries}/5)...")



def find_roi(text_d, keyword: str) -> Optional[Tuple[int, int, int, int]]:
    """
    Find Region of Interest (ROI) in the image based on the keyword.

    Args:
        text_d (dict): The image to search the keyword in.
        keyword (str): The keyword to search for.
       
    Returns:
        Tuple[int, int, int, int]: The bounding box of the ROI (x_min, x_max, y_min, y_max).
        None if the keyword is not found in the image.
    """
    n_boxes = len(text_d['text'])

    # Create phrases with the same number of words as the keyword
    phrases = [' '.join(text_d['text'][i:i+len(keyword.split(' '))]) for i in range(n_boxes - len(keyword.split(' ')) + 1)]

    for i, phrase in enumerate(phrases):
        if keyword.lower() in phrase.lower():
            keyword_boxes = [(text_d['left'][j], text_d['top'][j], text_d['left'][j] + text_d['width'][j], text_d['top'][j] + text_d['height'][j]) 
                             for j in range(i, i+len(keyword.split(' ')))]
            x_min, y_min = min(box[0] for box in keyword_boxes), min(box[1] for box in keyword_boxes)
            x_max, y_max = max(box[2] for box in keyword_boxes), max(box[3] for box in keyword_boxes)
            
            return (x_min, x_max, y_min, y_max)

    return None



def find_roi_refined(text_d, keyword: str, image: np.array) -> Optional[Tuple[int, int, int, int]]:
    """Find region of interest (ROI) in the image based on the keyword. This function is a refinement of the find_roi function. 
    It takes the image as input and returns the bounding box of the ROI. The refinement consists in taking the area corresponding to the
    exaxt keyword in the image, instead of the area corresponing of the full block of words (.e.g. if we are looking for 'Min Piece' 
    but the model find that it belog to the block 'Min Piece 1000' it will return the area corresponding to 'Min Piece' only and
    not the full block)

    Args:
        text_d (_type_): text of the image
        keyword (str): keyword we are looking for
        image (np.array): image of the table

    Returns:
        Optional[Tuple[int, int, int, int]]: coordinates of the ROI: (x_min, x_max, y_min, y_max)
    """
    # Look for the general ROI
    of = 5

    h = image.shape[0]
    w = image.shape[1]

    roi = find_roi(text_d, keyword)
    if roi is None:
        return None
    x_min, x_max, y_min, y_max = roi
    im = image[y_min:y_max, x_min:x_max]

    # Set coordinates & get image characters with boxes method
    new_xmin = max(x_min-5, 0)
    new_xmax = min(x_max+15, w)
    new_ymin = max(y_min-of, 0)
    new_ymax = min(y_max+of, h)
    small_image = image[new_ymin:new_ymax, new_xmin:new_xmax]
    # show image
    # cv2.imshow('image', small_image)
    # cv2.waitKey(0)
    char_boxes = get_text(small_image, mode='boxes')
    char_box_splitted = char_boxes.splitlines()

    # Make keyword and text of ROI without spaces
    keyord_united = keyword.replace(' ', '')
    roi_text = "".join([i[0] for i in char_box_splitted])
    roi_text_l = roi_text.lower()

    # Find position of keyword in the string
    index = roi_text_l.index(keyord_united)
    key_in_roy_text = char_box_splitted[index:index+len(keyord_united)]
    first_xmin = key_in_roy_text[0].split(' ')[1]
    last_xmax = key_in_roy_text[-1].split(' ')[3]

    # adjust for the new position in image
    x_min = x_min + int(first_xmin) - of
    x_max = x_min + int(last_xmax) - of

    return (x_min, x_max, y_min, y_max)


def get_quadrant(text_d, keyword: str, width: int) -> Optional[Tuple[int, int, int, int]]:
    """
    Find Quadrant of the value corresponding to a key (ROI) in the image based on the keyword.

    Args:
        text_d (dict): The image to search the keyword in.
        keyword (str): The keyword to search for.
        width (int): Width of specificed field of the value corresponding to the key.

    Returns:
        Tuple[int, int, int, int]: The bounding box of the ROI (x, y, width, height).
        None if the keyword is not found in the image.
    """

    roi = find_roi(text_d, keyword)
    if roi is None:
        return None
    x_min, x_max, y_min, y_max = roi

    return (x_max, y_min, width, y_max- y_min)

# review better input would be text, not the image
def check_for_word(image, word, text='') -> bool:
    """
    Checks if a word is present in the image.

    Args:
        image (numpy.ndarray): The image to check.
        word (str): The word to check for.
        text (str, optional): The text in the image. Defaults to ''.

    Returns:
        bool: True if the word is present in the image, False otherwise.
    """

    if not text:
        text = get_text(image, mode="string")
        return word.lower() in text.lower()
    if word in text['text']:
        return True
    else:
        return False


def check_for_symbol(image, folder_path: str) -> List[str]:
    """
    Given an image and a folder path, this function checks for the presence of symbols in the image
    by comparing it with all the images in the folder. If a symbol is found, its filename (without
    the extension) is added to a list of symbols and returned. If no symbols are found, the function
    returns False.

    Args:
        image: A numpy array representing the image to be searched for symbols.
        folder_path: A string representing the path to the folder containing the symbol images.

    Returns:
        A list of strings representing the filenames (without extension) of the symbols found in
        the image. If no symbols are found, returns False.
    """
    symbols = []
  
    for filename in os.listdir(folder_path):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            symbol_image = cv2.imread(os.path.join(folder_path, filename), cv2.IMREAD_GRAYSCALE)
            h, w= symbol_image.shape
            
            # Convert the main image to grayscale if it is not already
            if len(image.shape) == 3:  # If image has 3 dimensions (i.e., it's a color image)
                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:  # If image is already grayscale
                gray_image = image

            # # Apply template Matching
            res = cv2.matchTemplate(gray_image, symbol_image, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            threshold = 0.8
            
            if max_val > threshold:
                symbols.append(filename[:-4])

    symbols = list(set(symbols))

    if symbols:
        return symbols
    else:
        return False




### TO TEST #####
# def find_roi_2(image, target_text):

#     custom_config = r'--oem 3 --psm 6'
#     d = pytesseract.image_to_data(image, config=custom_config, output_type=pytesseract.Output.DICT)

#     roi = None
#     target_found = False

#     for i, word_text in enumerate(d['text']):
#         if target_text in word_text:
#             target_found = True
#             x, y, w, h = d['left'][i], d['top'][i], d['width'][i], d['height'][i]
#             roi = image[y:y+h, x:x+w]

#             break

#     if not target_found:
#         print(f"Target text '{target_text}' not found in the image.")
    

#     cv2.imshow('ROI', roi)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

#     return roi