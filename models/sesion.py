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