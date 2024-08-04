import sqlite3

def get_all_transactions(cursor):
    try:
        cursor.execute('''
        SELECT t.*, a.name, COALESCE(c.name, 'Unknown'), COALESCE(c.name, 'N/A') FROM transactions AS t
        JOIN accounts AS a
            ON t.account_id = a.id
        LEFT JOIN identifiers AS i
            ON t.identifier_id = i.id
        LEFT JOIN categories AS c
            ON i.category_id = c.id
        LEFT JOIN categories as p
            ON c.parent_id = p.id
        ORDER BY date DESC;
        ''')
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f'Error fetching transactions: {e}')

def add_transactions(conn, cursor, data):
    try:
        cursor.execute('SELECT COUNT(*) FROM transactions;')
        initial_count = cursor.fetchone()[0]

        for date, amount, description, identifier_id, account_id in data:
            cursor.execute('''
                INSERT OR IGNORE INTO transactions (date, amount, description, identifier_id, account_id)
                VALUES (?, ?, ?, ?, ?);
            ''', (date, amount, description, identifier_id, account_id))
        conn.commit()

        cursor.execute('SELECT COUNT(*) FROM transactions;')
        final_count = cursor.fetchone()[0]

        inserted_count = final_count - initial_count

    except sqlite3.Error as e:
        raise RuntimeError(f"An error occurred while inserting data into the database: {e}")

    return inserted_count
