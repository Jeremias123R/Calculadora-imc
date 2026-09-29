import sqlite3

def conectar_db():
conexion = sqlite3.connect("imc.db")

cursor = conexion.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS personas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        edad INTEGER NOT NULL,
        peso REAL NOT NULL,
        altura REAL NOT NULL,
        imc REAL NOT NULL,
        categoria TEXT NOT NULL
    )
""")

conexion.commit()

return conexion
