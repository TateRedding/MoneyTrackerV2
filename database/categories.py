import sqlite3

def get_all_categories(cursor):
    try:
        cursor.execute('''
            SELECT c.*, p.name
            FROM categories AS c
            LEFT JOIN categories AS p
                ON c.parent_id = p.id;
        ''')
        return cursor.fetchall()
    except sqlite3.Error as e:
        raise RuntimeError(f'Error fetching categories: {e}')

def get_category_by_id(cursor, id):
    try:
        cursor.execute('''
            SELECT c.*, p.name
            FROM categories AS c
            LEFT JOIN categories AS p
                ON c.parent_id = p.id
            WHERE c.id = ?;
        ''', (id,))
        return cursor.fetchone()
    except sqlite3.Error as e:
        raise RuntimeError(f'Error fetching category: {e}')

def get_category_by_name(cursor, name):
    try:
        cursor.execute('SELECT * FROM categories WHERE name = ?;', (name,))
        return cursor.fetchone()
    except sqlite3.Error as e:
        raise RuntimeError(f'Error fetching category: {e}')

def add_category(conn, cursor, name, parent_id, type):
    try:
        cursor.execute('INSERT INTO categories (name, parent_id, type) VALUES (?, ?, ?);', (name, parent_id, type))
        conn.commit()
    except sqlite3.Error as e:
        raise RuntimeError(f'Error adding category: {e}')
    
def update_category(conn, cursor, category_id, name, parent_id, type):
    try:
        cursor.execute('UPDATE categories SET name = ?, parent_id = ?, type = ? WHERE id = ?;', (name, parent_id, type, category_id))
        conn.commit()
    except sqlite3.Error as e:
        raise RuntimeError(f'Error updating category: {e}')
