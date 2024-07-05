"""
This file contains the tags used to extract the data from the KID and GKID documents.
"""

from typing import List

from pydantic import BaseModel, Field
#from pydantic.fields import Optional  # This is what creates the 1st error
from typing import Optional


# Your other imports and code


NF = "not found"
NA = "N/A"


#######
# KID #
#######
class InformazioniBase(BaseModel):
    indicatore_sintetico_rischio: int = Field(NF, description="Indicatore Sintetico di Rischio")
    periodo_detenzione_raccomandato: str = Field(NF, description="periodo di detenzione raccomandato in anni")
    date: str = Field(NF, description="data di realizzazione del documento")


companies = ["Anima", "Arca", "Eurizon", "Euromobiliare"]
class CompanyName(BaseModel):
    company_name: str = Field(NF, description="dal documento, estrarre il nome dell'azienda"
                              , enum = companies)



class TabellaScenariPerformance(BaseModel):
    stress_return: str = Field(NF, description="Rendimento percetuale(%) o '-' 1 anno scenario di stress")
    sfavorevole_return: str = Field(NF, description="Rendimento percentuale(%) o '-'  a 1 anno scenario sfavorevole ")
    moderato_return: str = Field(NF, description="Rendimento percentuale(%) o '-'  1 anno scenario moderato")
    favorable_return: str = Field(NF, description="Rendimento percentuale(%) o '-'  a 1 anno scenario favorevole")
    stress_return_rhp: str = Field(NF, description="Rendimento percetuale(%) a RHP anni scenario di stress")
    sfavorevole_return_rhp: str = Field(NF, description="Rendimento percentuale(%) a RHP anni scenario sfavorevole")
    moderato_return_rhp: str = Field(NF, description="Rendimento percentuale(%) a RHP anni scenario moderato")
    favorable_return_rhp: str = Field(NF, description="Rendimento percentuale(%) a RHP anni scenario favorevole")
    scenario_morte_1: str = Field(NF, description="scenario morte o decesso, Valore in euro(€) o '-'  a 1 anno scenario moderato")
    scenario_morte_rhp: str = Field(NF, description="scenario morte o decesso, Valore in euro(€) a RHP anni scenario moderato")

class ScenariPerformanceAbsoluteEuro(BaseModel):

    stress_amount: str = Field(NF, description="Ammontare in € o '-' 1 anno(prima colonna) scenario di stress")
    sfavorevole_amount: str = Field(NF, description="Ammontare in € o '-'  a 1 anno(prima colonna) scenario sfavorevole ")
    moderato_amount: str = Field(NF, description="Ammontare in € o '-'  1 anno(prima colonna) scenario moderato")
    favorable_amount: str = Field(NF, description="Ammontare in € o '-'  a 1 anno(prima colonna) scenario favorevole")
    stress_amount_rhp: str = Field(NF, description="Ammontare in € a RHP anni(ultima colonna) scenario di stress")
    sfavorevole_amount_rhp: str = Field(NF, description="Ammontare in € a RHP anni(ultima colonna) scenario sfavorevole")
    moderato_amount_rhp: str = Field(NF, description="Ammontare in € a RHP anni(ultima colonna) scenario moderato")
    favorable_amount_rhp: str = Field(NF, description="Ammontare in € a RHP anni(ultima colonna) scenario favorevole")


class ScenariPerformanceRHP2(BaseModel):

    stress_amount_x: str = Field(NF, description="Ammontare in € a X anni(ultima colonna) scenario di stress")
    sfavorevole_amount_x: str = Field(NF, description="Ammontare in € a X anni(ultima colonna) scenario sfavorevole")
    moderato_amount_x: str = Field(NF, description="Ammontare in € a X anni(ultima colonna) scenario moderato")
    favorable_amount_x: str = Field(NF, description="Ammontare in € a X anni(ultima colonna) scenario favorevole")
    stress_return_x: str = Field(NF, description="Rendimento percetuale(%) a X anni scenario di stress")
    sfavorevole_return_x: str = Field(NF, description="Rendimento percentuale(%) a X anni scenario sfavorevole")
    moderato_return_x: str = Field(NF, description="Rendimento percentuale(%) a X anni scenario moderato")
    favorable_return_x: str = Field(NF, description="Rendimento percentuale(%) a X anni scenario favorevole")
    scenario_morte_x: str = Field(NF, description="scenario morte o decesso, Valore in euro(€) a X anni scenario moderato")


class TabellaRiy(BaseModel):
    # 1 ANNO
    incidenza_costo_perc_1year: Optional[str] = Field(
        NF, description="Impatto sul rendimento annuale dei costi in caso di uscida dopo 1 anno in PERCENTUALE%"
    )
    costi_totali_eur_1year: Optional[str] = Field(
        NF, description="Costi totali dopo 1 anno in EURO €"
    )
    # RHP
    incidenza_costo_perc_rhp: str = Field(
        NF, description="Impatto sul rendimento annuale dei costi in caso di uscida dopo RHP anni in PERCENTUALE%"
    )
    costi_totali_eur_rhp: float = Field(
        NF, description="Costi totali dopo RHP anni in EURO €"
    )

class TabellaRiySmall(BaseModel):
    # 1 ANNO
    incidenza_costo_perc_1year: Optional[str] = Field(
        NF, description="Impatto sul rendimento annuale dei costi in caso di uscida dopo 1 anno in PERCENTUALE%"
    )
    # RHP
    incidenza_costo_perc_rhp: str = Field(
        NF, description="Impatto sul rendimento annuale dei costi in caso di uscida dopo RHP anni in PERCENTUALE%"
    )


class TabellaRiyRHP2(BaseModel):
    # 1 YEAR
    incidenza_costo_perc_1year: Optional[str] = Field(
        NF, description="Impatto sul rendimento annuale dei costi in caso di uscida dopo 1 anno in PERCENTUALE%"
    )
    costi_totali_eur_1year: Optional[str] = Field(
        NF, description="Costi totali dopo 1 anno in EURO €"
    )
    # RHP/2
    incidenza_costo_perc_xyear: str = Field(
        NF, description="Impatto sul rendimento annuale dei costi in caso di uscida dopo X anni in PERCENTUALE%"
    )
    costi_totali_eur_xyear: float = Field(
        NF, description="Costi totali dopo X anni in EURO €"
    )
    # RHP
    incidenza_costo_perc_rhp: str = Field(
        NF, description="Impatto sul rendimento annuale dei costi in caso di uscida dopo RHP anni in PERCENTUALE%"
    )

    costi_totali_eur_rhp: float = Field(
        NF, description="Costi totali dopo RHP anni in EURO €"
    )




class TabellaCostiIngresso(BaseModel):
    costi_ingresso: str = Field(
        NF, description="Costo una tantum di ingresso (nella colonna più a destra, può essere n/a)"
    )
    costingresso_dirittifissi: str =Field(
        NF, description="Diritti fissi d'ingresso valore massimo in Euro"
    )
    costi_uscita: str = Field(
        NF, description="Costo una tantum di uscita (nella colonna più a destra, può essere n/a)"
    )
    costiuscita_dirittifissi: str = Field(
        NF, description="Diritti fissi d'uscita valore massimo in Euro"

    )


class TabellaCostiGestione(BaseModel):
    commissione_gestione: str = Field(NF, description="Commissioni di gestione in PERCENTUALE % (colonna a destra)")
    commissione_transazione: str = Field(NF, description="Costi di transazione in PERCENTUALE % (colonna a destra)")
    commissione_performance: str = Field(
        NF, description="Commissioni di performance IN PERCENTUALE % (colonna a destra)"
    )

class TabellaCostiGestionepercentuale(BaseModel):
    commissione_gestione: str = Field(NF, description="Commissioni di gestione in PERCENTUALE % (prima colonna)")
    commissione_transazione: str = Field(NF, description="Costi di transazione in PERCENTUALE % (prima colonna)")
    commissione_performance: str = Field(
        NF, description="Commissioni di performance  (prima colonna)"
    )



########
# GKID #
########



### ENGLISH
class PerformanceScenarios(BaseModel):
    # 1 Year
    stress_return: str = Field(NF, description="1-year stress scenario percentage return")
    # stress_valore: str = Field(NF, description="1-year stress scenario monetary value")
    sfavorevole_return: str = Field(NF, description="Unfavorable scenario percentage return")
    # sfavorevole_valore: str = Field(NF, description="Unfavorable scenario 1-year monetary value")
    moderato_return: str = Field(NF, description="Moderate scenario percentage return")
    moderato_valore: str = Field(NF, description="Moderate scenario 1-year monetary value")
    favorable_return: str = Field(NF, description="Favorable scenario percentage return")
    # favorable_valore: str = Field(NF, description="Favorable scenario 1-year monetary value")

    # RHP (presumably referring to Risk-Adjusted Horizon Period)
    stress_return_rhp: str = Field(NF, description="RHP stress scenario percentage return")
    # stress_valore_rhp: str = Field(NF, description="RHP stress scenario monetary value")
    sfavorevole_return_rhp: str = Field(NF, description="RHP unfavorable scenario percentage return")
    # sfavorevole_valore_rhp: str = Field(NF, description="RHP unfavorable scenario monetary value")
    moderato_return_rhp: str = Field(NF, description="RHP moderate scenario percentage return")
    moderato_valore_rhp: str = Field(NF, description="RHP moderate scenario monetary value")
    favorable_return_rhp: str = Field(NF, description="RHP favorable scenario percentage return")
    favorable_valore_rhp: str = Field(NF, description="RHP favorable scenario monetary value")


class TableRiy(BaseModel):
    # 1 Year
    costo_1: str = Field(NF, description="Cost after 1 year")
    incidenza_costo_1: str = Field(NF, description="Cost incidence in percentage after 1 year")
    # RHP
    costo_thp: str = Field(NF, description="Cost after RHP years")
    incidenza_costo_rhp: str = Field(NF, description="Cost incidence in percentage after 1 year")
    costo_3: str = Field(NF, description="Cost after RHP years")



### ENGLISH
class PerformanceScenarios(BaseModel):
    # 1 Year
    stress_return: str = Field(NF, description="1-year stress scenario percentage return")
    # stress_valore: str = Field(NF, description="1-year stress scenario monetary value")
    sfavorevole_return: str = Field(NF, description="Unfavorable scenario percentage return")
    # sfavorevole_valore: str = Field(NF, description="Unfavorable scenario 1-year monetary value")
    moderato_return: str = Field(NF, description="Moderate scenario percentage return")
    moderato_valore: str = Field(NF, description="Moderate scenario 1-year monetary value")
    favorable_return: str = Field(NF, description="Favorable scenario percentage return")
    # favorable_valore: str = Field(NF, description="Favorable scenario 1-year monetary value")

    # RHP (presumably referring to Risk-Adjusted Horizon Period)
    stress_return_rhp: str = Field(NF, description="RHP stress scenario percentage return")
    # stress_valore_rhp: str = Field(NF, description="RHP stress scenario monetary value")
    sfavorevole_return_rhp: str = Field(NF, description="RHP unfavorable scenario percentage return")
    # sfavorevole_valore_rhp: str = Field(NF, description="RHP unfavorable scenario monetary value")
    moderato_return_rhp: str = Field(NF, description="RHP moderate scenario percentage return")
    moderato_valore_rhp: str = Field(NF, description="RHP moderate scenario monetary value")
    favorable_return_rhp: str = Field(NF, description="RHP favorable scenario percentage return")
    favorable_valore_rhp: str = Field(NF, description="RHP favorable scenario monetary value")


class TableRiy(BaseModel):
    # 1 Year
    costo_1: str = Field(NF, description="Cost after 1 year")
    incidenza_costo_1: str = Field(NF, description="Cost incidence in percentage after 1 year")
    # RHP
    costo_thp: str = Field(NF, description="Cost after RHP years")
    incidenza_costo_rhp: str = Field(NF, description="Cost incidence in percentage after 1 year")
    costo_3: str = Field(NF, description="Cost after RHP years")

    