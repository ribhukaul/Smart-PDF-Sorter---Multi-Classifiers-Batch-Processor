from datetime import datetime
from pathlib import Path
import cv2
import numpy as np



def convert_isin(isin_str):
    # common needed conversions
    isin_str = isin_str.replace('$', 'S')
    isin_str = ''.join(e for e in isin_str if e.isalnum())
    
    # if len(isin_str) != 12:
    #     return None
    return isin_str


def convert_date(date_str):
    """
    Converts date string from "%m/%d/%Y" format to "%d-%m-%Y".

    Args:
        date_str (str): The date string to convert.

    Returns:
        str: The converted date string.
    """
    if not date_str.strip():
        return "NA"
    if is_valid_date(date_str):
        date_str = ''.join(e for e in date_str if e.isnumeric() or e == '/')
        # If the year is only 2 digits, add 20 to the front of the year
        if len(date_str.split('/')[-1]) == 2:
            date_str = date_str[:-2] + '20' + date_str[-2:]            
        
        return datetime.strptime(date_str.strip(), "%m/%d/%Y").strftime("%d/%m/%Y")
    else:
        return "NA"


def convert_price(price_str):
    """
    Converts price string to a float.

    Args:
        price_str (str): The price string to convert.

    Returns:
        float: The converted price.
    """
    try:
        # Minimal cleaning for conversion
        price_str = [e for e in price_str if e.isnumeric() or e in ['.', ',']]
        price_str = ''.join(price_str)
        price_str = price_str.replace(',', '.')

        return round(float(price_str), 3)
    except ValueError:
        return None


def is_valid_date(date_string: str) -> bool:
    """
    Checks if a string is a valid date.

    Args:
        date_string (str): The string to check.

    Returns:
        bool: True if the string is a valid date, False otherwise.
    """
    try:
        # Attempt to convert the string into a datetime object
        # Here %m/%d/%Y is the date format, change it as per your needs
        # remove everything apart from numbers and '/' from the string
        date_string = ''.join(e for e in date_string if e.isnumeric() or e == '/')
        # If the year is only 2 digits, add 20 to the front
        if len(date_string.split('/')[-1]) == 2:
            datetime.strptime(date_string, "%m/%d/%y") 
        else:
            datetime.strptime(date_string, "%m/%d/%Y") 
        return True
    except ValueError:
        return False


def is_valid_price(price_str):
    """
    Checks if a string could represent a valid price.

    Args:
        price_str (str): The string to check.

    Returns:
        bool: True if the string could represent a valid price, False otherwise.
    """
    try:
        float(price_str)
        return True
    except ValueError:
        return False


def preprocess_image(image_path: Path) -> np.ndarray:
    """
    Preprocess the image to make it suitable for OCR.

    Args:

    Returns:
        numpy.ndarray: Preprocessed image.
    """
    # image = cv2.imread(str(image_path))
    # image = cv2.resize(image, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # _, thresh1 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # kernel = np.ones((1, 1), np.uint8)
    # img_dilation = cv2.dilate(thresh1, kernel, iterations=1)
    # img_erode = cv2.erode(img_dilation, kernel, iterations=1)
    #
    print("image_path:", image_path)
    image = cv2.imread(str(image_path))
    print("red image:", image)
    image = cv2.resize(image, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
    print("resized image:", image)
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    print("gray image:", gray)
    return gray

