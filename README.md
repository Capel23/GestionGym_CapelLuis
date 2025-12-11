# 🏋️ GymForTheMoment — Sistema de Gestión para Gimnasio  
*Proyecto Individual en Python — Diciembre 2025*

> Aplicación informática para la gestión integral de un gimnasio abierto **24 horas, de lunes a viernes**, con control de reservas, pagos y morosos.

---

## 📋 Índice
- [📌 Requisitos Funcionales](#-requisitos-funcionales)
- [🎬 Diagrama de Casos de Uso](#-diagrama-de-casos-de-uso)
- [📊 Diagrama Entidad-Relación y Normalización](#-diagrama-entidad-relación-y-normalización)
- [⚙️ Tecnologías y Arquitectura](#️-tecnologías-y-arquitectura)
- [🚀 Instrucciones de Ejecución](#-instrucciones-de-ejecución)


---

## 📌 Requisitos Funcionales

| ID | Requisito | Estado |
|----|-----------|--------|
| RF1 | Gestión de clientes (alta, baja, modificación) | ✅ Implementado |
| RF2 | Gestión de aparatos (cada unidad como ID único) | ✅ Implementado |
| RF3 | Reserva de sesiones de 30 min (lunes a viernes, 24h) | ✅ Implementado |
| RF4 | Consulta de disponibilidad por día/aparato/cliente | ✅ Implementado |
| RF5 | Generación automática de recibos mensuales | ✅ Implementado |
| RF6 | Registro de pagos y control de morosos | ✅ Implementado |
| RF7 | Autenticación: login, registro, roles (cliente/admin) | ✅ Implementado |
| RF8 | Clases grupales (Spinning, Yoga, HIIT) | ✅ Bonus implementado |
| RF9 | Exportar morosos a CSV | ✅ Bonus implementado |
| RF10 | Interfaz gráfica moderna con tema oscuro/claro | ✅ Bonus implementado |

---

## 🎬 Diagrama de Casos de Uso

+----------------+
| Administrador |
+----------------+
|
|---[Gestionar Clientes]----------------> (Crear, listar, dar de baja)
|---[Gestionar Aparatos]----------------> (Añadir, listar)
|---[Gestionar Clases]------------------> (Crear clases grupales)
|---[Consultar Morosos]-----------------> (Filtrar por mes/año)
|---[Exportar Morosos a CSV]------------> (Generar archivo)
|
+-------------+
| Cliente |
+-------------+
|
|---[Iniciar Sesión / Registrarse]------> (Autenticación)
|---[Reservar Máquina o Clase]---------> (Seleccionar día, hora, tipo)
|---[Ver Mis Reservas]------------------> (Listado histórico)
|---[Ver Mis Cuotas]--------------------> (Pagadas/Pendientes)
|---[Marcar Cuota como Pagada]----------> (Actualización en BD)


> 📝 **Actor único**: `Usuario` (con roles `cliente` o `admin`). No hay interacción directa del cliente sin login.

---

## 📊 Diagrama Entidad-Relación y Normalización

### Modelo E-R (en texto)

- **Cliente** (1) —< **Usuario** (1)  
  *(Un cliente tiene una cuenta de usuario; un admin no tiene cliente asociado)*
- **Cliente** (1) —< **Sesion** (N)  
- **Cliente** (1) —< **Recibo** (N)  
- **Aparato** (1) —< **Sesion** (N) *(opcional: una sesión puede ser de aparato **o** clase)*  
- **Clase** (1) —< **Sesion** (N)  

### Modelo Relacional (DBML)

```dbml
Table cliente {
  id_cliente int [pk]
  nombre varchar
  email varchar [unique]
  telefono varchar
  activo boolean
}

Table usuario {
  id_usuario int [pk]
  id_cliente int [ref: > cliente.id_cliente, unique, null]
  username varchar [unique]
  password_hash text
  rol varchar [note: "'cliente' o 'admin'"]
}

Table aparato {
  id_aparato int [pk]
  tipo varchar
  nombre varchar [unique]
}

Table clase {
  id_clase int [pk]
  nombre varchar
  instructor varchar
  duracion_min int
  capacidad int
}

Table sesion {
  id_sesion int [pk]
  id_cliente int [ref: > cliente.id_cliente]
  id_aparato int [ref: > aparato.id_aparato, null]
  id_clase int [ref: > clase.id_clase, null]
  dia_semana int [note: '0=Lun, 4=Vie']
  hora_inicio time
  fecha_reserva date
}

Table recibo {
  id_recibo int [pk]
  id_cliente int [ref: > cliente.id_cliente]
  mes int
  anio int
  monto decimal
  pagado boolean
  fecha_pago date [null]
}

Ref: sesion.id_aparato + sesion.dia_semana + sesion.hora_inicio > aparato.id_aparato [delete: restrict]
Ref: sesion.id_clase + sesion.dia_semana + sesion.hora_inicio > clase.id_clase [delete: restrict]

Normalización (3NF cumplida)

1NF
Todos los atributos son atómicos (no hay listas en campos).
2NF
No hay dependencias parciales: claves primarias simples o compuestas completas (ej: (id_cliente, mes, anio) → todos los atributos dependen de toda la PK).
3NF
No hay dependencias transitivas: ej, monto es fijo (no depende del cliente), y no se repite información de cliente en otras tablas.

Capa,Tecnología,Detalle
Interfaz,tkinter + ttk,"GUI moderna, con temas personalizados, icono y validación en tiempo real"
Lógica,Python POO,Clases para todas las entidades (Cliente", "Sesion", "Recibo...)
Persistencia,sqlite3,"BD local robusta con constraints, claves foráneas y transacciones"
Seguridad,hashlib,Contraseñas con PBKDF2-HMAC-SHA256 + sal fija (suficiente para entorno académico)
Extras,csv", "pathlib,"Exportación a CSV, gestión de rutas multiplataforma"

Instrucciones de Ejecución
Requisitos
Python 3.8+
Entorno con tkinter habilitado (viene por defecto en instalaciones estándar)
Pasos
Clonar o descargar el proyecto.
Abrir en Visual Studio (File → Open → Folder).
Ejecutar seed.py (clic derecho → Run Python File):
→ Genera gym.db con datos de ejemplo.
Ejecutar main.py:
→ Se abre la ventana de login.