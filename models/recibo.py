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
    def marcar_pagado(cls, id_cliente, mes, anio, fecha_pago=None):
        """Marca un recibo como pagado. Retorna True si tuvo éxito."""
        conn = get_db_connection()
        try:
            if fecha_pago:
                conn.execute("""
                    UPDATE recibo
                    SET pagado = 1, fecha_pago = ?
                    WHERE id_cliente = ? AND mes = ? AND anio = ?
                """, (fecha_pago, id_cliente, mes, anio))
            else:
                conn.execute("""
                    UPDATE recibo
                    SET pagado = 1, fecha_pago = date('now')
                    WHERE id_cliente = ? AND mes = ? AND anio = ?
                """, (id_cliente, mes, anio))
            conn.commit()
            return True
        except:
            return False
        finally:
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

    @classmethod
    def listar_todos(cls, filtro_estado=None, filtro_mes=None, filtro_anio=None, id_cliente=None):
        """Lista todos los recibos con filtros opcionales.
        
        Args:
            filtro_estado: 'pagado', 'pendiente' o None para todos
            filtro_mes: mes específico o None
            filtro_anio: año específico o None
            id_cliente: ID de cliente específico o None
        """
        conn = get_db_connection()
        
        query = """
            SELECT r.*, c.nombre AS cliente_nombre, c.email AS cliente_email
            FROM recibo r
            JOIN cliente c ON r.id_cliente = c.id
            WHERE 1=1
        """
        
        params = []
        
        if filtro_estado == 'pagado':
            query += " AND r.pagado = 1"
        elif filtro_estado == 'pendiente':
            query += " AND r.pagado = 0"
        
        if filtro_mes is not None:
            query += " AND r.mes = ?"
            params.append(filtro_mes)
        
        if filtro_anio is not None:
            query += " AND r.anio = ?"
            params.append(filtro_anio)
        
        if id_cliente is not None:
            query += " AND r.id_cliente = ?"
            params.append(id_cliente)
        
        query += " ORDER BY r.anio DESC, r.mes DESC, c.nombre"
        
        rows = conn.execute(query, params).fetchall()
        conn.close()
        return rows

    @classmethod
    def get_ultimo_pago(cls, id_cliente):
        """Obtiene el último recibo pagado de un cliente."""
        conn = get_db_connection()
        row = conn.execute("""
            SELECT * FROM recibo
            WHERE id_cliente = ? AND pagado = 1
            ORDER BY anio DESC, mes DESC
            LIMIT 1
        """, (id_cliente,)).fetchone()
        conn.close()
        return row