# models/aparato.py
from database import get_db_connection

class Aparato:
    def __init__(self, id, tipo, nombre):
        self.id = id
        self.tipo = tipo
        self.nombre = nombre

    @classmethod
    def create(cls, tipo, nombre):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO aparato (tipo, nombre) VALUES (?, ?)", (tipo, nombre))
            conn.commit()
            aparato_id = cursor.lastrowid
            return cls(aparato_id, tipo, nombre)
        finally:
            conn.close()

    @classmethod
    def listar(cls):
        conn = get_db_connection()
        rows = conn.execute("SELECT * FROM aparato ORDER BY tipo, nombre").fetchall()
        conn.close()
        return [cls(r['id'], r['tipo'], r['nombre']) for r in rows]