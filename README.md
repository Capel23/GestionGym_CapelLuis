# 🏋️ GymForTheMoment — Sistema de Gestión para Gimnasio  
*Proyecto Individual en Python — Diciembre 2025*

> Aplicación informática para la gestión integral de un gimnasio abierto **24 horas, de lunes a viernes**, con control de reservas, clases grupales, pagos y morosos.

---

## 📋 Índice
- [📌 Descripción del Proyecto](#-descripción-del-proyecto)
- [✨ Características Principales](#-características-principales)
- [📌 Requisitos Funcionales](#-requisitos-funcionales)
- [🎬 Diagrama de Casos de Uso](#-diagrama-de-casos-de-uso)
- [📊 Diagrama Entidad-Relación y Normalización](#-diagrama-entidad-relación-y-normalización)
- [⚙️ Tecnologías y Arquitectura](#️-tecnologías-y-arquitectura)
- [🚀 Instrucciones de Instalación y Ejecución](#-instrucciones-de-instalación-y-ejecución)
- [🖥️ Descripción de la Interfaz](#️-descripción-de-la-interfaz)
- [🧩 Lógica de Reservas y Pagos](#-lógica-de-reservas-y-pagos)
- [📂 Estructura del Código](#-estructura-del-código)
- [👥 Usuarios de Prueba](#-usuarios-de-prueba)
- [📸 Capturas de Pantalla](#-capturas-de-pantalla)
- [🔮 Mejoras Futuras](#-mejoras-futuras)
- [📝 Autor](#-autor)

---

## 📌 Descripción del Proyecto

`GymForTheMoment` es un sistema de gestión completo para gimnasios que permite:

- **Gestión de clientes**: Alta, consulta, modificación y desactivación de usuarios.
- **Reservas de equipamiento**: Sistema de reservas de máquinas de cardio, pesas y equipamiento funcional en franjas de 30 minutos.
- **Clases grupales**: Programación y reserva de clases como Spinning, Yoga, HIIT y Zumba.
- **Control de pagos**: Generación automática de recibos mensuales, registro de pagos y control de morosos.
- **Panel de administración**: Interfaz completa para gestionar todos los aspectos del gimnasio.
- **Interfaz moderna**: Diseño con tema claro/oscuro, validación en tiempo real y experiencia de usuario optimizada.

El sistema está diseñado para gimnasios que operan **24 horas al día, de lunes a viernes**, permitiendo una gestión eficiente tanto para administradores como para clientes.

---

## ✨ Características Principales

### Para Clientes 👤
- 🔐 **Registro y autenticación segura** con contraseñas hasheadas
- 📅 **Reservas de máquinas** con visualización de disponibilidad en tiempo real
- 🏃 **Clases grupales** con límite de capacidad y horarios semanales fijos
- 💳 **Gestión de cuotas** con historial de pagos y recibos
- 📊 **Historial personal** de todas las reservas realizadas
- 🎨 **Interfaz intuitiva** con indicadores visuales de disponibilidad

### Para Administradores 👨‍💼
- 📋 **Panel completo** con pestañas para cada función
- 👥 **Gestión de clientes**: crear, editar, buscar y desactivar clientes
- 🏋️ **Gestión de aparatos**: añadir y visualizar equipamiento del gimnasio
- 🎓 **Gestión de clases**: crear clases, asignar horarios y controlar capacidad
- 💰 **Control de morosos**: filtrado por mes/año, marcado de pagos, exportación a CSV
- 📈 **Visualización de reservas**: consulta de todas las reservas por día y recurso
- 📄 **Generación de recibos**: creación automática de recibos mensuales para todos los clientes

---

## 📌 Requisitos Funcionales

| ID | Requisito | Descripción | Estado |
|----|-----------|-------------|--------|
| **RF1** | Gestión de clientes | Alta, baja, modificación y búsqueda de clientes | ✅ Implementado |
| **RF2** | Gestión de aparatos | Cada unidad como ID único, categorización por tipo | ✅ Implementado |
| **RF3** | Reserva de sesiones | Slots de 30 min (lunes a viernes, 24h), validación de conflictos | ✅ Implementado |
| **RF4** | Consulta de disponibilidad | Filtrado por día/aparato/cliente con indicadores visuales | ✅ Implementado |
| **RF5** | Generación de recibos | Recibos mensuales automáticos con monto configurable | ✅ Implementado |
| **RF6** | Control de morosos | Registro de pagos, marcado manual, fecha de pago | ✅ Implementado |
| **RF7** | Autenticación | Login, registro, roles (cliente/admin), hash de contraseñas | ✅ Implementado |
| **RF8** | Clases grupales | Spinning, Yoga, HIIT, Zumba con horarios semanales | ✅ Bonus implementado |
| **RF9** | Exportar morosos | Exportación a CSV con filtros de mes/año | ✅ Bonus implementado |
| **RF10** | Interfaz moderna | GUI con tema oscuro/claro, validación, UX optimizada | ✅ Bonus implementado |

---

## 🎬 Diagrama de Casos de Uso

```
┌────────────────┐
│ Administrador  │
└────────────────┘
        │
        ├──[Gestionar Clientes]─────────────▶ (Crear, editar, buscar, desactivar)
        ├──[Gestionar Aparatos]─────────────▶ (Añadir, listar por tipo)
        ├──[Gestionar Clases]───────────────▶ (Crear clases, asignar horarios)
        ├──[Ver Todas las Reservas]─────────▶ (Filtrar por día/recurso)
        ├──[Consultar Morosos]──────────────▶ (Filtrar por mes/año)
        ├──[Generar Recibos Mensuales]──────▶ (Automático para todos los clientes)
        ├──[Marcar Pagos]───────────────────▶ (Actualizar estado de recibos)
        └──[Exportar Morosos a CSV]─────────▶ (Generar archivo descargable)

┌─────────────┐
│   Cliente   │
└─────────────┘
        │
        ├──[Iniciar Sesión / Registrarse]───▶ (Autenticación segura)
        ├──[Reservar Máquina]───────────────▶ (Seleccionar día, hora, aparato)
        ├──[Reservar Clase Grupal]──────────▶ (Inscribirse en horario fijo)
        ├──[Ver Mis Reservas]───────────────▶ (Historial completo)
        ├──[Ver Mis Cuotas]─────────────────▶ (Recibos pagados/pendientes)
        └──[Marcar Cuota como Pagada]───────▶ (Actualización en BD)*

*Funcionalidad limitada a clientes para autogestión de pagos
```

> 📝 **Actor único**: `Usuario` (con roles `cliente` o `admin`). La autenticación es obligatoria para acceder al sistema.

---

## 📊 Diagrama Entidad-Relación y Normalización

### Modelo E-R (Relaciones)

```
┌─────────────┐       ┌──────────────┐
│   Usuario   │──1:1──│   Cliente    │
└─────────────┘       └──────────────┘
                             │
                       ┌─────┴─────┬──────────┐
                       │           │          │
                      1:N         1:N        1:N
                       │           │          │
              ┌─────────────┐ ┌─────────┐ ┌─────────┐
              │   Sesion    │ │ Recibo  │ │  (...)  │
              └─────────────┘ └─────────┘ └─────────┘
                       │
                  ┌────┴─────┐
                  │          │
                 N:1        N:1
                  │          │
         ┌─────────────┐ ┌─────────────────┐
         │   Aparato   │ │     Clase       │
         └─────────────┘ └─────────────────┘
                                  │
                                 1:N
                                  │
                         ┌────────────────┐
                         │ ClaseHorario   │
                         └────────────────┘
```

**Notas sobre relaciones:**
- Un **Cliente** tiene un **Usuario** asociado (1:1), pero un **Admin** solo tiene Usuario
- Una **Sesión** puede ser de **Aparato** (máquina) **o** **Clase** (grupal), pero no ambos
- Las **Clases** tienen múltiples **Horarios** semanales fijos (1:N)

---

### Modelo Relacional (DBML Normalizado)

```dbml
Table cliente {
  id_cliente int [pk, increment]
  nombre varchar(100) [not null]
  email varchar(100) [unique, not null]
  telefono varchar(20)
  activo boolean [default: true]
  fecha_alta date [default: CURRENT_DATE]
}

Table usuario {
  id_usuario int [pk, increment]
  id_cliente int [ref: > cliente.id_cliente, unique, null]
  username varchar(50) [unique, not null]
  password_hash text [not null]
  rol varchar(20) [not null, note: "'cliente' o 'admin'"]
}

Table aparato {
  id_aparato int [pk, increment]
  tipo varchar(50) [not null, note: "Cardio, Pesas, Funcional"]
  nombre varchar(100) [unique, not null]
}

Table clase {
  id_clase int [pk, increment]
  nombre varchar(100) [not null]
  instructor varchar(100)
  duracion_min int [not null]
  capacidad int [not null, note: "Máximo de participantes"]
}

Table clase_horario {
  id_horario int [pk, increment]
  id_clase int [ref: > clase.id_clase]
  dia_semana int [not null, note: "0=Lun, 1=Mar, 2=Mié, 3=Jue, 4=Vie"]
  hora_inicio time [not null]
  
  Indexes {
    (id_clase, dia_semana, hora_inicio) [unique]
  }
}

Table sesion {
  id_sesion int [pk, increment]
  id_cliente int [ref: > cliente.id_cliente, not null]
  id_aparato int [ref: > aparato.id_aparato, null]
  id_clase int [ref: > clase.id_clase, null]
  dia_semana int [not null, note: "0=Lun, 4=Vie"]
  hora_inicio time [not null]
  fecha_reserva date [default: CURRENT_DATE]
  
  Indexes {
    (id_cliente, dia_semana, hora_inicio) [unique, note: "Un cliente no puede estar en 2 sitios"]
    (id_aparato, dia_semana, hora_inicio) [unique, note: "Un aparato solo para 1 persona"]
  }
  
  Note: "CHECK: (id_aparato IS NULL AND id_clase IS NOT NULL) OR (id_aparato IS NOT NULL AND id_clase IS NULL)"
}

Table recibo {
  id_recibo int [pk, increment]
  id_cliente int [ref: > cliente.id_cliente, not null]
  mes int [not null, note: "1-12"]
  anio int [not null]
  monto decimal(10,2) [default: 40.00]
  pagado boolean [default: false]
  fecha_pago date [null]
  
  Indexes {
    (id_cliente, mes, anio) [unique]
  }
}
```

---

### Normalización (3NF Cumplida) ✅

| Forma Normal | Criterio | Cumplimiento |
|--------------|----------|--------------|
| **1NF** | Todos los atributos son atómicos | ✅ No hay listas en campos |
| **2NF** | No hay dependencias parciales | ✅ Todas las claves primarias son simples o las dependencias son de toda la PK |
| **3NF** | No hay dependencias transitivas | ✅ No se repite información derivable (ej: nombre de cliente en sesión, se accede via FK) |

**Ejemplos de normalización aplicada:**
- `sesion` no almacena `nombre_cliente`, sino `id_cliente` (FK)
- `recibo.monto` es un valor base, no calculado de otros campos
- `clase_horario` separa los horarios semanales de la clase en tabla aparte (evitar listas)

---

## ⚙️ Tecnologías y Arquitectura

### Stack Tecnológico

| Capa | Tecnología | Detalle |
|------|------------|---------|
| **Interfaz** | `tkinter` + `ttk` | GUI moderna con temas personalizados (claro/oscuro), validación en tiempo real |
| **Lógica** | Python POO | Clases para todas las entidades (`Cliente`, `Sesion`, `Recibo`, `Aparato`, `Clase`) |
| **Persistencia** | `sqlite3` | BD local robusta con constraints, claves foráneas y transacciones ACID |
| **Seguridad** | `hashlib` (PBKDF2-HMAC-SHA256) | Contraseñas con hash + sal (100,000 iteraciones) |
| **Extras** | `csv`, `pathlib`, `datetime` | Exportación a CSV, gestión de rutas multiplataforma, manejo de fechas |

---

### Arquitectura en 3 Capas

```
┌─────────────────────────────────────┐
│     CAPA DE PRESENTACIÓN (UI)       │
│  login.py, cliente.py, admin_ui.py  │  ← Tkinter/ttk
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│      CAPA DE LÓGICA (MODELS)        │
│  usuario.py, cliente.py, sesion.py  │  ← POO + Validaciones
│  aparato.py, clase.py, recibo.py    │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   CAPA DE DATOS (DATABASE)          │
│  database.py, gym.db (SQLite)       │  ← SQL + Constraints
└─────────────────────────────────────┘
```

**Ventajas de esta arquitectura:**
- 🔄 **Separación de responsabilidades**: cada capa tiene un propósito claro
- 🛡️ **Robustez**: validaciones en modelo + constraints en BD
- 🔧 **Mantenibilidad**: cambios en UI no afectan lógica de negocio
- 🧪 **Testeable**: cada capa se puede probar de forma independiente

---

## 🚀 Instrucciones de Instalación y Ejecución

### Requisitos Previos

- **Python 3.8+** (recomendado: Python 3.10 o superior)
- Sistema operativo: Windows, macOS o Linux
- `tkinter` habilitado (viene por defecto en instalaciones estándar de Python)

### Verificar instalación de Python

```bash
python --version
# o
python3 --version
```

### Verificar tkinter

```bash
python -m tkinter
# Debe abrir una ventana de prueba
```

---

### Pasos de Instalación

#### 1️⃣ Clonar o descargar el proyecto

```bash
git clone https://github.com/tuusuario/GymForTheMoment.git
cd GymForTheMoment
```

O descargar el ZIP y extraer en una carpeta.

---

#### 2️⃣ Ejecutar el script de inicialización (seed)

Este script crea la base de datos `gym.db` con datos de ejemplo:

```bash
python seed.py
```

**Salida esperada:**
```
✅ Base de datos inicializada correctamente.
🔄 Creando reservas de ejemplo...
✅ 10 reservas de ejemplo creadas.
✅ 5 recibos generados para diciembre 2025.

✅ Datos de ejemplo listos.
🔐 Usuarios:
   Cliente: user1–user5 | Contraseña: 1234
   Admin: admin | Contraseña: admin123

▶️ Ahora ejecuta `main.py` para iniciar la app.
```

**Datos de ejemplo incluidos:**
- 5 clientes de prueba (`user1` a `user5`)
- 2 administradores (`admin`, `jefe`)
- 30+ aparatos de gimnasio (cintas, bicicletas, pesas, etc.)
- 4 clases grupales (Spinning, Yoga, HIIT, Zumba)
- Horarios semanales para cada clase
- 10 reservas de ejemplo
- Recibos mensuales con algún pago marcado

---

#### 3️⃣ Ejecutar la aplicación

```bash
python main.py
```

Se abrirá la ventana de login de `GymForTheMoment`.

---

### Estructura de Archivos Generados

```
GymForTheMoment/
├── gym.db              # ← Base de datos SQLite (generada por seed.py)
├── morosos_YYYY_MM.csv # ← Exportaciones CSV (generadas al exportar)
```

---

## 🖥️ Descripción de la Interfaz

### Pantalla de Login 🔐

- **Funciones:**
  - Inicio de sesión con usuario y contraseña
  - Registro de nuevos clientes
  - Validación de credenciales en tiempo real
  - Redirección automática según rol (cliente/admin)

- **Validaciones:**
  - Usuario no vacío
  - Contraseña mínima (configurable)
  - Usuario único en registro
  - Contraseñas hasheadas con PBKDF2

---

### Panel de Cliente 👤

#### Pestaña: Reservar 📅
- **Vista de aparatos:**
  - Organización por tipo (Cardio, Pesas, Funcional)
  - Tarjetas clickeables con indicador de disponibilidad (🟢 disponible, 🟡 ocupado)
  - Selector de día (lunes a viernes) y hora (slots de 30 min, 00:00-23:30)
  - Confirmación de reserva con validación de conflictos

- **Vista de clases:**
  - Tarjetas con información completa (instructor, duración, capacidad)
  - Horarios semanales fijos mostrados claramente
  - Indicador de plazas disponibles en tiempo real
  - Inscripción con un click

#### Pestaña: Mis Reservas 📋
- Listado completo de reservas (aparatos y clases)
- Información detallada: recurso, día, hora, fecha de reserva
- Ordenado por fecha

#### Pestaña: Mis Cuotas 💳
- Historial de recibos (mes, año, monto)
- Estados: ✅ Pagado (con fecha) o ❌ Pendiente
- Botón para marcar como pagado (autogestión)*
- Cálculo automático de deuda total

---

### Panel de Administrador 👨‍💼

#### Pestaña: Clientes 👥
- **Funciones:**
  - ➕ Crear nuevos clientes (nombre, email, teléfono)
  - 🔍 Buscar por nombre, email o teléfono
  - ✏️ Editar información de cliente
  - 🚫 Desactivar clientes (soft delete, no elimina de BD)
  - 📊 Ver estadísticas (total activos, inactivos)

- **Tabla:**
  - Columnas: ID, Nombre, Email, Teléfono, Estado
  - Indicadores visuales por estado (✅ Activo, ❌ Inactivo)
  - Scroll para muchos registros

#### Pestaña: Aparatos 🏋️
- **Funciones:**
  - ➕ Añadir nuevos aparatos (tipo, nombre único)
  - 📋 Listar todos los aparatos agrupados por tipo
  - 🔢 Contador de aparatos por categoría

- **Tipos disponibles:**
  - Cardio (cintas, bicicletas, elípticas, remo, escaladora)
  - Pesas (press banca, leg press, Smith machine, dorsales, etc.)
  - Funcional (TRX, kettlebells, battle ropes)

#### Pestaña: Clases 🎓
- **Funciones:**
  - ➕ Crear clases (nombre, instructor, duración, capacidad)
  - 📅 Asignar horarios semanales (día + hora)
  - 📋 Listar clases con todos sus horarios
  - 🔢 Ver capacidad máxima y reservas actuales

- **Validaciones:**
  - No duplicar horarios para la misma clase
  - Duración entre 30-120 minutos
  - Capacidad mínima de 1 persona

#### Pestaña: Reservas 📆
- **Funciones:**
  - 🔍 Filtrar reservas por día de la semana
  - 📊 Ver todas las reservas (aparatos y clases)
  - 👤 Identificar cliente, recurso, hora
  - 📅 Ordenar por día y hora

- **Vista:**
  - Tabla completa con: Cliente, Tipo (Aparato/Clase), Recurso, Día, Hora
  - Diferenciación visual entre tipos de reserva

#### Pestaña: Pagos y Recibos 💰
- **Funciones:**
  - 🏭 Generar recibos mensuales para todos los clientes activos
  - 🔍 Filtrar morosos por mes y año
  - ✅ Marcar recibos como pagados manualmente
  - 📄 Ver todos los recibos (pagados y pendientes)
  - 📊 Exportar morosos a CSV con formato: `morosos_YYYY_MM.csv`

- **Vista de morosos:**
  - Cliente, Mes, Año, Monto, Estado, Fecha Pago
  - Indicadores visuales (❌ Pendiente, ✅ Pagado)
  - Estadísticas: total deudores, monto adeudado

- **Exportación CSV:**
  ```csv
  Cliente,Mes,Año,Monto,Pagado,Fecha Pago
  María Gómez,12,2025,40.00,False,
  Pablo Díaz,12,2025,40.00,False,
  ```

---

## 🧩 Lógica de Reservas y Pagos

### Sistema de Reservas 📅

#### Reglas de Negocio

1. **Horario del gimnasio:**
   - Lunes a Viernes (días 0-4)
   - 24 horas: 00:00 - 23:30
   - Slots de 30 minutos

2. **Restricciones por cliente:**
   - ❌ No puede tener 2 reservas a la misma hora (mismo día/hora)
   - ✅ Puede reservar múltiples recursos en días/horas diferentes
   - ✅ Puede tener reservas de aparatos y clases simultáneamente (si no coinciden en horario)

3. **Restricciones por aparato:**
   - ❌ Solo 1 persona por aparato en cada franja de 30 min
   - ✅ Validación en BD con constraint UNIQUE (id_aparato, dia_semana, hora_inicio)

4. **Restricciones por clase:**
   - ❌ Capacidad máxima definida (ej: Spinning = 10 personas)
   - ✅ Horarios fijos semanales (tabla `clase_horario`)
   - ✅ Validación de plazas disponibles en tiempo real

---

#### Flujo de Reserva

```
Usuario selecciona APARATO/CLASE
            ↓
    ¿Horario disponible?
       /         \
     NO          SÍ
      ↓           ↓
  ❌ Error   Confirmar reserva
              ↓
        Insertar en BD
              ↓
      ✅ Reserva exitosa
```

**Validaciones en código:**
- `Sesion.reservar()` hace validación de conflictos antes de insertar
- Manejo de excepciones `sqlite3.IntegrityError` para constraints
- Mensajes en UI con `messagebox` (tkinter)

---

### Sistema de Pagos 💳

#### Generación de Recibos

1. **Automático mensual:**
   - Admin ejecuta "Generar recibos del mes"
   - Se crean recibos para **todos los clientes activos**
   - Monto fijo: 40.00 € (configurable en `Recibo.MONTO_DEFECTO`)
   - Solo si no existe ya un recibo para ese cliente en ese mes/año

2. **Campos del recibo:**
   - `id_cliente`: FK a cliente
   - `mes`, `anio`: periodo de facturación
   - `monto`: cantidad a pagar
   - `pagado`: booleano (False por defecto)
   - `fecha_pago`: se rellena al marcar como pagado

---

#### Control de Morosos

**Definición:** Cliente con al menos 1 recibo `pagado = False`.

**Consulta de morosos:**
```sql
SELECT c.nombre, r.mes, r.anio, r.monto, r.fecha_pago
FROM recibo r
JOIN cliente c ON r.id_cliente = c.id_cliente
WHERE r.pagado = 0 AND r.mes = ? AND r.anio = ?
ORDER BY c.nombre
```

**Exportación a CSV:**
- Formato: `morosos_YYYY_MM.csv`
- Ubicación: misma carpeta del proyecto
- Contenido: Cliente, Mes, Año, Monto, Estado Pagado, Fecha Pago

---

## 📂 Estructura del Código

```
GymForTheMoment/
│
├── 📄 main.py                 # ← PUNTO DE ENTRADA
│   └── Inicializa DB, configura ventana principal, carga LoginUI
│
├── 📄 database.py             # ← Gestión de BD SQLite
│   ├── init_db()              # Crea todas las tablas con constraints
│   └── get_db_connection()    # Conexión singleton
│
├── 📄 auth.py                 # ← Lógica de autenticación
│   ├── hash_password()        # PBKDF2-HMAC-SHA256 + sal
│   └── verify_password()      # Validación de credenciales
│
├── 📄 utils.py                # ← Utilidades generales
│   └── set_theme()            # Tema claro/oscuro para ttk
│
├── 📄 seed.py                 # ← Script de datos de ejemplo
│   └── Crea aparatos, clases, usuarios, reservas, recibos
│
├── 📁 models/                 # ← Entidades del negocio (POO)
│   ├── __init__.py
│   ├── usuario.py             # Usuario (cliente/admin)
│   ├── cliente.py             # Cliente (info personal)
│   ├── aparato.py             # Máquinas del gym
│   ├── clase.py               # Clases grupales
│   ├── clase_horario.py       # Horarios semanales de clases
│   ├── sesion.py              # Reservas (aparatos + clases)
│   └── recibo.py              # Recibos mensuales + pagos
│
├── 📁 ui/                     # ← Interfaces gráficas (Tkinter)
│   ├── __init__.py
│   ├── login.py               # Pantalla de login + registro
│   ├── cliente.py             # Panel de cliente (3 pestañas)
│   └── admin_ui.py            # Panel de admin (5 pestañas)
│
├── 📁 assets/                 # ← Recursos (iconos, imágenes)
│   └── gym_icon.ico           # Icono de la ventana
│
└── 📄 README.md               # ← Documentación (este archivo)
```

---

### Descripción de Archivos Clave

#### `main.py`
- **Responsabilidad:** iniciar la aplicación
- **Funciones:**
  - Llama a `init_db()` para crear/verificar la BD
  - Configura ventana raíz de tkinter (título, tamaño, icono)
  - Carga `LoginUI` como primera pantalla
  - Inicia el loop principal (`mainloop()`)

#### `database.py`
- **Responsabilidad:** configuración y conexión a SQLite
- **Funciones:**
  - `init_db()`: ejecuta DDL (CREATE TABLE) con constraints
  - `get_db_connection()`: retorna conexión con foreign_keys=ON
- **Tablas creadas:**
  - `cliente`, `usuario`, `aparato`, `clase`, `clase_horario`, `sesion`, `recibo`

#### `models/sesion.py`
- **Responsabilidad:** lógica de reservas
- **Métodos principales:**
  - `Sesion.reservar(id_cliente, id_aparato=None, id_clase=None, dia_semana, hora_inicio)`
    - Valida que solo se pase aparato O clase (no ambos)
    - Verifica disponibilidad (no conflicto de horario)
    - Inserta en BD y maneja excepciones
  - `Sesion.obtener_reservas_cliente(id_cliente)`
    - Retorna todas las reservas de un cliente
  - `Sesion.check_disponibilidad_aparato(id_aparato, dia, hora)`
    - Retorna True si el aparato está libre en ese slot

#### `models/recibo.py`
- **Responsabilidad:** gestión de pagos
- **Métodos principales:**
  - `Recibo.generar_recibos_mes(mes, anio)`
    - Crea recibos para todos los clientes activos (si no existen)
  - `Recibo.obtener_morosos(mes=None, anio=None)`
    - Retorna recibos no pagados, con filtro opcional
  - `Recibo.marcar_pagado(id_cliente, mes, anio)`
    - Actualiza `pagado=1` y `fecha_pago=CURRENT_DATE`

#### `ui/admin_ui.py`
- **Responsabilidad:** interfaz completa de administrador
- **Estructura:** 5 pestañas (Notebook de ttk)
  - Clientes, Aparatos, Clases, Reservas, Pagos
- **Características:**
  - Uso de Treeview para tablas
  - Formularios con validación
  - Botones de acción con confirmación
  - Exportación a CSV

---

## 👥 Usuarios de Prueba

Una vez ejecutado `seed.py`, puedes iniciar sesión con:

### Clientes 👤
| Usuario | Contraseña | Cliente Asociado |
|---------|------------|------------------|
| `user1` | `1234` | María Gómez |
| `user2` | `1234` | Javier Ruiz |
| `user3` | `1234` | Lucía Fernández |
| `user4` | `1234` | Pablo Díaz |
| `user5` | `1234` | Elena Sánchez |

### Administradores 👨‍💼
| Usuario | Contraseña |
|---------|------------|
| `admin` | `admin123` |
| `jefe` | `gym2025` |

---

## 📸 Capturas de Pantalla

> 💡 **Nota:** Esta sección puede incluir screenshots de la aplicación en funcionamiento. Puedes añadir imágenes en `assets/screenshots/` y referenciarlas aquí:

```markdown
![Login Screen](assets/screenshots/login.png)
![Client Panel](assets/screenshots/client_panel.png)
![Admin Panel](assets/screenshots/admin_panel.png)
```

---

## 🔮 Mejoras Futuras

Posibles extensiones del proyecto:

### Funcionalidades
- [ ] 📧 **Notificaciones por email** al generar recibos o reservar clases
- [ ] 📊 **Dashboard con estadísticas** (reservas por día, ingresos mensuales, ocupación)
- [ ] 🎫 **Sistema de bonos** (packs de 10 sesiones)
- [ ] 📱 **Aplicación móvil** (React Native / Flutter)
- [ ] 🔔 **Recordatorios** de clases 1 hora antes (push notifications)
- [ ] ⭐ **Sistema de valoraciones** de clases e instructores
- [ ] 📅 **Calendario visual** para ver disponibilidad semanal
- [ ] 🏆 **Gamificación** (logros por asistencia, rankings)

### Técnicas
- [ ] 🔐 **Autenticación OAuth2** (login con Google/Facebook)
- [ ] ☁️ **Migración a PostgreSQL/MySQL** para multi-usuario
- [ ] 🌐 **API REST** (FastAPI) para separar backend/frontend
- [ ] 🐳 **Dockerización** del proyecto
- [ ] 🧪 **Tests unitarios** (pytest) con >80% cobertura
- [ ] 📝 **Logs con logging** (auditoría de operaciones)
- [ ] 🔄 **Sistema de backup automático** de la BD

### UX/UI
- [ ] 🎨 **Más temas** (modo oscuro mejorado, modo alto contraste)
- [ ] 🌍 **Internacionalización** (i18n: inglés, francés)
- [ ] ♿ **Accesibilidad** (lectores de pantalla, atajos de teclado)
- [ ] 📱 **Diseño responsive** (adaptar a diferentes resoluciones)

---

## 📝 Autor

**Luis Capel** — *Estudiante de Desarrollo de Aplicaciones Multiplataforma*

- 📧 Email: [tu-email@example.com]
- 💼 LinkedIn: [linkedin.com/in/tuusuario]
- 🐙 GitHub: [@Capel23](https://github.com/Capel23)

---

### 📄 Licencia

Este proyecto fue desarrollado como trabajo académico para el módulo de **Programación** (DAM, 1º curso) en diciembre de 2025.

Si deseas usar este código como referencia, por favor da crédito al autor original.

---

### 🙏 Agradecimientos

- **Profesores del módulo** por las directrices del proyecto
- **Comunidad de Stack Overflow** por resolver dudas de tkinter
- **Documentación oficial de Python** (sqlite3, hashlib, tkinter)

---

<div align="center">

**🏋️ ¡Gracias por usar GymForTheMoment! 🏋️**

Si tienes preguntas o sugerencias, no dudes en abrir un issue en GitHub.

*Hecho con ❤️ y ☕ en Python*

</div>