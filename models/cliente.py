# models/cliente.py
from database import get_db_connection

class Cliente:
    def __init__(self, id, nombre, email, telefono, activo=True):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.activo = activo

    @classmethod
    def create(cls, nombre, email, telefono):
        """Crea un cliente y devuelve el objeto."""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO cliente (nombre, email, telefono)
                VALUES (?, ?, ?)
            """, (nombre, email, telefono))
            conn.commit()
            cliente_id = cursor.lastrowid
            return cls(cliente_id, nombre, email, telefono)
        finally:
            conn.close()

    @classmethod
    def get_by_id(cls, cliente_id):
        conn = get_db_connection()
        row = conn.execute("SELECT * FROM cliente WHERE id = ?", (cliente_id,)).fetchone()
        conn.close()
        if row:
            return cls(row['id'], row['nombre'], row['email'], row['telefono'], row['activo'])
        return None

    @classmethod
    def listar_activos(cls):
        conn = get_db_connection()
        rows = conn.execute("SELECT * FROM cliente WHERE activo = 1").fetchall()
        conn.close()
        return [cls(r['id'], r['nombre'], r['email'], r['telefono']) for r in rows]

    @classmethod
    def delete_by_id(cls, cliente_id):
        """Elimina (borra) un cliente por id. Usado para limpieza si falla creación de usuario."""
        conn = get_db_connection()
        try:
            conn.execute("DELETE FROM cliente WHERE id = ?", (cliente_id,))
            conn.commit()
        finally:
            conn.close()