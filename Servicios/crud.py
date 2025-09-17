from Almacenamiento.gestor_datos import ejecutar_query, fetch_all

class CRUD:
    def __init__(self):
        pass

    # ==========================
    #   ÁREAS
    # ==========================
    def crear_area(self, nombre):
        query = "INSERT INTO areas (nombre) VALUES (%s)"
        ejecutar_query(query, (nombre,))
        return {"nombre": nombre}

    def leer_areas(self):
        query = "SELECT * FROM areas"
        return fetch_all(query)

    def actualizar_area(self, nombre_actual, nuevo_nombre):
        query = "UPDATE areas SET nombre = %s WHERE nombre = %s"
        ejecutar_query(query, (nuevo_nombre, nombre_actual))
        return True

    def eliminar_area(self, nombre):
        query = "DELETE FROM areas WHERE nombre = %s"
        ejecutar_query(query, (nombre,))
        return True

    # ==========================
    #   OFICINAS
    # ==========================
    def crear_oficina(self, nombre):
        query = "INSERT INTO oficinas (nombre) VALUES (%s)"
        ejecutar_query(query, (nombre,))
        return {"nombre": nombre}

    def leer_oficinas(self):
        query = "SELECT * FROM oficinas"
        return fetch_all(query)

    def actualizar_oficina(self, nombre_actual, nuevo_nombre):
        query = "UPDATE oficinas SET nombre = %s WHERE nombre = %s"
        ejecutar_query(query, (nuevo_nombre, nombre_actual))
        return True

    def eliminar_oficina(self, nombre):
        query = "DELETE FROM oficinas WHERE nombre = %s"
        ejecutar_query(query, (nombre,))
        return True

    # ==========================
    #   PERSONAS
    # ==========================
    def crear_profesor(self, nombre, apellido, edad, area, oficina, tipo_profesor, especialidad=""):
        # Insertar persona y obtener su ID
        query_persona = """
        INSERT INTO personas (tipo, area, oficina, nombre, apellido, edad)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        persona_id = ejecutar_query(
            query_persona,
            ("Profesor", area, oficina, nombre, apellido, edad),
            return_last_id=True
        )

        # Insertar profesor
        query_prof = "INSERT INTO profesores (persona_id, tipo_profesor, especialidad) VALUES (%s, %s, %s)"
        ejecutar_query(query_prof, (persona_id, tipo_profesor, especialidad))

        return {
            "id": persona_id,
            "tipo": "Profesor",
            "area": area,
            "oficina": oficina,
            "nombre": nombre,
            "apellido": apellido,
            "edad": edad,
            "tipo_profesor": tipo_profesor,
            "especialidad": especialidad
        }

    def crear_administrativo(self, nombre, apellido, edad, area, oficina, puesto=""):
        # Insertar persona y obtener su ID
        query_persona = """
        INSERT INTO personas (tipo, area, oficina, nombre, apellido, edad)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        persona_id = ejecutar_query(
            query_persona,
            ("Administrativo", area, oficina, nombre, apellido, edad),
            return_last_id=True
        )

        # Insertar administrativo
        query_admin = "INSERT INTO administrativos (persona_id, puesto) VALUES (%s, %s)"
        ejecutar_query(query_admin, (persona_id, puesto))

        return {
            "id": persona_id,
            "tipo": "Administrativo",
            "area": area,
            "oficina": oficina,
            "nombre": nombre,
            "apellido": apellido,
            "edad": edad,
            "puesto": puesto
        }

    def leer_personas(self):
        query = """
        SELECT p.id, p.tipo, p.area, p.oficina, p.nombre, p.apellido, p.edad,
               pr.tipo_profesor, pr.especialidad,
               ad.puesto
        FROM personas p
        LEFT JOIN profesores pr ON p.id = pr.persona_id
        LEFT JOIN administrativos ad ON p.id = ad.persona_id
        """
        return fetch_all(query)

    def actualizar_persona(self, id_val, nuevos_datos):
        query = """
        UPDATE personas
        SET area = %s, oficina = %s, nombre=%s, apellido=%s, edad=%s
        WHERE id = %s
        """
        ejecutar_query(query, (
            nuevos_datos.get("area"),
            nuevos_datos.get("oficina"),
            nuevos_datos.get("nombre"),
            nuevos_datos.get("apellido"),
            nuevos_datos.get("edad"),
            id_val
        ))

        if "tipo_profesor" in nuevos_datos:
            query_prof = "UPDATE profesores SET tipo_profesor = %s, especialidad=%s WHERE persona_id = %s"
            ejecutar_query(query_prof, (
                nuevos_datos["tipo_profesor"],
                nuevos_datos.get("especialidad", ""),
                id_val
            ))

        if "puesto" in nuevos_datos:
            query_admin = "UPDATE administrativos SET puesto = %s WHERE persona_id = %s"
            ejecutar_query(query_admin, (nuevos_datos["puesto"], id_val))

        return True

    def eliminar_persona(self, id_val):
        ejecutar_query("DELETE FROM profesores WHERE persona_id = %s", (id_val,))
        ejecutar_query("DELETE FROM administrativos WHERE persona_id = %s", (id_val,))
        ejecutar_query("DELETE FROM personas WHERE id = %s", (id_val,))
        return True
