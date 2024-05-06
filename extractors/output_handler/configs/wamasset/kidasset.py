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

kidasset = {
    "fields": {
        "date": {
            "field_name": "cod_date",
            "renaming": "Data",
            "allow_null": FALSE,
            "type_of": DATE,
            "model_of": NA,
            "decimals_of": NA,
            "range_of": DATE_RANGE        
            },
        "isin": {
            "field_name": "cod_isin",
            "renaming": "ISIN",
            "allow_null": FALSE,
            "type_of": STRING,
            "model_of": CAPS,
            "decimals_of": NA,
            "range_of": ISIN_RANGE        
            },
        "periodo_detenzione_raccomandato": {
            "field_name": "cod_rhp",
            "renaming": "RHP (anni)",
            "allow_null": FALSE,
            "type_of": INT,
            "model_of": YEARS,
            "decimals_of": NA,
            "range_of": PERCENT_RANGE        
            },
        "favorable_return": {
            "field_name": "cod_rsfav_1y",
            "renaming": "RSFAV 1Y %",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "favorable_return_rhp": {
            "field_name": "cod_rsfav_rhp",
            "renaming": "RSFAV RHP %",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "indicatore_sintetico_rischio": {
            "field_name": "cod_sri",
            "renaming": "SRI",
            "allow_null": FALSE,
            "type_of": INT,
            "model_of": YEARS,
            "decimals_of": NA,
            "range_of": SRI_RANGE        
            },
        "moderato_return": {
            "field_name": "cod_rsmod_1y",
            "renaming": "RSMOD 1Y %",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "moderato_return_rhp": {
            "field_name": "cod_rsmod_rhp",
            "renaming": "RSMOD RHP %",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "scenario_morte_1": {
            "field_name": "cod_smor_1y",
            "renaming": "SMOR 1Y (€)",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": EURO,
            "decimals_of": 2,
            "range_of": NO_RANGE        
            },
        "scenario_morte_rhp": {
            "field_name": "cod_smor_rhp",
            "renaming": "SMOR RHP (€)",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": EURO,
            "decimals_of": 2,
            "range_of": NO_RANGE        
            },
        "sfavorevole_return": {
            "field_name": "cod_rssfav_1y",
            "renaming": "RSSFAV 1Y %",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "sfavorevole_return_rhp": {
            "field_name": "cod_rssfav_rhp",
            "renaming": "RSSFAV RHP %",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "stress_return": {
            "field_name": "cod_rsstr_1y",
            "renaming": "RSSTR 1Y %",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "stress_return_rhp": {
            "field_name": "cod_rsstr_rhp",
            "renaming": "RSSTR RHP %",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "incidenza_costo_1": {
            "field_name": "cod_riy_1y",
            "renaming": "RIY 1Y %",
            "allow_null": TRUE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "incidenza_costo_rhp": {
            "field_name": "cod_riy_rhp",
            "renaming": "RIY RHP %",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "costi_ingresso": {
            "field_name": "cod_costi_ingresso",
            "renaming": "Costi ingresso",
            "allow_null": TRUE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "costi_uscita": {
            "field_name": "cod_costi_uscita",
            "renaming": "Costi uscita",
            "allow_null": TRUE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "commissione_gestione": {
            "field_name": "cod_commissioni_di_gestione",
            "renaming": "Commissioni di gestione",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "commissione_transazione": {
            "field_name": "cod_costi_di_transazione",
            "renaming": "Costi di transazione",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "commissione_performance": {
            "field_name": "cod_commissioni_di_performance",
            "renaming": "Commissioni di performance",
            "allow_null": TRUE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "target_market": {
            "field_name": "cod_target_market",
            "renaming": "Target Market",
            "allow_null": FALSE,
            "type_of": STRING,
            "model_of": NA,
            "decimals_of": NA,
            "range_of": NO_RANGE        
            }
    },
    "sections": {
        "section0": {
            "name": "Informazioni di base",
            "list": ["cod_date", "cod_isin", "cod_sri", "cod_rhp"]
        },
        "section1": {
            "name": "Performance",
            "list": ["cod_rsfav_1y", "cod_rsfav_rhp", "cod_rsmod_1y", "cod_rsmod_rhp", "cod_smor_1y", "cod_smor_rhp", "cod_rssfav_1y", "cod_rssfav_rhp", "cod_rsstr_1y", "cod_rsstr_rhp"]
        },
        "section2": {
            "name": "Reduction In Yield",
            "list": ["cod_riy_1y", "cod_riy_rhp"]
        },
        "section3": {
            "name": "Costi e Commissioni",
            "list": ["cod_costi_ingresso", "cod_costi_uscita", "cod_commissioni_di_gestione", "cod_costi_di_transazione", "cod_commissioni_di_performance"]
        },
        "section4": {
            "name": "Target Market",
            "list": ["cod_target_market"]
        }
    }
}
