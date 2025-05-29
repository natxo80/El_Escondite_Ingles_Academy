![Logo de la Academia](resources/el_escondite_ingles.jpg)

# El Escondite Inglés - Gestión de Academia

Aplicación de escritorio desarrollada en Python con PySide2/PySide6 para la gestión interna de una academia de inglés. Permite controlar alumnos, niveles, clases, pagos, recompensas y usuarios, todo desde una interfaz gráfica intuitiva.

---

## Índice

- [Descripción general](#descripción-general)
- [Tecnologías utilizadas](#tecnologías-utilizadas)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Base de datos](#base-de-datos)
- [Funcionalidades principales](#funcionalidades-principales)
- [Instalación y ejecución](#instalación-y-ejecución)
- [Pruebas y validación](#pruebas-y-validación)
- [Capturas de pantalla (opcional)](#capturas-de-pantalla-opcional)
- [Licencia](#licencia)

---

## Descripción general

Este proyecto fue desarrollado como aplicación final del ciclo formativo de Desarrollo de Aplicaciones Multiplataforma. Tiene como objetivo facilitar la gestión completa de una academia de inglés en local, sin depender de servidores externos.

La app ofrece un sistema de autenticación con dos roles:

- `admin`: acceso completo a todas las funcionalidades.
- `user`: acceso limitado (solo cerrar sesión).

---

## Tecnologías utilizadas

- Python 3.8+
- PySide2 
- SQLite3
- Estilo personalizado con QSS
- openpyxl (para exportar Excel)
- pytest (para pruebas unitarias)
- dateutil (para manejo de fechas)

---

## Estructura del proyecto

```
Proyecto/
│
├── db/
│   ├── __init__.py  
│   ├── database.py          # Lógica de conexión y operaciones en base de datos
│   └── el_escondite_ingles.db
│
├── resources/
│   ├── el_escondite_ingles.bmp  
│   ├── el_escondite_ingles.jpg
│   └── styles.qss
│
├── test/
│   └── test_database.py     # Pruebas unitarias con pytest
│
├── ui/
│   ├── __init__.py 
│   ├── login_window.py
│   ├── main_window.py 
│   ├── manage_classes_window.py
│   ├── manage_levels_window.py
│   ├── manage_payments_window.py
│   ├── manage_rewards_window.py
│   ├── manage_students_window.py 
│   └── manage_users_window.py
│
├── init_db.py               # Script para inicializar la base de datos con usuario admin
├── main.py
├── pytest.ini
└── README.md 
```

---

## Base de datos

Base de datos SQLite local con las siguientes tablas principales:

- `students`: Alumnos de la academia
- `levels`: Niveles de inglés (A1–C2, infantil y adultos)
- `classes`: Clases programadas
- `payments`: Pagos realizados por alumnos
- `rewards`: Recompensas por traer nuevos alumnos
- `users`: Autenticación y gestión de accesos

---

## Funcionalidades principales

- Autenticación de usuarios con roles
- Gestión de alumnos: alta, edición, búsqueda y eliminación
- Gestión de niveles
- Gestión de clases
- Gestión de pagos y filtrado
- Gestión de recompensas por recomendación
- Exportación a CSV y Excel
- Backup y restauración de base de datos
- Gestión de usuarios (solo para administradores)
- Pruebas unitarias con `pytest`

---

## Instalación y ejecución

1. Clona el repositorio:

   ```bash
   git clone https://github.com/tu_usuario/academia-ingles.git
   cd academia-ingles
   ```

2. Crea un entorno virtual e instálalo todo:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Ejecuta el programa:

   ```bash
   python main.py
   ```

> El primer usuario se puede crear mediante `init_db.py` o desde la interfaz si ya tienes permisos de admin.

---

## Pruebas y validación

El archivo `test/test_database.py` contiene pruebas para:

- Inserción, modificación y eliminación de alumnos, niveles y pagos.
- Recompensas activas y expiradas.
- Detección de errores comunes como duplicados.
- Validación de lógica de bonificaciones.

Para ejecutarlas:

```bash
   pytest
```

---

## Capturas de pantalla (opcional)

> Puedes insertar aquí imágenes de la interfaz con la sintaxis:

```markdown
![Ventana Principal](resources/main_window.png)
```

---

## Licencia

Este proyecto es de uso académico y no tiene fines comerciales. Puedes usarlo como base para tus propios desarrollos.
