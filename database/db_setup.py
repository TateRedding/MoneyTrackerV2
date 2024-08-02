def drop_tables(conn, cursor):
    try:
        cursor.execute('DROP TABLE IF EXISTS accounts')
        cursor.execute('DROP TABLE IF EXISTS identifiers')
        cursor.execute('DROP TABLE IF EXISTS categories')
        cursor.execute('DROP TABLE IF EXISTS transactions')
        conn.commit()
    except Exception as e:
        print(f"Error dropping tables: {e}")

def create_tables(conn, cursor):
    try:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(128) UNIQUE NOT NULL
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(128) NOT NULL,
            type VARCHAR(32),
            parent_id INTEGER,
            FOREIGN KEY (parent_id) REFERENCES categories (id)
            UNIQUE(name, parent_id)
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS identifiers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phrase TEXT UNIQUE NOT NULL,
            category_id INTEGER NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount FLOAT NOT NULL,
            description TEXT NOT NULL,
            date DATE NOT NULL,
            account_id INTEGER NOT NULL,
            identifier_id INTEGER,
            FOREIGN KEY (account_id) REFERENCES accounts (id),
            FOREIGN KEY (identifier_id) REFERENCES identifiers (id)
            UNIQUE(amount, description, date, account_id)
        )
        ''')

        conn.commit()
    except Exception as e:
        print(f"Error creating tables: {e}")

def create_triggers(conn, cursor):
    try:
        cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS enforce_single_level_subcategory_insert
        BEFORE INSERT ON categories
        FOR EACH ROW
        BEGIN
            SELECT RAISE(FAIL, 'A subcategory cannot be a parent')
            WHERE NEW.parent_id IS NOT NULL AND EXISTS (
                SELECT 1
                FROM categories
                WHERE id = NEW.parent_id
                AND parent_id IS NOT NULL
            );
        END;
        ''')

        cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS enforce_single_level_subcategory_update
        BEFORE UPDATE OF parent_id ON categories
        FOR EACH ROW
        BEGIN
            SELECT RAISE(FAIL, 'A subcategory cannot be a parent')
            WHERE NEW.parent_id IS NOT NULL AND EXISTS (
                SELECT 1
                FROM categories
                WHERE parent_id = NEW.id
            );
        END;
        ''')

        cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS enforce_type_no_parent_insert
        BEFORE INSERT ON categories
        FOR EACH ROW
        BEGIN
            SELECT RAISE(FAIL, 'A category with a type cannot have a parent or vice versa')
            WHERE NEW.type IS NOT NULL AND NEW.parent_id IS NOT NULL;
        END;
        ''')

        cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS enforce_type_no_parent_update
        BEFORE UPDATE OF parent_id, type ON categories
        FOR EACH ROW
        WHEN NEW.parent_id IS NOT NULL AND NEW.type IS NOT NULL
        BEGIN
            SELECT RAISE(FAIL, 'A category with a type cannot have a parent or vice versa');
        END;
        ''')

        cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS enforce_top_level_type_insert
        BEFORE INSERT ON categories
        FOR EACH ROW
        BEGIN
            SELECT RAISE(FAIL, 'A category without a parent must have a type')
            WHERE NEW.parent_id IS NULL AND NEW.type IS NULL;
        END;
        ''')

        cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS enforce_top_level_type_update
        BEFORE UPDATE OF parent_id, type ON categories
        FOR EACH ROW
        WHEN NEW.parent_id IS NULL AND NEW.type IS NULL
        BEGIN
            SELECT RAISE(FAIL, 'A category without a parent must have a type');
        END;
        ''')

        conn.commit()
    except Exception as e:
        print(f"Error creating triggers: {e}")

def seed_database(conn, cursor):
    try:
        # Accounts
        cursor.execute('INSERT INTO accounts (name) VALUES (?)', ('Discover Credit',))
        cursor.execute('INSERT INTO accounts (name) VALUES (?)', ('First Bank Checking',))
        cursor.execute('INSERT INTO accounts (name) VALUES (?)', ('Chase Credit',))
        cursor.execute('INSERT INTO accounts (name) VALUES (?)', ('Wells Fargo Checking',))
        cursor.execute('INSERT INTO accounts (name) VALUES (?)', ('Wells Fargo Credit',))

        # Top-level Categories
        cursor.execute('INSERT INTO categories (name, type) VALUES (?, ?)', ('Subscriptions', 'payments'))
        cursor.execute('INSERT INTO categories (name, type) VALUES (?, ?)', ('Groceries', 'payments'))
        cursor.execute('INSERT INTO categories (name, type) VALUES (?, ?)', ('Bills', 'payments'))
        cursor.execute('INSERT INTO categories (name, type) VALUES (?, ?)', ('Saving Transfer', 'external transfer'))
        cursor.execute('INSERT INTO categories (name, type) VALUES (?, ?)', ('Credit Card Payment', 'internal transfer'))
        cursor.execute('INSERT INTO categories (name, type) VALUES (?, ?)', ('Paycheck', 'income'))

        # Second-level Categories
        cursor.execute('INSERT INTO categories (name, parent_id) VALUES (?, ?)', ('Netflix', 1))
        cursor.execute('INSERT INTO categories (name, parent_id) VALUES (?, ?)', ('King Soopers', 2))
        cursor.execute('INSERT INTO categories (name, parent_id) VALUES (?, ?)', ('Sprouts', 2))
        cursor.execute('INSERT INTO categories (name, parent_id) VALUES (?, ?)', ('Electricity', 3))
        cursor.execute('INSERT INTO categories (name, parent_id) VALUES (?, ?)', ('First Bank Savings Allocation', 4))
        cursor.execute('INSERT INTO categories (name, parent_id) VALUES (?, ?)', ('WF Credit Payment', 5))
        
        # Identifiers
        cursor.execute('INSERT INTO identifiers (phrase, category_id) VALUES (?, ?)', ('NETFLIX', 7))
        cursor.execute('INSERT INTO identifiers (phrase, category_id) VALUES (?, ?)', ('KING SOOPERS', 8))
        cursor.execute('INSERT INTO identifiers (phrase, category_id) VALUES (?, ?)', ('SPROUTS', 9))
        cursor.execute('INSERT INTO identifiers (phrase, category_id) VALUES (?, ?)', ('PROG DIRECT', 3))
        cursor.execute('INSERT INTO identifiers (phrase, category_id) VALUES (?, ?)', ('ELECTRIC BILL', 10))
        cursor.execute('INSERT INTO identifiers (phrase, category_id) VALUES (?, ?)', ('TRANSFER TO FIRST BANK SAVINGS', 11))
        cursor.execute('INSERT INTO identifiers (phrase, category_id) VALUES (?, ?)', ('ONLINE PAYMENT THANK YOU', 12))
        cursor.execute('INSERT INTO identifiers (phrase, category_id) VALUES (?, ?)', ('MARIGOLD', 6))

        # Transactions
        cursor.execute('INSERT INTO transactions (date, amount, description, identifier_id, account_id) VALUES (?, ?, ?, ?, ?)', ('2024-01-15', -50.00, 'King Soopers Grocery Purchase', 2, 1))
        cursor.execute('INSERT INTO transactions (date, amount, description, identifier_id, account_id) VALUES (?, ?, ?, ?, ?)', ('2024-01-20', -30.00, 'Sprouts Grocery Purchase', 3, 1))
        cursor.execute('INSERT INTO transactions (date, amount, description, identifier_id, account_id) VALUES (?, ?, ?, ?, ?)', ('2024-02-05', -120.00, 'Electricity Bill Payment', 5, 1))
        cursor.execute('INSERT INTO transactions (date, amount, description, identifier_id, account_id) VALUES (?, ?, ?, ?, ?)', ('2024-02-10', -10.00, 'Netflix Renewal', 1, 3))
        cursor.execute('INSERT INTO transactions (date, amount, description, identifier_id, account_id) VALUES (?, ?, ?, ?, ?)', ('2024-03-01', -15.00, 'Online Payment Thank You', 7, 4))
        cursor.execute('INSERT INTO transactions (date, amount, description, identifier_id, account_id) VALUES (?, ?, ?, ?, ?)', ('2024-03-01', 2000.00, 'Marigold Paycheck', 8, 1))
        conn.commit()

        # Trigger testing
        # cursor.execute('INSERT INTO categories (name, parent_id) VALUES (?, ?)', ('Some Value', 7))
        # cursor.execute('UPDATE categories SET parent_id = ? WHERE id = ?', (3, 4))
        # cursor.execute('INSERT INTO categories (name, parent_id, type) VALUES (?, ?, ?)', ('Some Value', 1, 'subcategory'))
        # cursor.execute('UPDATE categories SET parent_id = ? WHERE id = ?', (1, 2))
        # cursor.execute('UPDATE categories SET type = ? WHERE id = ?', ('Some Value', 8))
        # cursor.execute('INSERT INTO categories (name) VALUES (?)', ('Some Value',))
        # cursor.execute('UPDATE categories set parent_id = ? WHERE id = ?', (None, 10))
        # cursor.execute('UPDATE categories set type = ? WHERE id = ?', (None, 5))

    except Exception as e:
        print(f"Error seeding database: {e}")

def init_db(conn, cursor):
    try:
        drop_tables(conn, cursor)
        create_tables(conn, cursor)
        create_triggers(conn, cursor)
        seed_database(conn, cursor)
    except Exception as e:
        print(f"Error initializing database: {e}")
