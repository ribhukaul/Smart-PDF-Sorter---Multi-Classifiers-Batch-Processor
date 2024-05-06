# regex for cleaning, matches things to keep
REGEX_NUMBERS_COMMA = "[+-]?(\s)?\d+((\s)?[,\.]?(\s)?\d+)*"  #example 1,000.00
REGEX_NUMBER = "[+-]?(\s)?\d+((\s)?\d+)*"  #example 1000
REGEX_DATE = "\d{1,2}\/\d{1,2}\/\d{2,4}|\d+\s[A-Za-z]+\s\d+" #example 01/01/2022
REGEX_ISIN = "[A-Z]{2}[A-Z0-9]{9}[0-9]" #example IT0000000000
CURRENCY = "[A-Z]{3}" #example EUR
ANY = ".+"
ANYTHING_WITH_NUMBERS = ".*\d+.*" #example dsjsd1000dsds



regex_cleaning = {
    "it": {
        "general_info_gkid": {
            "periodo_detenzione_raccomandato": REGEX_NUMBER,
            "indicatore_sintetico_rischio_min": REGEX_NUMBER,
            "indicatore_sintetico_rischio_max": REGEX_NUMBER,
            "date": REGEX_DATE,
        },
        "performance-gkid": {""},
        "riy%/-gkid": {
            "incidenza_costo_perc_1_min": REGEX_NUMBERS_COMMA,
            "incidenza_costo_perc_1_max": REGEX_NUMBERS_COMMA,
            "incidenza_costo_perc_2_min": REGEX_NUMBERS_COMMA,
            "incidenza_costo_perc_2_max": REGEX_NUMBERS_COMMA,
            "incidenza_costo_perc_rhp_min": REGEX_NUMBERS_COMMA,
            "incidenza_costo_perc_rhp_max": REGEX_NUMBERS_COMMA,
        },
        "riy€-gkid": {
            "incidenza_costo_eur_1_min": REGEX_NUMBERS_COMMA,
            "incidenza_costo_eur_1_max": REGEX_NUMBERS_COMMA,
            "incidenza_costo_eur_2_min": REGEX_NUMBERS_COMMA,
            "incidenza_costo_eur_2_max": REGEX_NUMBERS_COMMA,
            "incidenza_costo_eur_rhp_min": REGEX_NUMBERS_COMMA,
            "incidenza_costo_eur_rhp_max": REGEX_NUMBERS_COMMA,
        },
        "costi_ingresso_gkid": {
            "costi_ingresso_min": REGEX_NUMBERS_COMMA,
            "costi_ingresso_max": REGEX_NUMBERS_COMMA,
            "costi_uscita_min": REGEX_NUMBERS_COMMA,
            "costi_uscita_max": REGEX_NUMBERS_COMMA,
        },
        "costi_gestione_gkid": {
            "commissione_gestione_min": REGEX_NUMBERS_COMMA,
            "commissione_gestione_max": REGEX_NUMBERS_COMMA,
            "commissione_transazione_min": REGEX_NUMBERS_COMMA,
            "commissione_transazione_max": REGEX_NUMBERS_COMMA,
            "commissione_performance_min": REGEX_NUMBERS_COMMA,
            "commissione_performance_max": REGEX_NUMBERS_COMMA,
        },
        "rhp": {
            "rhp": "\d+",
        },
        },
    "en": {},
}
regex_search = {
    "it": {
        "costi_ingresso_gkid": ".{0,3}cost.{0,6}ingress.{0,5}",
        "costi_uscita_gkid": ".{0,3}cost.{0,6}uscit.{0,5}",
        "commissione_gestione_gkid": ".{0,3}co.{0,14}gestion.{0,5}",
        "commissione_transazione_gkid": ".{0,3}co.{0,14}transazion.{0,5}",
        "commissione_performance_gkid": ".{0,3}co.{0,14}performance.{0,5}",
        "costi_totali-gkid": ".{0,4}cost.{0,4}total.{0,5}",
        "incidenza-gkid": ".{0,7}ncidenz.{0,30}|.*RIY.*",
    },
    "en": {},
}
strips_cleaning = {
    "it": {
        "general_info_gkid": [],
        "performance-gkid": [],
        "riy-gkid": [],
        "costi_ingresso_gkid": [],
        "costi_gestione_gkid": [],
        "market_gkid": [
            "\\n",
            "Tipo di investitore  al dettaglio",
            "Tipo di investitore al dettaglio",
            "Investitore al dettaglio cui si intende commercializzare il prodotto",
            "Investitore  al dettaglio  a cui è destinata  l'opzione  di investimento:",
            "Investitori al dettaglio a cui si intende commercializzare il prodotto",
            "Investitori al dettaglio cui si intende commercializzare il prodotto",
            "TIPO DI INVESTITORE AL DETTAGLIO",
            "INVESTITORI AL DETTAGLIO A CUI SI INTENDE COMMERCIALIZZARE IL PRODOTTO",
            "INVESTITORE AL DETTAGLIO A CUI SI INTENDE COMMERCIALIZZARE IL PRODOTTO",
        ],
        "text_gkid": ["su 7", "su7", "su  7"],
    },
    "en": {},
}