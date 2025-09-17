import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",       # Cambia si tu servidor no es local
        user="root",      # Aquí tu usuario de MySQL
        password="123456789",  # Tu contraseña de MySQL
        database="colegio_cambridge"  # Nombre de la BD
    )
