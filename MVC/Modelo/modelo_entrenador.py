from Database.conexion import ejecutar


class ModeloEntrenador:

    def obtener_entrenadores(self):
        return ejecutar(
            """
            SELECT ent_cedula        AS cedula,
                   ent_nombre        AS nombre,
                   ent_telefono      AS telefono,
                   ent_especialidad  AS especialidad,
                   ent_activo        AS activo
            FROM entrenador
            ORDER BY ent_nombre
            """,
            fetchall=True
        )

    def validar_entrenador(self, cedula, telefono):

        por_cedula = ejecutar(
            "SELECT 1 FROM entrenador WHERE ent_cedula = %s",
            (cedula,),
            fetchone=True
        )
        if por_cedula:
            return False, "La cédula ya está registrada"

        por_telefono = ejecutar(
            "SELECT 1 FROM entrenador WHERE ent_telefono = %s",
            (telefono,),
            fetchone=True
        )
        if por_telefono:
            return False, "El teléfono ya está registrado"

        return True, ""

    def agregar_entrenador(self, entrenador, password):

        ejecutar(
            """
            INSERT INTO usuario (usu_cedula, usu_password, usu_rol)
            VALUES (%s, %s, 'entrenador')
            """,
            (entrenador["cedula"], password)
        )

        ejecutar(
            """
            INSERT INTO entrenador
                (ent_cedula, ent_nombre, ent_telefono, ent_especialidad, ent_activo)
            VALUES (%s, %s, %s, %s, TRUE)
            """,
            (
                entrenador["cedula"],
                entrenador["nombre"],
                entrenador["telefono"],
                entrenador["especialidad"]
            )
        )

    def eliminar_entrenador(self, entrenador):
        ejecutar(
            "DELETE FROM usuario WHERE usu_cedula = %s",
            (entrenador["cedula"],)
        )
