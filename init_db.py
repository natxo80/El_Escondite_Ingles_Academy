import sqlite3
from db.database import connect_db  # Asegúrate de que esta función esté definida correctamente en db/database.py

def create_table():
    """Crea la tabla users si no existe."""
    conn = connect_db()  # Conectamos a la base de datos
    cursor = conn.cursor()

    # Creamos la tabla users si no existe
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    ''')

    conn.commit()  # Guardamos los cambios
    conn.close()  # Cerramos la conexión

def create_admin_user():
    """Crea un usuario admin por defecto en la base de datos."""
    conn = connect_db()  # Conectamos a la base de datos
    cursor = conn.cursor()

    # Comprobamos si el usuario admin ya existe
    cursor.execute('SELECT * FROM users WHERE username = ?', ('admin',))
    user = cursor.fetchone()

    if user is None:
        # Si no existe, insertamos al usuario admin
        cursor.execute('''
        INSERT INTO users (username, password, role)
        VALUES (?, ?, ?)
        ''', ('admin', 'admin', 'admin'))  # Definir 'admin' como el rol
        conn.commit()  # Guardamos los cambios
        print("Usuario admin creado.")
    else:
        print("El usuario admin ya existe.")

    conn.close()  # Cerramos la conexión

# Llamamos a la función para crear la tabla y luego al usuario admin
if __name__ == "__main__":
    create_table()  # Crear la tabla si no existe
    create_admin_user()  # Crear el usuario admin