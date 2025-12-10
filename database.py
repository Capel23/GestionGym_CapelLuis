# database.py
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "gym.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Acceso por nombre: row['nombre']
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Usuarios (clientes y admins)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER UNIQUE,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            rol TEXT CHECK(rol IN ('cliente', 'admin')) NOT NULL DEFAULT 'cliente'
        )
    ''')

    # Clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cliente (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            telefono TEXT,
            activo BOOLEAN DEFAULT 1
        )
    ''')

    # Aparatos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS aparato (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            nombre TEXT NOT NULL UNIQUE
        )
    ''')

    # Clases grupales
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clase (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            instructor TEXT NOT NULL,
            duracion_min INTEGER DEFAULT 45,
            capacidad INTEGER DEFAULT 12
        )
    ''')

    # Sesiones (reservas: máquina O clase)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sesion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER NOT NULL,
            id_aparato INTEGER,            -- NULL si es clase
            id_clase INTEGER,              -- NULL si es máquina
            dia_semana INTEGER NOT NULL CHECK(dia_semana BETWEEN 0 AND 4),
            hora_inicio TEXT NOT NULL,
            fecha_reserva DATE DEFAULT (date('now')),
            FOREIGN KEY(id_cliente) REFERENCES cliente(id),
            FOREIGN KEY(id_aparato) REFERENCES aparato(id),
            FOREIGN KEY(id_clase) REFERENCES clase(id),
            CHECK((id_aparato IS NOT NULL AND id_clase IS NULL) OR (id_clase IS NOT NULL AND id_aparato IS NULL)),
            UNIQUE(id_aparato, dia_semana, hora_inicio),
            UNIQUE(id_clase, dia_semana, hora_inicio)
        )
    ''')

    # Recibos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recibo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER NOT NULL,
            mes INTEGER NOT NULL CHECK(mes BETWEEN 1 AND 12),
            anio INTEGER NOT NULL,
            monto REAL NOT NULL,
            pagado BOOLEAN DEFAULT 0,
            fecha_pago DATE,
            FOREIGN KEY(id_cliente) REFERENCES cliente(id),
            UNIQUE(id_cliente, mes, anio)
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Base de datos inicializada.")