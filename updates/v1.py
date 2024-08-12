import sqlite3
import database.db_setup as setup

def update_v1(conn, cursor):
    setup.create_tables(conn, cursor)
    setup.create_triggers(conn, cursor)

    try:
        cursor.execute('INSERT INTO accounts (name, type) VALUES (?, ?);', ('Discover Credit', 'credit'))
        cursor.execute('INSERT INTO accounts (name, type) VALUES (?, ?);', ('Chase Credit', 'credit'))
        cursor.execute('INSERT INTO accounts (name, type) VALUES (?, ?);', ('First Bank Checking', 'checking'))
        cursor.execute('INSERT INTO accounts (name, type) VALUES (?, ?);', ('Wells Fargo Checking', 'checking'))
        cursor.execute('INSERT INTO accounts (name, type) VALUES (?, ?);', ('Wells Fargo Credit', 'checking'))

        conn.commit

    except sqlite3.Error as e:
        raise RuntimeError(f'Error seeding database: {e}')
