from Database.conexion import ejecutar


class ModeloClientes:

    def obtener_clientes(self):
        return ejecutar(
            """
            SELECT cli_cedula    AS cedula,
                   cli_nombre    AS nombre,
                   cli_telefono  AS telefono,
                   cli_membresia AS membresia,
                   cli_activo    AS activo
            FROM cliente
            ORDER BY cli_nombre
            """,
            fetchall=True
        )

    def validar_cliente(self, nombre, cedula, telefono, password):

        nombre   = nombre.strip()
        cedula   = cedula.strip()
        telefono = telefono.strip()
        password = password.strip()

        if not nombre:
            return False, "El nombre es obligatorio"
        if len(nombre) < 3:
            return False, "El nombre debe tener mínimo 3 caracteres"
        if nombre.isdigit():
            return False, "El nombre no puede contener solo números"

        if not cedula:
            return False, "La cédula es obligatoria"
        if not cedula.isdigit():
            return False, "La cédula solo debe contener números"
        if len(cedula) < 6 or len(cedula) > 12:
            return False, "La cédula debe tener entre 6 y 12 dígitos"

        existe = ejecutar(
            "SELECT 1 FROM cliente WHERE cli_cedula = %s",
            (cedula,),
            fetchone=True
        )
        if existe:
            return False, "La cédula ya está registrada"

        if not telefono:
            return False, "El teléfono es obligatorio"
        if not telefono.isdigit():
            return False, "El teléfono solo debe contener números"
        if len(telefono) < 10:
            return False, "El teléfono debe tener mínimo 10 dígitos"

        if not password:
            return False, "La contraseña es obligatoria"
        if len(password) < 6:
            return False, "La contraseña debe tener mínimo 6 caracteres"

        return True, "Cliente válido"

    def agregar_cliente(self, cliente, password):

        ejecutar(
            """
            INSERT INTO usuario (usu_cedula, usu_password, usu_rol)
            VALUES (%s, %s, 'cliente')
            """,
            (cliente["cedula"], password)
        )

        ejecutar(
            """
            INSERT INTO cliente
                (cli_cedula, cli_nombre, cli_telefono, cli_membresia, cli_activo)
            VALUES (%s, %s, %s, NULL, TRUE)
            """,
            (cliente["cedula"], cliente["nombre"], cliente["telefono"])
        )

    def eliminar_cliente(self, cliente):
        # CASCADE elimina el registro en cliente automáticamente
        ejecutar(
            "DELETE FROM usuario WHERE usu_cedula = %s",
            (cliente["cedula"],)
        )
