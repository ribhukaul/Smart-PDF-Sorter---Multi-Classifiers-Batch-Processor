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
BOOL_RANGE = [TRUE, FALSE]

SRI_RANGE = []
NO_RANGE = []

kid = {
    "fields": {
        #General info
        "date": {
            "field_name": "cod_document_date",
            "renaming": "Data",
            "allow_null": FALSE,
            "type_of": DATE,
            "model_of": NA,
            "decimals_of": NA,
            "range_of": DATE_RANGE        
            },
        "is_product_complex": {
            "field_name": "cod_is_complex",
            "renaming": "Complex product?",
            "allow_null": FALSE,
            "type_of": BOOL,
            "model_of": NA,
            "decimals_of": NA,
            "range_of": DATE_RANGE        
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
        "indicatore_sintetico_rischio": {
            "field_name": "cod_sri",
            "renaming": "SRI",
            "allow_null": FALSE,
            "type_of": INT,
            "model_of": YEARS,
            "decimals_of": NA,
            "range_of": SRI_RANGE        
            },
        # PERFORMANCE SCENARIOS
        "stress_return": {
            "field_name": "cod_stress_scenario_perc_1y",
            "renaming": "Stress Return 1Y %",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "stress_return_rhp": {
            "field_name": "cod_stress_scenario_perc_rhp",
            "renaming": "Stress Return RHP %",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "stress_return_x": {
            "field_name": "cod_stress_scenario_perc_rhp2",
            "renaming": "Stress Return RHP/2 %",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE
            },
        "stress_amount": {
            "field_name": "cod_stress_scenario_abs_1y",
            "renaming": "Stress Amount 1Y €",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": EURO,
            "decimals_of": 2,
            "range_of": NO_RANGE
            },
        "stress_amount_rhp": {
            "field_name": "cod_stress_scenario_abs_rhp",
            "renaming": "Stress Amount RHP €",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": EURO,
            "decimals_of": 2,
            "range_of": NO_RANGE
            },
        "stress_amount_x": {
            "field_name": "cod_stress_scenario_abs_rhp2",
            "renaming": "Stress Amount RHP/2 €",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": EURO,
            "decimals_of": 2,
            "range_of": NO_RANGE
            },
        "sfavorevole_return": {
            "field_name": "cod_unfavorable_scenario_perc_1y",
            "renaming": "Unfavorable Return 1Y %",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "sfavorevole_return_rhp": {
            "field_name": "cod_unfavorable_scenario_perc_rhp",
            "renaming": "Unfavorable Return RHP %",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "sfavorevole_return_x": {
            "field_name": "cod_unfavorable_scenario_perc_rhp2",
            "renaming": "Unfavorable Return RHP/2 %",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE
            },
        "sfavorevole_amount": {
            "field_name": "cod_unfavorable_scenario_abs_1y",
            "renaming": "Unfavorable Amount 1Y €",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": EURO,
            "decimals_of": 2,
            "range_of": NO_RANGE
            },
        "sfavorevole_amount_rhp": {
            "field_name": "cod_unfavorable_scenario_abs_rhp",
            "renaming": "Unfavorable Amount RHP €",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": EURO,
            "decimals_of": 2,
            "range_of": NO_RANGE
            },
        "sfavorevole_amount_x": {
            "field_name": "cod_unfavorable_scenario_abs_rhp2",
            "renaming": "Unfavorable Amount RHP/2 €",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": EURO,
            "decimals_of": 2,
            "range_of": NO_RANGE
            },
        "moderato_return": {
            "field_name": "cod_moderate_scenario_perc_1y",
            "renaming": "Moderate Return 1Y %",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "moderato_return_rhp": {
            "field_name": "cod_moderate_scenario_perc_rhp",
            "renaming": "Moderate Return RHP %",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "moderato_return_x": {
            "field_name": "cod_moderate_scenario_perc_rhp2",
            "renaming": "Moderate Return RHP/2 %",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE
            },
        "moderato_amount": {
            "field_name": "cod_moderate_scenario_abs_1y",
            "renaming": "Moderate Amount 1Y €",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": EURO,
            "decimals_of": 2,
            "range_of": NO_RANGE
            },
        "moderato_amount_rhp": {
            "field_name": "cod_moderate_scenario_abs_rhp",
            "renaming": "Moderate Amount RHP €",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": EURO,
            "decimals_of": 2,
            "range_of": NO_RANGE
            },
        "moderato_amount_x": {
            "field_name": "cod_moderate_scenario_abs_rhp2",
            "renaming": "Moderate Amount RHP/2 €",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": EURO,
            "decimals_of": 2,
            "range_of": NO_RANGE
            },
        "favorable_return": {
            "field_name": "cod_favorable_scenario_perc_1y",
            "renaming": "Favorable Return 1Y %",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "favorable_return_rhp": {
            "field_name": "cod_favorable_scenario_perc_rhp",
            "renaming": "Favorable Return RHP %",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "favorable_return_x": {
            "field_name": "cod_favorable_scenario_perc_rhp2",
            "renaming": "Favorable Return RHP/2 %",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE
            },
        "favorable_amount": {
            "field_name": "cod_favorable_scenario_abs_1y",
            "renaming": "Favorable Amount 1Y €",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": EURO,
            "decimals_of": 2,
            "range_of": NO_RANGE
            },
        "favorable_amount_rhp": {
            "field_name": "cod_favorable_scenario_abs_rhp",
            "renaming": "Favorable Amount RHP €",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": EURO,
            "decimals_of": 2,
            "range_of": NO_RANGE
            },
        "favorable_amount_x": {
            "field_name": "cod_favorable_scenario_abs_rhp2",
            "renaming": "Favorable Amount RHP/2 €",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": EURO,
            "decimals_of": 2,
            "range_of": NO_RANGE
            },
        "scenario_morte_1": {
            "field_name": "cod_death_scenario_abs_1y",
            "renaming": "Death Scenario 1Y €",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": EURO,
            "decimals_of": 2,
            "range_of": NO_RANGE        
            },
        "scenario_morte_rhp": {
            "field_name": "cod_death_scenario_abs_rhp",
            "renaming": "Death Scenario RHP €",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": EURO,
            "decimals_of": 2,
            "range_of": NO_RANGE        
            },
        "scenario_morte_x": {
            "field_name": "cod_death_scenario_abs_rhp2",
            "renaming": "Death Scenario RHP/2 €",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": EURO,
            "decimals_of": 2,
            "range_of": NO_RANGE        
            },
        # RIY
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
        "incidenza_costo_perc_xyear": {
            "field_name": "cod_riy_perc_rhp2",
            "renaming": "RIY RHP/2 %",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "costi_totali_eur_1year": {
            "field_name": "cod_riy_abs_1y",
            "renaming": "Total costs 1Y €",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": EURO,
            "decimals_of": 2,
            "range_of": NO_RANGE        
            },
        "costi_totali_eur_rhp": {
            "field_name": "cod_riy_abs_rhp",
            "renaming": "Total costs RHP €",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": EURO,
            "decimals_of": 2,
            "range_of": NO_RANGE        
            },
        "costi_totali_eur_xyear": {
            "field_name": "cod_riy_abs_rhp2",
            "renaming": "Total costs RHP/2 €",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": EURO,
            "decimals_of": 2,
            "range_of": NO_RANGE        
            },
        # COSTS
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
        # TARGET MARKET
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
            "list": ["cod_document_date", "cod_is_complex", "cod_rhp", "cod_sri"]
        },
        "section1": {
            "name": "Performance",
            "list": ["cod_stress_scenario_perc_1y", "cod_stress_scenario_perc_rhp", "cod_stress_scenario_perc_rhp2", "cod_stress_scenario_abs_1y", 
                     "cod_stress_scenario_abs_rhp", "cod_stress_scenario_abs_rhp2", "cod_unfavorable_scenario_perc_1y", "cod_unfavorable_scenario_perc_rhp", 
                     "cod_unfavorable_scenario_perc_rhp2", "cod_unfavorable_scenario_abs_1y", "cod_unfavorable_scenario_abs_rhp", 
                     "cod_unfavorable_scenario_abs_rhp2", "cod_moderate_scenario_perc_1y", "cod_moderate_scenario_perc_rhp", 
                     "cod_moderate_scenario_perc_rhp2", "cod_moderate_scenario_abs_1y", "cod_moderate_scenario_abs_rhp", "cod_moderate_scenario_abs_rhp2", 
                     "cod_favorable_scenario_perc_1y", "cod_favorable_scenario_perc_rhp", "cod_favorable_scenario_perc_rhp2", "cod_favorable_scenario_abs_1y", 
                     "cod_favorable_scenario_abs_rhp", "cod_favorable_scenario_abs_rhp2", "cod_death_scenario_abs_1y", "cod_death_scenario_abs_rhp", 
                     "cod_death_scenario_abs_rhp2"]
        },
        "section2": {
            "name": "Reduction In Yield",
            "list": ["cod_riy_perc_1y", "cod_riy_perc_rhp", "cod_riy_perc_rhp2", "cod_riy_abs_1y", "cod_riy_abs_rhp", "cod_riy_abs_rhp2"]
        },
        "section3": {
            "name": "Costi e Commissioni",
            "list": ["cod_entry_costs_perc", "cod_exit_costs_perc", "cod_management_costs_perc", "cod_transaction_costs_perc", "cod_performance_costs_perc"]
        },
        "section4": {
            "name": "Target Market",
            "list": ["cod_target_market"]
        }
    }
}
