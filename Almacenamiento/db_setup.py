from Almacenamiento.db_config import get_connection

def inicializar_bd():
    conn = get_connection()
    cursor = conn.cursor()

    # Crear base si no existe
    cursor.execute("CREATE DATABASE IF NOT EXISTS colegio_cambridge")
    cursor.execute("USE colegio_cambridge")

    # ======================
    # CREAR TABLAS
    # ======================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS areas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100) UNIQUE NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS oficinas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100) UNIQUE NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS personas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        tipo ENUM('Profesor', 'Administrativo') NOT NULL,
        area VARCHAR(100),
        oficina VARCHAR(100),
        nombre VARCHAR(100),
        apellido VARCHAR(100),
        edad INT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profesores (
        id INT AUTO_INCREMENT PRIMARY KEY,
        persona_id INT NOT NULL,
        tipo_profesor ENUM('Planta', 'Contratista') NOT NULL,
        especialidad VARCHAR(100),
        FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS administrativos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        persona_id INT NOT NULL,
        puesto VARCHAR(100),
        FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print(" Base de datos inicializada correctamente")
