"""
This file contains the tags used to extract the data from the KID and GKID documents.
"""

from typing import List

from pydantic import BaseModel, Field

NF = "not found"
NA = "N/A"


#######
# KID #
#######
class InformazioniBase(BaseModel):
    indicatore_sintetico_rischio: int = Field(NF, description="Indicatore Sintetico di Rischio")
    periodo_detenzione_raccomandato: str = Field(NF, description="periodo di detenzione raccomandato in anni")
    date: str = Field(NF, description="data di realizzazione del documento")


class TabellaScenariPerformance(BaseModel):
    stress_return: str = Field(NF, description="Rendimento percetuale(%) o '-' 1 anno scenario di stress")
    sfavorevole_return: str = Field(NF, description="Rendimento percentuale(%) o '-'  a 1 anno scenario sfavorevole ")
    moderato_return: str = Field(NF, description="Rendimento percentuale(%) o '-'  1 anno scenario moderato")
    favorable_return: str = Field(NF, description="Rendimento percentuale(%) o '-'  a 1 anno scenario favorevole")
    stress_return_rhp: str = Field(NF, description="Rendimento percetuale(%) a RHP anni scenario di stress")
    sfavorevole_return_rhp: str = Field(NF, description="Rendimento percentuale(%) a RHP anni scenario sfavorevole")
    moderato_return_rhp: str = Field(NF, description="Rendimento percentuale(%) a RHP anni scenario moderato")
    favorable_return_rhp: str = Field(NF, description="Rendimento percentuale(%) a RHP anni scenario favorevole")
    scenario_morte_1: str = Field(NF, description="Valore in euro(€) o '-'  a 1 anno scenario moderato")
    scenario_morte_rhp: str = Field(NF, description="Valore in euro(€) a RHP anni scenario moderato")

class TabellaScenariPerformanceCredem(BaseModel):
    moderato_return_rhp: str = Field(NF, description="Rendimento percentuale(%) a RHP anni scenario moderato")
    favorable_return_rhp: str = Field(NF, description="Rendimento percentuale(%) a RHP anni scenario favorevole")

class TabellaRiy(BaseModel):
    # 1 ANNO
    incidenza_costo_1: str = Field(
        NF, description="Impatto sul rendimento annuale dei costi in caso di uscida dopo 1 anno in PERCENTUALE%"
    )
    # RHP
    incidenza_costo_rhp: str = Field(
        NF, description="Impatto sul rendimento annuale dei costi in caso di uscida dopo RHP anni in PERCENTUALE%"
    )


class TabellaCostiIngresso(BaseModel):
    costi_ingresso: str = Field(
        NF, description="Costi di ingresso in PERCENTUALE %(nella colonna più a destra, può essere n/a)"
    )
    costi_uscita: str = Field(
        NF, description="Costi di uscita in PERCENTUALE %(nella colonna più a destra, può essere n/a)"
    )


class TabellaCostiGestione(BaseModel):
    commissione_gestione: str = Field(NF, description="Commissioni di gestione in PERCENTUALE % (colonna di destra)")
    commissione_transazione: str = Field(NF, description="Costi di transazione in PERCENTUALE % (colonna di destra)")
    commissione_performance: str = Field(
        NF, description="Commissioni di performance IN PERCENTUALE % (colonna a destra)"
    )


########
# GKID #
########
class InformazioniBaseGkid(BaseModel):
    indicatore_sintetico_rischio_min: str = Field(
        NF, description="Indicatore Sintetico di Rischio nel caso minimo o peggiore,(da:)(il primo)"
    )
    indicatore_sintetico_rischio_max: str = Field(
        NF, description="Indicatore Sintetico di Rischio nel caso massimo o migliore,(a:)(il secondo)"
    )
    periodo_detenzione_raccomandato: List[int] = Field(
        [],
        description="il periodo di detenzione massimo raccomandato in anni,ritorna solo un valore, quello maggiore di quelli dati",
    )
    date: str = Field(NF, description="data di realizzazione del documento")


class TabellaScenariPerformanceGkid(BaseModel):
    stress_return: str = Field(NF, description="Rendimento percetuale(%) o '-' 1 anno scenario di stress")
    sfavorevole_return: str = Field(NF, description="Rendimento percentuale(%) o '-'  a 1 anno scenario sfavorevole ")
    moderato_return: str = Field(NF, description="Rendimento percentuale(%) o '-'  1 anno scenario moderato")
    favorable_return: str = Field(NF, description="Rendimento percentuale(%) o '-'  a 1 anno scenario favorevole")
    stress_return_rhp: str = Field(NF, description="Rendimento percetuale(%) a RHP anni scenario di stress")
    sfavorevole_return_rhp: str = Field(NF, description="Rendimento percentuale(%) a RHP anni scenario sfavorevole")
    moderato_return_rhp: str = Field(NF, description="Rendimento percentuale(%) a RHP anni scenario moderato")
    favorable_return_rhp: str = Field(NF, description="Rendimento percentuale(%) a RHP anni scenario favorevole")
    scenario_morte_1: str = Field(NF, description="Valore in euro(€) o '-'  a 1 anno scenario moderato")
    scenario_morte_rhp: str = Field(NF, description="Valore in euro(€) a RHP anni scenario moderato")


class TabellaRiyPercGkid(
    BaseModel
):  # incidenza 2 comes later because of the way the data is structured, we prioritize the 1 year and rhp data
    incidenza_costo_perc: List[float] = Field(
        NF,
        description="Incidenza annuale dei costi dopo un anno,se esiste dopo RHMEZZI anni, e dopo RHP anni in PERCENTUALE% non fare calcoli, ritorna i valori presenti nel documento",
    )
    # 1 ANNO
    incidenza_costo_perc_1_min: str = Field(
        NF,
        description="Incidenza annuale dei costi in caso di uscita dopo 1 anno in PERCENTUALE% nel caso minimo o peggiore,(da:) situato a sinistra (colonna più a sinistra), non fare calcoli, ritorna il valore presente nel documento",
    )
    incidenza_costo_perc_1_max: str = Field(
        NF,
        description="Incidenza annuale dei costi in caso di uscita dopo 1 anno in PERCENTUALE% nel caso massimo o migliore,(a:) situato a destra(colonna più a sinistra), non fare calcoli, ritorna il valore presente nel documento",
    )
    # RHP
    incidenza_costo_perc_rhp_min: str = Field(
        NF,
        description="Incidenza annuale dei costi in caso di uscita dopo RHP anni in PERCENTUALE% nel caso minimo o peggiore,(da:) situato a sinistra(colonna più a destra), non fare calcoli, ritorna il valore presente nel documento",
    )
    incidenza_costo_perc_rhp_max: str = Field(
        NF,
        description="Incidenza annuale dei costi in caso di uscita dopo RHP anni in PERCENTUALE% nel caso massimo o migliore,(a:) situato a destra(colonna più a destra), non fare calcoli, ritorna il valore presente nel documento",
    )
    # MEZZI
    incidenza_costo_perc_2_min: str = Field(
        NA,
        description="Incidenza annuale dei costi in caso di uscita dopo RHMEZZI(o circa) anni in PERCENTUALE% nel caso minimo o peggiore,(da:) situato a sinistra (colonna centrale se esiste), non fare calcoli, ritorna il valore presente nel documento",
    )
    incidenza_costo_perc_2_max: str = Field(
        NA,
        description="Incidenza annuale dei costi in caso di uscita dopo RHMEZZI anni in PERCENTUALE% nel caso massimo o migliore,(a:) situato a destra (colonna centrale se esiste), non fare calcoli, ritorna il valore presente nel documento",
    )


class TabellaRiyEurGkid(BaseModel):
    # 1 ANNO
    incidenza_costo_eur_1_min: str = Field(
        NF,
        description="Costi totali in caso di uscita dopo 1 anno in EURO€ nel caso minimo o peggiore,(da:) situato a sinistra (colonna più a sinistra), non fare calcoli, ritorna il valore presente nel documento",
    )
    incidenza_costo_eur_1_max: str = Field(
        NF,
        description="Costi totali in caso di uscita dopo 1 anno in EURO€ nel caso massimo o migliore,(a:) situato a destra(colonna più a sinistra), non fare calcoli, ritorna il valore presente nel documento",
    )
    # RHP
    incidenza_costo_eur_rhp_min: str = Field(
        NF,
        description="Costi totali in caso di uscita dopo RHP anni in EURO€ nel caso minimo o peggiore,(da:) situato a sinistra(colonna più a destra), non fare calcoli, ritorna il valore presente nel documento",
    )
    incidenza_costo_eur_rhp_max: str = Field(
        NF,
        description="Costi totali in caso di uscita dopo RHP anni in EURO€ nel caso massimo o migliore,(a:) situato a destra(colonna più a destra), non fare calcoli, ritorna il valore presente nel documento",
    )
    # MEZZI
    incidenza_costo_eur_2_min: str = Field(
        NA,
        description="Costi totali in caso di uscita dopo RHMEZZI anni in EURO€ nel caso minimo o peggiore,(da:) situato a sinistra (colonna centrale se esiste), non fare calcoli, ritorna il valore presente nel documento",
    )
    incidenza_costo_eur_2_max: str = Field(
        NA,
        description="Costi totali in caso di uscita dopo RHMEZZI anni in EURO€ nel caso massimo o migliore,(a:) situato a destra (colonna centrale se esiste), non fare calcoli, ritorna il valore presente nel documento",
    )


class TabellaCostiIngressoGkid(BaseModel):
    costi_ingresso_min: str = Field(
        NF,
        description="Costi di ingresso in PERCENTUALE % nel caso minimo o peggiore,(da:)(nella colonna più a destra, può essere n/a)",
    )
    costi_ingresso_max: str = Field(
        NF,
        description="Costi di ingresso in PERCENTUALE % nel caso massimo o migliore,(a:) (nella colonna più a destra, può essere n/a)",
    )
    costi_uscita_min: str = Field(
        NF,
        description="Costi di uscita in PERCENTUALE % nel caso minimo o peggiore,(da:)(nella colonna più a destra, può essere n/a)",
    )
    costi_uscita_max: str = Field(
        NF,
        description="Costi di uscita in PERCENTUALE % nel caso massimo o migliore, (a:)(nella colonna più a destra, può essere n/a)",
    )


class TabellaCostiGestioneGkid(BaseModel):
    commissione_gestione_min: str = Field(
        NF, description="Commissioni di gestione in PERCENTUALE % nel caso minimo o peggiore,(da:) (colonna di destra)"
    )
    commissione_gestione_max: str = Field(
        NF, description="Commissioni di gestione in PERCENTUALE % nel caso massimo o migliore,(a:) (colonna di destra)"
    )
    commissione_transazione_min: str = Field(
        NF, description="Costi di transazione in PERCENTUALE % nel caso minimo o peggiore,(da:) (colonna di destra)"
    )
    commissione_transazione_max: str = Field(
        NF, description="Costi di transazione in PERCENTUALE % nel caso massimo o migliore,(a:) (colonna di destra)"
    )
    commissione_performance_min: str = Field(
        NF,
        description="Commissioni di performance IN PERCENTUALE % nel caso minimo o peggiore,(da:) (colonna a destra)",
    )
    commissione_performance_max: str = Field(
        NF,
        description="Commissioni di performance IN PERCENTUALE % nel caso massimo o migliore,(a:) (colonna a destra)",
    )


class ScenariPercentage(BaseModel):
    # 1 ANNO
    stress_return: str = Field(NF, description="Rendimento percetuale 1 anno scenario di stress(può essere vuoto)")
    sfavorevole_return: str = Field(
        NF, description="Rendimento percentuale a 1 anno scenario sfavorevole (può essere vuoto)"
    )
    moderato_valore: str = Field(
        NF, description="Valore monetario in euro(€) a 1 anno scenario moderato (può essere vuoto)"
    )
    favorable_return: str = Field(
        NF, description="Rendimento percentuale(%) a 1 anno scenario favorevole( può essere vuoto)"
    )
    # RHP
    stress_return_rhp: str = Field(NF, description="Rendimento percetuale(%) a RHP anni scenario di stress")
    sfavorevole_return_rhp: str = Field(NF, description="Rendimento percentuale(%) a RHP anni scenario sfavorevole")
    moderato_return_rhp: str = Field(NF, description="Rendimento percentuale(%) a RHP anni scenario moderato")
    moderato_valore_rhp: str = Field(NF, description="Valore in euro(€) a RHP anni scenario moderato")
    favorable_return_rhp: str = Field(NF, description="Rendimento percentuale(%) a RHP anni scenario favorevole")


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
