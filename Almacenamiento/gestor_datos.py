import mysql.connector
from Almacenamiento.db_config import get_connection


def ejecutar_query(query, params=None, return_last_id=False):
    """
    Ejecuta un INSERT, UPDATE o DELETE en la BD.
    Si return_last_id=True, devuelve el ID autoincrement generado.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params or ())
        conn.commit()

        # Si se pide, devolver el último ID generado
        if return_last_id:
            last_id = cursor.lastrowid
            return last_id

    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()


def fetch_all(query, params=None):
    """
    Ejecuta un SELECT y devuelve los resultados como lista de diccionarios.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        results = cursor.fetchall()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()

    return results


def fetch_one(query, params=None):
    """
    Ejecuta un SELECT que devuelve una sola fila como diccionario.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        result = cursor.fetchone()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()

    return result
