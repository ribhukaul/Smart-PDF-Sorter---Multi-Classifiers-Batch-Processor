
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


gkid = {
    "fields": {
        # GENERAL INFO
        "date": {
            "field_name": "cod_document_date",
            "renaming": "Data",
            "allow_null": FALSE,
            "type_of": DATE,
            "model_of": NA,
            "decimals_of": None,
            "range_of": DATE_RANGE        
            },
        "is_product_complex": {
            "field_name": "cod_is_complex",
            "renaming": "Prodotto complesso?",
            "allow_null": FALSE,
            "type_of": BOOL,
            "model_of": NA,
            "decimals_of": None,
            "range_of": NO_RANGE
            },
        "periodo_detenzione_raccomandato": {
            "field_name": "cod_rhp",
            "renaming": "RHP (anni)",
            "allow_null": FALSE,
            "type_of": INT,
            "model_of": YEARS,
            "decimals_of": None,
            "range_of": PERCENT_RANGE        
            },
        "indicatore_sintetico_rischio_min": {
            "field_name": "cod_sri_min",
            "renaming": "SRI MIN",
            "allow_null": FALSE,
            "type_of": INT,
            "model_of": YEARS,
            "decimals_of": None,
            "range_of": SRI_RANGE        
            },
        "indicatore_sintetico_rischio_max": {
            "field_name": "cod_sri_max",
            "renaming": "SRI MAX",
            "allow_null": FALSE,
            "type_of": INT,
            "model_of": YEARS,
            "decimals_of": None,
            "range_of": SRI_RANGE        
            },
        # REDUCTION IN YIELD
        "incidenza_costo_eur_1_min": {
            "field_name": "cod_riy_abs_1y_min",
            "renaming": "RIY 1Y EUR MIN",
            "allow_null": TRUE,
            "type_of": FLOAT,
            "model_of": EURO,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "incidenza_costo_eur_1_max": {
            "field_name": "cod_riy_abs_1y_max",
            "renaming": "RIY 1Y EUR MAX",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": EURO,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "incidenza_costo_eur_2_min": {
            "field_name": "cod_riy_abs_rhp2_min",
            "renaming": "RIY RHP/2 EUR MIN",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": EURO,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "incidenza_costo_eur_2_max": {
            "field_name": "cod_riy_abs_rhp2_max",
            "renaming": "RIY RHP/2 EUR MAX",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": EURO,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "incidenza_costo_eur_rhp_min": {
            "field_name": "cod_riy_abs_rhp_min",
            "renaming": "RIY RHP EUR MIN",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": EURO,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "incidenza_costo_eur_rhp_max": {
            "field_name": "cod_riy_abs_rhp_max",
            "renaming": "RIY RHP EUR MAX",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": EURO,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "incidenza_costo_perc_1_min": {
            "field_name": "cod_riy_perc_1y_min",
            "renaming": "RIY 1Y % MIN",
            "allow_null": TRUE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "incidenza_costo_perc_1_max": {
            "field_name": "cod_riy_perc_1y_max",
            "renaming": "RIY 1Y % MAX",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "incidenza_costo_perc_2_min": {
            "field_name": "cod_riy_perc_rhp2_min",
            "renaming": "RIY RHP/2 % MIN",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "incidenza_costo_perc_2_max": {
            "field_name": "cod_rIy_perc_rhp2_max",
            "renaming": "RIY RHP/2 % MAX",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "incidenza_costo_perc_rhp_min": {
            "field_name": "cod_riy_perc_rhp_min",
            "renaming": "RIY RHP % MIN",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "incidenza_costo_perc_rhp_max": {
            "field_name": "cod_riy_perc_rhp_max",
            "renaming": "RIY RHP % MAX",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        # COSTI E COMMISSIONI
        "costi_ingresso_gkid_min": {
            "field_name": "cod_entry_costs_perc_min",
            "renaming": "Costi ingresso MIN",
            "allow_null": TRUE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "costi_ingresso_gkid_max": {
            "field_name": "cod_entry_costs_perc_max",
            "renaming": "Costi ingresso MAX",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "costi_uscita_gkid_min": {
            "field_name": "cod_exit_costs_perc_min",
            "renaming": "Costi uscita MIN",
            "allow_null": TRUE,
            "type_of": FLOAT,
            "model_of": EURO,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "costi_uscita_gkid_max": {
            "field_name": "cod_exit_costs_perc_max",
            "renaming": "Costi uscita MAX",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": EURO,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "commissione_gestione_gkid_min": {
            "field_name": "cod_management_costs_perc_min",
            "renaming": "Commissioni di gestione MIN",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "commissione_gestione_gkid_max": {
            "field_name": "cod_management_costs_perc_max",
            "renaming": "Commissioni di gestione MAX",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "commissione_transazione_gkid_min": {
            "field_name": "cod_transaction_costs_perc_min",
            "renaming": "Costi di transazione MIN",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "commissione_transazione_gkid_max": {
            "field_name": "cod_transaction_costs_perc_max",
            "renaming": "Costi di transazione MAX",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "commissione_performance_gkid_min": {
            "field_name": "cod_performance_costs_perc_min",
            "renaming": "Commissioni di performance MIN",
            "allow_null": TRUE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "commissione_performance_gkid_max": {
            "field_name": "cod_performance_costs_perc_max",
            "renaming": "Commissioni di performance MAX",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        # TARGET MARKET
        "target_market": {
            "field_name": "cod_target_market",
            "renaming": "Target Market",
            "allow_null": FALSE,
            "type_of": STRING,
            "model_of": NA,
            "decimals_of": None,
            "range_of": NO_RANGE        
            },
        "api_costs": {
            "renaming": "Costi API",
            }
        },
    "sections":{
        "section0": {
            "name": "Informazioni di base",
            "list": ["cod_document_date", "is_product_complex", "cod_rhp", "cod_sri_min", "cod_sri_max"]
        },
        "section1": {
            "name": "Reduction In Yield",
            "list": ["cod_riy_abs_1y_min", "cod_riy_abs_1y_max", "cod_riy_abs_rhp2_min", "cod_riy_abs_rhp2_max", 
                     "cod_riy_abs_rhp_min", "cod_riy_abs_rhp_max", "cod_riy_perc_1y_min", "cod_riy_perc_1y_max", 
                     "cod_riy_perc_rhp2_min", "cod_riy_perc_rhp2_max", "cod_riy_perc_rhp_min", "cod_riy_perc_rhp_max"]
        },
        "section2": {
            "name": "Costi e Commissioni",
            "list": ["cod_entry_costs_perc_min", "cod_entry_costs_perc_max", "cod_exit_costs_perc_min", 
                    "cod_exit_costs_perc_max", "cod_management_costs_perc_min", "cod_management_costs_perc_max",
                    "cod_transaction_costs_perc_min", "cod_transaction_costs_perc_max", "cod_performance_costs_perc_min",
                    "cod_performance_costs_perc_max"]
        },
        "section3": {
            "name": "Target Market",
            "list": ["cod_target_market"]
        }
    }
}

