# DDE - ESPORTAZIONE DATI

Al momento l'applicativo DDE prevede due formati di esportazione dati: JSON e EXCEL.

Il formato JSON è il formato nativo dell'engine LLM, quindi tutte le estrazioni effettuate dall'engine LLM saranno in formato JSON. I dati in formato JSON vengono esposti solo tramite notifica su topic AWS SNS e non sono direttamente consultabili dall'utente.

L'application DDE prevede la possibilità di esportare i dati in formato excel, per permettere una più facile consultazione e analisi dei dati. La funzionalità di esportazione in formato excel è disponibile per tutte le estrazioni effettuate dall'engine LLM e può essere attivata dall'utente tramite l'interfaccia grafica.

L'esportazione dei dati da un estrazione fatta sull' applicativo potrà essere fatta in delta così da poter permettere il passaggio di una sola parte di dati estratti o modificati da un analista in piattaforma.

## JSON

### Struttura del file JSON

Il formato JSON prevede 5 sezioni principali:

- sections
  - elenco delle sezioni presenti nel documento
    - name: nome della sezione
    - list: elenco dei campi presenti nella sezione
- extraction
  - elenco dei campi estratti dal documento
    - name: nome del campo
    - value: valore del campo
    - metric: unità di misura del campo (suffisso)
    - data_type: tipo di dato del campo
      - DATE (formato yyyy-mm-dd)
      - INTEGER
      - FLOAT (separatore: .)
      - STRING
      - BOOLEAN
    - range: range di valori del campo
      - DATE: range di date

        ```json
        "range": ["2022-01-01", "2022-12-31"]
        ```

      - INTEGER, FLOAT: range di valori

        ```json
        "range": [1.00, 100.00]
        ```

      - STRING: dominio di valori

        ```json
        "range": ["val1", "val2", "val3"]
        ```
    - is_error: boolean che indica se c'è stato un errore in fase di estrazione
    - coord: coordinate del campo (TBD)
    - decimals: numero di decimali del campo
    - allownull: se il campo può essere nullo
- extraction_cost
  - total: costo totale dell'estrazione
    - tokens: numero di token estratti
    - cost: costo totale dell'estrazione
  - currency: valuta del costo totale
  - breakdown del costo per modello/servizio
- extraction_time -> formato "mm:ss
- file_path

### Esempio

```json
{
    "file_path": "kid\\documents\\testdoc\\RIV\\202212_CNP Cross Life.pdf",
    "extraction_time": "0:34", 
    "extraction_cost": {
      "total": {
        "tokens": 10168,
        "cost": 0.19
      },
      "currency": "EUR",
      "models": {
            "gpt-4-turbo": {
                "tokens": 3945,
                "cost": 0.11
            },
            "gpt-3.5-turbo-16k": {
                "tokens": 5311,
                "cost": 0.02
            },
            "azure": {
                "pages": 2,
                "cost": 0.02
            }
        }
    },
    "sections": {
      "section0": {
        "name": "Informazioni di base",
        "list": [
          "cod_data",
          "cod_isin",
          "cod_rhp"
        ]
      },
      "section1": {
        "name": "Performance",
        "list": [
          "cod_rsfav_1y",
          "cod_rsfav_rhp",
          "cod_sri",
          "cod_rsmod_1y",
          "cod_rsmod_rhp",
          "cod_smor_1y",
          "cod_smor_rhp",
          "cod_rssfav_1y",
          "cod_rssfav_rhp",
          "cod_rsstr_1y",
          "cod_rsstr_rhp"
        ]
      },
      "section2": {
        "name": "Reduction In Yield",
        "list": [
          "cod_riy_1y",
          "cod_riy_rhp"
        ]
      },
      "section3": {
        "name": "Costi e Commissioni",
        "list": [
          "cod_costi_ingresso",
          "cod_costi_uscita",
          "cod_commissioni_di_gestione",
          "cod_costi_di_transazione",
          "cod_commissioni_di_performance"
        ]
      },
      "section4": {
        "name": "Target Market",
        "list": [
          "cod_target_market"
        ]
      }
    },
    "extraction": {
      "cod_data": {
        "name": "Data",
        "value": "19/12/2022",
        "metric": "N/A",
        "data_type": "Date",
        "range": {
        },
        "is_error": "false",
        "is_error": "false",
        "coord": {},
        "decimals": "N/A",
        "allownull": "false",
      },
      "cod_isin": {
        "name": "ISIN",
        "value": "-",
        "metric": "caps",
        "data_type": "String",
        "range": {
        },
        "is_error": "false",
        "coord": {},
        "decimals": "N/A",
        "allownull": "false",
      },
      "cod_rhp": {
        "name": "RHP (anni)",
        "value": "5",
        "metric": "anni",
        "data_type": "Integer",
        "range": {
          "min": 1,
          "max": 50
        },
        "coord": {},
        "decimals": "N/A",
        "allownull": "false",
      },
      "cod_rsfav_1y": {
        "name": "RSFAV 1Y %",
        "value": "0,05%",
        "metric": "%",
        "data_type": "Float",
        "range": {
        },
        "is_error": "false",
        "coord": {},
        "decimals": 2,
        "allownull": "false",
      },
      "cod_rsfav_rhp": {
        "name": "RSFAV RHP %",
        "value": "2,44%",
        "metric": "%",
        "data_type": "Float",
        "range": {
        },
        "is_error": "false",
        "coord": {},
        "decimals": 2,
        "allownull": "false",
      },
      "cod_sri": {
        "name": "SRI",
        "value": "1",
        "metric": "anni",
        "data_type": "Integer",
        "range": {
          "min": 1,
          "max": 7
        },
        "coord": {},
        "decimals": "N/A",
        "allownull": "false",
      },
      "cod_rsmod_1y": {
        "name": "RSMOD 1Y %",
        "value": "-0,16%",
        "metric": "%",
        "data_type": "Float",
        "range": {
        },
        "is_error": "false",
        "coord": {},
        "decimals": 2,
        "allownull": "false",
      },
      "cod_rsmod_rhp": {
        "name": "RSMOD RHP %",
        "value": "1,93%",
        "metric": "%",
        "data_type": "Float",
        "range": {
        },
        "is_error": "false",
        "coord": {},
        "decimals": 2,
        "allownull": "false",
      },
      "cod_smor_1y": {
        "name": "SMOR 1Y (€)",
        "value": " 10.240€",
        "metric": "€",
        "data_type": "Float",
        "range": "N/A",
        "coord": {},
        "decimals": 2,
        "allownull": "false",
      },
      "cod_smor_rhp": {
        "name": "SMOR RHP (€)",
        "value": " 11.000€",
        "metric": "€",
        "data_type": "Float",
        "range":{},
        "coord": {},
        "decimals": 2,
        "allownull": "false",
      },
      "cod_rssfav_1y": {
        "name": "RSSFAV 1Y %",
        "value": "-0,23%",
        "metric": "%",
        "data_type": "Float",
        "range": {
        },
        "is_error": "false",
        "coord": {},
        "decimals": 2,
        "allownull": "false",
      },
      "cod_rssfav_rhp": {
        "name": "RSSFAV RHP %",
        "value": "1,51%",
        "metric": ",%",
        "data_type": "Float",
        "range": {
        },
        "is_error": "false",
        "coord": {},
        "decimals": 2,
        "allownull": "false",
      },
      "cod_rsstr_1y": {
        "name": "RSSTR 1Y %",
        "value": "-2,64%",
        "metric": "%",
        "data_type": "Float",
        "range": {
        },
        "is_error": "false",
        "coord": {},
        "decimals": 2,
        "allownull": "false",
      },
      "cod_rsstr_rhp": {
        "name": "RSSTR RHP %",
        "value": "-0,06%",
        "metric": "%",
        "data_type": "Float",
        "range": {
        },
        "is_error": "false",
        "coord": {},
        "decimals": 2,
        "allownull": "false",
      },
      "cod_riy_1y": {
        "name": "RIY 1Y %",
        "value": "3,4%",
        "metric": "%",
        "data_type": "Float",
        "range": {
        },
        "is_error": "false",
        "coord": {},
        "decimals": 2,
        "allownull": "true",
      },
      "cod_riy_rhp": {
        "name": "RIY RHP %",
        "value": "1,9%",
        "metric": "%",
        "data_type": "Float",
        "range": {
        },
        "is_error": "false",
        "coord": {},
        "decimals": 2,
        "allownull": "false",
      },
      "cod_costi_ingresso": {
        "name": "Costi ingresso",
        "value": "0,1%",
        "metric": "%",
        "data_type": "Float",
        "range": {
        },
        "is_error": "false"
        "coord": {},
        "decimals": 2,
        "allownull": "true",
      },
      "cod_costi_uscita": {
        "name": "Costi uscita",
        "value": "-",
        "metric": "%",
        "data_type": "Float",
        "range": {
        },
        "is_error": "false",
        "coord": {},
        "decimals": 2,
        "allownull": "true",
      },
      "cod_commissioni_di_gestione": {
        "name": "Commissioni di gestione",
        "value": "1,4%",
        "metric": "%",
        "data_type": "Float",
        "range": {
        },
        "is_error": "false",
        "coord": {},
        "decimals": 2,
        "allownull": "false",
      },
      "cod_costi_di_transazione": {
        "name": "Costi di transazione",
        "value": "-",
        "metric": "%",
        "data_type": "Float",
        "range": {
        },
        "is_error": "false",
        "coord": {},
        "decimals": 2,
        "allownull": "false",
      },
      "cod_commissioni_di_performance": {
        "name": "Commissioni di performance",
        "value": "-",
        "metric": "%",
        "data_type": "Float",
        "range": {
        },
        "is_error": "false",
        "coord": {},
        "decimals": 2,
        "allownull": "true",
      },
      "cod_target_market": {
        "name": "Target Market",
        "value": "Investitori al dettaglio ai quali si intende commercializzare il prodotto : il prodotto risponde a esigenze di investimento ed è rivolto ai clienti con conoscenze e/o esperienze di base del mercato assicurativo e finanziario, che intendono investire nel medio periodo, con una bassa tolleranza al rischio finanziario, con l’obiettivo di conservare il capitale investito in predeterminate ricorrenze e in caso di decesso, consapevoli della possibilità di incorrere in contenute perdite finanziare dovute anche all’assenza di consolidamento delle prestazioni.",
        "metric": "N/A",
        "data_type": "String",
        "range": {
        },
        "is_error": "false",
        "coord": {},
        "decimals": "N/A",
        "allownull": "false",
      }
    }
  }
```

## EXCEL

### Struttura del file excel

L'esportazione excel prevede la creazione di un file excel contenente i dati recuperati dall'estrattore llm.
Il nome del file avrà la seguente struttura: `{workspace_name}_{extraction_name}.xlsx`
Il file presenterà una riga per ogni file dell'estrazione llm e le colonne corrisponderanno ai valori recuperati per i relativi campi. Nel caso in cui un campo non dovesse essere disponibile per un deteminato file, la cella sarà vuota.

Segue il dominio delle colonne del file excel, con le seguenti informazioni:

- intestazione-colonna: chiave del campo
- descrizione: descrizione del campo
- data_type: tipo di dato del campo
  - INTEGER
  - FLOAT (separatore: .)
  - DATE (formato: yyyy-mm-dd)
  - STRING
  - BOOLEAN

| nome-colonna | descrizione | data_type
| --- | --- | --- |
| document_id | id del file | STRING |
| cod_data | data | DATE |
| cod_isin | ISIN | STRING |
| cod_rhp | RHP (anni) | INTEGER |
| cod_rsfav_1y | RSFAV 1Y % | FLOAT |
| cod_rsfav_rhp | RSFAV RHP % | FLOAT |
| cod_sri | SRI | INTEGER |
| cod_rsmod_1y | RSMOD 1Y % | FLOAT |
| cod_rsmod_rhp | RSMOD RHP % | FLOAT |
| cod_smor_1y | SMOR 1Y (€) | FLOAT |
| cod_smor_rhp | SMOR RHP (€) | FLOAT |
| cod_rssfav_1y | RSSFAV 1Y % | FLOAT |
| cod_rssfav_rhp | RSSFAV RHP % | FLOAT |
| cod_rsstr_1y | RSSTR 1Y % | FLOAT |
| cod_rsstr_rhp | RSSTR RHP % | FLOAT |
| cod_riy_1y | RIY 1Y % | FLOAT |
| cod_riy_rhp | RIY RHP % | FLOAT |
| cod_costi_ingresso | Costi ingresso | FLOAT |
| cod_costi_uscita | Costi uscita | FLOAT |
| cod_commissioni_di_gestione | Commissioni di gestione | FLOAT
| cod_costi_di_transazione | Costi di transazione | FLOAT |
| cod_commissioni_di_performance | Commissioni di performance | FLOAT |
| cod_target_market | Target Market | STRING |

### Esempio di file excel
in allegato workspace1_estrazione1.xlsx