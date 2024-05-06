from typing import List, Optional, Required
from pydantic import BaseModel, Field

ISSUER = ['Marex Financial','Leonteq Securities AG/Guernsey','Vontobel Financial Products GmbH','SG Issuer', 'Unicredit SPA', 'Unicredit Bank','Banca Akros S.p.a.']
ISSUER_ROUTINGCHAIN = ['Unicredit', 'Marex']
CURRENCIES = ['EUR', 'USD', 'CHF', 'GBP']
QUOTATION_MARKETS = ['EuroTLX','SeDeX','SIX','Frankfurt', 'IDEM', 'No Listing']
BARRIER_TYPE = ['Europea','Americana']

class PydanticSchema_unicredit_noLangChain(BaseModel):

    ISIN : Required[str] = Field(
        description="Codice ISIN"
    )

    description : Required[str] = Field(
        description="Instrument description"
    )

    issuer : Required[str] = Field(
        description="Certificate's issuer, correspond to the issuer name",
        enum = ISSUER
    )

    specified_currency : Required[str] = Field(
        description="Currency of the product it can be EUR, USD, CHF, GBP",
        enum= CURRENCIES
    )

    listing : Required[str] = Field(
        description="Relevant exchange for the instrument, it can be SeDeX, EuroTLX or NO Listing",
        enum=  QUOTATION_MARKETS
    )

    issue_price : Required[str] = Field(
        description="the Issue price or Nominal Amount (NA)"
    )

    floor_amount: Required[str] = Field(
        description="The guaranteed level, Protection, Floor level, Floor Amount"
    )

    protection: Required[str] = Field(
        description="The percentage of protection"
    )

    barrier_level: Required[str] = Field(
        description="the Barrier Level"
    )

    strike_level: Required[str] = Field(
        description="the Strike Level"
    )

    barrier_type: Required[str] = Field(
        description="If name 'Protected' then 'None',"
                           "if the final redemption amount is computed on multiple dates then 'Americana',"
                           "if the final redemption amount is computed on a single final valuation date then 'Europea'",
        enum= BARRIER_TYPE
    )

    Additional_Conditional_Amount: Required[str] = Field(
        description="Number expressing the Additional Conditional Amount or the Additional Conditional Amount(m). Give me the number",
    )

    additional_unconditional_amount: Required[str] = Field(
        description="Number expressing the Additional Unconditional Amount or the Additional Unconditional Amount(m). Give me the number only if present, otherwise 'None'",
    )

    Additional_Conditional_Amount_Payment_Level: Required[str] = Field(
        description="it is Additional Conditional Amount Payment Level, the Percentage number expressing the threshold above which the Additional Conditional Amount will be paid. Give me the percentage"
    )

    memory_effect: Required[int] = Field(
        description="Additional Conditional Amount Payment with Memory: Yes then 1, otherwise 0",
        enum = [0,1],
    )

    maximum_payment: Required[str] = Field(
        description = "Maximum Amount paid at the Redemtpion date",
    )

    underlying_bloomberg: Required[str] = Field(
        description = "Product's underlying, give me the Bloomberg Codes",
    )

    underlying_isin: Required[str] = Field(
        description = "Product's underlying, give me the ISIN",
    )

    issue_date: Required[str] = Field(
        description = "Certificate's issue date",
    )

    final_payment_date: Required[str] = Field(
        description = "Final Payment date, also described by Maturity date",
    )

    early_redemption: Required[int] = Field(
        description = "If there is 'Early Redemption', an Early Redemption Amount or  an Early Redemption Level, then 1 else 0",
        enum=[0, 1]
    )

    callable: Required[int] = Field(
        description =  "In order to be 1 there must be 'right but nont obligation', else 0",
        enum=[0, 1]
    )
    putable: Required[int] = Field(
        description =  "If the investor has the right to early excercise the certificate 1, else 0",
        enum=[0, 1]
    )
    early_redemption_amount: Required[str] = Field(
        description="Number expressing the Early Redemption Amount. Give me the number only if present, otherwise 'None'",
    )


####################
# NOT USED FOR NOW #
####################
    

class schema_pydantic_RoutingChain(BaseModel):

    ISIN : Required[str] = Field(
        description="Codice ISIN formato da 12 caratteri, rappresenta l'identificativo dello strumento"
    )

    nome_del_prodotto : Required[str] = Field(
        description="Descrizione dello strumento, corrisponde al Nome del prodotto"
    )

    Emittente : Required[str] = Field(
        description="Corrisponde a 'IDEATORE di PRIIP', l'emittente del certificato",
        enum=ISSUER_ROUTINGCHAIN
    )


class PydanticSchema_preprocess_marex(BaseModel):

    ISIN : Required[str] = Field(
        description="Codice ISIN formato da 12 caratteri, rappresenta l'identificativo dello strumento"
    )

    nome_del_prodotto : Required[str] = Field(
        description="Descrizione dello strumento, corrisponde al Nome del prodotto"
    )

    Emittente : Required[str] = Field(
        description="Corrisponde a 'IDEATORE di PRIIP', l'emittente del certificato",
        enum = ISSUER
    )

    Valuta : Required[str] = Field(
        description="Valuta del prodotto, può essere EUR, USD, CHF",
        enum= CURRENCIES
    )

    quotazione_di_borsa : Required[str] = Field(
        description="'Quotazione in Borsa', mercato di quotazione dello strumento può essere EuroTLX, SeDeX, Frankfurt",
        enum=  QUOTATION_MARKETS
    )

    ammontare_nominale_del_prodotto : Required[str] = Field(
        description="Valore Nominale del prodotto, corrisponde all'ammontare nominale del prodotto, può essere 1000, 500, 900, 2000"
    )

    pagamento_minimo: Required[str] = Field(
        description="E' il pagamento minimo che lo strumento paga a scadenza, se nel nome del prodotto è presente 'Protected' allora numero >0. Individuato anche da 'Estinzione alla data di scadenza'"
    )

    barriera_finale_capitale: Required[str] = Field(
          description="è il numero corrispondente alla frase 'Barriera Finale Capitale % del livello di riferimento iniziale', non è 'Barriera Estinzione Anticipata' e non è 'Barriera Cedola', se non lo trovi metti 'None'",
    )

    prezzo_esercizio: Required[str] = Field(
        description="è il numero corrispondente alla frase 'Prezzo di esercizio % del livello di riferimento iniziale', non è 'Prezzo della barriera per il rimborso anticipato inziale' e non è  'Prezzo della barriera della cedola'",
   )

    TipologiaBarriera: Required[str] = Field(
        description="Se nel nome del prodotto è presente 'Protected' allora metti 'None',"
                           "altrimenti se il livello di riferimento finale viene valutato su più date allora 'American',"
                           "altrimenti se il livello/prezzo di riferimento finale è valutato alla data di valutazione finale allora 'European'",
        enum= BARRIER_TYPE
    )

    Cedola: Required[str] = Field(
        description="Numero che rappresenta il coupon, la cedola pagata. Dammi questo valore solo se presente, altrimenti 'None'",
    )

    premio_garantito_certificato: Required[str] = Field(
        description="Numero che rappresenta il Premio Garantito del Certificato, è nella frase 'Premio Garantito del Certificato: X EUR del sottostante', dammi lo stesso il valore anche se lo hai già estratto per la cedola'",
    )

    barriera_cedola: Required[str] = Field(
        description="E' il numero corrispondente alla frase 'Barriera Cedola % del livello di riferimento iniziale', non è 'Barriera Estinzione Anticipata' e non è  'Barriera Finale Capitale'"
    )

    effetto_memoria: Required[int] = Field(
        description="Se c'è la frase 'pagamento della cedola precedentemente maturato, ma tuttora non corrisposto' allora 1, altrimenti 0",
        enum = [0,1],
    )

    PagamentoMassimo: Required[str] = Field(
        description = "Pagamento massimo che il certificato può rimborsare all'estinzione del prodotto, si trova tra parentesi (il pagamento massimo)",
    )

    Sottostanti_isin: Required[str] = Field(
        description = "Rappresenta il sottostante o i sottostanti dello strumento, possono essere azioni oridnarie o Indici. Il sottostante è quello strumento su cui si calcola la performance per determinare il rimborso del prodotto. Dammi ISIN",
    )

    Sottostanti_bloomberg: Required[str] = Field(
        description = "Rappresenta il sottostante o i sottostanti dello strumento, possono essere azioni ordinarie o Indici. Il sottostante è quello strumento su cui si calcola la performance per determinare il rimborso del prodotto. Dammi Bloomberg",
    )

    Data_Emissione: Required[str] = Field(
        description = "Data di emissione del certificato, prima data di negoziazione dello strumento",
    )

    data_di_scadenza: Required[str] = Field(
        description = "Data di scadenza / termine, rappresenta la data a cui l'investitore riceverà il rimborso dello strumento",
    )

    estinzione_anticipata: Required[int] = Field(
        description = "Se c'è la frase 'rimborso anticipato' allora 1, altrimenti 0. Meccanismo di rimborso anticipato per cui il certificato viene rimborsato anticipatamente rispetto alla data di scadenza, in questo caso il sottostante peggiore è sopra alla barriera di rimborso anticipato",
        enum=[0, 1]
    )

    callable: Required[int] = Field(
        description =  "se l'emittente può richiamare a discrezione lo strumento allora 1 altrimenti 0, affinchè sia 1 ci deve essere scritto 'diritto ma non obbligo'",
        enum=[0, 1]
    )
    putable: Required[int] = Field(
        description =  "se l'investitore può richiamare il prodotto metti 1 altrimenti 0",
        enum=[0, 1]
    )


class PydanticSchema(BaseModel):

    ISIN : Required[str] = Field(
        description="Codice ISIN formato da 12 caratteri, rappresenta l'identificativo dello strumento"
    )

    nome_del_prodotto : Required[str] = Field(
        description="Descrizione dello strumento, corrisponde al Nome del prodotto"
    )


    Emittente : Required[str] = Field(
        description="Corrisponde a 'IDEATORE di PRIIP', l'emittente del certificato",
        enum = ISSUER
    )

    Valuta : Required[str] = Field(
        description="Valuta del prodotto, può essere EUR, USD, CHF",
        enum= CURRENCIES
    )

    quotazione_di_borsa : Required[str] = Field(
        description="'Quotazione in Borsa', mercato di quotazione dello strumento può essere EuroTLX, SeDeX, Frankfurt",
        enum=  QUOTATION_MARKETS
    )

    ammontare_nominale_del_prodotto : Required[str] = Field(
        description="Valore Nominale del prodotto, corrisponde all'ammontare nominale del prodotto, può essere 1000, 500, 900, 2000"
    )

    pagamento_minimo: Required[str] = Field(
        description="E' il pagamento minimo che lo strumento paga a scadenza, se nel nome del prodotto è presente 'Protected' allora numero >0. Individuato anche da 'Estinzione alla data di scadenza'"
    )

    livello_barriera: Required[str] = Field(
        description="Se nel nome del prodotto è presente 'Protected' allora metti 0. è il numero corrispondente alla frase  'Livello della barriera % del livello di riferimento iniziale', non è 'Livello della barriera per il rimborso anticipato inziale' e non è  'Livello della barriera della cedola'"
    )

    prezzo_barriera: Required[str] = Field(
          description="è il numero corrispondente alla frase  'Prezzo della barriera % del livello di riferimento iniziale', non è 'Prezzo della barriera per il rimborso anticipato inziale' e non è  'Prezzo della barriera della cedola'",
    )

    prezzo_esercizio: Required[str] = Field(
        description="è il numero corrispondente alla frase  'Prezzo di esercizio % del livello di riferimento iniziale', non è 'Prezzo della barriera per il rimborso anticipato inziale' e non è  'Prezzo della barriera della cedola'",
   )

    TipologiaBarriera: Required[str] = Field(
        description="Se nel nome del prodotto è presente 'Protected' allora metti 'None',"
                           "altrimenti se il livello di riferimento finale viene valutato su più date allora 'American',"
                           "altrimenti se il livello/prezzo di riferimento finale è valutato alla data di valutazione finale allora 'European'",
        enum= BARRIER_TYPE
    )

    Cedola: Required[str] = Field(
        description="Numero che rappresenta il coupon, la cedola pagata, condizionato a un livello/prezzo della cedola. Dammi questo valore solo se presente un livello o un prezzo della barriera per la cedola, altrimenti 'None'",
    )

    cedola_garantita: Required[str] = Field(
        description="Numero che rappresenta il coupon garantito. Dammi questo valore solo se i pagamenti della cedola non sono correlati alla performance del sottostante, altrimenti 'None'",
    )

    livello_barriera_cedola: Required[str] = Field(
        description="E' il numero corrispondente alla frase 'Livello della barriera della cedola % del livello di riferimento iniziale', non è 'Livello della barriera per il rimborso anticipato inziale' e non è  'Livello della barriera'"
    )

    effetto_memoria: Required[int] = Field(
        description="Se c'è la frase 'pagamento della cedola precedentemente maturato, ma tuttora non corrisposto' allora 1, altrimenti 0",
        enum = [0,1],
    )

    PagamentoMassimo: Required[str] = Field(
        description = "Pagamento massimo che il certificato può rimborsare all'estinzione del prodotto, si trova tra parentesi (il pagamento massimo)",
    )

    Sottostanti: Required[str] = Field(
        description = "Rappresenta il sottostante o i sottostanti dello strumento, possono essere azioni oridnarie o Indici. Il sottostante è quello strumento su cui si calcola la performance per determinare il rimborso del prodotto. Dammi Bloomberg Code",
    )

    Data_Emissione: Required[str] = Field(
        description = "Data di emissione del certificato, prima data di negoziazione dello strumento",
    )

    data_di_scadenza: Required[str] = Field(
        description = "Data di scadenza / termine, rappresenta la data a cui l'investitore riceverà il rimborso dello strumento",
    )

    estinzione_anticipata: Required[int] = Field(
        description = "Se c'è la frase 'rimborso anticipato' allora 1, altrimenti 0. Meccanismo di rimborso anticipato per cui il certificato viene rimborsato anticipatamente rispetto alla data di scadenza, in questo caso il sottostante peggiore è sopra alla barriera di rimborso anticipato",
        enum=[0, 1]
    )

    callable: Required[int] = Field(
        description =  "se l'emittente può richiamare a discrezione lo strumento allora 1 altrimenti 0, affinchè sia 1 ci deve essere scritto 'diritto ma non obbligo'",
        enum=[0, 1]
    )
    putable: Required[int] = Field(
        description =  "se l'investitore può richiamare il prodotto metti 1 altrimenti 0",
        enum=[0, 1]
    )


class PydanticSchema_unicredit(BaseModel):

    ISIN : Required[str] = Field(
        description="Codice ISIN formato da 12 caratteri, rappresenta l'identificativo dello strumento"
    )

    description : Required[str] = Field(
        description="Instrument description"
    )


    issuer : Required[str] = Field(
        description="Certificate's issuer, correspond to the issuer name",
        enum = ISSUER
    )

    specified_currency : Required[str] = Field(
        description="Currency of the product it can be EUR, USD, CHF, GBP",
        enum= CURRENCIES
    )

    listing : Required[str] = Field(
        description="Relevant exchange for th einstrument, it can be SeDeX, EuroTLX",
        enum=  QUOTATION_MARKETS
    )

    issue_price : Required[str] = Field(
        description="Product's nominal amount, it corresponds to the Issue price (Nominal Amount) and Nominal Amount (NA)"
    )

    floor_amount: Required[str] = Field(
        description="Floor level, it corresponds to Protection level, it is not the Barrier Level"
    )

    barrier_level: Required[str] = Field(
        description="Barrier Level used to calculate the Final redemption amount, if you not find put 'None'"
    )

    barrier_type: Required[str] = Field(
        description="If name 'Protected' then 'None',"
                           "if the final redemption amount is computed on multiple dates then 'Americana',"
                           "if the final redemption amount is computed on a single final valuation date then 'Europea'",
        enum= BARRIER_TYPE
    )

    conditional_premio: Required[str] = Field(
        description="Number expressing the Conditional Premio. Give me the number",
    )

    additional_unconditional_amount: Required[str] = Field(
        description="Number expressing the Additional Unconditional Amount. Give me the number only if present, otherwise 'None'",
    )

    barrier_premio: Required[str] = Field(
        description="Percentage number expressing the threshold above which the Additional Conditional Amount will be paid. Give me the percentage"
    )

    memory_effect: Required[int] = Field(
        description="Effect expressed by the phrase 'ess all Additional Conditional Amounts paid on the preceding Additional Amount Payment Dates',if there is 'Memory' then 1, else 0",
        enum = [0,1],
    )

    maximum_payment: Required[str] = Field(
        description = "Maximum Amount paid at the Redemtpion date",
    )

    underlying_bloomberg: Required[str] = Field(
        description = "Product's underlying, give me the Bloomberg Codes",
    )

    underlying_isin: Required[str] = Field(
        description = "Product's underlying, give me the ISIN",
    )

    issue_date: Required[str] = Field(
        description = "Certificate's issue date",
    )

    final_payment_date: Required[str] = Field(
        description = "Final Payment date, also described by Maturity date",
    )

    early_redemption: Required[int] = Field(
        description = "If there is 'Early Redemption Amount' or 'Early Redemption Level', then 1 else 0",
        enum=[0, 1]
    )

    callable: Required[int] = Field(
        description =  "In order to be 1 there must be 'right but nont obligation', else 0",
        enum=[0, 1]
    )
    putable: Required[int] = Field(
        description =  "If the investor has the right to early excercise the certificate 1, else 0",
        enum=[0, 1]
    )



class PydanticSchema_akros(BaseModel):

    ISIN : Required[str] = Field(
        description="Codice ISIN formato da 12 caratteri, rappresenta l'identificativo dello strumento"
    )

    nome_del_prodotto : Required[str] = Field(
        description="Descrizione dello strumento, corrisponde al Nome del prodotto"
    )


    Emittente : Required[str] = Field(
        description="Corrisponde all'emittente del certificato",
        enum = ISSUER
    )

    Valuta_di_emissione_e_regolamento : Required[str] = Field(
        description="Valuta del prodotto, può essere EUR, USD, CHF",
        enum= CURRENCIES
    )

    quotazione : Required[str] = Field(
        description="'Quotazione', mercato di quotazione dello strumento può essere EuroTLX, SeDeX, Frankfurt",
        enum=  QUOTATION_MARKETS
    )

    valore_nominale : Required[str] = Field(
        description="Valore Nominale del prodotto, corrisponde all'ammontare nominale del prodotto, può essere 1000, 500, 900, 2000"
    )

    protezione_e_livello_di_protezione: Required[str] = Field(
        description="Numero percentuale individuato dalla frase 'PROTEZIONE E LIVELLO DI PROTEZIONE'. Dammi il numero"
    )

    barriera_e_livello_barriera: Required[str] = Field(
        description="Numero percentuale individuato dalla frase 'BARRIERA E LIVELLO BARRIERA'. Dammi il numero"
    )

    TipologiaBarriera: Required[str] = Field(
        description="Se nel nome del prodotto è presente 'Protected' allora metti 'None',"
                           "altrimenti se il livello di riferimento finale viene valutato su più date allora 'Americana',"
                           "altrimenti se il livello/prezzo di riferimento finale è valutato alla data di valutazione finale allora 'Europea'",
        enum= BARRIER_TYPE
    )

    cedola_digitale_esima: Required[str] = Field(
        description="Numero percentuale che corrisponde alla frase 'CEDOLA DIGITALE i-esima'",
    )

    cedola_garantita: Required[str] = Field(
        description="Numero che rappresenta la cedola garantita. Dammi questo valore solo se i pagamenti della cedola non sono correlati alla performance del sottostante, altrimenti 'None'",
    )

    soglia_cedola_livello_soglia_cedola: Required[str] = Field(
        description="Numero percentuale che corrisponde alla frase 'SOGLIA CEDOLA E LIVELLO DI SOGLIA CEDOLA i-esimo'"
    )

    cedola_memoria: Required[int] = Field(
        description="Se c'è la frase 'CEDOLA MEMORIA' allora 1, altrimenti 0",
        enum = [0,1],
    )

    cap: Required[str] = Field(
        description = "Numero percentuale che corrisponde alla frase 'CAP E LIVELLO CAP'",
    )

    Sottostante: Required[str] = Field(
        description = "Rappresenta il sottostante o i sottostanti dello strumento, possono essere azioni oridnarie o Indici. Il sottostante è quello strumento su cui si calcola la performance per determinare il rimborso del prodotto. Dammi Bloomberg Code",
    )

    Data_Emissione: Required[str] = Field(
        description = "Data di emissione del certificato, prima data di negoziazione dello strumento",
    )

    data_di_scadenza: Required[str] = Field(
        description = "Data di scadenza / termine, rappresenta la data a cui l'investitore riceverà il rimborso dello strumento",
    )

    rimborso_anticipato: Required[int] = Field(
        description = "Se c'è la frase 'EVENTO DI RIMBORSO ANTICIPATO n-esimo' allora 1, altrimenti 0. Meccanismo di rimborso anticipato per cui il certificato viene rimborsato anticipatamente rispetto alla data di scadenza, in questo caso il sottostante peggiore è sopra alla barriera di rimborso anticipato",
        enum=[0, 1]
    )

    callable: Required[int] = Field(
        description =  "se l'emittente può richiamare a discrezione lo strumento allora 1 altrimenti 0, affinchè sia 1 ci deve essere scritto 'diritto ma non obbligo'",
        enum=[0, 1]
    )
    putable: Required[int] = Field(
        description =  "se l'investitore può richiamare il prodotto metti 1 altrimenti 0",
        enum=[0, 1]
    )

