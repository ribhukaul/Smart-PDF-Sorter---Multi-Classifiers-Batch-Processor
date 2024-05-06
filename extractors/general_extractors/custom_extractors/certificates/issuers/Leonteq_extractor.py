from extractors.general_extractors.custom_extractors.certificates.derivati_extractor import DerivatiKidExtractor
import asyncio
import os
import re
import pandas as pd
from extractors.general_extractors.llm_functions import (
    llm_extraction_and_tag,
)
from extractors.general_extractors.llm_functions import general_table_inspection

from extractors.models import Models
from extractors.general_extractors.utils import check_valid
from ..certificates_config.cert_cleaning import header_mappings


class LeonteqDerivatiKidExtractor(DerivatiKidExtractor):

    def __init__(self, doc_path) -> None:
        self.doc_path = doc_path
        super().__init__(doc_path, "it")

    async def extract_general_data(self):
        """
        Extract general data from the document (ISIN, descrizione, emittente).

        Returns: dict(): data extracted
        """
        extraction = dict()
        try:
            # Extract and clean data
            extraction = dict(
                llm_extraction_and_tag([self.text[0]], self.language, "general_info_certificati", self.file_id)
            )

            # Extract ISIN and update the extraction dictionary
            extraction["isin"] = self.extract_isin()

            # Uncomment the following line if you need to clean the response with regex
            # extraction = clean_response_regex("general_info_certificati", self.language, extraction)

        except Exception as error:
            print(f"Extract general data error: {error!r}")
            error_keys = ["isin", "descrizione", "emittente"]
            extraction = {key: extraction.get(key, "ERROR") for key in error_keys}

        return extraction

    def extract_isin(self):
        """extract isin with regex

        Returns:
            str: isin or -
        """
        to_search = self.text[0].page_content[:1600]
        isin = re.search(r"[A-Z]{2}[A-Z0-9]{9}\d", to_search)
        return isin.group(0) if isin else "-"

    async def extract_cedola(self, table):
        """extracts the cedola from the table
        can be a complex table or a dense text

        Args:
            table (pd.DataFrame): table containing the cedola

        Returns:
            dict(): dictionary containing the cedola
        """
        extraction = dict()
        try:
            if isinstance(table, str):
                extraction = self.regex_cedola(table)
            else:
                # kind of complex table extraction without tagging
                # TODO: check if works
                extraction = general_table_inspection(
                    table.to_string(),
                    "cedola",
                    self.file_id,
                    language=self.language,
                )
        except Exception as error:
            print("extract_cedola error" + repr(error))
            error_list=[
                "data_osservazione_cedola",
                "liv_attiv_cedola",
                "data_pagamento_cedola",
                "importo_cedola",
                "data_osservazione_autocall",
                "liv_attiv_autocall",
                "data_pagamento_autocall"
            ]
            extraction = {key: extraction.get(key, "ERROR") for key in error_list}

        return extraction

    def regex_cedola(self, og_string):
        """splits dense text into a list of dictionaries

        Args:
            og_string (str): the entire page as a string

        Returns:
            dict: cedole
        """
        names, ret = [], []
        first_divide = re.split(r"▪", og_string)[:-1]

        if not first_divide:
            return [{"cedola": "not found"}]

        # Extract and remove first header
        found_name = re.search(r"data.*$", first_divide.pop(0), re.IGNORECASE)
        if found_name:
            names.append("Data " + found_name.group(0))

        # Remove and append other headers until date format is found
        while first_divide and not re.match(r"1[/\-.]\d+[/\-.]\d+", first_divide[0]):
            names.append(first_divide.pop(0))

        # Reassemble remaining text and split by dates
        string = "▪".join(first_divide)
        dates = re.findall(r"(\d{1,2}[/\-.](?:\n)?\d{1,2}[/\-.]\d{1,2}[/\-.]\d{1,4})", string)
        if dates:
            names.append(first_divide[0].replace(dates[0], ""))

        names = self.clean_names(names)

        # Clean dates from potential leading characters
        dates = [date[date.find(".") + 1 :] for date in dates]
        divided = re.split(r"\d{1,2}[/\-.](?:\n)?\d{1,2}[/\-.]\d{1,2}[/\-.]\d{1,4}", string)[1:]

        # Iterate over split sections to build dictionaries
        for i, section in enumerate(divided, start=1):
            items = re.split("▪", section)
            extracted = {
                names[idx] if idx < len(names) else "name not found": items[idx] if idx == 0 else first_date[i - 1]
                for idx in range(len(items))
            }
            ret.append(extracted)

        # Handle last date, if present
        last_data = re.search(r"\d{1,2}[/\-.]\d{1,2}[/\-.]\d{1,4}", first_divide[-1])
        if last_data:
            ret[-1][names[-1]] = last_data.group(0)

        return ret

    def clean_names(self, names):
        """cleans the names of the headers

        Args:
            names ([str]): the uncleaned names

        Returns:
            [str]: the cleaned names
        """
        for idx, name in enumerate(names):
            for search, value in header_mappings.items():
                if re.search(search, name, re.IGNORECASE):
                    names[idx] = value
                    break
        return names

    async def extract_sottostanti(self, table):
        """Extracts the sottostanti from the table.

        Args:
            table (pd.DataFrame): Table containing the sottostanti.
            extracts from table and from header

        Returns:
            dict: Dictionary containing the sottostanti.
                First extractions are arrays, second are single data.
        """
        extraction = {
            "liv_fixing_iniziale": "ERROR",
            "liv_att_cedola_perc": "ERROR",
            "strike_level_perc": "ERROR", 
            "livello_barriera": "ERROR",
            "livello_cap": "ERROR",
            "sottostante": "ERROR",
            "tipo": "ERROR",
            "borsa": "ERROR",
            "bloom": "ERROR",
            "isin": "ERROR",
            "fixing_eur": "ERROR",
            "barriera_eur": "ERROR",
            "coupon_eur": "ERROR",  
        }
        try:
            # Asynchronous tasks for general table inspection
            tasks = [
                asyncio.create_task(
                    general_table_inspection(table, "sottostanti", self.file_id, language=self.language)
                ),
                asyncio.create_task(
                    general_table_inspection(table.iloc[0], "sottostanti_header", self.file_id, language=self.language)
                ),
            ]
            await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)

            # Merging results from the tasks
            extraction.update({**dict(tasks[0].result()), **dict(tasks[1].result())})
        except Exception as error:
            print(f"extract_sottostanti first phase error: {error}")

        try:
            # Search for coupon trigger percentage in reverse order
            found_liv = "N/A"
            for cell in table.iloc[0][::-1]:
                if cell and re.search(r"coupon.{0,4}trigge", cell, re.IGNORECASE):
                    if percentage_match := re.search(r"\d+\.?\d* ?%", cell):
                        found_liv = percentage_match.group(0)
                        break
            extraction["liv_att_cedola_perc"] = found_liv
        except Exception as error:
            print(f"extract_sottostanti second phase error: {error}")

        return extraction

    async def extract_main_info(self, table):
        """Extracts the main info from the table

        Args:
            table (pd.DataFrame): Table containing the main info

        Returns:
            dict: Dictionary containing the main info
        """
        try:
            # Attempt to extract main info using general table inspection
            extraction = await general_table_inspection(
                table,
                "main_info",
                self.file_id,
                language=self.language,
            )
        except Exception as error:
            print(f"extract_main_info error: {repr(error)}")
            # Define keys to check in case of error
            error_keys = [
                "valuta","data_emissione","periodo",
                "data_rimborso","prezzo","liv_fix_fin","quotazione","perf_peg","inv_min","garanzia_min_perc",
                "data_fix_ini","data_negoziazione","data_fix_fin","liv_fix_ini","mod_pagamento","tasso_cedola_cond",
                "cedola_garantita_perc","rischio_cambio","importo_rimborso","importo_protezione_capitale","partecipazione",
            ]
            # Update extraction with 'ERROR' for missing keys in case of exception
            extraction = {key: extraction.get(key, "ERROR") for key in error_keys}

        return extraction

        
    def check_validity_cedola(self, sottostanti_table, main_info_table, cedola_table, cedola_table_2):
        """check validity of table cedola and cedola2, if both are valid, it concatenates them

        Args:
            sottostanti_table (pd.Dataframe): to confront
            main_info_table (pd.Dataframe): to confront
            cedola_table (pd.Dataframe): found cedola table
            cedola_table_2 (pd.Dataframe): found cedola table

        Returns:
            pd.Dataframe: valid cedola table
        """
        cedola_valid= check_valid(cedola_table, [sottostanti_table, main_info_table])
        
        cedola2_valid = check_valid(cedola_table_2, [sottostanti_table, main_info_table])

        if not cedola_valid and not cedola2_valid:
            cedola_table = (
                str(getattr(self.text[0], "page_content", "")) + " " + str(getattr(self.text[1], "page_content", ""))
            )
        elif cedola_valid and cedola2_valid:
            try:
                while not cedola_table_2.empty and re.search(r"[A-Za-z].*[A-Za-z]", cedola_table_2.iloc[0, 0]):
                    cedola_table_2 = cedola_table_2.iloc[1:, :]
                cedola_table = pd.concat([cedola_table, cedola_table_2], ignore_index=True)
            except Exception as error:
                print("more lines ignored:" + self.file_id+ error)
        elif not cedola_valid and cedola2_valid:
            cedola_table = cedola_table_2
        
        return cedola_table, cedola_table_2


    async def get_tables(self):
        """Calc table extractor, it extracts the tables from the document asynchronously

        Returns:
            dict([pandas.dataframe]): tables as dataframe
        """
        try:
            self.fill_tables([1,2,3])

            sottostanti_table,_ = self._extract_table_only_header("sottostanti", api_version="2023-10-31-preview")
            main_info_table,_ = self._extract_table("main_info")
            cedola_table,_ = self._extract_table("cedola", black_list_pages=[1])
            cedola_table_2,_ = self._extract_table("cedola", black_list_pages=[0])

            cedola_table,cedola_table_2 = self.check_validity_cedola(cedola_table, main_info_table, sottostanti_table, cedola_table_2)
                
        except Exception as error:
            print("calc table error" + repr(error))
            error_list=["cedola_table", "sottostanti_table", "main_info_table"]
            for error in error_list:
                if error not in locals():
                    locals()[error] = "ERROR"

        return {"cedola": cedola_table, "sottostanti": sottostanti_table, "main_info": main_info_table}

    
    async def extract_callable(self):
        """extracts the callable from the document
        looks if the word is in the document thats it

        Returns:
            dict(): dictionary containing the callable
        """
        is_callable = {
            "autocallable": 0,
            "softcallable": 0,
            "putable": 0,
            "effetto_memoria": 0,
        }
        is_callable = self.extract_regex_text("leonteq", 0, is_callable)

        return is_callable

    def fill_array(self, dictionary):
        """fills the arrays in the dictionary with '-'
        so that they all have the same length for excel
        
        Args:
            dictionary (dict): dictionary to fill
            
        Returns:
            dict: dictionary with filled arrays
        """

        max_length = max((len(value) for value in dictionary.values() if isinstance(value, list)), default=0)
        # Iterate through the dictionary and fill the arrays with '-'
        for key, value in dictionary.items():
            if isinstance(value, list):
                # If the array is shorter than max_length, fill with '-'
                dictionary[key] = value + ["-"] * (max_length - len(value))

        return dictionary

    def _write_to_excel(self, complete, exploded_cedola, sottostanti, api_costs, filename):
        """writes the results to an excel file

        Args:
            args (dict()): all the results
        """
        

        with pd.ExcelWriter(
            "results\\30gennaio\\resultsmarco_{}.xlsx".format(os.path.basename(self.file_id)),
            engine="xlsxwriter",
        ) as excel_writer:
            # Write the first DataFrame to Sheet1
            results1 = pd.DataFrame(complete, index=[filename]).T
            results1.to_excel(excel_writer, sheet_name="info_anagrafiche", header=True)

            results2 = pd.DataFrame(self.raccorda(exploded_cedola, "leonteq", keep=True))
            results2.to_excel(excel_writer, sheet_name="date cedole autocall", header=True)

            # Write the second DataFrame to Sheet2
            results3 = pd.DataFrame(self.raccorda(dict(sottostanti), "leonteq", keep=True)).T
            results3.to_excel(excel_writer, sheet_name="sottostanti", header=True)

            # Write the second DataFrame to Sheet2
            results4 = pd.DataFrame.from_dict(api_costs, orient="index")
            results4 = pd.concat(
                [
                    pd.DataFrame([results4.columns], columns=results4.columns),
                    results4,
                ]
            )
            results4.reset_index(inplace=True)
            results4.columns = ["API"] + list(results4.columns)[1:]
            results4.to_excel(excel_writer, sheet_name="api costs", header=True, index=False)

    async def process(self):
        """main processor in different phases, first phases extracts the tables and general information,
        and target market, second phase extracts the rest of the fields.

        Returns:
            dict(filename,dict()): dictionary containing the results for the file
        """
        # FIRST STAGE: get tables and general information
        try:
            print("REAL START")
            tasks = []

            tasks.append(asyncio.create_task(self.get_tables()))
            tasks.append(asyncio.create_task(self.extract_general_data()))
            tasks.append(asyncio.create_task(self.extract_callable()))

            await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)

            tables, basic_information, is_callable = [task.result() for task in tasks]

        except Exception as error:
            print("first stage error" + repr(error))
        # SECOND STAGE: extract RIY, costs, commissions and performances
        try:
            tasks = []
            tasks.append(asyncio.create_task(self.extract_cedola(tables["cedola"])))
            tasks.append(asyncio.create_task(self.extract_sottostanti(tables["sottostanti"])))
            tasks.append(asyncio.create_task(self.extract_main_info(tables["main_info"])))

            await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)

            cedola, sottostanti, main_info = [task.result() for task in tasks]

        except Exception as error:
            print("second stage error" + repr(error))

        try:
            # Merge and orders all the results
            exploded_cedola = dict()

            if isinstance(tables["cedola"], str):
                for ced in dict(cedola):
                    for key, value in ced.items():
                        exploded_cedola.setdefault(key, []).append(value)
            else:
                for ced in cedola:
                    exploded_cedola.update({ced[0]: ced[1]})

            exploded_cedola = self.fill_array(exploded_cedola)

            sottostanti = self.fill_array(dict(sottostanti))

            filename = os.path.splitext(os.path.basename(self.doc_path))[0]

            api_costs = self._process_costs()

            # raccordo
            complete = self.raccorda(
                {
                    **dict(is_callable),
                    **dict(basic_information),
                    **dict(main_info),
                },
                "leonteq",
                keep=True,
            )

            
            json=self.create_json({
                    "file_name": filename,
                    **dict(is_callable),
                    **dict(basic_information),
                    **dict(api_costs),
                    **dict(sottostanti),
                    **dict(exploded_cedola),
                    **dict(basic_information),
                    **dict(main_info),
                }, "bnp")
            
            self._write_to_excel(complete, exploded_cedola, sottostanti, api_costs, filename)
            
            return json

        except Exception as error:
            print("dictionary error: " + repr(error))
            filename = os.path.splitext(os.path.basename(self.doc_path))[0]
            complete = None

        Models.clear_resources_file(filename)
        return complete
