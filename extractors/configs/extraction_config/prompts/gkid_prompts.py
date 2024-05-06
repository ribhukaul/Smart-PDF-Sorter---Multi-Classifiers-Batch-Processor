general_info_gkid = """Dal documento seguente, estrai
            - Periodo di detenzione raccomandato 
            - indicatore sintetico di rischio minimo o peggiore(da:)(il primo)
            - indicatore sintetico di rischio massimo o migliore(a:)(il secondo)
            - Data di realizzazione del documento
            DOCUMENTO:
            {context}"""

performance1y_gkid = """Considerando la seguente tabella,estrai qual'è il rendimento percentuale dei seguenti scenari:
            - STRESS
            - SFAVOREVOLE
            - MODERATO
            - FAVOREVOLE 
            a 1 anno?
            --ritorna solo 4 valori, non di più non di meno
            TABELLA:
                {context}?"""

performancerhp_gkid =  """Considerando la seguente tabella,estrai il rendimento percentuale dei seguenti scenari:
            - STRESS
            - SFAVOREVOLE
            - MODERATO
            - FAVOREVOLE 
            a {rhp} anni?
            --ritorna solo i valori dopo {rhp} anni

            TABELLA:
                {context}?""",
performancemorte_gkid = """Considerando la seguente tabella fornita,
        -dopo o nella la sezione scenario di morte o decesso di evento assicurato
        estrai i possibili rimborsi ai beneficiari al netto dei costi
        -se trovi 3 valori, ritorna solo il primo e l'ultimo
        -ritorna sempre 2 valori, non di più non di meno
 
            TABELLA:
                {context}?"""

market_gkid =  """"Dal documento seguente cita ciò che si dice sugli investitori al dettaglio cui si intende commercializzare il prodotto
        ---ritorna solamente la citazione niente introduzione
        ---dovrebbero essere multiple lunghe frasi
        ---ritorna solamente ciò che è riportato nel documento non rifrasare, non puoi aggiungere niente,non voglio introduzione, fornisci la risposta esatta
        ---se non trovi la citazione, la frase da cercare potrebbe essere leggermente diversa
        

            DOCUMENTO:
            {context}"""

