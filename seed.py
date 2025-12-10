# seed.py
from database import init_db, get_db_connection
from models.usuario import Usuario
from models.cliente import Cliente
from models.aparato import Aparato
from models.clase import Clase
from models.clase_horario import ClaseHorario
from models.recibo import Recibo

def seed_data():
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()

    # Aparatos - Lista completa de máquinas del gimnasio
    aparatos = [
        # Cardio
        ("Cinta", "Cinta01"), ("Cinta", "Cinta02"), ("Cinta", "Cinta03"), ("Cinta", "Cinta04"),
        ("Bicicleta", "Bici01"), ("Bicicleta", "Bici02"), ("Bicicleta", "Bici03"), 
        ("Bicicleta", "Bici04"), ("Bicicleta", "Bici05"),
        ("Elíptica", "Eliptica01"), ("Elíptica", "Eliptica02"), ("Elíptica", "Eliptica03"),
        ("Remo", "Remo01"), ("Remo", "Remo02"), ("Remo", "Remo03"),
        ("Escaladora", "Escaladora01"), ("Escaladora", "Escaladora02"),
        
        # Pesas y Fuerza
        ("Pesas", "Press Banca 01"), ("Pesas", "Press Banca 02"),
        ("Pesas", "Leg Press 01"), ("Pesas", "Leg Press 02"),
        ("Pesas", "Smith Machine 01"), ("Pesas", "Smith Machine 02"),
        ("Pesas", "Dorsales 01"), ("Pesas", "Dorsales 02"),
        ("Pesas", "Pectoral 01"), ("Pesas", "Hombros 01"),
        ("Pesas", "Curl Bíceps 01"), ("Pesas", "Extensión Tríceps 01"),
        ("Funcional", "TRX 01"), ("Funcional", "TRX 02"),
        ("Funcional", "Kettlebells"), ("Funcional", "Battle Ropes")
    ]
    for tipo, nombre in aparatos:
        cursor.execute("INSERT OR IGNORE INTO aparato (tipo, nombre) VALUES (?, ?)", (tipo, nombre))

    # Clases grupales
    clases = [
        ("Spinning Energético", "Ana M.", 45, 10),
        ("Yoga Restaurativo", "Carlos R.", 60, 15),
        ("HIIT Total", "Laura K.", 30, 12),
        ("Zumba Fitness", "María S.", 50, 20)
    ]
    for nombre, inst, dur, cap in clases:
        cursor.execute("""
            INSERT OR IGNORE INTO clase (nombre, instructor, duracion_min, capacidad)
            VALUES (?, ?, ?, ?)
        """, (nombre, inst, dur, cap))

    # Horarios de clases (programación semanal)
    # Días: 0=Lun, 1=Mar, 2=Mié, 3=Jue, 4=Vie
    conn.commit()  # Commit para obtener los IDs
    
    horarios_clases = [
        # Spinning Energético (id=1): Martes y Jueves 19:00
        (1, 1, "19:00"), (1, 3, "19:00"),
        # Yoga Restaurativo (id=2): Lunes, Miércoles y Viernes 18:00
        (2, 0, "18:00"), (2, 2, "18:00"), (2, 4, "18:00"),
        # HIIT Total (id=3): Lunes 20:00, Viernes 18:30
        (3, 0, "20:00"), (3, 4, "18:30"),
        # Zumba Fitness (id=4): Martes 18:30, Jueves 18:00, Viernes 19:30
        (4, 1, "18:30"), (4, 3, "18:00"), (4, 4, "19:30")
    ]
    for id_clase, dia, hora in horarios_clases:
        cursor.execute("""
            INSERT OR IGNORE INTO clase_horario (id_clase, dia_semana, hora_inicio)
            VALUES (?, ?, ?)
        """, (id_clase, dia, hora))

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

    # Reservas de ejemplo para mostrar máquinas ocupadas
    print("\n🔄 Creando reservas de ejemplo...")
    from models.sesion import Sesion
    
    reservas_ejemplo = [
        # Cliente 1: Lunes
        (1, 1, None, 0, "10:00"),   # Cinta01, Lunes 10:00
        (1, 3, None, 0, "10:30"),   # Bici01, Lunes 10:30
        # Cliente 2: Martes
        (2, 2, None, 1, "18:00"),   # Cinta02, Martes 18:00
        (2, 11, None, 1, "19:00"),  # Eliptica01, Martes 19:00
        # Cliente 3: Miércoles
        (3, 5, None, 2, "12:00"),   # Bici03, Miércoles 12:00
        (3, 13, None, 2, "17:00"),  # Remo01, Miércoles 17:00
        # Cliente 4: Jueves
        (4, 17, None, 3, "15:00"),  # Press Banca 01, Jueves 15:00
        (4, 19, None, 3, "16:00"),  # Leg Press 01, Jueves 16:00
        # Cliente 5: Viernes
        (5, 4, None, 4, "11:00"),   # Cinta04, Viernes 11:00
        (5, 9, None, 4, "12:00"),   # Bici05, Viernes 12:00
    ]
    
    for id_cliente, id_aparato, id_clase, dia, hora in reservas_ejemplo:
        try:
            Sesion.reservar(id_cliente, id_aparato=id_aparato, id_clase=id_clase, 
                          dia_semana=dia, hora_inicio=hora)
        except Exception as e:
            pass  # Ignorar duplicados
    
    print(f"✅ {len(reservas_ejemplo)} reservas de ejemplo creadas.")
    
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