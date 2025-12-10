# models/recibo.py
from database import get_db_connection
from datetime import date

class Recibo:
    MONTO_MENSUAL = 49.90  # Puedes sacarlo a config si quieres

    def __init__(self, id, id_cliente, mes, anio, monto, pagado=False, fecha_pago=None):
        self.id = id
        self.id_cliente = id_cliente
        self.mes = mes
        self.anio = anio
        self.monto = monto
        self.pagado = pagado
        self.fecha_pago = fecha_pago

    @classmethod
    def generar_recibos_mes(cls, mes=None, anio=None):
        """Genera recibos para todos los clientes activos del mes actual (o especificado)."""
        hoy = date.today()
        mes = mes or hoy.month
        anio = anio or hoy.year

        conn = get_db_connection()
        clientes = conn.execute("SELECT id FROM cliente WHERE activo = 1").fetchall()
        creados = 0
        for cli in clientes:
            try:
                conn.execute("""
                    INSERT INTO recibo (id_cliente, mes, anio, monto, pagado)
                    VALUES (?, ?, ?, ?, 0)
                """, (cli['id'], mes, anio, cls.MONTO_MENSUAL))
                creados += 1
            except:
                pass  # Ya existe (por UNIQUE)
        conn.commit()
        conn.close()
        return creados

    @classmethod
    def listar_por_cliente(cls, id_cliente):
        """Devuelve todos los recibos de un cliente."""
        conn = get_db_connection()
        rows = conn.execute("""
            SELECT * FROM recibo
            WHERE id_cliente = ?
            ORDER BY anio DESC, mes DESC
        """, (id_cliente,)).fetchall()
        conn.close()
        return rows

    @classmethod
    def marcar_pagado(cls, id_cliente, mes, anio):
        """Marca un recibo como pagado."""
        conn = get_db_connection()
        conn.execute("""
            UPDATE recibo
            SET pagado = 1, fecha_pago = date('now')
            WHERE id_cliente = ? AND mes = ? AND anio = ?
        """, (id_cliente, mes, anio))
        conn.commit()
        conn.close()

    @classmethod
    def listar_morosos(cls, mes=None, anio=None):
        """Devuelve lista de clientes morosos (no pagado) del mes/anio."""
        hoy = date.today()
        mes = mes or hoy.month
        anio = anio or hoy.year

        conn = get_db_connection()
        rows = conn.execute("""
            SELECT c.id, c.nombre, c.email, r.mes, r.anio
            FROM cliente c
            JOIN recibo r ON c.id = r.id_cliente
            WHERE r.mes = ? AND r.anio = ? AND r.pagado = 0
            ORDER BY c.nombre
        """, (mes, anio)).fetchall()
        conn.close()
        return rows  # Lista de sqlite3.Row (accesible como dict)