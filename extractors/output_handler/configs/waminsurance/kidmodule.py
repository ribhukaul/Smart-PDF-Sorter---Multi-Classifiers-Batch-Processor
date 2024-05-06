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

kid = {
    "fields": {
        # GENERAL INFO
        "date": {
            "field_name": "cod_document_date",
            "renaming": "Data",
            "allow_null": FALSE,
            "type_of": DATE,
            "model_of": NA,
            "decimals_of": NA,
            "range_of": DATE_RANGE        
            },
        # "isin": {
        #     "field_name": "cod_isin",
        #     "renaming": "ISIN",
        #     "allow_null": FALSE,
        #     "type_of": STRING,
        #     "model_of": CAPS,
        #     "decimals_of": NA,
        #     "range_of": ISIN_RANGE        
        #     },
        # UNDERLYING_TYPE
        # PREMIUM_TYPE
        # UNDERLYING_NAME
        "periodo_detenzione_raccomandato": {
            "field_name": "cod_rhp",
            "renaming": "RHP (anni)",
            "allow_null": FALSE,
            "type_of": INT,
            "model_of": YEARS,
            "decimals_of": NA,
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
        #PERFORMANCE SCENARIO
        "stress_return": {
            "field_name": "cod_stress_scenario_perc_1y",
            "renaming": "Stress scenario 1Y %",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "stress_return_rhp": {
            "field_name": "cod_stress_scenario_perc_rhp",
            "renaming": "Stress scenario RHP %",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "sfavorevole_return": {
            "field_name": "cod_unfavorable_scenario_perc_1y",
            "renaming": "Unfavorable scenario 1Y %",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "sfavorevole_return_rhp": {
            "field_name": "cod_unfavorable_scenario_perc_rhp",
            "renaming": "Unfavorable scenario RHP %",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "moderato_return": {
            "field_name": "cod_mod_scenario_perc_1y",
            "renaming": "Moderate scenario 1Y %",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "moderato_return_rhp": {
            "field_name": "cod_mode_scenario_perc_rhp",
            "renaming": "Moderae scenario RHP %",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },                
        "favorable_return": {
            "field_name": "cod_favorable_scenario_perc_1y",
            "renaming": "Favorable scenario 1Y %",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "favorable_return_rhp": {
            "field_name": "cod_favorable_scenario_perc_rhp",
            "renaming": "Favorable scenario RHP %",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "scenario_morte_1": {
            "field_name": "cod_death_scenario_abs_1y",
            "renaming": "Death scenario 1Y (€)",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": EURO,
            "decimals_of": 2,
            "range_of": NO_RANGE        
            },
        "scenario_morte_rhp": {
            "field_name": "cod_death_scenario_abs_rhp",
            "renaming": "Death scenario RHP (€)",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": EURO,
            "decimals_of": 2,
            "range_of": NO_RANGE        
            },
        # REDUCTION IN YIELD
        "incidenza_costo_perc_1year": {
            "field_name": "cod_riy_perc_1y",
            "renaming": "RIY 1Y %",
            "allow_null": TRUE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "incidenza_costo_perc_rhp": {
            "field_name": "cod_riy_perc_rhp",
            "renaming": "RIY RHP %",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        # COSTS AND COMMISSIONS
        "costi_ingresso": {
            "field_name": "cod_entry_costs_perc",
            "renaming": "Costi ingresso",
            "allow_null": TRUE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "costi_uscita": {
            "field_name": "cod_exit_costs_perc",
            "renaming": "Costi uscita",
            "allow_null": TRUE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "commissione_gestione": {
            "field_name": "cod_management_costs_perc",
            "renaming": "Commissioni di gestione",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "commissione_transazione": {
            "field_name": "cod_transaction_costs_perc",
            "renaming": "Costi di transazione",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "commissione_performance": {
            "field_name": "cod_performance_costs_perc",
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
            "list": ["cod_document_date", "cod_sri", "cod_rhp"]
        },
        "section1": {
            "name": "Performance",
            "list": ["cod_stress_scenario_perc_1y", "cod_stress_scenario_perc_rhp", "cod_unfavorable_scenario_perc_1y", 
                    "cod_unfavorable_scenario_perc_rhp", "cod_moderate_scenario_perc_1y", "cod_moderate_scenario_perc_rhp", 
                    "cod_favorable_scenario_perc_1y", "cod_favorable_scenario_perc_rhp", "cod_death_scenario_abs_1y", 
                    "cod_death_scenario_abs_rhp"]
        },
        "section2": {
            "name": "Reduction In Yield",
            "list": ["cod_riy_perc_1y", "cod_riy_perc_rhp"]
        },
        "section3": {
            "name": "Costi e Commissioni",
            "list": ["cod_entry_costs_perc", "cod_exit_costs_perc", "cod_management_costs_perc", "cod_transaction_costs_perc",
                    "cod_performance_costs_perc"]
                },
        "section4": {
            "name": "Target Market",
            "list": ["cod_target_market"]
        }
    }
}
