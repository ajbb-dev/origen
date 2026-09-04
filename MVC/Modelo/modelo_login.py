from Database.conexion import ejecutar


class ModeloLogin:

    def verificar_usuario(self, login, password):

        usuario = ejecutar(
            """
            SELECT usu_rol
            FROM usuario
            WHERE usu_cedula = %s AND usu_password = %s
            """,
            (login, password),
            fetchone=True
        )

        if not usuario:
            return None, None

        rol = usuario["usu_rol"]

        if rol == "administrador":
            return "administrador", None

        elif rol == "entrenador":
            entrenador = ejecutar(
                """
                SELECT ent_cedula   AS cedula,
                       ent_nombre   AS nombre,
                       ent_telefono AS telefono,
                       ent_especialidad AS especialidad,
                       ent_activo   AS activo
                FROM entrenador
                WHERE ent_cedula = %s
                """,
                (login,),
                fetchone=True
            )
            return "entrenador", entrenador

        elif rol == "cliente":
            cliente = ejecutar(
                """
                SELECT cli_cedula    AS cedula,
                       cli_nombre    AS nombre,
                       cli_telefono  AS telefono,
                       cli_membresia AS membresia,
                       cli_activo    AS activo
                FROM cliente
                WHERE cli_cedula = %s
                """,
                (login,),
                fetchone=True
            )
            return "usuario", cliente

        return None, None
