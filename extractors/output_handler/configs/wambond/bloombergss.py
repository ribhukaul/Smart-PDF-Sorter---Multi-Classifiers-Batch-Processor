
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


bloombergss = {
    "fields": {
        "isin": {
            "field_name": "cod_isin",
            "renaming": "ISIN",
            "allow_null": FALSE,
            "type_of": STRING,
            "model_of": CAPS,
            "decimals_of": NA,
            "range_of": ISIN_RANGE        
            },
        "name": {
            "field_name": "cod_name",
            "renaming": "Name",
            "allow_null": FALSE,
            "type_of": STRING,
            "model_of": NA,
            "decimals_of": NA,
            "range_of": NO_RANGE        
            },
        "currency": {
            "field_name": "cod_currency",
            "renaming": "Currency",
            "allow_null": FALSE,
            "type_of": STRING,
            "model_of": NA,
            "decimals_of": NA,
            "range_of": NO_RANGE        
            }, 
        "rank": {
            "field_name": "cod_rank",
            "renaming": "Rank",
            "allow_null": FALSE,
            "type_of": STRING,
            "model_of": NA,
            "decimals_of": NA,
            "range_of": NO_RANGE        
            },
        "coupon": {
            "field_name": "cod_coupon",
            "renaming": "Coupon",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": PERCENT_RANGE        
            },
        "type": {
            "field_name": "cod_type",
            "renaming": "Type",
            "allow_null": FALSE,
            "type_of": STRING,
            "model_of": NA,
            "decimals_of": NA,
            "range_of": NO_RANGE        
            },
        "day_cnt": {
            "field_name": "cod_daycnt",
            "renaming": "DayCnt",
            "allow_null": FALSE,
            "type_of": STRING,
            "model_of": NA,
            "decimals_of": NA,
            "range_of": NO_RANGE        
            },
        "maturity": {
            "field_name": "cod_maturity",
            "renaming": "Maturity",
            "allow_null": FALSE,
            "type_of": DATE,
            "model_of": NA,
            "decimals_of": NA,
            "range_of": DATE_RANGE        
            },
        "pricing_date": {
            "field_name": "cod_pricing_date",
            "renaming": "PricingDate",
            "allow_null": FALSE,
            "type_of": DATE,
            "model_of": NA,
            "decimals_of": NA,
            "range_of": DATE_RANGE        
            },
        "interest_accrual_date": {
            "field_name": "cod_interest_accrual_date",
            "renaming": "InterestAccrualDate",
            "allow_null": FALSE,
            "type_of": DATE,
            "model_of": NA,
            "decimals_of": NA,
            "range_of": DATE_RANGE        
            },
        "first_settle_date": {
            "field_name": "cod_first_settle_date",
            "renaming": "FirstSettleDate",
            "allow_null": FALSE,
            "type_of": DATE,
            "model_of": NA,
            "decimals_of": NA,
            "range_of": DATE_RANGE        
            },
        "first_coupon_date": {
            "field_name": "cod_first_coupon_date",
            "renaming": "FirstCouponDate",
            "allow_null": FALSE,
            "type_of": DATE,
            "model_of": NA,
            "decimals_of": NA,
            "range_of": DATE_RANGE        
            },
        "amount_issued": {
            "field_name": "cod_amt_issued",
            "renaming": "AmtIssued",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": EURO,
            "decimals_of": 2,
            "range_of": NO_RANGE        
            },
        "amount_outstanding": {
            "field_name": "cod_amt_outstanding",
            "renaming": "AmtOutstanding",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": EURO,
            "decimals_of": 2,
            "range_of": NO_RANGE        
            },
        "min_piece": {
            "field_name": "cod_min_piece",
            "renaming": "MinPiece",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": EURO,
            "decimals_of": 2,
            "range_of": NO_RANGE        
            },
        "par_amount": {
            "field_name": "cod_par_amount",
            "renaming": "ParAmount",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": EURO,
            "decimals_of": 2,
            "range_of": NO_RANGE        
            },
        "exchange": {
            "field_name": "cod_exchange",
            "renaming": "Exchange",
            "allow_null": FALSE,
            "type_of": STRING,
            "model_of": NA,
            "decimals_of": NA,
            "range_of": NO_RANGE        
            },
        "formula_des": {
            "field_name": "cod_formula_des",
            "renaming": "Formula",
            "allow_null": FALSE,
            "type_of": STRING,
            "model_of": NA,
            "decimals_of": NA,
            "range_of": NO_RANGE        
            },
        "esg_type": {
            "field_name": "cod_esg_type",
            "renaming": "ESG_bond",
            "allow_null": FALSE,
            "type_of": STRING,
            "model_of": NA,
            "decimals_of": NA,
            "range_of": NO_RANGE        
            },
        "sinkability": {
            "field_name": "cod_sinkable",
            "renaming": "Sinkable",
            "allow_null": FALSE,
            "type_of": BOOL,
            "model_of": NA,
            "decimals_of": NA,
            "range_of": NO_RANGE        
            },
        "callability": {
            "field_name": "cod_callable",
            "renaming": "Callable",
            "allow_null": FALSE,
            "type_of": BOOL,
            "model_of": NA,
            "decimals_of": NA,
            "range_of": NO_RANGE        
            },
        "make_whole": {
            "field_name": "cod_make_whole",
            "renaming": "MakeWhole",
            "allow_null": FALSE,
            "type_of": BOOL,
            "model_of": NA,
            "decimals_of": NA,
            "range_of": NO_RANGE        
            },
        "perpetual": {
            "field_name": "cod_perpetual",
            "renaming": "Perpetual",
            "allow_null": FALSE,
            "type_of": BOOL,
            "model_of": NA,
            "decimals_of": NA,
            "range_of": NO_RANGE        
            },
        "status": {
            "field_name": "cod_status",
            "renaming": "Status",
            "allow_null": FALSE,
            "type_of": STRING,
            "model_of": NA,
            "decimals_of": NA,
            "range_of": NO_RANGE        
            },
        "cpn_freq": {
            "field_name": "cod_cpn_freq",
            "renaming": "CpnFreq",
            "allow_null": FALSE,
            "type_of": STRING,
            "model_of": NA,
            "decimals_of": NA,
            "range_of": NO_RANGE        
            },
        "note_des": {
            "field_name": "cod_note_des",
            "renaming": "noteDES",
            "allow_null": FALSE,
            "type_of": STRING,
            "model_of": NA,
            "decimals_of": NA,
            "range_of": NO_RANGE        
            },
        "bond_type": {
            "field_name": "cod_bond_type",
            "renaming": "BondType",
            "allow_null": FALSE,
            "type_of": STRING,
            "model_of": NA,
            "decimals_of": NA,
            "range_of": NO_RANGE        
            },
        "description": {
            "field_name": "cod_description",
            "renaming": "Description",
            "allow_null": FALSE,
            "type_of": STRING,
            "model_of": NA,
            "decimals_of": NA,
            "range_of": NO_RANGE        
            },
        "index 1": {
            "field_name": "cod_index_1",
            "renaming": "Index1",
            "allow_null": FALSE,
            "type_of": STRING,
            "model_of": NA,
            "decimals_of": NA,
            "range_of": NO_RANGE        
            },
        "index 2": {
            "field_name": "cod_index_2",
            "renaming": "Index2",
            "allow_null": FALSE,
            "type_of": STRING,
            "model_of": NA,
            "decimals_of": NA,
            "range_of": NO_RANGE        
            },
        "spread_cpn1": {
            "field_name": "cod_spread_cpn1",
            "renaming": "Spread1",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": NO_RANGE        
            },
        "spread 1": {
            "field_name": "cod_spread_1",
            "renaming": "Spread2",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": NO_RANGE        
            },
        "formula": {
            "field_name": "cod_formula",
            "renaming": "FormulaCoupon",
            "allow_null": FALSE,
            "type_of": STRING,
            "model_of": NA,
            "decimals_of": NA,
            "range_of": NO_RANGE        
            },
        "multiplier 1": {
            "field_name": "cod_multiplier_1",
            "renaming": "Multiplier1",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": NA,
            "decimals_of": NA,
            "range_of": NO_RANGE        
            },
        "multiplier 2": {
            "field_name": "cod_multiplier_2",
            "renaming": "Multiplier2",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": NA,
            "decimals_of": NA,
            "range_of": NO_RANGE        
            },
        "multiplier 3": {
            "field_name": "cod_multiplier_3",
            "renaming": "Multiplier3",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": NA,
            "decimals_of": NA,
            "range_of": NO_RANGE        
            },
        "cap": {
            "field_name": "cod_cap",
            "renaming": "Cap",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": NO_RANGE        
            },
        "floor": {
            "field_name": "cod_floor",
            "renaming": "Floor",
            "allow_null": FALSE,
            "type_of": FLOAT,
            "model_of": PERCENT,
            "decimals_of": 2,
            "range_of": NO_RANGE        
            },
        "in arrears": {
            "field_name": "cod_in_arrears",
            "renaming": "InArrears",
            "allow_null": FALSE,
            "type_of": STRING,
            "model_of": NA,
            "decimals_of": NA,
            "range_of": NO_RANGE        
            },
        "refix frequency": {
            "field_name": "cod_refix_frequency",
            "renaming": "RefixFrequency",
            "allow_null": FALSE,
            "type_of": STRING,
            "model_of": NA,
            "decimals_of": NA,
            "range_of": NO_RANGE        
            },
        "pay frequency": {
            "field_name": "cod_pay_frequency",
            "renaming": "PayFrequency",
            "allow_null": FALSE,
            "type_of": STRING,
            "model_of": NA,
            "decimals_of": NA,
            "range_of": NO_RANGE        
            },
        "lookback day": {
            "field_name": "cod_lookback_day",
            "renaming": "LookbackDays",
            "allow_null": FALSE,
            "type_of": INT,
            "model_of": NA,
            "decimals_of": NA,
            "range_of": NO_RANGE        
            },
        "structure type": {
            "field_name": "cod_structure_type",
            "renaming": "StructureType",
            "allow_null": FALSE,
            "type_of": STRING,
            "model_of": NA,
            "decimals_of": NA,
            "range_of": NO_RANGE        
            },
        "effective dt_cpn2": {
            "field_name": "cod_effective_dt_cpn2",
            "renaming": "switchDate",
            "allow_null": FALSE,
            "type_of": DATE,
            "model_of": NA,
            "decimals_of": NA,
            "range_of": DATE_RANGE        
            }
    },
    "sections": 
    {
        "section0": {
            "name": "DES Information",
            "list": ["cod_isin", "cod_name", "cod_currency", "cod_rank", "cod_coupon", "cod_type", "cod_daycnt", "cod_maturity", "cod_pricing_date", "cod_interest_accrual_date", "cod_first_settle_date", "cod_first_coupon_date", "cod_amt_issued", "cod_amt_outstanding", "cod_min_piece", "cod_par_amount", "cod_exchange", "cod_formula_des", "cod_esg_type", "cod_sinkable", "cod_callable", "cod_make_whole", "cod_perpetual", "cod_status", "cod_cpn_freq", "cod_note_des", "cod_bond_type", "cod_description"]
        },
        "section1": {
            "name": "CPN Information",
            "list": ["cod_index_1", "cod_index_2", "cod_spread_cpn1", "cod_spread_1", "cod_formula", "cod_multiplier_1", "cod_multiplier_2", "cod_multiplier_3", "cod_cap", "cod_floor", "cod_in_arrears", "cod_refix_frequency", "cod_pay_frequency", "cod_lookback_day", "cod_structure_type", "cod_effective_dt_cpn2"]
        }
    }
}


