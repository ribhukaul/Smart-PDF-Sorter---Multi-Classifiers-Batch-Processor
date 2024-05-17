from abc import abstractmethod
from ..models import Models
from .config.cost_config import cost_per_token
from .utils import get_document_text
from extractors.general_extractors.config.cost_config import cost_per_token
from .llm_functions import get_doc_language, llm_extraction
from extractors.azure.document_intelligence import get_tables_from_doc
from .utils import select_desired_page, select_desired_table
from extractors.general_extractors.llm_functions import general_table_inspection

from .config.prompt_config import word_representation
import threading
from extractors.output_handler.OutputHandler import OutputHandler

class ThreadFunction(threading.Thread):
    def __init__(self, function, args):
        threading.Thread.__init__(self)
        self.function = function
        self.args = args
        self.result = None
    def run(self):
        if self.args is None:
            self.result = self.function()
        else:
            self.result = self.function(**self.args)
    def get_result(self):
        return self.result



class Extractor:
    """parent class for all extractors"""

    def __init__(self, doc_path, predefined_language=False):
        self.file_id = doc_path
        self.doc_path = doc_path
        self.text = get_document_text(doc_path)
        if predefined_language:
            self.language = predefined_language
        else:
            self.language = get_doc_language(self.text, self.file_id)

        self.di_tables_pages = {}
        self.raw_data_pages = {}
        self.extraction = {}
        
    # DOCSTRING MISSING
    def threader(self, functions_parameters):

        threads = {}
        results = {}
        for function_name, parameters in functions_parameters.items():
            func, args = parameters['function'], parameters.get('args')
            print(func, args)
          
            thread = ThreadFunction(func, args)
            threads[function_name] = thread
            thread.start()
        for _, thread in threads.items():
            thread.join()
        for function_name, thread in threads.items():
            results[function_name] = thread.get_result()
        return results

    
    
    def _extract_table(self, type, black_list_pages=[]):
        """General table extractor, given a table type it first finds the page within
        the document where the table is located, it then extracts all the tables from
        that page and returns the one with the most occurrences of the words of the table
        type.

        Args:
           type (str): type of table to extract, used to get configuration.
           black_list_pages (int[], optional): Pages to ignore. Defaults to [].

        Returns:
            pandas.DataFrame: dataframe containing the table.
        """
        try:
            # Select page with table
            keywords = word_representation[self.language][type]
            text = [page if i not in black_list_pages else "" for i, page in enumerate(self.text)]
            page = select_desired_page(text, keywords)

            # Get all the tables from the page
            if self.di_tables_pages is not None and page not in self.di_tables_pages.keys():
                page_num = int(page) + 1
                tables, raw_data = get_tables_from_doc(self.doc_path, specific_pages=page_num, language=self.language)
                self.di_tables_pages[page] = tables
                self.raw_data_pages[page] = raw_data
            else:
                tables = self.di_tables_pages[page]
                raw_data = self.raw_data_pages[page]

            # Select the right table
            table_nr = select_desired_table(tables, keywords)
            return tables[int(table_nr)], raw_data

        except Exception as error:
            print("extract table error" + repr(error))
            return None
            # @ELIA?
            # exreturn = dict()
            # for table in tables:
            #     exreturn.update(table)
            





    def fill_tables(self, pages):
        """experimental for faster runs, fills the tables in the document asynchronously all in one

        Args:
            page (_type_): _description_
        """
        fill, raw_data = get_tables_from_doc(self.doc_path, specific_pages=pages, language=self.language)
        for idx, table in enumerate(fill):
            safe_number= getattr(raw_data.tables[idx] if idx < len(raw_data.tables) else None, 'bounding_regions', None)[0].get("pageNumber", None)
            if safe_number:
                self.di_tables_pages.setdefault(str(safe_number - 1), []).append(table)
                self.raw_data_pages.setdefault(str(safe_number - 1), []).append(raw_data)

    # REVIEW
    def _process_costs(self):
        """processes the cost of the calls given local config and prepares them for the output

        Returns:
            _type_: _description_
        """
        api_costs = Models.get_costs(self.file_id)
        azure_costs = {
            "azure": {"pages": len(self.di_tables_pages), "cost": len(self.di_tables_pages) * cost_per_token["azure"]}
        }
        api_costs.update(azure_costs)

        total_tokens = sum(entry.get("tokens", 0) for entry in api_costs.values())
        total_cost = sum(entry.get("cost", 0) for entry in api_costs.values())

        # Add the "total" element to the dictionary
        api_costs["total"] = {"tokens": total_tokens, "cost": total_cost}
        for entry in api_costs.values():
            if "cost" in entry:
                entry["cost"] = round(entry["cost"], 2)
        return api_costs

    def extract_from_multiple_tables(self, pages, tags, complex=False):
        """extracts from multiple tables

        Args:
            pages (int[]): pages to extract from

        Returns:
            dict(): dict containing the results
        """
        try:

            extraction = dict()
            list_tables = list(self.di_tables_pages)
            tables = []
            concatenated_str = "i valori sono in una di queste tabelle e solo in una o in nessuna, se si riferisce all'allegato ignoralo "
            for page in pages:
                tables += self.di_tables_pages[list_tables[page]]

            for idx, table in enumerate(tables):
                concatenated_str = concatenated_str + f"||||||||||||tabella numero {idx}:{table.to_string( na_rep='N/A')} "
                

            for tag in tags:
                llm_extract=concatenated_str
                if complex:
                    #concatenated_str += " " + "Aggiungi un # alla fine della risposta"
                    llm_extract = llm_extraction(concatenated_str, tag, self.file_id, language=self.language)
                extraction.update(
                    dict(
                        general_table_inspection(
                            llm_extract,
                            tag,
                            self.file_id,
                            language=self.language,
                        )
                    )
                )

        except Exception as error:
            print("extract multiple tables error" + repr(error))

        return extraction

    def create_output(self, tenant, extractor_type, results):
        """creates a output with correct format

        Args:
            results (dict()): results to convert
            type (str, optional): type of extraction.

        Returns:
            dict: dictionary containing the results
        """
        extraction_output = OutputHandler(tenant=tenant, extractor_type=extractor_type, results=results, doc_path=self.doc_path)
        return extraction_output.complete_output
    
    # TEMPORARY
    def raccorda(self, dictionary, renaming:dict, keep=False):  # could tecnically go to utils
        """renames fiels

        Args:
            dictionary (dict()): dict to rename
            rename (dict()): dict containing the renaming
            keep (bool, optional): if true, keeps the old field. Defaults to False.

        Returns:
            new_dict dict(): dict renamed
        """
        # uncomment for extra fields
        # dictionary=self.create_json(dictionary)
        new_dict = {renaming[key]: value for key, value in dictionary.items() if key in renaming.keys()}
        if keep:
            new_dict.update({key: value for key, value in dictionary.items() if key not in renaming.keys()})
        return new_dict

    @abstractmethod
    def process(self):
        ...
