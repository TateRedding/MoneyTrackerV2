import sqlite3

def get_all_transactions(cursor):
    try:
        cursor.execute('''
        SELECT t.*, a.name, COALESCE(c.name, 'Unknown'), COALESCE(p.name, 'N/A') FROM transactions AS t
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
        raise RuntimeError(f'Error fetching transactions: {e}')
    
def get_month_range(cursor):
    try:
        cursor.execute('''
            SELECT DISTINCT strftime('%Y-%m', date) AS month
            FROM transactions
            ORDER BY month;
        ''')
        return [row[0] for row in cursor.fetchall()]
    except sqlite3.Error as e:
        raise RuntimeError(f"An error occurred while fetching available months: {e}")
    
def get_totals_by_month(cursor, selected_month):
    try:
        cursor.execute('''
            SELECT c.name AS category_name, p.name AS parent_category_name,
            CASE 
                WHEN c.parent_id IS NOT NULL THEN p.type 
                ELSE c.type 
            END AS type,
            SUM(t.amount) AS total_amount
            FROM transactions t
            JOIN identifiers i
                ON t.identifier_id = i.id
            JOIN categories c
                ON i.category_id = c.id
            LEFT JOIN categories p
                ON c.parent_id = p.id
            WHERE strftime('%Y-%m', t.date) = ?
            GROUP BY c.id
            ORDER BY c.name;
        ''', (selected_month,))
        subcategory_totals = cursor.fetchall()
        return subcategory_totals
    except sqlite3.Error as e:
        raise RuntimeError(f"An error occurred while fetching totals: {e}")
    

def get_monthly_totals_with_range(cursor, start_month, end_month):
    try:
        cursor.execute('''
            WITH monthly_totals AS (
                SELECT
                    strftime('%Y-%m', t.date) AS month,
                    CASE 
                        WHEN c.parent_id IS NOT NULL THEN p.name 
                        ELSE c.name
                    END AS parent_category_name,
                    SUM(t.amount) AS total_amount
                FROM transactions t
                JOIN identifiers i ON t.identifier_id = i.id
                JOIN categories c ON i.category_id = c.id
                LEFT JOIN categories p on c.parent_id = p.id
                WHERE strftime('%Y-%m', t.date) BETWEEN ? AND ?
                GROUP BY month, parent_category_name
            )
            SELECT
                month,
                parent_category_name,
                total_amount
            FROM monthly_totals
            ORDER BY month, parent_category_name;
        ''', (start_month, end_month))
        return cursor.fetchall()
    except sqlite3.Error as e:
        raise RuntimeError(f"An error occurred while fetching monthly totals: {e}")

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
