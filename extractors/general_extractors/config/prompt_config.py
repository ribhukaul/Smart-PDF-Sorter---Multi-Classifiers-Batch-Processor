from extractors.general_extractors.custom_extractors.certificates.certificates_config.cert_tags import (
    InformazioniBaseBNP,
    TabellaAllegatiBNP,
    TabellaAllegatoScadenzaBNP,
    TabellaCedola,
    TabellaDeductableVontobel,
    TabellaFirstInfoVontobel,
    TabellaMainInfoVontobel,
    TabellaSottostanti,
    TabellaMainInfo,
    CedolaStr,
    InformazioniBaseCertificati,
    TabellaSottostantiHeader,
    TabellaAllegatoPremioBNP,
    TabellaFirstInfoBNP,
    TabellaSottostanteBNP,
    TabellaMainInfoBNP,
)

#KID
from extractors.configs.extraction_config.tags.kid_tags import (
    InformazioniBase, TabellaScenariPerformance, TabellaRiy, TabellaRiySmall, TabellaRiyRHP2, TabellaCostiIngresso, TabellaCostiGestione, TabellaCostiGestionepercentuale, PerformanceScenarios, TableRiy,
    ScenariPerformanceAbsoluteEuro, ScenariPerformanceRHP2, CompanyName)
#GKID
from extractors.configs.extraction_config.tags.gkid_tags import (
    InformazioniBaseGkid, TabellaRiyPercGkid, TabellaRiyEurGkid, TabellaCostiIngressoGkid, TabellaCostiGestioneGkid)
# WAMINSURANCE 
from extractors.configs.extraction_config.tags.waminsurance.waminsurance_tags import (
    InformazioniBaseKidGov, TabellaScenariPerformanceCredem, IsDisclaimerThere)

# CERTIFICATES

prompts = {
    "it": {
        "general_info": """Dal documento seguente, estrai 
            - Periodo di detenzione raccomandato o per quanto tempo si presuppone di detenere il prodotto(anni), converti in anni se necessario
            - indicatore sintetico di rischio
            - Data di realizzazione del documento
            DOCUMENTO:
            {context}""",
        "general_info_kid_governance": """Dal documento seguente, estrai 
            - Periodo di detenzione raccomandato o per quanto tempo si presuppone di detenere il prodotto(anni), converti in anni se necessario
            - indicatore sintetico di rischio
            - Data di realizzazione del documento
            - è presente nella prima parte della prima pagina il disclaimer: 'State per acquistare un prodotto che non è semplice e può essere di difficile comprensione"?
            DOCUMENTO:
            {context}""",
        "company_name": """ dal documento,
             - estrarre il nome dell'azienda
            DOCUMENTO: 
            {context}""",
        "performance1y": """Considerando la seguente tabella,estrai qual'è il rendimento percentuale dei seguenti scenari:
            - STRESS
            - SFAVOREVOLE
            - MODERATO
            - FAVOREVOLE 
            a 1 anno?
            --ritorna solo 4 valori, non di più non di meno
            TABELLA:
                {context}?""",
        "performancerhp": """Considerando la seguente tabella,estrai il rendimento percentuale dei seguenti scenari:
            - STRESS
            - SFAVOREVOLE
            - MODERATO
            - FAVOREVOLE 
            a {rhp} anni?
            --ritorna solo i valori dopo {rhp} anni

            TABELLA:
                {context}?""",
        "performancemorte": """Considerando la seguente tabella fornita,
        -dopo o nella la sezione scenario di morte o decesso di evento assicurato
        estrai i possibili rimborsi ai beneficiari al netto dei costi
        -se trovi 3 valori, ritorna solo il primo e l'ultimo
        -ritorna sempre 2 valori, non di più non di meno
 
            TABELLA:
                {context}?""",
        "target_market": """"Dal documento seguente cita ciò che si dice sugli investitori al dettaglio cui si intende commercializzare il prodotto
        ---ritorna solamente la citazione niente introduzione
        ---dovrebbero essere multiple lunghe frasi
        ---ritorna solamente ciò che è riportato nel documento non rifrasare, non puoi aggiungere niente,non voglio introduzione, fornisci la risposta esatta
        ---se non trovi la citazione, la frase da cercare potrebbe essere leggermente diversa
        

            DOCUMENTO:
            {context}""",
        "riy_rhp2": """La prima cifra (sia per i costi totali che per incidenza annuale dei costi) riguarda 1 anno, poi X anni e infine RHP anni.
                Se ne manca 1, manca quello a 1 anno (in tal caso è rimpiazzato da un trattino (-))
                #####
                Considera che X={}anni, RHP={}anni, 
                ####
                DOCUMENT={}""",
        "riy": """La prima cifra (sia per i costi totali che per incidenza annuale dei costi) riguarda 1 anno e poi RHP anni.
                ###
                RHP={}
                ###
                DOCUMENT={}""",
        "riy_small": """La prima cifra (sia per i costi totali che per incidenza annuale dei costi) riguarda 1 anno e poi RHP anni.
                ###
                RHP={}
                ###
                DOCUMENT={}""",
        "general_info_gkid": """Dal documento seguente, estrai
            - Periodo di detenzione raccomandato 
            - indicatore sintetico di rischio minimo o peggiore(da:)(il primo)
            - indicatore sintetico di rischio massimo o migliore(a:)(il secondo)
            - Data di realizzazione del documento
            DOCUMENTO:
            {context}""",
        "performance1y-gkid": """Considerando la seguente tabella,estrai qual'è il rendimento percentuale dei seguenti scenari:
            - STRESS
            - SFAVOREVOLE
            - MODERATO
            - FAVOREVOLE 
            a 1 anno?
            --ritorna solo 4 valori, non di più non di meno
            TABELLA:
                {context}?""",
        "performancerhp-gkid": """Considerando la seguente tabella,estrai il rendimento percentuale dei seguenti scenari:
            - STRESS
            - SFAVOREVOLE
            - MODERATO
            - FAVOREVOLE 
            a {rhp} anni?
            --ritorna solo i valori dopo {rhp} anni

            TABELLA:
                {context}?""",
        "performancemorte-gkid": """Considerando la seguente tabella fornita,
        -dopo o nella la sezione scenario di morte o decesso di evento assicurato
        estrai i possibili rimborsi ai beneficiari al netto dei costi
        -se trovi 3 valori, ritorna solo il primo e l'ultimo
        -ritorna sempre 2 valori, non di più non di meno
 
            TABELLA:
                {context}?""",
        "market_gkid": """"Dal documento seguente cita ciò che si dice sugli investitori al dettaglio cui si intende commercializzare il prodotto
        ---ritorna solamente la citazione niente introduzione
        ---dovrebbero essere multiple lunghe frasi
        ---ritorna solamente ciò che è riportato nel documento non rifrasare, non puoi aggiungere niente,non voglio introduzione, fornisci la risposta esatta
        ---se non trovi la citazione, la frase da cercare potrebbe essere leggermente diversa
        

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



table_schemas = {
    "it": {
        "general_info": InformazioniBase,
        "company_name": CompanyName,
        "general_info_kid_governance": InformazioniBaseKidGov,
        "is_product_complex": IsDisclaimerThere,
        "performance": TabellaScenariPerformance,
        "performance_abs": ScenariPerformanceAbsoluteEuro,
        'performance_rhp_2': ScenariPerformanceRHP2,
        "performance_credem": TabellaScenariPerformanceCredem,
        "riy": TabellaRiy,
        "riy_small": TabellaRiySmall,
        "riy_rhp2": TabellaRiyRHP2,
        "costi_ingresso": TabellaCostiIngresso,
        "costi_gestione": TabellaCostiGestione,
        "costi_gestione_%": TabellaCostiGestionepercentuale,
        "general_info_gkid": InformazioniBaseGkid,
        "riy%/-gkid": TabellaRiyPercGkid,
        "riy€-gkid": TabellaRiyEurGkid,
        "costi_ingresso_gkid": TabellaCostiIngressoGkid,
        "costi_gestione_gkid": TabellaCostiGestioneGkid,
        "cedola": TabellaCedola,
        "sottostanti": TabellaSottostanti,
        "main_info": TabellaMainInfo,
        "cedola_str": CedolaStr,
        "general_info_certificati": InformazioniBaseCertificati,
        "sottostanti_header": TabellaSottostantiHeader,
        "general_info_bnp": InformazioniBaseBNP,
        "main_info_bnp": TabellaMainInfoBNP,
        "allegato_bnp_premio": TabellaAllegatoPremioBNP,
        "allegato_bnp_scadenza": TabellaAllegatoScadenzaBNP,
        "allegati_bnp": TabellaAllegatiBNP,
        "first_info_bnp": TabellaFirstInfoBNP,
        "sottostante_bnp": TabellaSottostanteBNP,
        
    },
    "en": {
        "performance": PerformanceScenarios,
        "riy": TableRiy,
        "first_info_vontobel": TabellaFirstInfoVontobel,
        "main_info_vontobel": TabellaMainInfoVontobel,
        "deductables_vontobel": TabellaDeductableVontobel,

        },
}


word_representation = {
    "it": {
        "performance": ["moderato", "sfavorevole", "favorevole", "stress", "possibile rimborso al"],
        "riy": ["costi totali", "riy"],
        "riy_perc_gkid": ["costi totali", "riy"],
        "costi_ingresso": ["costi di ingresso", "costi di uscita"],
        "costi_gestione": [
            "commissioni di gestione",
            "costi di transazione",
            "commissioni di performance",
            "costi amministrativi",
        ],
        "costi_ingresso_gkid": ["costi di ingresso", "costi di uscita"],
        "costi_gestione_gkid": [
            "commissioni di gestione",
            "costi di transazione",
            "commissioni di performance",
            "costi amministrativi",
        ],
        "cedola": [
            "cedola",
            "cedola",
            "data di osservazione della cedola",
            "data di pagamento della cedola condizionale",
            "importo della cedola condizionale",
        ],
        "sottostanti": ["bloomberg ticker", "ticker", "sottostante", "isin"],
        "main_info": ["valuta del prodotto", "performance peggiore", "modalità di pagamento"],
        "sottostanti_table": ["bloomberg ticker", "ticker", "sottostante", "isin"],
        "first_info_bnp": ["codice isin", "isin", "autorità competente", "redazione", "produttore"],
        "main_info_bnp": ["data di strike", "strike", "prezzo di emissione", "emissione", "(rimborso)"],
        "main_info_bnp2": ["valuta", "valuta del prodotto", "importo nozionale", "nozionale"],
        "sottostante_bnp": ["bloomberg", "codice bloomberg", "sottostante"],
        "allegato_bnp_premio": ["premio/i", "premio", "barriera/e", "condizionato"],
        "allegato_bnp_scadenza": ["liquidazione", "anticipata", "facoltativa", "scadenza, rimborso"],
    },
    "en": {
        "performance": [
            "moderate",
            "unfavorable",
            "favorable",
            "stress",
            "might get back",
        ],
        "riy": ["total costs", "annual cost"],
    },
}
