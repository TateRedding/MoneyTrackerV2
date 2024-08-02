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
    except Exception as e:
        print(f"Error fetching identifiers: {e}")
