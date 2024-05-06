from typing import List
from pydantic import BaseModel, Field

NF = "not found"
NA = "N/A"

class InformazioniBaseBNP(BaseModel):
    periodo_detenzione_raccomandato: str = Field("-", description="il periodo detenzione raccomandato")
    indicatore_sintetico_rischio: int = Field(NF, description="l'indicatore sintetico di rischio")


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
    conditional_coupon_barrier: List[str] = Field(
        [NF], description="Barriera/e o barrierale per il Versamento del Premio/i Condizionato/i"
    )
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
    conditional_coupon_barrier: List[str] = Field(
        [NF], description="Barriera/e o barrierale per il Versamento del Premio/i Condizionato/i"
    )
    unconditional_coupon: List[str] = Field([NF], description="Premio/i")
    conditional_coupon: List[str] = Field([NF], description="Premio/i Condizionato/i")
    payment_callable_date: List[str] = Field([NF], description="Data di Liquidazione Anticipata Facoltativa")
    observation_autocall_date: List[str] = Field(
        [NF], description="Data/e di Valutazione dell’Importo di Liquidazione (rimborso) Anticipato"
    )
    barrier_autocall: List[str] = Field([NF], description="Barriera/e o barrierale per la Scadenza Anticipata")
    payment_autocall_date: List[str] = Field([NF], description="Data di Scadenza Anticipata")
    value_autocall: List[str] = Field([NF], description="Premio/I di Uscita")


class TabellaMainInfoBNP(BaseModel):
    currency: str = Field(NF, description="Valuta del nominal di emissione / Valuta del prodotto")
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
    # barrier_autocall: List[str] = Field([NF], description="Barriera/e per la Scadenza Anticipata")
    barrier_autocall: str = Field(NF, description="Barriera/e per la Scadenza Anticipata")
    # payment_autocall_date: List[str] = Field([NF], description="Data di Scadenza Anticipata")
    payment_autocall_date: str = Field(NF, description="tutte le Date in: Data di Scadenza Anticipata")
    value_autocall: str = Field(NF, description="Premio/I di Uscita")