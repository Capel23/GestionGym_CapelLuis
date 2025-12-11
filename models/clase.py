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
    
    @classmethod
    def get_by_id(cls, id):
        """Obtiene una clase por su ID."""
        conn = get_db_connection()
        row = conn.execute("SELECT * FROM clase WHERE id = ?", (id,)).fetchone()
        conn.close()
        if row:
            return cls(row['id'], row['nombre'], row['instructor'], row['duracion_min'], row['capacidad'])
        return None
    
    @classmethod
    def update(cls, id, nombre, instructor, duracion_min, capacidad):
        """Actualiza una clase existente."""
        conn = get_db_connection()
        try:
            conn.execute("""
                UPDATE clase 
                SET nombre = ?, instructor = ?, duracion_min = ?, capacidad = ?
                WHERE id = ?
            """, (nombre, instructor, duracion_min, capacidad, id))
            conn.commit()
            return True
        except Exception as e:
            return False
        finally:
            conn.close()
    
    @classmethod
    def delete(cls, id):
        """Elimina una clase de la base de datos (y sus horarios en cascada)."""
        conn = get_db_connection()
        try:
            conn.execute("DELETE FROM clase_horario WHERE id_clase = ?", (id,))
            conn.execute("DELETE FROM clase WHERE id = ?", (id,))
            conn.commit()
            return True
        except Exception as e:
            return False
        finally:
            conn.close()
    
    @classmethod
    def tiene_reservas(cls, id):
        """Verifica si una clase tiene reservas activas."""
        conn = get_db_connection()
        count = conn.execute("""
            SELECT COUNT(*) as count 
            FROM sesion 
            WHERE id_clase = ?
        """, (id,)).fetchone()['count']
        conn.close()
        return count > 0