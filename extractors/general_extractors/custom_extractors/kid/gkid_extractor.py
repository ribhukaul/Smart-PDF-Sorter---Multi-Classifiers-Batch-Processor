from .kid_extractor import KidExtractor
from .kid_utils import clean_response_strips, clean_response_regex, regex_extract
from ...llm_functions import llm_extraction_and_tag
# TO REVIEW @elia
#from extractors.general_extractors.custom_extractors.kid.kid_config.cleaning_gkid  import regex_cleaning, regex_search, strips_cleaning


class GKidExtractor(KidExtractor):

    def __init__(self, doc_path, predefined_language="it") -> None:
        super().__init__(doc_path, predefined_language)

    def get_tables(self):
        """Get GKID tables asynchronusly.

        Returns:
            dict([pandas.dataframe]): tables as dataframe
        """
        try:
            riy_table,_ = self._extract_table("riy_perc_gkid")
            costi_ingresso,_ = self._extract_table("costi_ingresso_gkid", black_list_pages=[0])
            costi_gestione,_ = self._extract_table("costi_gestione_gkid")
        
        #@ELIA?
        except Exception as error:
            print("calc table error" + repr(error))
            error_list = [costi_ingresso, costi_gestione, riy_table]
            for i, key in enumerate(error_list):
                if not key:
                    error_list[i] = dict([("ERROR", "ERROR")])

        return dict(
            [
                ("costi_ingresso", costi_ingresso),
                ("costi_gestione", costi_gestione),
                ("riy_table", riy_table),
            ]
        )

    def extract_general_data(self):
        """
        Extract general data from the document. Namely ISIN, RHP and SRI.

        Returns: dict(): data extracted
        """
        try:
            # Clean to eliminate ambuigity @elia?
            for page in self.text:
                setattr(
                    page,
                    "page_content",
                    clean_response_strips("text_gkid", self.language, page.page_content),
                )

            # extract and clean
            extraction = llm_extraction_and_tag(self.text, self.language, "general_info_gkid", self.file_id)
            #extraction = clean_response_regex("general_info_gkid", self.language, extraction)
            extraction = dict(extraction)
            if extraction["periodo_detenzione_raccomandato"] != []:
                extraction["periodo_detenzione_raccomandato"] = str(
                    max(extraction["periodo_detenzione_raccomandato"], key=lambda x: x)
                )
            else:
                # bad but trying to save the other data
                extraction["periodo_detenzione_raccomandato"] = "multipli"

            self.rhp = extraction["periodo_detenzione_raccomandato"]

        except Exception as error:
            print("extract general data error" + repr(error))
            error_list = ["indicatore_sintetico_rischio_max","indicatore_sintetico_rischio_min"]
            extraction = {key: (extraction[key] if extraction.get(key) is not None else "ERROR") for key in error_list}
            self.rhp = extraction["periodo_detenzione_raccomandato"] = "multiple"

        return extraction

    # TO REVIEW @elia
    def extract_riy(self, table):
        """
        Extracts the riy from the given table.

        Parameters:
        - table: The table containing the riy information.

        Returns:
        - extraction_riy: A dictionary containing the extracted riy information.
        """

        try:
            # clean rhp to avoid errors
            clean = clean_response_regex("rhp", self.language, dict([("rhp", self.rhp)]))["rhp"]
            rhp = str(int(clean if clean != "-" else "10"))

            extraction_riy = dict()
            # iterativly extract last column and then remove it, rename results and repeat
            transform = {
                "costi_totali-gkid_min": "incidenza_costo_eur_rhp_min",
                "costi_totali-gkid_max": "incidenza_costo_eur_rhp_max",
                "incidenza-gkid_min": "incidenza_costo_perc_rhp_min",
                "incidenza-gkid_max": "incidenza_costo_perc_rhp_max",
            }
            riy_rhp = self.raccorda(
                    regex_extract(["costi_totali-gkid", "incidenza-gkid"], table, self.language), transform, keep=True
                )

            table = table.iloc[:, :-1]

            # rhp/2 exist only if rhp>=10
            if int(rhp) >= 10:
                transform.update(
                    {
                        "costi_totali-gkid_min": "incidenza_costo_eur_2_min",
                        "costi_totali-gkid_max": "incidenza_costo_eur_2_max",
                        "incidenza-gkid_min": "incidenza_costo_perc_2_min",
                        "incidenza-gkid_max": "incidenza_costo_perc_2_max",
                    }
                )
                riy_2_rhp = self.raccorda(
                        regex_extract(
                            ["costi_totali-gkid", "incidenza-gkid"],
                            table,
                            self.language,
                        ),
                        transform,
                    )
        
                table = table.iloc[:, :-1]
            else:
                riy_2_rhp = {
                        "incidenza_costo_eur_2_min": "-",
                        "incidenza_costo_eur_2_max": "-",
                        "incidenza_costo_perc_2_min": "-",
                        "incidenza_costo_perc_2_max": "-",
                    }
                

            transform.update(
                {
                    "costi_totali-gkid_min": "incidenza_costo_eur_1_min",
                    "costi_totali-gkid_max": "incidenza_costo_eur_1_max",
                    "incidenza-gkid_min": "incidenza_costo_perc_1_min",
                    "incidenza-gkid_max": "incidenza_costo_perc_1_max",
                }
            )
            riy_1 = self.raccorda(
                    regex_extract(["costi_totali-gkid", "incidenza-gkid"], table, self.language),
                    transform)
            
            extraction_riy = {**riy_rhp, **riy_1, **riy_2_rhp}
            # divide ,clean, reunite
            # codice di @elia da rivedere
            eur = {key: value for key, value in extraction_riy.items() if "eur" in key}
            perc = {key: value for key, value in extraction_riy.items() if "perc" in key}
            perc = clean_response_regex("riy%/-gkid", self.language, perc, to_add="")
            eur = clean_response_regex("riy€-gkid", self.language, eur, to_add="")
            extraction_riy = {**perc, **eur}

        except Exception as error:
            print("extract riy error" + repr(error))
            error_list = [
                "incidenza_costo_perc_1_min",
                "incidenza_costo_perc_1_max",
                "incidenza_costo_perc_2_min",
                "incidenza_costo_perc_2_max",
                "incidenza_costo_perc_rhp_min",
                "incidenza_costo_perc_rhp_max",
                "incidenza_costo_eur_1_min",
                "incidenza_costo_eur_1_max",
                "incidenza_costo_eur_2_min",
                "incidenza_costo_eur_2_max",
                "incidenza_costo_eur_rhp_min",
                "incidenza_costo_eur_rhp_max",
            ]
            extraction_riy = {key: (extraction_riy[key] if extraction_riy.get(key) is not None else "ERROR") for key in error_list}

        return extraction_riy

    def extract_cost_commissions(self, table_ingresso, table_gestione):
        """extracts costs and commissions from the document

        Args:
            table_ingresso (pandas.dataframe): table for ingresso and uscita
            table_gestione (pandas.dataframe): table for gestione, transazione and performance

        Returns:
            dict(): data extracted
        """
        try:
            # extract and clean
            costi_ingresso = regex_extract(
                ["costi_ingresso_gkid", "costi_uscita_gkid"],
                table_ingresso,
                self.language,
            )
            costi_gestione = regex_extract(
                [
                    "commissione_gestione_gkid",
                    "commissione_transazione_gkid",
                    "commissione_performance_gkid",
                ],
                table_gestione,
                self.language,
            )
            costi_ingresso = clean_response_regex("costi_ingresso_gkid", self.language, costi_ingresso, to_add="%")
            costi_gestione = clean_response_regex("costi_gestione_gkid", self.language, costi_gestione, to_add="%")

        except Exception as error:
            print("extract cost commissions error" + repr(error))
            if not costi_ingresso or costi_ingresso == {"ERROR": "ERROR"}:
                error_list = [
                    "costi_ingresso_min",
                    "costi_ingresso_max",
                    "costi_uscita_min",
                    "costi_uscita_max",
                ]
                costi_ingresso = {
                    key: (costi_ingresso[key] if costi_ingresso.get(key) is not None else "ERROR") for key in error_list
                }
            if not costi_gestione or costi_gestione == {"ERROR": "ERROR"}:
                error_list = [
                    "commissione_gestione_min",
                    "commissione_gestione_max",
                    "commissione_transazione_min",
                    "commissione_transazione_max",
                    "commissione_performance_min",
                    "commissione_performance_max",
                ]
                costi_gestione = {
                    key: (costi_gestione[key] if costi_gestione.get(key) is not None else "ERROR") for key in error_list
                }

        costi = {**dict(costi_gestione), **dict(costi_ingresso)}

        return costi

    def raccorda(self, dictionary, renaming, keep=False):
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
