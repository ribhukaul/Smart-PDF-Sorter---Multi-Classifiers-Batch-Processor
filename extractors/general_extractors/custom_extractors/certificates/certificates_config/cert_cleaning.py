header_mappings = {
    "Data.+realizzazion": "data_realizzazione_cedola",
    "Data.+osservazion.+cedol.+": "data_osservazione_cedola",
    "Data.+osservazion.+autocal.+": "data_osservazione_autocall",
    "Autocal.+Trigge": "autocall_trigger_lvl",
    "Data.+Pagament": "data_pagamento_cedola",
    "Import.+": "importo_cedola",
    "Giorno.+ monitor": "giorno_monitoraggio_rimborso",
    "data.+rimbors.+": "data_rimborso_cedola",
}


regex_callable = {
    "leonteq": {
        "autocall": "autocallable|rimbors.{1,5}anticipat",
        "callable": "softcallable|diritt.{1,4}non.{0,3}obblig",
        "memory": "effett.{1,5}memori",
        "putable": "putable",
    },
    "bnp": {
        "callable": r"Scadenza\s*Anticipata\s*Opzionale",
        "autocall": r"Scadenza\s*Anticipata\s*Automatica",
        "unconditional_protection": r"quest.\s*prodott.\s*offre\s*.{0,5}\s*protezione\s*totale\s*.{0,10}Importo\s*Nozionale\s*.{0,5}\s*scadenza",
        "memory": r"Tutt.\s*.{0,5}\s*Premi\s*Condizionat.\s*.{0,5}\s*versat.\s*.{0,5}\s*accumuleranno\s*.{0,5}\s*saranno\s*versat.\s*solo\s*.{0,5}\s*.{0,5}\s*Condizion.\s*del\s*Premio\s*Condizionato\s*verrà\s*soddisfatta\s*successivamente",
        "barrier_type": r"corrspondenz.\s*.{0,5}\s*data\s*.{0,5}\s*Valutazione\s*.{0,10}importo\s*.{0,5}\s*Liqidazione,\s*.{0,5}\s*prezzo\s*.{0,5}\s*Riferimento\s*Finale\s*.{0,5}\s*inferiroe\s*.{0,5}\s*barriera",
        "importo_minimo": r"tuttavia\s*.{0,5}importo\s*minimo\s*.{0,5}\s*pari\s*.{0,5}\s*\d{0,3}[,\.]?\d{1,2}\s?%\s*.{0,10}Importo\s*Nozionale",
        "leva_cedolare": r"(aumentato\s*.{0,5}\s*\d{0,3}[,\.]?\d{1,2}\s?%\s*.{0,5}\s*performance\s*.{0,5}\s*Sottostante\s*)|(più\s*.{0,5}\s*importo\s*commisurato\s*.{0,5}\s*\d{0,3}[,\.]?\d{1,2}\s?%\s*.{0,5}\s*Performance)",
        "cap": r"\s*Riferimento\s*Finale\s*.{0,25}\s*pari\s*.{0,5}\s*superiore\s*.{0,5}\s*.{5,20}\s*Prezzo\s*.{0,5}\s*Riferimento\s*Iniziale\s*.{0,20}\s*contant.{0,10}\d{0,3}[,\.]?\d{1,2}\s?%.{0,10}importo\s*nozional",
        "leva_airbag": r"meno\s*.{0,5}\s*importo\s*commisurato\s*.{0,10}\s*.{0,5}\s*Performance\s*.{0,5}\s*Sottostante",
    },
}
REGEX_PERC = r"\d{0,3}[,\.]?\d{1,3}\s?%"
check_for = {
    "leonteq": {},
    "bnp": {
        "importo_minimo": REGEX_PERC,
        "leva_cedolare": REGEX_PERC,
        "cap": REGEX_PERC,
        "leva_airbag": REGEX_PERC,
    },
}
