import sqlite3
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Conectar a la base de datos (o crearla si no existe)
def connect_db():
    """Conecta a la base de datos"""
    conn = sqlite3.connect('db/el_escondite_ingles.db')  # Ruta de la base de datos
    return conn

# Crear tablas
def create_tables():
    """Crea las tablas necesarias en la base de datos"""
    conn = connect_db()
    cursor = conn.cursor()

    # Crear tabla de usuarios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    ''')

    # Crear tabla de estudiantes
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        level TEXT NOT NULL,
        user_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')

    # Crear tabla de niveles
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS levels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    ''')

    # Crear tabla de clases si no existe
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS classes (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        date TEXT NOT NULL,
        professor TEXT NOT NULL
    )
    ''')

    # Crear tabla de pagos si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,   
            student_id INTEGER NOT NULL,            
            amount REAL NOT NULL,                   
            date TEXT NOT NULL,                     
            method TEXT,                            
            notes TEXT,                             
            FOREIGN KEY(student_id) REFERENCES students(id)  
        )
    ''')

    # Crear tabla de recompensas si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rewards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recommender_id INTEGER NOT NULL,
            new_student_id INTEGER NOT NULL,
            reward_name TEXT NOT NULL,
            months_rewarded INTEGER NOT NULL,
            date_awarded TEXT NOT NULL,
            FOREIGN KEY (recommender_id) REFERENCES students(id),
            FOREIGN KEY (new_student_id) REFERENCES students(id)
        )
        ''')

    conn.commit()
    conn.close()

# =============================
# FUNCIONES PARA LA GESTIÓN DE USUARIOS
# =============================

# Insertar usuario
def insert_user(username, password, role):
    """Añade un nuevo usuario a la base de datos"""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO users (username, password, role)
    VALUES (?, ?, ?)
    ''', (username, password, role))

    conn.commit()
    conn.close()

def fetch_users():
    """Recupera todos los usuarios desde la base de datos."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, username, password, role FROM users")
    users = cursor.fetchall()

    conn.close()
    return users

def update_user(user_id, new_username, new_role):
    """Actualiza el nombre de usuario y rol de un usuario existente."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE users
        SET username = ?, role = ?
        WHERE id = ?
    ''', (new_username, new_role, user_id))

    conn.commit()
    conn.close()

def delete_user(username):
    """Elimina un usuario de la base de datos por su ID."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE username = ?", (username,))

    conn.commit()
    conn.close()

# =============================
# FUNCIONES PARA LA GESTIÓN DE ESTUDIANTES
# =============================

# Insertar estudiante
def insert_student(name, age, level, user_id=None):
    """Añade un nuevo alumno a la base de datos"""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO students (name, age, level, user_id)
    VALUES (?, ?, ?, ?)
    ''', (name, age, level, user_id))

    conn.commit()
    conn.close()

# Eliminar un estudiante
def delete_student(name):
    """Elimina un alumno de la base de datos por su nombre"""
    conn = connect_db()
    cursor = conn.cursor()

    # Eliminar el alumno de la tabla 'students' utilizando el nombre
    cursor.execute('''DELETE FROM students WHERE name = ?''', (name,))

    conn.commit()
    conn.close()

# Modificarar un estudiante
def update_student(old_name, new_name, new_age, new_level):
    """
    Actualiza los datos de un alumno existente en la base de datos.

    Args:
        old_name (str): Nombre actual del alumno (clave para buscarlo).
        new_name (str): Nuevo nombre del alumno.
        new_age (int): Nueva edad del alumno.
        new_level (str): Nuevo nivel asignado.
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE students
        SET name = ?, age = ?, level = ?
        WHERE name = ?
    ''', (new_name, new_age, new_level, old_name))

    conn.commit()
    conn.close()

# Obtener todos los estudiantes
def fetch_students():
    """Obtiene todos los alumnos desde la base de datos"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    conn.close()

    # Convertimos los resultados en un diccionario
    return [{"id": student[0], "name": student[1], "age": student[2], "level": student[3]} for student in students]

# Obtener todos los estudiantes con detalles del usuario
def get_students():
    """Obtiene todos los estudiantes con detalles del usuario asociado"""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT students.id, students.name, students.age, students.level, users.username FROM students LEFT JOIN users ON students.user_id = users.id')
    students = cursor.fetchall()

    conn.close()
    return students


# =============================
# FUNCIONES PARA LA GESTIÓN DE NIVELES
# =============================

# Insertar los niveles en la tabla levels
def init_levels():
    """Inserta los niveles predefinidos si no existen"""
    conn = connect_db()
    cursor = conn.cursor()

    levels = ["A1", "A2", "B1", "B2", "C1", "C2",
              "A1_Ad", "A2_Ad", "B1_Ad", "B2_Ad", "C1_Ad", "C2_Ad"]

    for level in levels:
        cursor.execute("INSERT OR IGNORE INTO levels (name) VALUES (?)", (level,))

    conn.commit()
    conn.close()

def fetch_levels():
    """
    Recupera todos los niveles almacenados en la base de datos.

    Returns:
        list of tuples: Una lista de tuplas que contienen los datos de cada nivel.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM levels")
    levels = cursor.fetchall()
    conn.close()
    return levels

def insert_level(level_name):
    """
    Inserta un nuevo nivel en la base de datos.

    Args:
        level_name (str): El nombre del nivel a insertar (por ejemplo, 'A1', 'B2_Ad').
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO levels (name) VALUES (?)", (level_name,))
    conn.commit()
    conn.close()

def delete_level(level_name):
    """
    Elimina un nivel específico de la base de datos.

    Args:
        level_name (str): El nombre del nivel que se desea eliminar.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM levels WHERE name = ?", (level_name,))
    conn.commit()
    conn.close()

def update_level(old_name, new_name):
    """
    Actualiza el nombre de un nivel existente en la base de datos.

    Args:
        old_name (str): El nombre actual del nivel.
        new_name (str): El nuevo nombre que se desea asignar.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE levels SET name = ? WHERE name = ?", (new_name, old_name))
    conn.commit()
    conn.close()

# ==============================
# FUNCIONES PARA GESTIÓN DE CLASES
# ==============================

def insert_class(name, date, professor):
    """
    Inserta una nueva clase en la base de datos.

    Args:
        name (str): Nombre de la clase.
        date (str): Fecha de la clase en formato YYYY-MM-DD.
        professor (str): Nombre del profesor que la imparte.
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
                INSERT INTO classes (name, date, professor)
                VALUES (?, ?, ?)
            ''', (name, date, professor))

    conn.commit()
    conn.close()

def fetch_classes():
    """
    Recupera todas las clases almacenadas en la base de datos.

    Returns:
        list: Lista de tuplas con los datos de cada clase.
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM classes')
    classes = cursor.fetchall()

    conn.close()
    return classes

def update_class(old_name, new_name, new_date, new_professor):
    """
    Actualiza los datos de una clase existente.

    Args:
        old_name (str): Nombre actual de la clase (para localizarla).
        new_name (str): Nuevo nombre de la clase.
        new_date (str): Nueva fecha.
        new_professor (str): Nuevo nombre del profesor.
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
                UPDATE classes
                SET name = ?, date = ?, professor = ?
                WHERE name = ?
            ''', (new_name, new_date, new_professor, old_name))

    conn.commit()
    conn.close()

def delete_class(name):
    """
    Elimina una clase de la base de datos por su nombre.

    Args:
        name (str): Nombre de la clase a eliminar.
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM classes WHERE name = ?', (name,))

    conn.commit()
    conn.close()

# ==============================
# FUNCIONES PARA GESTIÓN DE PAGOS
# ==============================

def insert_payment(student_id, amount, date, method=None, notes=None):
    """
    Inserta un nuevo pago en la base de datos.

    Args:
        student_id (int): ID del alumno que realiza el pago.
        amount (float): Cantidad pagada.
        date (str): Fecha del pago (formato YYYY-MM-DD).
        method (str, optional): Metodo de pago (efectivo, tarjeta...).
        notes (str, optional): Observaciones adicionales.
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO payments (student_id, amount, date, method, notes)
        VALUES (?, ?, ?, ?, ?)
    ''', (student_id, amount, date, method, notes))

    conn.commit()
    conn.close()

def fetch_payments():
    """
    Recupera todos los pagos registrados, junto con el nombre del alumno.

    Returns:
        list of tuples: [(pago_id, nombre_alumno, cantidad, fecha, método, notas), ...]
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT payments.id, students.name, payments.amount, payments.date, payments.method, payments.notes
        FROM payments
        JOIN students ON payments.student_id = students.id
    ''')

    payments = cursor.fetchall()
    conn.close()
    return payments

def update_payment(payment_id, amount, date, method=None, notes=None):
    """
    Actualiza un pago existente.

    Args:
        payment_id (int): ID del pago a actualizar.
        amount (float): Nueva cantidad pagada.
        date (str): Nueva fecha del pago.
        method (str, optional): Nuevo método de pago.
        notes (str, optional): Nuevas observaciones.
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE payments
        SET amount = ?, date = ?, method = ?, notes = ?
        WHERE id = ?
    ''', (amount, date, method, notes, payment_id))

    conn.commit()
    conn.close()

def delete_payment(payment_id):
    """
    Elimina un pago de la base de datos por su ID.

    Args:
        payment_id (int): ID del pago a eliminar.
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM payments WHERE id = ?', (payment_id,))

    conn.commit()
    conn.close()

# ==============================
# FUNCIONES PARA GESTIÓN DE RECOMPENSAS
# ==============================

def insert_reward(recommender_id, new_student_id, months_rewarded, date_awarded):
    """
    Inserta una recompensa en la base de datos según la cantidad de meses premiados.
    Asigna automáticamente un nombre simbólico (Eire, Canada, USA).
    """
    # Determinar nombre de la recompensa simbólica
    if months_rewarded == 1:
        reward_name = "Eire"
    elif months_rewarded == 3:
        reward_name = "Canada"
    elif months_rewarded == 6:
        reward_name = "USA"
    else:
        reward_name = f"{months_rewarded} meses"

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO rewards (recommender_id, new_student_id, months_rewarded, date_awarded, reward_name)
        VALUES (?, ?, ?, ?, ?)
    ''', (recommender_id, new_student_id, months_rewarded, date_awarded, reward_name))

    conn.commit()
    conn.close()

def delete_reward(recommender_name, new_student_name):
    """Elimina una recompensa según los nombres del recomendador y nuevo alumno"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM rewards
        WHERE recommender_id = (SELECT id FROM students WHERE name = ?)
        AND new_student_id = (SELECT id FROM students WHERE name = ?)
    ''', (recommender_name, new_student_name))
    conn.commit()
    conn.close()

def fetch_rewards():
    """
    Devuelve una lista de recompensas, incluyendo nombres de usuarios y nombre simbólico de la recompensa.
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT rewards.id, s1.name AS recomendador, s2.name AS nuevo_alumno,
           rewards.months_rewarded, rewards.date_awarded, rewards.reward_name
        FROM rewards
        JOIN students s1 ON rewards.recommender_id = s1.id
        JOIN students s2 ON rewards.new_student_id = s2.id
    ''')

    results = cursor.fetchall()
    conn.close()
    return results

def reward_already_granted(new_student_id):
    """
    Verifica si ya se ha otorgado una recompensa para un nuevo alumno.

    :param new_student_id: ID del nuevo alumno.
    :return: True si ya tiene una recompensa, False en caso contrario.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM rewards WHERE new_student_id = ?", (new_student_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] > 0

# Función especial para saber si un estudiante está bajo el amparo de un bono
def is_student_under_bonus(student_id):
    """
    Verifica si el alumno tiene un bono gratuito vigente.

    :param student_id: ID del alumno a comprobar.
    :return: True si el bono está activo, False si ya terminó o no tiene.
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT date_awarded, months_rewarded
        FROM rewards
        WHERE recommender_id = ?
    ''', (student_id,))

    row = cursor.fetchone()
    conn.close()

    if row:
        date_awarded_str, months = row
        date_awarded = datetime.strptime(date_awarded_str, "%Y-%m-%d")
        end_date = date_awarded + relativedelta(months=months)
        return datetime.now() < end_date  # True si aún está en periodo de bono

    return False  # No tiene bono

# Funcion especial para saber cuando se van acabando los bonos
def get_students_with_expiring_bonus():
    """
    Devuelve una lista de alumnos cuyo bono termina dentro de los próximos 7 días.
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT s.name, r.date_awarded, r.months_rewarded
        FROM rewards r
        JOIN students s ON r.new_student_id = s.id
    ''')
    rows = cursor.fetchall()
    conn.close()

    expiring_soon = []
    for name, date_awarded_str, months in rows:
        date_awarded = datetime.strptime(date_awarded_str, "%Y-%m-%d")
        end_date = date_awarded + relativedelta(months=months)
        days_left = (end_date - datetime.now()).days
        if 0 <= days_left <= 7:
            expiring_soon.append((name, end_date.strftime("%Y-%m-%d"), days_left))

    return expiring_soon