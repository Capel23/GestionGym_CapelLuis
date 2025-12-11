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

    @classmethod
    def update(cls, cliente_id, nombre=None, email=None, telefono=None):
        """Actualiza datos de un cliente. Solo actualiza los campos proporcionados."""
        conn = get_db_connection()
        try:
            updates = []
            params = []
            
            if nombre is not None:
                updates.append("nombre = ?")
                params.append(nombre)
            if email is not None:
                updates.append("email = ?")
                params.append(email)
            if telefono is not None:
                updates.append("telefono = ?")
                params.append(telefono)
            
            if not updates:
                return False
            
            params.append(cliente_id)
            query = f"UPDATE cliente SET {', '.join(updates)} WHERE id = ?"
            conn.execute(query, params)
            conn.commit()
            return True
        except Exception as e:
            raise Exception(f"Error al actualizar cliente: {e}")
        finally:
            conn.close()

    @classmethod
    def dar_de_baja(cls, cliente_id):
        """Marca un cliente como inactivo (soft delete)."""
        conn = get_db_connection()
        try:
            conn.execute("UPDATE cliente SET activo = 0 WHERE id = ?", (cliente_id,))
            conn.commit()
            return True
        finally:
            conn.close()

    @classmethod
    def listar_todos(cls, incluir_inactivos=False):
        """Lista todos los clientes, opcionalmente incluyendo inactivos."""
        conn = get_db_connection()
        if incluir_inactivos:
            rows = conn.execute("SELECT * FROM cliente ORDER BY nombre").fetchall()
        else:
            rows = conn.execute("SELECT * FROM cliente WHERE activo = 1 ORDER BY nombre").fetchall()
        conn.close()
        return [cls(r['id'], r['nombre'], r['email'], r['telefono'], r['activo']) for r in rows]

    @classmethod
    def buscar(cls, termino):
        """Busca clientes por nombre, email o teléfono."""
        conn = get_db_connection()
        termino_like = f"%{termino}%"
        rows = conn.execute("""
            SELECT * FROM cliente 
            WHERE activo = 1 AND (
                nombre LIKE ? OR 
                email LIKE ? OR 
                telefono LIKE ?
            )
            ORDER BY nombre
        """, (termino_like, termino_like, termino_like)).fetchall()
        conn.close()
        return [cls(r['id'], r['nombre'], r['email'], r['telefono'], r['activo']) for r in rows]