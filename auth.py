"""
Gestión de la sesión actual del usuario.
Permite saber quién está logueado en cualquier parte de la app.
"""

class SesionActual:
    _usuario = None 

    @classmethod
    def iniciar(cls, usuario):
        """Inicia sesión con un objeto Usuario."""
        cls._usuario = usuario

    @classmethod
    def obtener(cls):
        """Devuelve el usuario actual o None si no hay sesión."""
        return cls._usuario

    @classmethod
    def cerrar(cls):
        """Cierra la sesión."""
        cls._usuario = None

    @classmethod
    def es_admin(cls):
        """¿El usuario actual es admin?"""
        return cls._usuario and cls._usuario.rol == 'admin'

    @classmethod
    def es_cliente(cls):
        """¿El usuario actual es cliente?"""
        return cls._usuario and cls._usuario.rol == 'cliente'