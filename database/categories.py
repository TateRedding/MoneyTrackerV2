def get_all_categories(cursor):
    try:
        cursor.execute('''
        SELECT c.*, p.name FROM categories AS c
        LEFT JOIN categories AS p
            ON c.parent_id = p.id
        ''')
        return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching categories: {e}")
