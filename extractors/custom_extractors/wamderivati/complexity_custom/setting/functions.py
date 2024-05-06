from datetime import datetime


def get_new_column_name(column_dict, column):
    for new_column, possible_columns in column_dict.items():
        if column in possible_columns:
            return new_column
    return column

def truncate(x):
    if isinstance(x, str):
        return x[:100]
    else:
        return x


def pulisci_emittenti(valore):
    valore_pulito = valore.replace(".", "").replace(",", "").lower()
    return valore_pulito


def clean_value(x):
    if isinstance(x, str):
        x = x.replace(',', '')  # Rimuovi le virgole
        x = x.replace('EUR', '')  # Rimuovi 'EUR'
        x = x.replace('%', '')  # Rimuovi '%'
        x = x.replace('per Certificate', '')  # Rimuovi '%'
        x = x.replace('per certificate', '')  # Rimuovi '%'
        return x
    else:
        return x


def convert_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%d/%m/%Y')
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        return date_str

