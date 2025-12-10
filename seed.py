# seed.py
from database import init_db, get_db_connection
from models.usuario import Usuario
from models.cliente import Cliente
from models.aparato import Aparato
from models.clase import Clase
from models.recibo import Recibo

def seed_data():
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()

    # Aparatos
    aparatos = [
        ("Cinta", "Cinta01"), ("Cinta", "Cinta02"),
        ("Bicicleta", "Bici01"), ("Bicicleta", "Bici02"),
        ("Pesas", "Prensa01"), ("Pesas", "JSmith01")
    ]
    for tipo, nombre in aparatos:
        cursor.execute("INSERT OR IGNORE INTO aparato (tipo, nombre) VALUES (?, ?)", (tipo, nombre))

    # Clases grupales
    clases = [
        ("Spinning Energético", "Ana M.", 45, 10),
        ("Yoga Restaurativo", "Carlos R.", 60, 15),
        ("HIIT Total", "Laura K.", 30, 12)
    ]
    for nombre, inst, dur, cap in clases:
        cursor.execute("""
            INSERT OR IGNORE INTO clase (nombre, instructor, duracion_min, capacidad)
            VALUES (?, ?, ?, ?)
        """, (nombre, inst, dur, cap))

    # Clientes + Usuarios
    clientes_data = [
        {"nombre": "María Gómez", "email": "maria@email.com", "telefono": "600111222"},
        {"nombre": "Javier Ruiz", "email": "javier@email.com", "telefono": "600333444"},
        {"nombre": "Lucía Fernández", "email": "lucia@email.com", "telefono": "600555666"},
        {"nombre": "Pablo Díaz", "email": "pablo@email.com", "telefono": "600777888"},
        {"nombre": "Elena Sánchez", "email": "elena@email.com", "telefono": "600999000"},
    ]
    for i, data in enumerate(clientes_data, 1):
        try:
            Usuario.create_cliente(f"user{i}", "1234", data)
        except Exception as e:
            print(f"⚠️ Error al crear user{i}: {e}")

    # Admins
    try:
        Usuario.create_admin("admin", "admin123")
        Usuario.create_admin("jefe", "gym2025")
    except Exception as e:
        print(f"⚠️ Error al crear admins: {e}")

    # Recibos del mes actual (diciembre 2025)
    # Solo generamos si no existen
    try:
        creados = Recibo.generar_recibos_mes(mes=12, anio=2025)
        # Marcamos algunos como pagados
        for i in range(1, 6):  # 5 clientes
            if i % 2 == 0:  # pares pagados
                Recibo.marcar_pagado(i, 12, 2025)
        print(f"✅ {creados} recibos generados para diciembre 2025.")
    except Exception as e:
        print(f"⚠️ Error al generar recibos: {e}")

    conn.close()
    print("\n✅ Datos de ejemplo listos.")
    print("🔐 Usuarios:")
    print("   Cliente: user1–user5 | Contraseña: 1234")
    print("   Admin: admin | Contraseña: admin123")
    print("\n▶️ Ahora ejecuta `main.py` para iniciar la app.")

if __name__ == "__main__":
    seed_data()