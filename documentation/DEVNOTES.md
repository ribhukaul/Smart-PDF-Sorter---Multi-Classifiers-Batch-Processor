## TODO:
Models.clearResource()
fatto per pulire le instanze e ei singletons di instance del gruppo che lo sta usando

derivati name refactoring
normalizzare attraverso i derivati i nomi delle variabili

derivati value overlapping
sistemi per raggruppare variabili diverse in un unica per il risultato

tabelle marco
raggruppare  dati e dividerli come serve a marco

controllare e modificare tutti i config come preferito


## NOTES:

i metodi process sono intenzionalmente molto lunghi in quanto sono comodi per debugging e leggibilità, molto facile usarli come dizionario, sempre in fondo

le exceptions sono poco testate e spesso outdated o copia incollate da altri metodi attenzione

pydantic tag è deprecated in quanto la nuova versione, che usa un BaseModel in un altra libreria, lascia l'api appesa per sempre sul tag, fino al timeout minuti dopo, potrebbe avere qualcosa a che fare con troppi token ma strano

documentazione è decente ma ovviamente potrebbero esserci docstring outdated

good luck  o7


