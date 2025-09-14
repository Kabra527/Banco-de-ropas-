from database import get_connection
from datetime import datetime

def create_donation(tipo, talla, cantidad, descripcion=""):
    conn = get_connection()
    c = conn.cursor()
    fecha = datetime.utcnow().isoformat()
    estado = "pendiente"
    c.execute('INSERT INTO donations (tipo,talla,cantidad,fecha,estado,descripcion) VALUES (?,?,?,?,?,?)',
              (tipo, talla, cantidad, fecha, estado, descripcion))
    conn.commit()
    id = c.lastrowid
    conn.close()
    return id

def list_inventory():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM donations WHERE cantidad > 0')
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def create_beneficiary(nombre, contacto, direccion=""):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO beneficiaries (nombre,contacto,direccion) VALUES (?,?,?)',
              (nombre, contacto, direccion))
    conn.commit()
    id = c.lastrowid
    conn.close()
    return id

def create_delivery(beneficiary_id, items, usuario="admin", observaciones=""):
    '''
    items: list of dicts [{'donation_id':1, 'cantidad':2}, ...]
    '''
    conn = get_connection()
    c = conn.cursor()
    fecha = datetime.utcnow().isoformat()
    c.execute('INSERT INTO deliveries (beneficiary_id, fecha, usuario, observaciones) VALUES (?,?,?,?)',
              (beneficiary_id, fecha, usuario, observaciones))
    delivery_id = c.lastrowid
    for it in items:
        donation_id = it['donation_id']
        cantidad = it['cantidad']
        # registrar item
        c.execute('INSERT INTO delivery_items (delivery_id, donation_id, cantidad_entregada) VALUES (?,?,?)',
                  (delivery_id, donation_id, cantidad))
        # actualizar inventario
        c.execute('SELECT cantidad FROM donations WHERE id=?', (donation_id,))
        row = c.fetchone()
        if row:
            nueva = max(0, row[0] - cantidad)
            c.execute('UPDATE donations SET cantidad=? WHERE id=?', (nueva, donation_id))
    conn.commit()
    conn.close()
    return delivery_id
