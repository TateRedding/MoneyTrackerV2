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
        print(f'Error fetching identifiers: {e}')

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
