


prompts = {
    "it": {

        "general_info_kid_governance": """Dal documento seguente, estrai 
            - Periodo di detenzione raccomandato o per quanto tempo si presuppone di detenere il prodotto(anni), converti in anni se necessario
            - indicatore sintetico di rischio
            - Data di realizzazione del documento
            - Il prodotto è complesso?
            DOCUMENTO:
            {context}""",





        "general_info_certificati": """Dal documento seguente, estrai 
            - ISIN
            - descrizione completa del certificato, appare scritta come certificato ... in VALUTA ... su .... , con valuta che può essere EUR o USD
            - emittente o ideatore del certificato, compare dopo: Ideatore:
            DOCUMENTO:
            {context}""",
        "cedola_str": """
            Dal documento seguente, estrai esattamente come riportato il pezzo di testo
            mi interessa tutto il denso testo numerato che comprende date e costi e che usa il carattere '▪' come spaziatore.
            potrebbe non esistere, in quel caso ritorna N/A
            DOCUMENTO:
            {context}""",
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
            "main_info_bnp":"""
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
            "allegato_bnp_premio":"""
            dal documento seguente, estrai
            tutte le data/e di valutazione del/i premio/i condizionato/i
            tutte le data/e di pagamento del/i premio/i
            barriera/e o barrierale per il versamento del Premio/i Condizionato/i
            premio/i
            Premio/i condizionato/i
            DOCUMENTO:
            {context}
            
            """,
            "allegato_bnp_scadenza":"""
            dal documento seguente, estrai:
            Data di Liquidazione Anticipata Facoltativa
            tutte le Data/e di Valutazione dell'Importo di Liquidazione (rimborso) Anticipato
            Barriera/e o barrierale per la Scadenza Anticipata
            Data di Scadenza Anticipata
            Premio/I di Uscita
            DOCUMENTO:
            {context}
            """,
            "allegati_bnp":"""
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
    "en": {
        "general_info": """From the following document, extract:
            - ISIN
            - Recommended holding period
            - Synthetic risk indicator

            DOCUMENT:
            {context}""",
        "performance": """Considering the following table, extract both the percentage return and the monetary amount in the following scenarios:
            - STRESS
            - UNFAVORABLE
            - MODERATE
            - FAVORABLE
            both 1 year and {rhp} years?

            TABLE:
                {context}?""",
        "riy": "",
        "market": """From the following document extract only the quote following (but do not add the phrase to the response)this phrase: 
        -the retail investors to whom we intend to market the product
        ---skip your introduction just say the quote
        ---return only what is specified on the document, do not rephrase, do not add anything, be precise
        ---if you cant find it, the phrase could be slightly different

            DOCUMENTO:
            {context}""",
        "first_info_vontobel":"""
            from the following document, extract:
            -title, found after: "Final Terms for"
            -the ISIN
            -Issuer
            DOCUMENT:
            {context}
            """,
        "main_info_vontobel":"""
            from the following document, extract:
            -Settlement Currency
            -Fixing Date
            -Issue date
            -Maturity date
            -Final Valuation Date
            -Calculation amount or Nominal Amount
            -Bonus Amount
            -Redemption Level
            -Bonus Threshold
            -Barrier percentages
            -Memory
            -Strike
            -Early Redemption
            -Barrier Event
            -Observation Date(s) 
            -Bonus Payment Date(s)
            -Valuation Date (s)
            -Early Redemption Date (n) 
            -Underlying title, often right after 'Underlying'
            -ISIN Underlying, in the section 'Underlying'
            -Bloomberg Symbol, in the section 'Underlying'
            DOCUMENT:
            {context}
            """,
        "deductables_vontobel":"""
            from the following document, extract:
            -Issue Price
            -Exchange Listing , often under 'Stock Exchange Listing'
            DOCUMENT:
            {context}
            """,
        "main_info_vontobel_2": """
            from the following document, extract:
            -Bonus Amount
            -Bonus Threshold
            -Barrier Event
            -Observation Dates, can be a lot
            -Bonus Payment Date(s)
            -Valuation Date (s)
            -Early Redemption Date (n) 
            DOCUMENT:
            {context}
            """,
    },
}
