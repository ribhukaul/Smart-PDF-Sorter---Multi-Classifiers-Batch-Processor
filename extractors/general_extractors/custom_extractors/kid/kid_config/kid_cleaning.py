# strips to cut from the text
exc_multiple_lines = (["commissione_gestione", "costi_totali", "incidenza"],)


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
    "en": {
        "performance": [],
        "riy": [],
    },
}
# regex for cleaning, matches things to keep
REGEX_NUMBERS_COMMA = "[+-]?(\s)?\d+((\s)?[,\.]?(\s)?\d+)*"
REGEX_NUMBER = "[+-]?(\s)?\d+((\s)?\d+)*"
REGEX_DATE = "\d{1,2}\/\d{1,2}\/\d{2,4}|\d+\s[A-Za-z]+\s\d+"
REGEX_ISIN = "[A-Z]{2}[A-Z0-9]{9}[0-9]"
CURRENCY="[A-Z]{3}"
ANY = ".+"
ANYTHING_WITH_NUMBERS = ".*\d+.*"
regex_cleaning = {
    "it": {
        "general_info": {
            "isin": "[A-Z0-9]{12}",
            "periodo_detenzione_raccomandato": ANY,
            "indicatore_sintetico_rischio": REGEX_NUMBER,
            "date": REGEX_DATE,
        },
        "general_info_kid_governance": {
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
        "performance_abs": {
            'stress_amount':REGEX_NUMBERS_COMMA,
            'sfavorevole_amount':REGEX_NUMBERS_COMMA,
            'moderato_amount':REGEX_NUMBERS_COMMA,
            'favorable_amount':REGEX_NUMBERS_COMMA,
            'stress_amount_rhp':REGEX_NUMBERS_COMMA,
            'sfavorevole_amount_rhp':REGEX_NUMBERS_COMMA,
            'moderato_amount_rhp':REGEX_NUMBERS_COMMA,
            'favorable_amount_rhp':REGEX_NUMBERS_COMMA,
        },
        "performance_rhp_2": {
            'stress_amount_x':REGEX_NUMBERS_COMMA,
            'sfavorevole_amount_x':REGEX_NUMBERS_COMMA,
            'moderato_amount_x':REGEX_NUMBERS_COMMA,
            'favorable_amount_x':REGEX_NUMBERS_COMMA,
            'stress_return_x':REGEX_NUMBERS_COMMA,
            'sfavorevole_return_x':REGEX_NUMBERS_COMMA,
            'moderato_return_x':REGEX_NUMBERS_COMMA,
            'favorable_return_x':REGEX_NUMBERS_COMMA,
            'scenario_morte_x':REGEX_NUMBERS_COMMA,
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
            "incidenza_costo_perc_1year": REGEX_NUMBERS_COMMA,
            "incidenza_costo_perc_rhp": REGEX_NUMBERS_COMMA,
            "incidenza_costo_perc_xyear": REGEX_NUMBERS_COMMA,
            "costi_totali_eur_xyear": REGEX_NUMBERS_COMMA,
            "costi_totali_eur_rhp": REGEX_NUMBERS_COMMA,
            "costi_totali_eur_1year": REGEX_NUMBERS_COMMA,
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
        "general_info_certificati": {
            "isin": REGEX_ISIN,
            "descrizione": ANY,
            "emittente": ANY,
        },
        "bnp_main": {
            "currency": CURRENCY,
            "strike_date": ANYTHING_WITH_NUMBERS,
            "issue_date": ANYTHING_WITH_NUMBERS,
            "expiry_date": ANYTHING_WITH_NUMBERS,
            "final_valuation_date": ANYTHING_WITH_NUMBERS,
            "nominal": ANYTHING_WITH_NUMBERS,
            "market": ANYTHING_WITH_NUMBERS,
            "barrier": ANYTHING_WITH_NUMBERS,
            "conditional_coupon_barrier": ANYTHING_WITH_NUMBERS,
            "issue_price_perc": ANYTHING_WITH_NUMBERS,
            "observation_coupon_date": ANYTHING_WITH_NUMBERS,
            "payment_coupon_date": ANYTHING_WITH_NUMBERS,
            "unconditional_coupon": ANYTHING_WITH_NUMBERS,
            "conditional_coupon": ANYTHING_WITH_NUMBERS,
            "payment_callable_date": ANYTHING_WITH_NUMBERS,
            "observation_autocall_date": ANYTHING_WITH_NUMBERS,
            "barrier_autocall": ANYTHING_WITH_NUMBERS,
            "payment_autocall_date": ANYTHING_WITH_NUMBERS,
            "value_autocall": ANYTHING_WITH_NUMBERS,
        },
    },
    "en": {
        "performance": [],
        "riy": [],
    },
}
# regex to search in table
regex_search = {
    "it": {
        "costi_ingresso": ".{0,3}cost.{0,6}ingress.{0,5}",
        "costi_uscita": ".{0,3}cost.{0,6}uscit.{0,5}",
        "commissione_gestione": ".{0,3}co.{0,14}gestion.{0,5}",
        "commissione_transazione": ".{0,3}co.{0,14}transazion.{0,5}",
        "commissione_performance": ".{0,3}co.{0,14}performance.{0,5}",
        "costi_totali": ".{0,4}cost.{0,4}total.{0,5}",
        "incidenza": ".{0,7}ncidenz.{0,30}|.*RIY.*",
        "costi_ingresso_gkid": ".{0,3}cost.{0,6}ingress.{0,5}",
        "costi_uscita_gkid": ".{0,3}cost.{0,6}uscit.{0,5}",
        "commissione_gestione_gkid": ".{0,3}co.{0,14}gestion.{0,5}",
        "commissione_transazione_gkid": ".{0,3}co.{0,14}transazion.{0,5}",
        "commissione_performance_gkid": ".{0,3}co.{0,14}performance.{0,5}",
        "costi_totali-gkid": ".{0,4}cost.{0,4}total.{0,5}",
        "incidenza-gkid": ".{0,7}ncidenz.{0,30}|.*RIY.*",
    },
    "en": {
        "performance": [],
        "riy": [],
    },
}
