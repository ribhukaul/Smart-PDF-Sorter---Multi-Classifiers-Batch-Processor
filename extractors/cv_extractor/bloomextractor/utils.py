import cv2
import numpy as np
from typing import Tuple, Dict
from .scraper_finder import find_roi, get_text, find_roi_refined


def recognize_image_type(image_path):
    """Recognize image type based on the text in the image and counting the occurences of certain words.

    Args:
        image_path (str): path to the image

    Returns:
        str: 'DES or 'CPN'
    """
    # Upload image and get text
    image = cv2.imread(str(image_path))
    text = get_text(image, mode='string').lower()
    print('THIS IS A TEST:')
    print(get_text(image).lower())


    # Words to find
    des = ["name", 'industry', 'security', 'mkt iss', 'rank', 'coupon', 'cpn freq',
              'maturity', 'calc type', 'figi', 'isin', 'cusip']
    cpn = ['index 1', 'index 2', 'multiplier 1', 'multiplier 2', 'multiplier 3','in arrears']

    # COunt occurrences
    des_count = sum([1 for word in des if word in text])
    cpn_count = sum([1 for word in cpn if word in text])
    if des_count > cpn_count:
        return 'DES'
    else: 
        return 'CPN'



############################
##### LEGACY APPROACH ######
############################
def recognize_image_type_original(image_path: np.ndarray) -> str:
    """
    Recognizes the type of the image based on the color of the background
    behind the text "11) Bond Info" OR "22) Coupons".

    Args:
        image_path (numpy.ndarray): The image to recognize the type of.

    Returns:
        str: The type of the image.
    """

    # Position of different tag within an image
    position_dict = {
        'DES': (437, 338, 10, 10),
        'CPN': (450,650, 20, 15),
        'SCHEDULES': (445, 622, 20, 15),
    }

    image = cv2.imread(str(image_path))
    # Iterate over the positions in the dictionary
    for image_type, position in position_dict.items():
        x, y, w, h = position

        area = image[y:y+h, x:x+w]
        # show the area
        cv2.imshow("Area", area)
        cv2.waitKey(0)
        #

        # Convert the area to RGB color space
        area_rgb = cv2.cvtColor(area, cv2.COLOR_BGR2RGB)

        # Calculate the mean color of the area
        mean_color = area_rgb.mean(axis=(0, 1))

        reference_color = np.array([30, 106, 180])

        # Calculate the difference between the mean color and the reference color
        color_difference = np.linalg.norm(mean_color - reference_color)

        threshold = 10
        if color_difference < threshold:
            return image_type

    return 'Others'

from .scraper_utils import preprocess_image
def recognize_image_type_2(image_path):

    image = cv2.imread(str(image_path))
    processed_image = preprocess_image(image_path)

    text = get_text(image, mode='data')
    text_2 = get_text(processed_image, mode='data')


    roi = find_roi(text, 'bond Info')
    if roi is not None:
        x, y, w, h = roi
        area = image[y:y+h, x:x+w]
        # show the area
        cv2.imshow("Area", area)
        cv2.waitKey(0)
        #

        # Convert the area to RGB color space
        area_rgb = cv2.cvtColor(area, cv2.COLOR_BGR2RGB)

        # Calculate the mean color of the area
        mean_color = area_rgb.mean(axis=(0, 1))

        reference_color = np.array([30, 106, 180])

        # Calculate the difference between the mean color and the reference color
        color_difference = np.linalg.norm(mean_color - reference_color)

        threshold = 10
        if color_difference < threshold:
            return 'DES'

