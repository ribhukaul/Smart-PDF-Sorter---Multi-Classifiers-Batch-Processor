from collections import defaultdict
import re
from langchain_community.document_loaders import PyPDFLoader
import tiktoken
import pandas as pd


def select_desired_page(text, words_repr):
    """Select the page with the most occurrences of the words in words_repr.

    Args:
        text (lst): list of pages text
        words_repr (lst): list of words to look for in the pages provided

    Returns:
        str: page nindex with the most occurrences of the words in words_repr
    """
    counter = defaultdict(int)

    for i, page in enumerate(text):
        if page == "":
            continue

        # Remove punctuation and replace \n with space
        content = page.page_content.lower().replace("\n", " ")
        for word in words_repr:
            # count how many times the word is in the page
            counter[str(i)] += content.count(word)

    # Page with most occurrences
    pg_number = max(counter, key=counter.get)

    return pg_number


def select_desired_table(tables, words_repr):
    """Select the table with the most occurrences of the words in words_repr.

    Args:
        tables (lst): list of df tables
        words_repr (lst): list of words to look for in the pages provided

    Returns:
        int: table index with the most occurrences of the words in words_repr
    """
    counter = defaultdict(int)
    # Search all the tables
    for i, table in enumerate(tables):
        for word in words_repr:
            # print(word)
            # print(table.apply(lambda col:col.str.count(word, flags=re.IGNORECASE)).sum().sum())

            counter[str(i)] += table.apply(lambda col: col.str.count(word, flags=re.IGNORECASE)).sum().sum()

    # Page with most occurrences
    tb_number = max(counter, key=counter.get)
    return tb_number


def select_desired_table_only_header(tables, words_repr):  # change from normal is that it only looks at the header
    """Select the table with the most occurrences of the words in words_repr.

    Args:
        tables (lst): list of df tables
        words_repr (lst): list of words to look for in the pages provided

    Returns:
        int: table index with the most occurrences of the words in words_repr
    """
    new_tables = [table.iloc[0].to_frame() for table in tables]

    counter = defaultdict(int)
    # Search all the tables
    for i, table in enumerate(new_tables):
        for word in words_repr:
            # print(word)
            # print(table.apply(lambda col:col.str.count(word, flags=re.IGNORECASE)).sum().sum())

            counter[str(i)] += table.apply(lambda col: col.str.count(word, flags=re.IGNORECASE)).sum().sum()

    # Page with most occurrences
    tb_number = max(counter, key=counter.get)
    return tb_number


def upload_df_as_excel(df:pd.DataFrame):
    """Upload DF as excel file for LargeLanguageModel analysis.

    Args:
        df (pd.DataFrame): dataframe to upload

    Returns:
        str: path of the uploaded file
    """
    import os
    #return df.to_string()

    if os.environ.get("ENV") == "local":
        tmp_path = "tmp"
    else:
        tmp_path = "/tmp"
    # Modify empty cells with " " to avoid upload errors
    df = df.replace(to_replace="", value=" ")
    df.fillna(' ', inplace=True)
    import uuid
    from langchain_community.document_loaders import UnstructuredExcelLoader

    # Save table to excel and upload it back
    random_file_name = str(uuid.uuid4()) + ".xlsx"
    save_name = os.path.join(tmp_path, random_file_name)
    df.to_excel(save_name, index=False, header=False)
    loader = UnstructuredExcelLoader(save_name)
    loaded_table = loader.load()
    os.remove(save_name)

    return loaded_table


def num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
    """
    Returns the number of tokens in a given string using the specified encoding.

    Args:
        string (str): The input string to count tokens from.
        encoding_name (str, optional): The name of the encoding to use. Defaults to 'cl100k_base'.

    Returns:
        int: The number of tokens in the input string.
    """
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def is_more_number(text):
    """Check if a text in the page is composed  more than 30% of numbers

    Args:
        text (str): text to check

    Returns:
        Bool: if the text is composed more than 30% of numbers
    """

    letter_count = sum(1 for char in text if char.isalpha())
    number_count = sum(1 for char in text if char.isnumeric())
    ratio = number_count / (number_count + letter_count)
    if ratio > 0.3:
        return True
    else:
        return False


def _decode_first_condtition(text):
    """Decode the first condition

    Args:
        text (str): text to decode

    Returns:
        str: decoded text
    """
    return "".join(
        char
        for char in text
        if char.isalnum() or char.isspace() or char in [",", ".", "€", "%", ":", ";", "(", ")", "-", "/"]
    )


def _decode_second_condition(text):
    """Decode the second condition

    Args:
        text (str): text to decode

    Returns:
        str: decoded text
    """
    content = text.split("/")
    return "".join([chr(int(code)) for code in content if code and 32 <= int(code) <= 110000000])


def get_document_text(file_path):
    """Uploads a file to the server and returns the pages.

    Args:
        file_name (path): _description_

    Returns:
        _type_: _description_
    """
    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load()
        del loader

        # Decoding conditions
        first_page = pages[0].page_content
        first_encoded_condition = first_page.count("\x00") > 100
        second_encoded_condition = is_more_number(first_page)
        # Decode
        for page in pages:
            content = page.page_content
            if first_encoded_condition:
                page.page_content = _decode_first_condtition(content)
            elif second_encoded_condition:
                page.page_content = _decode_second_condition(content)
        return pages

    except Exception as error:
        print("get document text error" + repr(error))
        raise error


def is_in_text(pattern, text) -> bool:
    """returns True if the pattern is found in the text

    Args:
        pattern (str): pattern to search
        text (str): text to search in

    Returns:
        bool: if the pattern is found in the text
    """

    pattern = re.compile(pattern, re.IGNORECASE)
    ret = bool(pattern.search(text))
    return ret


def search_in_pattern_in_text(pattern, text, pattern_inside):
    """searches for a pattern inside a pattern in a text

    Args:
        pattern (str): initial pattern
        text (str): text to search in
        pattern_inside (str): pattern of the value to return

    Returns:
        str: value found
    """
    match = re.search(pattern, text, re.IGNORECASE)
    if not match:
        return
    match_final = re.findall(pattern_inside, match.group(0), re.IGNORECASE)
    if not match_final:
        return
    return match_final[-1]


def extract_between(text, start, end):
    """extracts the text between two strings

    Args:
        text (str): text to search in
        start (str): start of where to look
        end (str): end of where to look

    Returns:
        str: text in between
    """
    pattern = f"(\\n)?\s*{re.escape(start)}\s*(\\n)?\s*(\S.*?)\s*(?={re.escape(end)})"
    matches = re.findall(pattern, text, re.IGNORECASE)
    return matches[0][-1] if matches and matches[0] else None


def format_pages_num(arr):
    """return the list as the function wants,

    Args:
        arr (_type_): _description_

    Returns:
        str: strified list
    """
    if not arr:
        return None
    if isinstance(arr, str):
        return arr
    if isinstance(arr, int):
        return str(arr)

    arr = sorted(set(arr))  # Sort the array and remove duplicates
    ranges = []
    start = arr[0]
    end = arr[0]

    for i in range(1, len(arr)):
        if arr[i] - arr[i - 1] == 1:
            end = arr[i]
        else:
            if start == end:
                ranges.append(str(start))
            else:
                ranges.append(f"{start}-{end}")
            start = arr[i]
            end = arr[i]

    # Add the last range or number
    if start == end:
        ranges.append(str(start))
    else:
        ranges.append(f"{start}-{end}")

    return ",".join(ranges)


def check_valid(main_table, other_tables):
    return all(
        not main_table.equals(other) for other in other_tables
    ) and isinstance(main_table, pd.DataFrame)

def set_flag(extraction, pattern):
    """sets a flag if the pattern is found in the extraction
    Args:
        extraction (str): to search in
        pattern (str): regex pattern
    Returns:
        bool: if the pattern is found in the extraction
    """

    if is_in_text(pattern, extraction):
        extraction = True
    else:
        extraction = False

    return extraction


def filter_list_by_pattern(extraction, pattern):
    """filter the list leaving only the pattern
    Args:
        extraction (List): to clean
        pattern (str): regex pattern
    Returns:
        List: cleaned list
    """

    searches = []
    for str in extraction:
        search = re.search(pattern, str)
        if search:
            searches.append(search.group(1))
    extraction = searches if searches else ["not found"]
    return extraction