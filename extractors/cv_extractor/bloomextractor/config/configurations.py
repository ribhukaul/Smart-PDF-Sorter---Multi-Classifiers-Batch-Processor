CONFIGURATIONS = {
    "DES": {
        'fields' : [
            "ESG_type","Name", "ISIN", "Rank", "Coupon", "Cpn Freq", 
            "Maturity","Interest Accrual Date",  "1st Settle Date",
            "1st Coupon Date","Par Amount","Currency", "Type","Day Cnt",
            "Exchange", "Sinkability",'Amount Issued', 'Min Piece', 
            'Callability', 'MakeWhole'
            # Formula
            ],
        
        "widths" : {
            "ISIN": 400,
            "Interest Accrual Date": 400, 
            "Pricing Date":550, 
            "1st Coupon Date": 500,
            "1st Settle Date": 520,
            'Coupon':200, 
            'Name':500, 
            'Par Amount': 350, 
            'Currency':100, 
            'Rank':300, 
            'Exchange':400, 
            "Day Cnt": 280, 
            "Type": 300,
            "Maturity": 600}
    },
    "COUPON": {
        'fields': ['Pay Frequency', 'Formula Des','Day Cnt Conv'],
        "widths": {}
    }
}




CALL_KEYWORDS = {
    "Callable on and anytime after date(s) shown": {"width": 250, "type": "American"},
    "Callable only on date(s) shown": {"width": 250, "type": "European"},
}

RESULTS_CONFIG = {
    'des': {
        'Name':'Emittente',
        'ISIN':'Isin',
        'Exchange':'Mercato_SM',
        'Currency':'Divisa',
        'Rank': 'Ranking',
        'Coupon': 'Coupon',
        'Type': 'TipoTasso',
        '1st Settle Date': 'DataEmissione',
        '1st Coupon Date':'DataPrimaCedola',
        'Maturity': 'Scadenza',
        'ESG_type': 'ESG_Bond_Type',
        'Cpn Freq': 'Frequenza',
        'Day Cnt': 'RegolaCalcolo',
        'Sinkability': 'Sinkability',
        'Amt Issued': 'AmmontareEmesso',
        'Amt Outstanding': 'AmountOutstanding',
        'Min Piece': 'MinimumDenomination',
        'Callability': 'Callability',
        'MakeWhole': 'MakeWhole',
        'Perpetual': 'Perpetual'
    }
}