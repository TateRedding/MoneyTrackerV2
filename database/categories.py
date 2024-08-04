import sqlite3

def get_all_categories(cursor):
    try:
        cursor.execute('''
        SELECT c.*, p.name FROM categories AS c
        LEFT JOIN categories AS p
            ON c.parent_id = p.id;
        ''')
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f'Error fetching categories: {e}')

def get_category_by_id(cursor, id):
    try:
        cursor.execute('SELECT * FROM categories WHERE id = ?', (id,))
        return cursor.fetchone()
    except sqlite3.Error as e:
        print(f'Error fetching category: {e}')

def get_category_by_name(cursor, name):
    try:
        cursor.execute('SELECT * FROM categories WHERE name = ?', (name,))
        return cursor.fetchone()
    except sqlite3.Error as e:
        print(f'Error fetching category: {e}')

def add_category(conn, cursor, name, parent_id, type):
    try:
        cursor.execute('INSERT INTO categories (name, parent_id, type) VALUES (?, ?, ?)', (name, parent_id, type))
        conn.commit()
    except sqlite3.Error as e:
        print(f'Error adding category: {e}')
