def get_all_accounts(cursor):
    try:
        cursor.execute('SELECT * FROM accounts;')
        return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching accounts: {e}")
