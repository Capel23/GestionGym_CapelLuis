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
    
    @classmethod
    def get_by_id(cls, id):
        """Obtiene un aparato por su ID."""
        conn = get_db_connection()
        row = conn.execute("SELECT * FROM aparato WHERE id = ?", (id,)).fetchone()
        conn.close()
        if row:
            return cls(row['id'], row['tipo'], row['nombre'])
        return None
    
    @classmethod
    def update(cls, id, tipo, nombre):
        """Actualiza un aparato existente."""
        conn = get_db_connection()
        try:
            conn.execute("""
                UPDATE aparato 
                SET tipo = ?, nombre = ? 
                WHERE id = ?
            """, (tipo, nombre, id))
            conn.commit()
            return True
        except Exception as e:
            return False
        finally:
            conn.close()
    
    @classmethod
    def delete(cls, id):
        """Elimina un aparato de la base de datos."""
        conn = get_db_connection()
        try:
            conn.execute("DELETE FROM aparato WHERE id = ?", (id,))
            conn.commit()
            return True
        except Exception as e:
            return False
        finally:
            conn.close()
    
    @classmethod
    def tiene_reservas(cls, id):
        """Verifica si un aparato tiene reservas activas."""
        conn = get_db_connection()
        count = conn.execute("""
            SELECT COUNT(*) as count 
            FROM sesion 
            WHERE id_aparato = ?
        """, (id,)).fetchone()['count']
        conn.close()
        return count > 0