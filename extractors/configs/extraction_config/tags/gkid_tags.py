from typing import List
from pydantic import BaseModel, Field

NF = "not found"
NA = "N/A"


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

