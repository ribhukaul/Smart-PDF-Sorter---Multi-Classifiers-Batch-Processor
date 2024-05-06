from ..scraper_finder import find_roi, get_text

def get_field_value(image_text, image, field_name):
    """
    Extracts the value of a specific field from an image.

    Args:
        image_text (str): The text extracted from the image.
        image (numpy.ndarray): The image to extract the field value from.
        field_name (str): The name of the field to extract the value from.

    Returns:
        str: The value of the specified field, or None if the field was not found.
    """
    roi = find_roi(image_text, field_name)
    if roi is not None:
        _, xmax, ymin, ymax = roi

        # text area
        text_area = image[ymin-5:ymax+3, xmax:xmax+350]
        
        value =get_text(text_area, "string")
    
        return value


def cpn_formula_extractor(images_text, image):
    """
    Extracts the formula from a CPN bond image.

    Args:
        images_text (str): The text extracted from the bond image.
        image (numpy.ndarray): The bond image.

    Returns:
        str: The formula extracted from the bond image.
    """
    field = "formula des"
    roi = find_roi(images_text, field)

    if roi is not None:
        xmin, xmax, ymin, ymax = roi
        # text area and text
        formula_text_area = image[ymax:, xmin-3:]
        formula_text = get_text(formula_text_area)
        roi = find_roi(formula_text, "formula")
        if roi is not None:
            xmin, xmax, ymin, ymax = roi
            formula_text_area = formula_text_area[ymin-5:ymax+3, xmax:xmax+400]
            formula = get_text(formula_text_area, "string")
            return formula
        else:
            return "N/A"
    else:
        return "N/A"


def check_date(date_extraction):
    """
    Extracts the date from a string and returns it in a standardized format.
    
    Args:
    date_extraction (str): A string containing a date in the format "MM/DD/YYYY <other text>".
    
    Returns:
    str: The date in the format "MM/DD/YYYY".
    If the input string is not in the expected format, returns None.
    """
    try:
        # Split the input string by spaces and take the first element (the date)
        date = date_extraction.split(" ")[0]
        # Remove any non-numeric characters or slashes from the date string
        date_str = ''.join(e for e in date if e.isnumeric() or e == '/')
    except Exception as e:
        print(f"Error extracting date: {e}")
        date_str = None
    
    return date_str

