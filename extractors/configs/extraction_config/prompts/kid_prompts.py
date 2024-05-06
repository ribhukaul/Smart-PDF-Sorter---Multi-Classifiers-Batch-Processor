general_info = """Dal documento seguente, estrai 
            - Periodo di detenzione raccomandato o per quanto tempo si presuppone di detenere il prodotto(anni), converti in anni se necessario
            - indicatore sintetico di rischio
            - Data di realizzazione del documento
            DOCUMENTO:
            {context}"""

is_product_complex = """Nel documento seguente è presente il disclaimer: 'State per acquistare un prodotto che non è semplice e può essere di difficile comprensione'?
            DOCUMENTO:{context}"""

performance1y = """"Considerando la seguente tabella,estrai qual'è il rendimento percentuale dei seguenti scenari:
            - STRESS
            - SFAVOREVOLE
            - MODERATO
            - FAVOREVOLE 
            a 1 anno?
            --ritorna solo 4 valori, non di più non di meno
            TABELLA:
                {context}?"""

performancerhp = """Considerando la seguente tabella,estrai il rendimento percentuale dei seguenti scenari:
            - STRESS
            - SFAVOREVOLE
            - MODERATO
            - FAVOREVOLE 
            a {rhp} anni?
            --ritorna solo i valori dopo {rhp} anni

            TABELLA:
                {context}?"""

performance_rhp_2 = """I primi valori in euro riguardano lo scenario di stress, poi sfavorevole moderato ed infine favorevole.
                    I valori in riferimento a uno scenario sono espressi prima in euro e poi in percentuale(queste informazioni ti possono servire nel caso in cui
                    le colonne di riferimento per capire di che scenario si tratti, sono formattate male).
                    (L'informazione che ti interessa è nell'ultima colonna)
                    ####
                    X={year}
                    ####
                    document={context}"""

performance_abs = """Considera che escludendo la riga dello scenario minimo. I primi valori in euro riguardano lo scenario di stress, poi sfavorevole
                moderato ed infine favorevole. I valori in riferimento a uno scenario sono espressi prima in euro e poi in percentuale(queste informazioni ti possono servire nel caso in cui
                le colonne di riferimento per capire di che scenario si tratti, sono formattate male).
                ####
                RHP={rhp}
                ####
                DOCUMENT={context}"""


# performancemorte = """Considerando la seguente tabella fornita,
#         -dopo o nella la sezione scenario di morte o decesso di evento assicurato
#         estrai i possibili rimborsi ai beneficiari al netto dei costi
#         -se trovi 3 valori, ritorna solo il primo e l'ultimo
#         -ritorna sempre 2 valori, non di più non di meno

#             TABELLA:
#                 {context}?"""

market = """"Dal documento seguente cita ciò che si dice sugli investitori al dettaglio cui si intende commercializzare il prodotto
        ---ritorna solamente la citazione niente introduzione
        ---dovrebbero essere multiple lunghe frasi
        ---ritorna solamente ciò che è riportato nel documento non rifrasare, non puoi aggiungere niente,non voglio introduzione, fornisci la risposta esatta
        ---se non trovi la citazione, la frase da cercare potrebbe essere leggermente diversa
        

            DOCUMENTO:
            {context}"""

