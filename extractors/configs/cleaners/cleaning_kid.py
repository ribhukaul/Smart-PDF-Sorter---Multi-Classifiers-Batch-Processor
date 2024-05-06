

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
        "general_info": {
            "isin": "[A-Z0-9]{12}",
            "periodo_detenzione_raccomandato": ANY,
            "indicatore_sintetico_rischio": REGEX_NUMBER,
            "date": REGEX_DATE,
        },
        "performance": {
            "favorable_return": REGEX_NUMBERS_COMMA,
            "favorable_return_rhp": REGEX_NUMBERS_COMMA,
            "moderato_return": REGEX_NUMBERS_COMMA,
            "moderato_return_rhp": REGEX_NUMBERS_COMMA,
            "sfavorevole_return": REGEX_NUMBERS_COMMA,
            "sfavorevole_return_rhp": REGEX_NUMBERS_COMMA,
            "stress_return": REGEX_NUMBERS_COMMA,
            "stress_return_rhp": REGEX_NUMBERS_COMMA,
            "scenario_morte_1": "",
            "scenario_morte_rhp": "",
        },
        "performance_morte": {
            "scenario_morte_1": REGEX_NUMBERS_COMMA,
            "scenario_morte_rhp": REGEX_NUMBERS_COMMA,
            "periodo_detenzione_raccomandato": REGEX_NUMBER,
            "indicatore_sintetico_rischio": REGEX_NUMBER,
            "indicatore_sintetico_rischio_max": REGEX_NUMBER,
            "date": REGEX_DATE,
        },
        "riy": {
            "incidenza_costo_1": REGEX_NUMBERS_COMMA,
            "incidenza_costo_rhp": REGEX_NUMBERS_COMMA,
        },
        "costi_ingresso": {
            "costi_ingresso": REGEX_NUMBERS_COMMA,
            "costi_uscita": REGEX_NUMBERS_COMMA,
        },
        "costi_gestione": {
            "commissione_gestione": REGEX_NUMBERS_COMMA,
            "commissione_transazione": REGEX_NUMBERS_COMMA,
            "commissione_performance": REGEX_NUMBERS_COMMA,
        },
        "rhp": {
            "rhp": "\d+",
        },
    },
    "en": {
    },
}
regex_search = {
    "it": {
        "costi_ingresso": ".{0,3}cost.{0,6}ingress.{0,5}",
        "costi_uscita": ".{0,3}cost.{0,6}uscit.{0,5}",
        "commissione_gestione": ".{0,3}co.{0,14}gestion.{0,5}",
        "commissione_transazione": ".{0,3}co.{0,14}transazion.{0,5}",
        "commissione_performance": ".{0,3}co.{0,14}performance.{0,5}",
        "costi_totali": ".{0,4}cost.{0,4}total.{0,5}",
        "incidenza": ".{0,7}ncidenz.{0,30}|.*RIY.*",
    },
    "en": {
    },
}
strips_cleaning = {
    "it": {
        "general_info": [],
        "performance": [],
        "riy": [],
        "costi_ingresso": [],
        "costi_gestione": [],
        "market": [
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
        "text": ["su 7", "su7", "su  7"],
    },
    "en": {
        "performance": [],
        "riy": [],
    },
}