import sqlite3

def get_all_accounts(cursor):
    try:
        cursor.execute('SELECT * FROM accounts;')
        return cursor.fetchall()
    except sqlite3.Error as e:
        raise RuntimeError(f'Error fetching accounts: {e}')
