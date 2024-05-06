
# typeof
INT = "Integer"
FLOAT = "Float"
STRING = "String"
DATE= "Date"
BOOL = "Boolean"
#model of
PERCENT = "%"
EURO = "€"
YEARS = "anni"
CAPS = "CAPS"

TRUE = "true"
FALSE = "false"
NA = "N/A"

PERCENT_RANGE = []
ISIN_RANGE = []
DATE_RANGE = []

SRI_RANGE = []
NO_RANGE = []
bnp = {
    "fields": {
        "isin": {
            "field_name": "cod_isin",
            "renaming": "Codice Isin",
            "allow_null": FALSE,
            "type_of": STRING,
            "model_of": CAPS,
            "decimals_of": None,
            "range_of": ISIN_RANGE
        },
        "description": {
            "field_name": "cod_descrizione",
            "renaming": "Descrizione",
            "allow_null": FALSE,
            "type_of": STRING,
            "model_of": NA,
            "decimals_of": None,
            "range_of": NO_RANGE
        },
        "currency": {
            "field_name": "cod_valuta",
            "renaming": "Valuta del prodotto",
            "allow_null": FALSE,
            "type_of": STRING,
            "model_of": EURO,
            "decimals_of": None,
            "range_of": NO_RANGE
        },
        "issuer_desc": {
            "field_name": "cod_emittente",
            "renaming": "Emittente",
            "allow_null": FALSE,
            "type_of": STRING,
            "model_of": NA,
            "decimals_of": None,
            "range_of": NO_RANGE
        },
        "strike_date": {
            "field_name": "cod_data_strike",
            "renaming": "Data di Strike",
            "allow_null": FALSE,
            "type_of": DATE,
            "model_of": NA,
            "decimals_of": None,
            "range_of": DATE_RANGE
        },
        "issue_date": {
            "field_name": "cod_data_emissione",
            "renaming": "Data di Emissione",
            "allow_null": FALSE,
            "type_of": DATE,
            "model_of": NA,
            "decimals_of": None,
            "range_of": DATE_RANGE
        },
        "expiry_date": {
            "field_name": "cod_data_liquidazione",
            "renaming": "Data di Liquidazione",
            "allow_null": FALSE,
            "type_of": DATE,
            "model_of": NA,
            "decimals_of": None,
            "range_of": DATE_RANGE
        },
        "final_valuation_date": {
            "field_name": "cod_data_valutazione_finale",
            "renaming": "Data di Valutazione dell'Importo di Liquidazione",
            "allow_null": FALSE,
            "type_of": DATE,
            "model_of": NA,
            "decimals_of": None,
            "range_of": DATE_RANGE
        },
        "leva_cedolare": {
            "field_name": "cod_leva_cedolare",
            "renaming": "Leva Cedolare",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE
        },
        "nominal": {
            "field_name": "cod_importo_nozionale",
            "renaming": "Importo Nozionale",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": EURO,
            "decimals_of": 2,
            "range_of": NO_RANGE
        },
        "market": {
            "field_name": "cod_quotazione",
            "renaming": "quotazione",
            "allow_null": FALSE,
            "type_of": STRING,
            "model_of": NA,
            "decimals_of": None,
            "range_of": NO_RANGE
        },
        "unconditional_protection": {
            "field_name": "cod_protezione_incondizionata",
            "renaming": "Protezione",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE
        },
        "protection": {
            "field_name": "cod_protezione_inferiore_100",
            "renaming": "Protezione < 100%",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE
        },
        "barrier": {
            "field_name": "cod_barriera",
            "renaming": "Barriera",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE
        },
        "barrier_type": {
            "field_name": "cod_tipo_barriera",
            "renaming": "Tipo Barriera",
            "allow_null": FALSE,
            "type_of": STRING,
            "model_of": NA,
            "decimals_of": None,
            "range_of": NO_RANGE
        },
        "callable": {
            "field_name": "cod_liquidazione_anticipata",
            "renaming": "Liquidazione Anticipata Facoltativa",
            "allow_null": FALSE,
            "type_of": STRING,
            "model_of": NA,
            "decimals_of": None,
            "range_of": NO_RANGE
        },
        "autocallable": {
            "field_name": "cod_autocallability",
            "renaming": "Autocallability",
            "allow_null": FALSE,
            "type_of": STRING,
            "model_of": NA,
            "decimals_of": None,
            "range_of": NO_RANGE
        },
        "unconditional_coupon_min": {
            "field_name": "cod_premio_incondizionato_min",
            "renaming": "Premio/i",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE
        },
        "conditional_coupon_min": {
            "field_name": "cod_premio_condizionato_min",
            "renaming": "Premio/i Condizionato/i",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE
        },
        "memory": {
            "field_name": "cod_effetto_memoria",
            "renaming": "Effetto memoria",
            "allow_null": FALSE,
            "type_of": STRING,
            "model_of": NA,
            "decimals_of": None,
            "range_of": NO_RANGE
        },
        "autocall": {
            "field_name": "cod_scadenza_anticipata",
            "renaming": "Scadenza Anticipata Automatica",
            "allow_null": FALSE,
            "type_of": STRING,
            "model_of": NA,
            "decimals_of": None,
            "range_of": NO_RANGE
        },
        "autocall_barrier": {
            "field_name": "cod_barriera_scadenza_anticipata",
            "renaming": "Barriera per la scadenza anticipata",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE
        },
        "conditional_coupon_barrier": {
            "field_name": "cod_barriera_premio_condizionato",
            "renaming": "Barriera/e per il Versamento del Premio/i Condizionato/i",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE
        },
        "cap": {
            "field_name": "cod_livello_cap",
            "renaming": "Livello Cap",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE
        },
        "airbag": {
            "field_name": "cod_airbag",
            "renaming": "airbag",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE
        },
        "issue_price_perc": {
            "field_name": "cod_prezzo_emissione",
            "renaming": "Prezzo di Emissione",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE
        },
        "instrument_bloombergcode": {
            "field_name": "cod_codice_bloomberg",
            "renaming": "Codice Bloomberg",
            "allow_null": FALSE,
            "type_of": STRING,
            "model_of": NA,
            "decimals_of": None,
            "range_of": NO_RANGE
        },
        "instrument_description": {
            "field_name": "cod_descrizione_strumento",
            "renaming": "Sottostante",
            "allow_null": FALSE,
            "type_of": STRING,
            "model_of": NA,
            "decimals_of": None,
            "range_of": NO_RANGE
        },
        "observation_coupon_date": {
            "field_name": "cod_data_osservazione_premio",
            "renaming": "Data/e di Valutazione del/i Premio/i Condizionato/i",
            "allow_null": FALSE,
            "type_of": DATE,
            "model_of": NA,
            "decimals_of": None,
            "range_of": DATE_RANGE
        },
        "payment_coupon_date": {
            "field_name": "cod_data_pagamento_premio",
            "renaming": "Data/e di Pagamento del/i Premio/i",
            "allow_null": FALSE,
            "type_of": DATE,
            "model_of": NA,
            "decimals_of": None,
            "range_of": DATE_RANGE
        },
        "barrier_coupon": {
            "field_name": "cod_barriera_premio",
            "renaming": "Barriera/e per il Versamento del Premio/i Condizionato/i",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE
        },
        "unconditional_coupon": {
            "field_name": "cod_premio_incondizionato",
            "renaming": "Premio/i",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE
        },
        "conditional_coupon": {
            "field_name": "cod_premio_condizionato",
            "renaming": "Premio/i Condizionato/i",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE
        },
        "payment_callable_date": {
            "field_name": "cod_data_pagamento_anticipato",
            "renaming": "Data di Liquidazione Anticipata Facoltativa",
            "allow_null": FALSE,
            "type_of": DATE,
            "model_of": NA,
            "decimals_of": None,
            "range_of": DATE_RANGE
        },
        "observation_autocall_date": {
            "field_name": "cod_data_osservazione_autocall",
            "renaming": "Data/e di Valutazione dell'Importo di Liquidazione (rimborso) Anticipato",
            "allow_null": FALSE,
            "type_of": DATE,
            "model_of": NA,
            "decimals_of": None,
            "range_of": DATE_RANGE
        },
        "barrier_autocall": {
            "field_name": "cod_barriera_autocall",
            "renaming": "Barriera/e per la Scadenza Anticipata",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE
        },
        "payment_autocall_date": {
            "field_name": "cod_data_pagamento_autocall",
            "renaming": "Data di Scadenza Anticipata",
            "allow_null": FALSE,
            "type_of": DATE,
            "model_of": NA,
            "decimals_of": None,
            "range_of": DATE_RANGE
        },
        "value_autocall": {
            "field_name": "cod_valore_autocall",
            "renaming": "Premio/I di Uscita",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE
        },
        "periodo_detenzione_raccomandato": {
            "field_name": "cod_periodo_detenzione",
            "renaming": "Periodo di detenzione raccomandato",
            "allow_null": FALSE,
            "type_of": INT,
            "model_of": NA,
            "decimals_of": None,
            "range_of": NO_RANGE
        },
        "indicatore_sintetico_rischio": {
            "field_name": "cod_indicatore_rischio",
            "renaming": "Indicatore sintetico di rischio",
            "allow_null": FALSE,
            "type_of": INT,
            "model_of": NA,
            "decimals_of": None,
            "range_of": NO_RANGE
        },
        "importo_minimo": {
            "field_name": "cod_importo_minimo",
            "renaming": "Importo Minimo",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": EURO,
            "decimals_of": 2,
            "range_of": NO_RANGE
        },
        "leva_airbag": {
            "field_name": "cod_leva_airbag",
            "renaming": "Leva Airbag",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE
        }
    },
    "sections": {
    
        "section0": {
        "name": "Informazioni di base",
        "list": [
            "periodo_detenzione_raccomandato",
            "indicatore_sintetico_rischio"
        ]
        },
        "section1": {
        "name": "Informazioni Principali",
        "list": [
            "isin",
            "issuer_desc",
            "currency",
            "strike_date",
            "issue_date",
            "expiry_date",
            "final_valuation_date",
            "nominal",
            "market",
            "barrier",
            "issue_price_perc"
        ]
        },
        "section2": {
        "name": "Dettagli Sottostante",
        "list": [
            "instrument_description",
            "instrument_bloombergcode",
            "instrument_isin"
        ]
        },
        "section3": {
        "name": "Informazioni sui Premi",
        "list": [
            "observation_coupon_date",
            "payment_coupon_date",
            "conditional_coupon_barrier",
            "unconditional_coupon",
            "conditional_coupon"
        ]
        },
        "section4": {
        "name": "Informazioni sulla Scadenza",
        "list": [
            "payment_callable_date",
            "observation_autocall_date",
            "barrier_autocall",
            "payment_autocall_date",
            "value_autocall"
        ]
    }
    }
}
