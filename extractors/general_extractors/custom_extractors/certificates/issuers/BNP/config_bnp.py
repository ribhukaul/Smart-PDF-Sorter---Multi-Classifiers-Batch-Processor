prompts={
    "it":{

        "general_info_bnp": """Dal documento seguente, estrai 
             -il periodo di detenzione raccomandato
             -l'indicatore di rischio su 7 come dato
            DOCUMENTO:
            {context}""",
        "first_info_bnp": """Dal documento seguente, estrai
            -ISIN
            - solamente l'emittente
            DOCUMENTO:
            {context}""",
        "main_info_bnp": """
            dal documento seguente, estrai
            -valuta del prezzo di emissione/valuta del prodotto
            -data di strike
            -data di emissione
            -data di liquidazione (rimborso)
            -data di valutazione dell'importo di liquidazione (rimborso)
            -valore nominale o importo nozionale
            -mercato di quotazione
            -barriera
            -barriera/e per il versamento del premio/i condizionato/i
            -prezzo di emissione
            -data/e di valutazione del/i premio/i condizionato/i
            -data/e di pagamento del/i premio/i
            -premio/i
            -premio/i condizionato/i
            -data di liquidazione anticipata facoltativa
            -tutte le date di valutazione dell' importo di liquidazione (rimborso) anticipato
            -barriera/e per la scadenza anticipata
            -tutte le date di scadenza anticipata
            -premio/i di uscita
            DOCUMENTO:
            {context}
            """,
        "allegato_bnp_premio": """
            dal documento seguente, estrai
            tutte le data/e di valutazione del/i premio/i condizionato/i
            tutte le data/e di pagamento del/i premio/i
            barriera/e o barrierale per il versamento del Premio/i Condizionato/i
            premio/i
            Premio/i condizionato/i
            DOCUMENTO:
            {context}
            
            """,
        "allegato_bnp_scadenza": """
            dal documento seguente, estrai:
            Data di Liquidazione Anticipata Facoltativa
            tutte le Data/e di Valutazione dell'Importo di Liquidazione (rimborso) Anticipato
            Barriera/e o barrierale per la Scadenza Anticipata
            Data di Scadenza Anticipata
            Premio/I di Uscita
            DOCUMENTO:
            {context}
            """,
        "allegati_bnp": """
            dal documento seguente, estrai:
            tutte le data/e di valutazione del/i premio/i condizionato/i
            tutte le data/e di pagamento del/i premio/i
            barriera/e o barrierale per il versamento del Premio/i Condizionato/i
            Premio/i
            Premio/i condizionato/i
            Data di Liquidazione Anticipata Facoltativa
            tutte le Data/e di Valutazione dell'Importo di Liquidazione (rimborso) Anticipato
            Barriera/e o barrierale per la Scadenza Anticipata
            Data di Scadenza Anticipata
            Premio/I di Uscita
            DOCUMENTO:
            {context}
            """,
        },
    "en":{},
}

word_representation={
    "it":{
        "performance": ["moderato", "sfavorevole", "favorevole", "stress", "possibile rimborso al"],
        "first_info_bnp": ["codice isin", "isin", "autorità competente", "redazione", "produttore"],
        "main_info_bnp": ["data di strike", "strike", "prezzo di emissione", "emissione", "(rimborso)"],
        "main_info_bnp2": ["valuta", "valuta del prodotto", "importo nozionale", "nozionale"],
        "sottostante_bnp": ["bloomberg", "codice bloomberg", "sottostante"],
        "allegato_bnp_premio": ["premio/i", "premio", "barriera/e", "condizionato"],
        "allegato_bnp_scadenza": ["liquidazione", "anticipata", "facoltativa", "scadenza, rimborso"],
        },
    "en":{},
}