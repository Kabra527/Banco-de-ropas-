import sqlite3
from contextlib import closing

DB_PATH = "bancode_ropas.db"

def init_db():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        c = conn.cursor()
        # Crear tablas
        c.execute('''
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT,
            talla TEXT,
            cantidad INTEGER,
            fecha TEXT,
            estado TEXT,
            descripcion TEXT
        );
        ''')
        c.execute('''
        CREATE TABLE IF NOT EXISTS beneficiaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            contacto TEXT,
            direccion TEXT
        );
        ''')
        c.execute('''
        CREATE TABLE IF NOT EXISTS deliveries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            beneficiary_id INTEGER,
            fecha TEXT,
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

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
