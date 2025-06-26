import sqlite3

# Conexión a la base de datos (crea el archivo si no existe)
conn = sqlite3.connect('complaints.db')
cursor = conn.cursor()

# Crear tabla de reclamos (sin email, con username)
cursor.execute('''
CREATE TABLE IF NOT EXISTS complaints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    username TEXT NOT NULL,
    service TEXT NOT NULL,
    description TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Pendiente',
    date TEXT NOT NULL,
    response TEXT
)
''')

# Crear tabla de usuarios
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('admin', 'user'))
)
''')

# Crear usuario administrador por defecto
cursor.execute("SELECT * FROM users WHERE username = 'admin'")
if not cursor.fetchone():
    cursor.execute('''
        INSERT INTO users (username, password, role)
        VALUES (?, ?, ?)
    ''', ('admin', 'admin123', 'admin'))

# Crear usuario común por defecto
cursor.execute("SELECT * FROM users WHERE username = 'usuario'")
if not cursor.fetchone():
    cursor.execute('''
        INSERT INTO users (username, password, role)
        VALUES (?, ?, ?)
    ''', ('usuario', 'usuario123', 'user'))

print("Base de datos y tablas inicializadas correctamente.")
conn.commit()
conn.close()
