import sqlite3
from contextlib import closing
DB_PATH = 'bancode_ropas.db'

def get_connection():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with closing(get_connection()) as conn:
        c = conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            talla TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            fecha TEXT DEFAULT CURRENT_TIMESTAMP,
            estado TEXT,
            descripcion TEXT
        );
        ''')
        c.execute('''
        CREATE TABLE IF NOT EXISTS beneficiaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            contacto TEXT,
            direccion TEXT
        );
        ''')
        c.execute('''
        CREATE TABLE IF NOT EXISTS deliveries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            beneficiary_id INTEGER,
            fecha TEXT DEFAULT CURRENT_TIMESTAMP,
            usuario TEXT,
            observaciones TEXT,
            FOREIGN KEY(beneficiary_id) REFERENCES beneficiaries(id)
        );
        ''')
        c.execute('''
        CREATE TABLE IF NOT EXISTS delivery_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            delivery_id INTEGER,
            donation_id INTEGER,
            cantidad_entregada INTEGER,
            FOREIGN KEY(delivery_id) REFERENCES deliveries(id),
            FOREIGN KEY(donation_id) REFERENCES donations(id)
        );
        ''')
        conn.commit()
