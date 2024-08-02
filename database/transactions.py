def get_all_transactions(cursor):
    try:
        cursor.execute('''
        SELECT t.*, a.name, c.name, p.name FROM transactions AS t
        JOIN accounts AS a
            ON t.account_id = a.id
        JOIN identifiers AS i
            ON t.identifier_id = i.id
        JOIN categories AS c
            ON i.category_id = c.id
        LEFT JOIN categories as p
            ON c.parent_id = p.id;
        ''')
        return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching transactions: {e}")
