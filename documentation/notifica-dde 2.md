# Notifica SNS con dati elaborati

Il messaggio di notifica SNS contiene le seguenti informazioni:

- `download_url`: L'URL S3 firmato del file tar gzippato contenente i risultati dei documenti elaborato. L'URL è firmato con una data di scadenza. L'URL è valido per 1 giorno dal momento in cui è stato generato. La data di scadenza è inclusa nel messaggio di notifica.
- `expiration_date`: La data di scadenza dell'URL S3. Formato ISO 8601.
- `file_format`: Il formato dei risultati del documento elaborato. (ad esempio, tar.gz)
- `success_keys`: Le chiavi S3 dei documenti elaborati con successo.
- `error_keys`: Le chiavi S3 dei documenti che non sono stati elaborati correttamente.

Il messaggio di notifica SNS viene inviato al topic SNS `dde-dev-notify-elaboration-topic`. Il topic ha un **filtro di sottoscrizione basato sul tenant** basato sulla proprietà del messaggio `tenant`.

> Esempio di messaggio di notifica SNS:
>
>```json
>{
>  "download_url": "https://s3.amazonaws.com/processed-documents/processed-documents-2021-10-01.tar.gz",
>  "expiration_date": "2021-10-08T00:00:00Z",
>  "file_format": "tar.gz",
>  "success_keys": [
>    "processed-document-1.json",
>    "processed-document-2.json"
>  ],
>  "error_keys": [
>    "error-document-3.json"
>  ],
>  "extractor_type": "kid",
>  "extractor_model": "gpt-4",
>  "tenant": "tenant"
>}
>```
>
>Esempio di attributi del messaggio SNS (la sezione degli attributi interessa il team cloud in fase di filtraggio della notifica alla subscription):
>
>```json
>{
>  "tenant": {
>    "Type": "String",
>    "Value": "tenant-1"
>  }
>}
>```
