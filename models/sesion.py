# models/sesion.py
from database import get_db_connection
from datetime import date

class Sesion:
    def __init__(self, id, id_cliente, id_aparato=None, id_clase=None, dia_semana=0, hora_inicio="00:00", fecha_reserva=None):
        self.id = id
        self.id_cliente = id_cliente
        self.id_aparato = id_aparato
        self.id_clase = id_clase
        self.dia_semana = dia_semana
        self.hora_inicio = hora_inicio
        self.fecha_reserva = fecha_reserva or date.today()

    @classmethod
    def reservar(cls, id_cliente, id_aparato=None, id_clase=None, dia_semana=0, hora_inicio="00:00"):
        """
        Reserva una sesión (máquina O clase). Devuelve True si éxito, False si conflicto.
        """
        if (id_aparato is None and id_clase is None) or (id_aparato and id_clase):
            raise ValueError("Debe especificar SOLO aparato o SOLO clase.")

        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO sesion (id_cliente, id_aparato, id_clase, dia_semana, hora_inicio)
                VALUES (?, ?, ?, ?, ?)
            """, (id_cliente, id_aparato, id_clase, dia_semana, hora_inicio))
            conn.commit()
            return True
        except Exception as e:
            if "UNIQUE constraint" in str(e):
                return False  # Ya ocupado
            raise
        finally:
            conn.close()

    @classmethod
    def horas_ocupadas_por_aparato(cls, id_aparato, dia_semana):
        """Devuelve lista de horas ocupadas (str) para un aparato y día."""
        conn = get_db_connection()
        rows = conn.execute("""
            SELECT hora_inicio FROM sesion
            WHERE id_aparato = ? AND dia_semana = ?
        """, (id_aparato, dia_semana)).fetchall()
        conn.close()
        return [r['hora_inicio'] for r in rows]

    @classmethod
    def horas_ocupadas_por_clase(cls, id_clase, dia_semana):
        """Devuelve lista de horas ocupadas (str) para una clase y día."""
        conn = get_db_connection()
        rows = conn.execute("""
            SELECT hora_inicio FROM sesion
            WHERE id_clase = ? AND dia_semana = ?
        """, (id_clase, dia_semana)).fetchall()
        conn.close()
        return [r['hora_inicio'] for r in rows]

    @classmethod
    def validar_horario_clase(cls, id_clase, dia_semana, hora_inicio):
        """Verifica que el horario existe en clase_horario antes de reservar"""
        from models.clase_horario import ClaseHorario
        return ClaseHorario.existe_horario(id_clase, dia_semana, hora_inicio)

    @classmethod
    def listar_por_cliente(cls, id_cliente):
        """Devuelve todas las sesiones de un cliente (con info de aparato/clase)."""
        conn = get_db_connection()
        rows = conn.execute("""
            SELECT s.*, a.nombre AS aparato, c.nombre AS clase
            FROM sesion s
            LEFT JOIN aparato a ON s.id_aparato = a.id
            LEFT JOIN clase c ON s.id_clase = c.id
            WHERE s.id_cliente = ?
            ORDER BY s.dia_semana, s.hora_inicio
        """, (id_cliente,)).fetchall()
        conn.close()
        return rows  # sqlite3.Row → accesible como dict

    @classmethod
    def listar_todas(cls, filtro_tipo=None, filtro_dia=None):
        """Lista todas las reservas con filtros opcionales.
        
        Args:
            filtro_tipo: 'aparato', 'clase' o None para todos
            filtro_dia: número de día (0-4) o None para todos
        """
        conn = get_db_connection()
        
        query = """
            SELECT s.id, s.id_cliente, s.id_aparato, s.id_clase,
                   s.dia_semana, s.hora_inicio, s.fecha_reserva,
                   c.nombre AS cliente_nombre,
                   a.nombre AS aparato_nombre, a.tipo AS aparato_tipo,
                   cl.nombre AS clase_nombre
            FROM sesion s
            JOIN cliente c ON s.id_cliente = c.id
            LEFT JOIN aparato a ON s.id_aparato = a.id
            LEFT JOIN clase cl ON s.id_clase = cl.id
            WHERE 1=1
        """
        
        params = []
        
        if filtro_tipo == 'aparato':
            query += " AND s.id_aparato IS NOT NULL"
        elif filtro_tipo == 'clase':
            query += " AND s.id_clase IS NOT NULL"
        
        if filtro_dia is not None:
            query += " AND s.dia_semana = ?"
            params.append(filtro_dia)
        
        query += " ORDER BY s.dia_semana, s.hora_inicio"
        
        rows = conn.execute(query, params).fetchall()
        conn.close()
        return rows

    @classmethod
    def cancelar(cls, sesion_id):
        """Cancela una reserva por ID. Retorna True si tuvo éxito."""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM sesion WHERE id = ?", (sesion_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    @classmethod
    def get_by_id(cls, sesion_id):
        """Obtiene una sesión por ID con toda la información."""
        conn = get_db_connection()
        row = conn.execute("""
            SELECT s.*, c.nombre AS cliente_nombre,
                   a.nombre AS aparato_nombre, a.tipo AS aparato_tipo,
                   cl.nombre AS clase_nombre
            FROM sesion s
            JOIN cliente c ON s.id_cliente = c.id
            LEFT JOIN aparato a ON s.id_aparato = a.id
            LEFT JOIN clase cl ON s.id_clase = cl.id
            WHERE s.id = ?
        """, (sesion_id,)).fetchone()
        conn.close()
        return row

    @classmethod
    def contar_por_cliente(cls, id_cliente):
        """Cuenta reservas activas de un cliente."""
        conn = get_db_connection()
        count = conn.execute("""
            SELECT COUNT(*) as total
            FROM sesion
            WHERE id_cliente = ?
        """, (id_cliente,)).fetchone()['total']
        conn.close()
        return count