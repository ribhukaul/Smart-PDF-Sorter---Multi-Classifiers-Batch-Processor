import pandas as pd
import datetime


def df_dataintegration(df_old):
# Crea un nuovo DataFrame basato sulle logiche specificate
    df_new = pd.DataFrame()

    df_new['Isin'] = df_old['Isin']
    df_new['Descrizione'] = df_old['Descrizione']
    df_new['TipoTitolo'] = 'CT'

    def map_emittente(row):
        if row['Emittente'] == 'Unicredit Bank':
            return 'Unicredit Bank - AG', 10299
        elif row['Emittente'] == 'Unicredit SPA':
            return 'UniCredit - SPA', 10283
        else:
            return None, None

    df_new['Emittente'], df_new['IdEmittente'] = zip(*df_old.apply(map_emittente, axis=1))
    df_new['Divisa'] = df_old['Divisa']
    df_new['Mercato'] = df_old['Mercato']
    df_new['Quotato'] = df_old['Mercato'].apply(lambda x: 1 if x != 'NON QUOTATO' else 0)
    df_new['ValoreNominale'] = df_old['ValoreNominale']

    def calculate_garanzia(row):
        if row['GaranziaMinimaPerc'] is not None and row['GaranziaMinimaPerc'] != 'Not specified in the document' and row['GaranziaMinimaPerc'] != 'None':
            return row['GaranziaMinimaPerc']
        elif row['Protezione'] is not None and row['Protezione'] != 'Not specified in the document' and row['Protezione'] != 'None':
            return row['Protezione']
        else:
            return 0

    df_new['GaranziaMinimaPerc'] = df_old.apply(calculate_garanzia, axis=1)
    df_new['Garantito'] = 0

    def calculate_protezione_condizionata(row):
        if row['GaranziaMinimaPerc'] == 0:
            return 100
        else:
            return 0

    df_new['ProtezioneCondizionataPerc'] = df_new.apply(calculate_protezione_condizionata, axis=1)

    df_new['BarrieraProtezionePerc'] = df_old['BarrieraProtezionePerc'].apply(lambda x: x if x is not None and x != 'Not specified in the document' and x != 'None' else df_old['PrezzoEsercizio'].values[0] if df_old['PrezzoEsercizio'].values[0] is not None else None)
    df_new['TipoBarrieraProtezione'] = df_old['TipoBarrieraProtezione']
    df_new['LevaCapitale'] = 0
    df_new['LevaPercCapitale'] = None
    df_new['LevaCedolare'] = 0
    df_new['LevaPercCedolare'] = None

    def calculate_cedola_garantita(row):
        if row['CedolaGarantitaPerc'] is not None and row['CedolaGarantitaPerc'] != 'Not specified in the document' and row['CedolaGarantitaPerc'] != 'None':
            return row['CedolaGarantitaPerc']
        else:
            return 0

    df_new['CedolaGarantitaPerc'] = df_old.apply(calculate_cedola_garantita, axis=1)

    def calculate_cedola_condizionata(row):
        if row['Cedola'] is not None and row['Cedola'] != 'Not specified in the document' and row['Cedola'] != 'None':
            return row['Cedola']
        elif row['Cedola_Autocall'] is not None and row['Cedola_Autocall'] != 'Not specified in the document':
            return row['Cedola_Autocall']
        else:
            return 0

    df_new['CedolaCondizionataPerc'] = df_old.apply(calculate_cedola_condizionata, axis=1)
    df_new['BarrieraCedolaCondizionataPerc'] = df_old['BarrieraCedolaCondizionataPerc'].apply(lambda x: x if x is not None and x != 'Not specified in the document' and x != 'None' else df_old['PrezzoEsercizio'].values[0] if df_old['PrezzoEsercizio'].values[0] is not None else None)
    df_new['MemoryCoupon'] = df_old['MemoryCoupon']
    df_new['CedolaCapPerc'] = df_old['CedolaCapPerc']

    def sottostanti(row):
        if row['SottostantiIsin'] is not None and row['SottostantiIsin'] != 'None':
            return row['SottostantiIsin']
        elif row['Sottostanti'] is not None and row['Sottostanti'] != 'None':
            return row['Sottostanti']
        else:
            return None
    df_new['CodiceSottostante'] = df_old.apply(sottostanti, axis=1)
    df_new['NomeSottostante'] = 'NA'
    df_new['DivisaSottostante'] = 'EUR'
    df_new['TipoSottostante'] = 'Azioni'
    df_new['SottostanteBasket'] = 0
    df_new['NumeroSottostanti'] = 1
    df_new["Sottostante_1(AnagraficaSottostanti)"] = None
    df_new["Sottostante_2(AnagraficaSottostanti)"] = None
    df_new["Sottostante_3(AnagraficaSottostanti)"] = None
    df_new["Sottostante_4(AnagraficaSottostanti)"] = None
    df_new["Sottostante_5(AnagraficaSottostanti)"] = None
    df_new['TipoCalcoloBasketPerf'] = None
    df_new['SottostanteOpaco'] = 0
    df_new['PosizioneLongShortSuSottostante'] = 'Long'
    df_new['StrategiaLongShort'] = 'Long'
    df_new['IsQuanto'] = None

    def map_path_dependent(row):
        if row['AutomaticEarlyRedemption'] == 1:
            return 1
        else:
            return 0

    df_new['PathDependent'] = df_old.apply(map_path_dependent, axis=1)

    def map_TipoRilevazione(row):
        if row['TipoBarrieraProtezione'] == 'Europea':
            return 'Discreta'
        elif row['TipoBarrieraProtezione'] == 'Americana':
            return 'Continua'
        else:
            return None
    df_new['TipoRilevazione'] = df_old.apply(map_TipoRilevazione, axis=1)
    df_new['FineCollocamento'] = None
    df_new['DataEmissione'] = df_old['DataEmissione']
    df_new['DataScadenza'] = df_old['DataScadenza']
    df_new['AutomaticEarlyRedemption'] = df_old['AutomaticEarlyRedemption']

    def map_tipo_payoff(row):
        if row['AutomaticEarlyRedemption'] == 1:
            return 'Esotico'
        else:
            return 'Digitale'

    df_new['TipoPayoff'] = df_old.apply(map_tipo_payoff, axis=1)
    df_new['DataInserimento'] = datetime.datetime.now().strftime("%Y-%m-%d")
    df_new['ClasseEUSIPA'] = None
    df_new['Tipo_IdEmittente'] = 'IdProm'
    df_new['BailIn'] = 1
    df_new['RankingBailIn'] = 'Certificate'
    df_new['Strike'] = None
    df_new['CedolaFloorPerc'] = None
    df_new['OpenEnd'] = 0
    df_new['Callable'] = df_old['Callable']
    df_new['Putable'] = df_old['Putable']
    df_new['CreditLinked'] = 0
    df_new['Decodifica'] = None
    df_new['Retail'] = None
    df_new['Defaulted'] = None
    df_new['Note'] = None
    df_new['Fare'] = 31
    df_new['FareBailIn'] = 1

    df_new = df_new.fillna('NULL')

    df_new.replace('Not specified in the document', 'NULL', inplace=True)

    # Lista delle colonne da pulire dagli spazi
    columns_to_strip = ['Isin', 'ValoreNominale', 'GaranziaMinimaPerc', 'ProtezioneCondizionataPerc',
                        'BarrieraProtezionePerc', 'Strike', 'LevaPercCapitale', 'LevaPercCedolare',
                        'CedolaGarantitaPerc', 'CedolaCondizionataPerc', 'BarrieraCedolaCondizionataPerc',
                        'CedolaFloorPerc', 'CedolaCapPerc']

    # Rimuovi gli spazi dalle colonne specificate
    df_new[columns_to_strip] = df_new[columns_to_strip].applymap(lambda x: x.strip() if isinstance(x, str) else x)

    string_columns = df_new.select_dtypes(include='string').columns
    df_new[string_columns] = df_new[string_columns].apply(lambda x: x.str.strip() if x.dtype == 'string' else x)
    df_new = df_new.replace('None', 'NULL')

    return df_new
