from database import get_db_connection

class ClaseHorario:
    def __init__(self, id, id_clase, dia_semana, hora_inicio):
        self.id = id
        self.id_clase = id_clase
        self.dia_semana = dia_semana
        self.hora_inicio = hora_inicio

    @classmethod
    def crear(cls, id_clase, dia_semana, hora_inicio):
        """Crea un horario programado para una clase"""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO clase_horario (id_clase, dia_semana, hora_inicio)
                VALUES (?, ?, ?)
            """, (id_clase, dia_semana, hora_inicio))
            conn.commit()
            horario_id = cursor.lastrowid
            return cls(horario_id, id_clase, dia_semana, hora_inicio)
        finally:
            conn.close()

    @classmethod
    def listar_por_clase(cls, id_clase):
        """Devuelve todos los horarios de una clase específica"""
        conn = get_db_connection()
        rows = conn.execute("""
            SELECT * FROM clase_horario
            WHERE id_clase = ?
            ORDER BY dia_semana, hora_inicio
        """, (id_clase,)).fetchall()
        conn.close()
        return [cls(r['id'], r['id_clase'], r['dia_semana'], r['hora_inicio']) for r in rows]

    @classmethod
    def listar_todos_con_detalles(cls):
        """Devuelve todos los horarios con información de la clase"""
        conn = get_db_connection()
        rows = conn.execute("""
            SELECT ch.*, c.nombre, c.instructor, c.duracion_min, c.capacidad
            FROM clase_horario ch
            JOIN clase c ON ch.id_clase = c.id
            ORDER BY c.nombre, ch.dia_semana, ch.hora_inicio
        """).fetchall()
        conn.close()
        return rows

    @classmethod
    def existe_horario(cls, id_clase, dia_semana, hora_inicio):
        """Verifica si existe un horario específico para una clase"""
        conn = get_db_connection()
        row = conn.execute("""
            SELECT COUNT(*) as count FROM clase_horario
            WHERE id_clase = ? AND dia_semana = ? AND hora_inicio = ?
        """, (id_clase, dia_semana, hora_inicio)).fetchone()
        conn.close()
        return row['count'] > 0
    
    @classmethod
    def create(cls, id_clase, dia_semana, hora_inicio):
        """Crea un nuevo horario para una clase."""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO clase_horario (id_clase, dia_semana, hora_inicio)
                VALUES (?, ?, ?)
            """, (id_clase, dia_semana, hora_inicio))
            conn.commit()
            horario_id = cursor.lastrowid
            return cls(horario_id, id_clase, dia_semana, hora_inicio)
        finally:
            conn.close()
    
    @classmethod
    def get_by_id(cls, id):
        """Obtiene un horario por su ID."""
        conn = get_db_connection()
        row = conn.execute("SELECT * FROM clase_horario WHERE id = ?", (id,)).fetchone()
        conn.close()
        if row:
            return cls(row['id'], row['id_clase'], row['dia_semana'], row['hora_inicio'])
        return None
    
    @classmethod
    def update(cls, id, dia_semana, hora_inicio):
        """Actualiza un horario existente."""
        conn = get_db_connection()
        try:
            conn.execute("""
                UPDATE clase_horario 
                SET dia_semana = ?, hora_inicio = ?
                WHERE id = ?
            """, (dia_semana, hora_inicio, id))
            conn.commit()
            return True
        except Exception as e:
            return False
        finally:
            conn.close()
    
    @classmethod
    def delete(cls, id):
        """Elimina un horario de la base de datos."""
        conn = get_db_connection()
        try:
            conn.execute("DELETE FROM clase_horario WHERE id = ?", (id,))
            conn.commit()
            return True
        except Exception as e:
            return False
        finally:
            conn.close()
