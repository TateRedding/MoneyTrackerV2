import sqlite3

def get_all_identifiers(cursor):
    try:
        cursor.execute('''
        SELECT i.*, c.name, p.name FROM identifiers AS i
        JOIN categories AS c
            ON i.category_id = c.id
        LEFT JOIN categories as p
            ON c.parent_id = p.id;
        ''')
        return cursor.fetchall()
    except sqlite3.Error as e:
        raise RuntimeError(f'Error fetching identifiers: {e}')

def get_identifier_by_phrase(cursor, phrase):
    try:
        cursor.execute('SELECT * FROM identifiers WHERE phrase = ?', (phrase,))
        return cursor.fetchone()
    except sqlite3.Error as e:
        raise RuntimeError(f'Error fetching identifier: {e}')

def identify_transaction_description(cursor, description):
    try:
        cursor.execute("SELECT id FROM identifiers WHERE ? LIKE '%' || phrase || '%' ORDER BY id ASC;", (description,))
        identifier = cursor.fetchone()
        if identifier:
            return identifier[0]
        else:
            return None
    except sqlite3.Error as e:
        raise RuntimeError(f'An error occurred while fetching identifier from description: {e}')
    
def add_identifier(conn, cursor, phrase, category_id):
    try:
        cursor.execute('INSERT INTO identifiers (phrase, category_id) VALUES (?, ?)', (phrase, category_id,))
        identifier_id = cursor.lastrowid
        cursor.execute('''
            UPDATE transactions
            SET identifier_id = ?
            WHERE description LIKE '%' || ? || '%'
            AND identifier_id IS NULL
        ''', (identifier_id, phrase))
        conn.commit()
    except sqlite3.Error as e:
        raise RuntimeError(f'An error occurred while adding a new identifier: {e}')

