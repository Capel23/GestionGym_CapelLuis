# models/usuario.py
from database import get_db_connection
import hashlib
from models.cliente import Cliente
from utils import validar_usuario


class Usuario:
    def __init__(self, id, username, rol, id_cliente=None):
        self.id = id
        self.username = username
        self.rol = rol
        self.id_cliente = id_cliente

    @staticmethod
    def _hash_password(password):
        salt = b"gym_salt_2025" 
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()

    @classmethod
    def login(cls, username, password):
        """Devuelve un Usuario si las credenciales son válidas, None si no."""
        conn = get_db_connection()
        user = conn.execute("""
            SELECT id, id_cliente, rol FROM usuario 
            WHERE username = ? AND password_hash = ?
        """, (username, cls._hash_password(password))).fetchone()
        conn.close()
        if user:
            return cls(user['id'], username, user['rol'], user['id_cliente'])
        return None

    @classmethod
    def create_cliente(cls, username, password, cliente):
        """Crea un cliente + su usuario. Devuelve el Usuario."""
       
        if not validar_usuario(username):
            raise ValueError("Usuario inválido: 3-20 caracteres, solo letras y números.")
        if not password or len(password) < 4:
            raise ValueError("Contraseña inválida: mínimo 4 caracteres.")

        cliente_obj = Cliente.create(**cliente)  
        conn = get_db_connection()
        try:
            try:
                conn.execute("""
                    INSERT INTO usuario (username, password_hash, rol, id_cliente)
                    VALUES (?, ?, 'cliente', ?)
                """, (username, cls._hash_password(password), cliente_obj.id))
                conn.commit()
                user_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
                return cls(user_id, username, 'cliente', cliente_obj.id)
            except Exception:
                try:
                    Cliente.delete_by_id(cliente_obj.id)
                except Exception:
                    pass
                raise
        finally:
            conn.close()

    @classmethod
    def create_admin(cls, username, password):
        """Crea un usuario admin (sin cliente asociado)."""
        conn = get_db_connection()
        try:
            conn.execute("""
                INSERT INTO usuario (username, password_hash, rol)
                VALUES (?, ?, 'admin')
            """, (username, cls._hash_password(password)))
            conn.commit()
            user_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            return cls(user_id, username, 'admin')
        finally:
            conn.close()