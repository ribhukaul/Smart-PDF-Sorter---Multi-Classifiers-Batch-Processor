import pandas as pd

# from Gestore_DB.GestoreQuery import getGest_DB,attivaCeODBC
# # Create DB connection
# #attivaCeODBC()
# db=getGest_DB('produzioneObbligazioni')

# Keys conversion Code to SQL TABLE
py_to_sql_keys= {
    #DES
    "isin": "Isin", 
    "name": "Name",
    "currency": "Currency",
    "rank": "Rank",
    "coupon": "Coupon",
    "type":"Type",
    "day_cnt": "DayCnt",
    "maturity": "Maturity",
    "pricing_date": "PricingDate",
    "interest_accrual_date": "InterestAccrualDate",
    "first_settle_date": "FirstSettleDate",
    "first_coupon_date": "FirstCouponDate",
    "amount_issued": "AmtIssued",
    "amount_outstanding": "AmtOutstanding",
    "min_piece": "MinPiece",
    "par_amount": "ParAmount",
    "exchange": "Exchange",
    "formula_des": "Formula",
    "esg_type": "ESG_bond",
    "sinkability": "Sinkable",
    "callability": "Callable",
    "make_whole": "MakeWhole",
    "perpetual": "Perpetual",
    "status": "Status",
    "cap": "Cap",
    "floor": "Floor",
    "cpn_freq":"CpnFreq",
    "note_des": "noteDES",
    "bond_type": "BondType",
    "description": "Description",

    # CPN 
    "index 1": "Index1",
    "index 2": "Index2",
    "spread_cpn1": "Spread1",
    "spread 1": "Spread2",
    "formula": "FormulaCoupon",
    "multiplier 1": "Multiplier1",
    "multiplier 2": "Multiplier2",
    "multiplier 3": "Multiplier3",
    "cap": "Cap",
    "floor": "Floor",
    "in arrears": "InArrears",
    "refix frequency": "RefixFrequency",
    "pay frequency": "PayFrequency",
    "lookback day": "LookbackDays",
    "structure type": "StructureType",
    "effective dt_cpn2": "switchDate"
    }


# def carica(data_dict):
#     """Upload data to SQL table via INSERT query

#     Args:
#         data (dict): dictionary containing the data to be uploaded

#     Raises:
#         ex: exception name in case of error
#     """
#     # Create query to import data
#     column_names = [k.upper() for k in data_dict.keys()]
#     column_names_str = ",".join(column_names)
#     data = [v for k,v in data_dict.items()]
#     data_str = ",".join([f"'{l}'" for l in data])
#     qIns = f"insert into alm.EstrazioniBond_BLOO ( {column_names_str}) values ( {data_str} )"

#     try:
#         db.execute(qIns)
#         db.commit()
#     except Exception as ex:
#         try:
#             db.rollback()
#         except:
#             pass
#         raise ex   


# def save_to_table(extractions):
#     """
#     Save extracted data to a SQL table.

#     Args:
#         extractions (dict): A dictionary containing the extracted data.

#     Returns:
#         None
#     """
#     # Flatten the dictionary
#     flattened_dict = {}
#     for key, value in extractions.items():
#         if isinstance(value, dict):
#             flattened_dict.update(value)
    
#     # Convert each value to a string
#     new_flattened_dict = {}
#     for key, value in flattened_dict.items():
#         if value != '':
#             value = str(value)
#             value = value.replace("'", '"')
#             if value.endswith(' '):
#                 value = value.rstrip()

#             new_flattened_dict[key] = value
        
#     # If isin not there, add a "NOT FOUND" value
#     if "isin" not in new_flattened_dict:
#         new_flattened_dict["isin"] = "NOT FOUND"

#     # Create a DataFrame from the flattened dictionary
#     df = pd.DataFrame(new_flattened_dict, index=[0])
#     df['dataestrazione'] = pd.to_datetime('today').strftime('%Y-%m-%d %H:%M:%S')
    
#     # Rename the columns using a mapping dictionary
#     df = df.rename(columns=py_to_sql_keys)
#     # df to dictionary only considering the first row
#     df_dict = df.to_dict(orient='records')[0]

#     # Load the data into the SQL table
#     carica(df_dict)

