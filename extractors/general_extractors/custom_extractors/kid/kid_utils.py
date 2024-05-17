import re
from .kid_config.kid_cleaning import (
    strips_cleaning,
    regex_cleaning,
    regex_search,
    exc_multiple_lines,
)


# TO REVIEW -VEDERE CODICE ELIA
def clean_response_regex(type, language, response, to_add=""):
    """cleans a response using a regex

        Args:
        type (str): type associated to regex
        language (str): language associated to regex
        response (dict()| object): data to clean
        to_add (str, optional): string to add to the cleaned data. Defaults to "".
    Returns:
        dict()| object: data cleaned
    """
    try:
        # dict of regexes
        reg_exp = regex_cleaning[language][type]

        for r in reg_exp.items():
            if r[0] in dict(response):
                # match each and keep the match if found
                match = re.search(r[1], str(dict(response)[r[0]]))
                value = "-"
                if match and match.group(0) != "":
                    value = match.group(0)
                    if to_add != "":
                        value = "".join([value, to_add])
                # response can be object or dict
                if isinstance(response, dict):
                    response[r[0]] = value
                else:
                    setattr(response, r[0], value)
    except Exception as e:
        print("clean_response_regex error" + repr(e))

    return response


def clean_response_strips(type, language, response):
    """cleans a response using a list of strings to strip

    Args:
        type (str): type associated to strips
        language (str): language associated to strips
        response (str): data to clean

    Returns:
        str: data cleaned
    """

    strips = strips_cleaning[language][type]
    # cut strips from response
    for s in strips:
        while response.find(s) != -1:
            response = response.replace(s, "")
    # remove leading and trailing spaces
    while response[0] in [",", ":", ".", ";", " ", '"', "'", "\\n"]:
        response = response[1:]
    # replace is for json format
    response = response.replace('"', r"\"")
    return response


def regex_extract(searches, table, language):
    """extract via regex from the table

    Args:
        searches ([str]): what to search
        table (pandas.dataframe): table to search on
        costi (dict()): return dictionary

    Returns:
        dict(): dict with value extracted for each search
    """
    ret = dict()
    intermediate = dict()
    # for each search find it via regex in first column and then extract the value in last column
    for idx, search in enumerate(searches):
        once = True
        intermediate.update(dict([(search, "")]))
        for a in range(1, len(table.index)):
            # if found in first column
            if search_reg(language, search, table.iloc[a, 0]):
                # handle multiple lines exception( exc_multiple_lines is a list of lists of strings, each list is a different exception)
                if search in exc_multiple_lines[0] and once:
                    once = False
                    exc = handle_exc(
                        table,
                        a,
                        searches[idx + 1 if idx + 1 < len(searches) else 0],
                        language,
                    )
                    intermediate.update(dict([(search, exc)]))
                    continue
                # add last column
                updated = " ".join([intermediate[search], str(table.iloc[a, -1])])
                intermediate.update(dict([(search, updated)]))

    # for each search divide the value in min and max and add to dict
    for field, value in intermediate.items():
        if field in searches:
            groups = divide_regex(value)
            # returning 0 and -1 takes care of all cases anyway
            ret.update(dict([(field + "_min", groups[0]), (field + "_max", groups[-1])]))
        else:
            ret.update(dict([(field, value)]))
    return ret


def search_reg(language, type, text):
    """Search a regex in a text and return the match if found.

    Args:
        language (str): language associated to regex
        regex (str): regex to search
        text (str): text to search in

    Returns:
        str: match if found
    """
    match = re.search(regex_search[language][type], text, re.IGNORECASE)
    return match is not None


def handle_exc(table, a, search, language):
    """handles exceptions where table may be split in multiple lines, looks until next search is found

    Args:
        table (pd.dataframe): table to look into
        a (int): index we are at
        search (str): what we are looking for
        language (str): language of the document

    Returns:
        str: values found
    """
    ret = ""
    # while not at the end and we didn't find the next search join the values
    while a < len(table.index) and (not search_reg(language, search, table.iloc[a, 0])):
        ret = " ".join([ret, str(table.iloc[a, -1])])
        a = a + 1
    return ret


# legacy code from gkid
def search_reg(language, type, text):
    """Search a regex in a text and return the match if found.

    Args:
        language (str): language associated to regex
        regex (str): regex to search
        text (str): text to search in

    Returns:
        str: match if found
    """
    match = re.search(regex_search[language][type], text, re.IGNORECASE)
    return match is not None


# legacy code from gkid
def divide_regex(text):
    """Divide a text in two parts using a regex.

    Args:
        text (str): text to divide

    Returns:
        tuple(str,str): tuple containing the two parts of the text
    """
    # gets the 2 numbers
    divided = [x.group() for x in re.finditer("\d+[\.,]?\d*", text, re.IGNORECASE)]
    if divided.__len__() != 0:
        return divided
    return ["-"]
