from typing import List
#from langchain_core.pydantic_v1 import BaseModel, Field
from pydantic import BaseModel, Field

NF = "not found"
NA = "N/A"


class TabellaCedola(BaseModel):
    data_osservazione_cedola: List[str] = Field([NA], description="Data di Osservazione della Cedola")
    liv_attiv_cedola: List[str] = Field([NA], description="Coupon Trigger Level o Livello di Attivazione della Cedola")
    data_pagamento_cedola: List[str] = Field([NF], description="Data di Pagamento")
    importo_cedola: List[str] = Field([NF], description="Importo della Cedola")
    data_osservazione_autocall: List[str] = Field([NF], description="Data di Osservazione Autocall")
    liv_attiv_autocall: List[str] = Field([NF], description="Autocall Trigger Level o Livello di Attivazione Autocall")
    data_pagamento_autocall: List[str] = Field([NF], description="Data di Rimborso Anticipato")


class TabellaSottostanti(BaseModel):
    sottostante: List[str] = Field([NF], description="Sottostante")
    tipo: List[str] = Field([NF], description="tipo")
    borsa: List[str] = Field([NF], description="Borsa di Riferimento")
    bloom: List[str] = Field([NF], description="Bloomberg Ticker")
    isin: List[str] = Field([NF], description="ISIN")
    fixing_eur: List[str] = Field([NF], description="Livello di Fixing Iniziale, in EUR o USD")
    barriera_eur: List[str] = Field([NA], description="Livello Barriera, in EUR o USD")
    coupon_eur: List[str] = Field(
        [NA], description="Coupon Trigger Level o Livello di Attivazione della Cedola, in EUR o USD"
    )
    strike_level_perc: List[str] = Field([NA], description="Strike Level")
    coupon_eur: List[str] = Field([NA], description="Livello Cap")


class TabellaMainInfo(BaseModel):
    valuta: str = Field(NF, description="Valuta del prodotto")
    data_emissione: str = Field(NF, description="Data di Emissione")
    periodo: str = Field(NF, description="Ultimo Giorno/Periodo di Negoziazione")
    data_rimborso: str = Field(NF, description="Data di Rimborso")
    prezzo: str = Field(NF, description="Prezzo di Emissione")
    liv_fix_fin: str = Field(NA, description="Livello di Fixing Finale")
    quotazione: str = Field(NF, description="Quotazione di borsa")
    perf_peg: str = Field(NA, description="Performance Peggiore")
    inv_min: str = Field(NF, description="Lotto Minimo di Negoziazione/ Investimento minimo")
    garanzia_min_perc: str = Field(NA, description="Protezione del Capitale")
    data_fix_ini: str = Field(NF, description="Data del Fixing Iniziale")
    data_negoziazione: str = Field(NF, description="Prima Data di Negoziazione di Mercato")
    data_fix_fin: str = Field(NA, description="Data del Fixing Finale")
    liv_fix_ini: str = Field(NA, description="Livello di Fixing Iniziale")
    mod_pagamento: str = Field(NF, description="Modalità di Pagamento")
    tasso_cedola_cond: str = Field(NA, description="Tasso della Cedola Condizionale")
    cedola_garantita_perc: str = Field(NA, description="Cedola")
    rischio_cambio: str = Field(NA, description="Rischio di Cambio")
    importo_rimborso: str = Field(NA, description="Importo di Rimborso Massimo")
    importo_protezione_capitale: str = Field(NA, description="Importo di Protezione del Capitale")
    partecipazione: str = Field(NA, description="Partecipazione")


class InformazioniBaseCertificati(BaseModel):
    isin: str = Field(NF, description="codice ISIN")
    descrizione: str = Field(NF, description="descrizione completa del certificato")
    emittente: str = Field(NF, description="ideatore del certificato")


class TabellaSottostantiHeader(BaseModel):
    liv_fixing_iniziale: str = Field(NA, description="Livello di Fixing iniziale in percentuale")
    liv_att_cedola_perc: str = Field(NA, description="Coupon Trigger in percentuale")
    strike_level_perc: str = Field(NA, description="Strike Level in percentuale")
    livello_barriera: str = Field(NA, description="Livello Barriera, in percentuale")
    livello_cap: str = Field(NA, description="Livello Cap, in percentuale")


class CedolaStr(BaseModel):
    cedola: str = Field(NA, description="il testo")


class InformazioniBaseBNP(BaseModel):
    periodo_detenzione_raccomandato: str = Field("-", description="il periodo detenzione raccomandato")
    indicatore_sintetico_rischio: str = Field(NF, description="l'indicatore sintetico di rischio")


class TabellaSottostanteBNP(BaseModel):
    instrument_description: List[str] = Field([NF], description="Sottostante")
    instrument_bloombergcode: List[str] = Field([NF], description="codice Bloomberg")
    instrument_isin: List[str] = Field([NF], description="ISIN del sottostante")


class TabellaFirstInfoBNP(BaseModel):
    isin: str = Field(NF, description="codice ISIN")
    issuer_desc: str = Field(NF, description="emittente")


class TabellaAllegatoPremioBNP(BaseModel):
    observation_coupon_date: List[str] = Field([NF], description="Data/e di Valutazione del/i Premio/i Condizionato/i")
    payment_coupon_date: List[str] = Field([NF], description="Data/e di Pagamento del/i Premio/i")
    conditional_coupon_barrier: List[str] = Field([NF], description="Barriera/e o barrierale per il Versamento del Premio/i Condizionato/i")
    unconditional_coupon: List[str] = Field([NF], description="Premio/i")
    conditional_coupon: List[str] = Field([NF], description="Premio/i Condizionato/i")


class TabellaAllegatoScadenzaBNP(BaseModel):
    payment_callable_date: List[str] = Field([NF], description="Data di Liquidazione Anticipata Facoltativa")
    observation_autocall_date: List[str] = Field(
        [NF], description="Data/e di Valutazione dell’Importo di Liquidazione (rimborso) Anticipato"
    )
    barrier_autocall: List[str] = Field([NF], description="Barriera/e o barrierale per la Scadenza Anticipata")
    payment_autocall_date: List[str] = Field([NF], description="Data di Scadenza Anticipata")
    value_autocall: List[str] = Field([NF], description="Premio/I di Uscita")
    
    
class TabellaAllegatiBNP(BaseModel):
    observation_coupon_date: List[str] = Field([NF], description="Data/e di Valutazione del/i Premio/i Condizionato/i")
    payment_coupon_date: List[str] = Field([NF], description="Data/e di Pagamento del/i Premio/i")
    conditional_coupon_barrier: List[str] = Field([NF], description="Barriera/e o barrierale per il Versamento del Premio/i Condizionato/i")
    unconditional_coupon: List[str] = Field([NF], description="Premio/i")
    conditional_coupon: List[str] = Field([NF], description="Premio/i Condizionato/i")
    payment_callable_date: List[str] = Field([NF], description="Data di Liquidazione Anticipata Facoltativa")
    observation_autocall_date: List[str] = Field([NF], description="Data/e di Valutazione dell Importo di Liquidazione (rimborso) Anticipato"
    )
    barrier_autocall: List[str] = Field([NF], description="Barriera/e o barrierale per la Scadenza Anticipata")
    payment_autocall_date: List[str] = Field([NF], description="Data di Scadenza Anticipata")
    value_autocall: List[str] = Field([NF], description="Premio/I di Uscita")

class TabellaMainInfoBNP(BaseModel):
    currency: str = Field(NF, description="Valuta del prezzo di emissione / Valuta del prodotto")
    strike_date: str = Field(NF, description="Data di Strike")
    issue_date: str = Field(NF, description="Data di Emissione")
    expiry_date: str = Field(NF, description="Data di Liquidazione (rimborso)")
    final_valuation_date: str = Field(NF, description="Data di Valutazione dell'Importo di Liquidazione (rimborso)")
    nominal: str = Field(NF, description="Valore Nominale o Importo Nozionale")
    market: str = Field(NA, description="Mercato di Quotazione")
    barrier: str = Field(NF, description="Barriera")
    conditional_coupon_barrier: str = Field(NA, description="Barriera/e per il Versamento del Premio/i Condizionato/i")
    issue_price_perc: str = Field(NF, description="Prezzo di Emissione")
    observation_coupon_date: str = Field(NF, description="Data/e di Valutazione del/i Premio/i Condizionato/i")
    payment_coupon_date: str = Field(NF, description="Data/e di Pagamento del/i Premio/i")
    unconditional_coupon: str = Field(NF, description="Premio/i o premio certo")
    conditional_coupon: str = Field(NF, description="Premio/i Condizionato/i")
    payment_callable_date: str = Field(NF, description="Data di Liquidazione Anticipata Facoltativa")
    observation_autocall_date: str = Field(
        NF, description="tutte le Date di Valutazione dell' Importo di Liquidazione (rimborso) Anticipato"
    )
    """observation_autocall_date: List[str] = Field(
        [NF], description="Data/e di Valutazione dell' Importo di Liquidazione (rimborso) Anticipato"
    )"""
    #barrier_autocall: List[str] = Field([NF], description="Barriera/e per la Scadenza Anticipata")
    barrier_autocall: str = Field(NF, description="Barriera/e per la Scadenza Anticipata")
    #payment_autocall_date: List[str] = Field([NF], description="Data di Scadenza Anticipata")
    payment_autocall_date: str = Field(NF, description="tutte le Date in: Data di Scadenza Anticipata")
    value_autocall: str = Field(NF, description="Premio/I di Uscita")


class TabellaFirstInfoVontobel(BaseModel):
    isin: str = Field(NF, description="ISIN")
    description: str = Field(NF, description="Title or description")
    issuer_desc: str = Field(NF, description="Issuer")


class TabellaMainInfoVontobel(BaseModel):
    conditional_protection: str = Field(NF, description="Barrier")#
    currency: str = Field(NF, description="Settlement Currency")
    strike_date: str = Field(NF, description="Fixing Date")
    issue_date: str = Field(NF, description="Issue date")
    expiry_date: str = Field(NF, description="Maturity date")
    final_valuation_date: str = Field(NF, description="Final Valuation Date")
    nominal: str = Field(NF, description="Calculation amount or Nominal Amount")
    autocall_barrier: str = Field(NF, description="Redemption Level")
    conditional_coupon_barrier: List[str] = Field([NF], description="Bonus Threshold")
    memory: str = Field(NF, description="Memory")
    strike_level: List[str] = Field([NF], description="Strike")
    autocallable: str = Field(NF, description="Early Redemption")
    barrier_type: str = Field(NF, description="Barrier Event")
    observation_coupon_date: List[str] = Field([NF], description="Observation Date")
    payment_coupon_date: List[str] = Field([NF], description="Bonus Payment Date")
    unconditional_coupon: List[str] = Field([NF], description="Bonus Amount")
    conditional_coupon: List[str] = Field([NF], description="Bonus Amount")
    payment_callable_date: List[str] = Field([NF], description="put default value")
    observation_autocall_date: List[str] = Field([NF], description="Valuation Date ")
    autocall_barrier: List[str] = Field([NF], description="Redemption Level ")
    payment_autocall_date: List[str] = Field([NF], description="Early Redemption Date ")
    instrument_description: List[str] = Field([NF], description="Underlying title")
    instrument_isin: List[str] = Field([NF], description="ISIN Underlying")
    instrument_bloombergcode: List[str] = Field([NF], description="Bloomberg Symbol Underlying")
    


class TabellaDeductableVontobel(BaseModel):
    market: List[str] = Field([NF], description="Exchange Listing")
    issue_price_perc: List[str] = Field([NF], description="Issue Price")