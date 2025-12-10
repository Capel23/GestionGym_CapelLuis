# models/clase.py
from database import get_db_connection

class Clase:
    def __init__(self, id, nombre, instructor, duracion_min=45, capacidad=12):
        self.id = id
        self.nombre = nombre
        self.instructor = instructor
        self.duracion_min = duracion_min
        self.capacidad = capacidad

    @classmethod
    def create(cls, nombre, instructor, duracion_min=45, capacidad=12):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO clase (nombre, instructor, duracion_min, capacidad)
                VALUES (?, ?, ?, ?)
            """, (nombre, instructor, duracion_min, capacidad))
            conn.commit()
            clase_id = cursor.lastrowid
            return cls(clase_id, nombre, instructor, duracion_min, capacidad)
        finally:
            conn.close()

    @classmethod
    def listar(cls):
        conn = get_db_connection()
        rows = conn.execute("SELECT * FROM clase ORDER BY nombre").fetchall()
        conn.close()
        return [cls(r['id'], r['nombre'], r['instructor'], r['duracion_min'], r['capacidad']) for r in rows]