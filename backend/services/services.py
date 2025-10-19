"""Servicios de acceso a datos y lógica de negocio."""
from backend.database import get_connection
from datetime import datetime

class DonationService:
    @staticmethod
    def create_donation(tipo, talla, cantidad, descripcion=''):
        """Crear una donación y devolver el id."""
        conn = get_connection()
        try:
            c = conn.cursor()
            c.execute(
                'INSERT INTO donations (tipo,talla,cantidad,estado,descripcion,fecha) VALUES (?,?,?,?,?,?)',
                (tipo, talla, cantidad, 'pendiente', descripcion, datetime.utcnow().isoformat())
            )
            conn.commit()
            return c.lastrowid
        finally:
            conn.close()

    @staticmethod
    def list_inventory():
        """Listar donaciones con cantidad > 0."""
        conn = get_connection()
        try:
            c = conn.cursor()
            c.execute('SELECT id,tipo,talla,cantidad,estado,descripcion,fecha FROM donations WHERE cantidad > 0')
            rows = c.fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    @staticmethod
    def reduce_stock(donation_id, cantidad):
        """Reducir stock de una donación identificada."""
        conn = get_connection()
        try:
            c = conn.cursor()
            c.execute('SELECT cantidad FROM donations WHERE id=?', (donation_id,))
            row = c.fetchone()
            if not row:
                raise ValueError('donation not found')
            nueva = max(0, row['cantidad'] - cantidad)
            c.execute('UPDATE donations SET cantidad=? WHERE id=?', (nueva, donation_id))
            conn.commit()
        finally:
            conn.close()
