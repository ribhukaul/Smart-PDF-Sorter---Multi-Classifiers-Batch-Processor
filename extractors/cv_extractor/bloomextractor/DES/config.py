FIELDS = {
    "isin": {"widths":400, "name": "ISIN"},
    "interest_accrual_date": {"widths":400, "name": "Interest Accrual Date"},
    "pricing_date":{"widths":550, "name": "Pricing Date"},
    "first_coupon_date": {"name": "1st Coupon Date"},
    "first_settle_date": {"widths":520, "name": "1st Settle Date"},
    'coupon':{"widths":200, "name": "Coupon"},
    'name':{"widths":500, "name": "Name"},
    'par_amount': {"widths":350, "name": "Par Amount"},
    'currency':{"widths":100, "name": "Currency"},
    'rank':{"widths":320, "name": "Rank"},
    'cpn_freq':{"widths":300, "name": "Cpn Freq"},
    'exchange':{"widths":400, "name": "Exchange"},
    "day_cnt": {"widths":280, "name": "Day Cnt"},
    "type": {"widths":280, "name": "Type"},
    "maturity": {"widths":600, "name": "Maturity"},
    "esg_type": {"name": "ESG_type"},
    "sinkability": {"name": "Sinkability"},
    'amount_issued': {"name": "Amt Issued"},
    'min_piece': {"name": "Min Piece"},
    'callability': {"name": "Callability"},
    'make_whole': {"name": "MakeWhole"},
    'formula_des': {"widths": 450, "name": "Formula"},
    #"tasso_type": {"name": "Tasso Type"},
    'status': {"name": "Status"},
    'note_des': {"name": "Note"},
    'bond_type': {"width":500, "name": "Mkt Iss"},
    "description": {"name": "Description"},
    }

SPECIFIC_EXTRACTORS  = [
    "isin", "name", "esg_type", "exchange", "sinkability", "amount_issued", 
    "min_piece", "callability", "make_whole", "maturity", "status", "note_des",
    "bond_type", "first_coupon_date", "formula_des", "description"#"tasso_type",
    ]

VALID_FIELDS_CONVENTION = {
    "day_cnt": [
        'ACT/ACT', '30/360', 'ACT/360', 'ACT/365'
        ],
    # "type": [
    #     'Fixed', 'Floating', 'Zero Coupon', 'Variable'
    #     ],
    "rank": [
        'Junior Subordinated','Jr Subordinated',  'SrUnsecured', 'Sr Non Preferred', 'ConvertibileSub','GVTGuaranteed',
        'PreferenceShare','SubJunior','SubND','SubTII','SubTI', 'Senior',  'Covered','Convertibile',
        'Secured','Subordinated', "Unsecured", "Sr Pref","Sr Preferred", "Sr Non Pref", "Sr Non Preferred", "Sr Non Preferr", "Sr Non", 
        "Preferred"],
    "currency": [
        'AED','AFN','ALL','AMD','ANG','AOA','ARS','ATS','AUD','AWG','AZN',
        'BAM','BBD','BDT','BGN','BHD','BIF','BMD','BND','BOB','BRL','BSD','BTN','BWP','BYN','BZD','CAD','CDF',
        'CHF','CKD','CLP','CNY','COP','CRC','CUP','CVE','CZK','DEM','DJF','DKK','DOP','DZD','EGP','ERN',
        'ETB','EUR','FJD','FKP','FOK','GBP','GEL','GGP','GHS','GIP','GMD','GNF','GTQ','GYD','HKD','HNL',
        'HRK','HTG','HUF','IDR','ILS','IMP','INR','IQD','IRR','ISK','ITL','JEP','JMD','JOD','JPY','KES',
        'KGS','KHR','KID','KMF','KPW','KRW','KWD','KYD','KZT','LAK','LBP','LKR','LRD','LSL','LYD','MAD',
        'MDL','MGA','MKD','MMK','MNT','MOP','MRU','MUR','MVR','MWK','MXN','MYR','MZN','NAD','NGN','NIO',
        'NOK','NPR','NZD','OMR','PAB','PEN','PGK','PHP','PKR','PLN','PND','PRB','PYG','QAR','RON','RSD',
        'RUB','RWF','SAR','SBD','SCR','SDG','SEK','SGD','SHP','SKK','SLL','SLS','SOS','SRD','SSP','STN',
        'SYP','SZL','THB','TJS','TMT','TND','TOP','TRY','TTD','TVD','TWD','TZS','UAH','UGX','USD','UYU',
        'UZS','VES','VND','VUV','WST','XAF','XCD','XOF','XPF','YER','ZAR','ZMW','ZWB'
        ]
    }
