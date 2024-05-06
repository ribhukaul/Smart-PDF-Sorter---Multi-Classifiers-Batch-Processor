from typing import List

from pydantic import BaseModel, Field

NF = "not found"
NA = "N/A"

# WAMINSURANCE


##################
# KID GOVERNANCE #
##################
class InformazioniBaseKidGov(BaseModel):
    indicatore_sintetico_rischio: int = Field(NF, description="Indicatore Sintetico di Rischio")
    periodo_detenzione_raccomandato: str = Field(NF, description="periodo di detenzione raccomandato in anni")
    date: str = Field(NF, description="data di realizzazione del documento")
    is_product_complex: bool = Field(False, description="è presente il disclaimer sui prodotti complessi?")

class IsDisclaimerThere(BaseModel):
    is_disclaimer_there: bool = Field(False, description="è presente il disclaimer 'State per acquistare un prodotto che non è semplice e può essere di difficile comprensione'")
    
##############
# KIDCREDEM #
##############
class TabellaScenariPerformanceCredem(BaseModel):
    moderato_return_rhp: str = Field(NF, description="Rendimento percentuale(%) a RHP anni scenario moderato")
    favorable_return_rhp: str = Field(NF, description="Rendimento percentuale(%) a RHP anni scenario favorevole")

