import csv
from datetime import datetime
import database.identifiers as idens

def parse_file(cursor, file_path, account_id, account_name):
    if not file_path.lower().endswith('.csv'):
        raise ValueError('The file is not a CSV. Please provide a valid CSV file.')
    
    bank_function_map = {
        'Discover Credit': discover,
        'Chase Credit': chase,
        'First Bank Checking': first_bank,
        'Wells Fargo Checking': wells_fargo,
        'Wells Fargo Credit': wells_fargo,
    }
    
    if account_name not in bank_function_map:
        raise ValueError(f'No parsing function for the account: {account_name}.')
    
    return bank_function_map[account_name](cursor, file_path, account_id)

def extract_transactions(file_path, date_idx, amount_idx, desc_idx, date_format, amount_multiplier=1, skip_header=False):
    data = []
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            if skip_header:
                next(csv_reader)
            for row in csv_reader:
                if len(row) > max(date_idx, amount_idx, desc_idx):
                    date_str = row[date_idx]
                    amount_str = row[amount_idx]
                    description = row[desc_idx].replace("'", "''")
                    date = datetime.strptime(date_str, date_format).strftime('%Y-%m-%d')
                    amount = float(amount_str) * amount_multiplier
                    data.append((date, amount, description))
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f'The file at {file_path} does not exist.')
    except Exception as e:
        raise RuntimeError(f'An error occurred while reading the file: {e}')

def identify_transactions(cursor, data, account_id):
    identified_data = []
    for date, amount, description in data:
        identifier_id = idens.identify_transaction_description(cursor, description)
        identified_data.append((date, amount, description, identifier_id, account_id))
    return identified_data

def wells_fargo(cursor, file_path, account_id):
    raw_transaction_data = extract_transactions(file_path, date_idx=0, amount_idx=1, desc_idx=4, date_format='%m/%d/%Y')
    return identify_transactions(cursor, raw_transaction_data, account_id)

def discover(cursor, file_path, account_id):
    raw_transaction_data = extract_transactions(file_path, date_idx=0, amount_idx=3, desc_idx=2, date_format='%m/%d/%Y', amount_multiplier=-1, skip_header=True)
    return identify_transactions(cursor, raw_transaction_data, account_id)

def chase(cursor, file_path, account_id):
    raw_transaction_data = extract_transactions(file_path, date_idx=0, amount_idx=5, desc_idx=2, date_format='%m/%d/%Y', skip_header=True)
    return identify_transactions(cursor, raw_transaction_data, account_id)

def first_bank(cursor, file_path, account_id):
    raw_transaction_data = extract_transactions(file_path, date_idx=0, amount_idx=3, desc_idx=1, date_format='%m/%d/%y')
    return identify_transactions(cursor, raw_transaction_data, account_id)
