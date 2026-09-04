from Database.conexion import ejecutar
from datetime import datetime


class ModeloRutina:

    def obtener_rutinas(self):
        rows = ejecutar(
            """
            SELECT
                rut_id                  AS id,
                rut_nombre_escenario    AS cancha,
                rut_objetivo            AS objetivo,
                rut_fecha::text         AS fecha,
                rut_hora                AS hora,
                cli_cedula              AS cliente_cedula,
                cli_nombre              AS cliente_nombre,
                cli_telefono            AS cliente_telefono,
                cli_membresia           AS cliente_membresia,
                ent_cedula              AS entrenador_cedula,
                ent_nombre              AS entrenador_nombre,
                ent_telefono            AS entrenador_telefono,
                ent_especialidad        AS entrenador_especialidad
            FROM rutina
            JOIN cliente    ON cli_cedula = rut_cedula_cliente
            JOIN entrenador ON ent_cedula = rut_cedula_entrenador
            ORDER BY rut_fecha DESC, rut_hora
            """,
            fetchall=True
        )
        return [self._formatear(r) for r in rows]

    def obtener_rutinas_cliente(self, cliente):
        rows = ejecutar(
            """
            SELECT
                rut_id                  AS id,
                rut_nombre_escenario    AS cancha,
                rut_objetivo            AS objetivo,
                rut_fecha::text         AS fecha,
                rut_hora                AS hora,
                cli_cedula              AS cliente_cedula,
                cli_nombre              AS cliente_nombre,
                cli_telefono            AS cliente_telefono,
                cli_membresia           AS cliente_membresia,
                ent_cedula              AS entrenador_cedula,
                ent_nombre              AS entrenador_nombre,
                ent_telefono            AS entrenador_telefono,
                ent_especialidad        AS entrenador_especialidad
            FROM rutina
            JOIN cliente    ON cli_cedula = rut_cedula_cliente
            JOIN entrenador ON ent_cedula = rut_cedula_entrenador
            WHERE rut_cedula_cliente = %s
            ORDER BY rut_fecha, rut_hora
            """,
            (cliente["cedula"],),
            fetchall=True
        )
        return [self._formatear(r) for r in rows]

    def obtener_rutina_hoy(self, cliente):
        hoy = datetime.now().strftime("%Y-%m-%d")
        row = ejecutar(
            """
            SELECT
                rut_id                  AS id,
                rut_nombre_escenario    AS cancha,
                rut_objetivo            AS objetivo,
                rut_fecha::text         AS fecha,
                rut_hora                AS hora,
                cli_cedula              AS cliente_cedula,
                cli_nombre              AS cliente_nombre,
                cli_telefono            AS cliente_telefono,
                cli_membresia           AS cliente_membresia,
                ent_cedula              AS entrenador_cedula,
                ent_nombre              AS entrenador_nombre,
                ent_telefono            AS entrenador_telefono,
                ent_especialidad        AS entrenador_especialidad
            FROM rutina
            JOIN cliente    ON cli_cedula = rut_cedula_cliente
            JOIN entrenador ON ent_cedula = rut_cedula_entrenador
            WHERE rut_cedula_cliente = %s AND rut_fecha = %s
            LIMIT 1
            """,
            (cliente["cedula"], hoy),
            fetchone=True
        )
        return self._formatear(row) if row else None

    def obtener_rutina_reservacion(self, cliente, fecha, hora):
        row = ejecutar(
            """
            SELECT
                rut_id                  AS id,
                rut_nombre_escenario    AS cancha,
                rut_objetivo            AS objetivo,
                rut_fecha::text         AS fecha,
                rut_hora                AS hora,
                cli_cedula              AS cliente_cedula,
                cli_nombre              AS cliente_nombre,
                cli_telefono            AS cliente_telefono,
                cli_membresia           AS cliente_membresia,
                ent_cedula              AS entrenador_cedula,
                ent_nombre              AS entrenador_nombre,
                ent_telefono            AS entrenador_telefono,
                ent_especialidad        AS entrenador_especialidad
            FROM rutina
            JOIN cliente    ON cli_cedula = rut_cedula_cliente
            JOIN entrenador ON ent_cedula = rut_cedula_entrenador
            WHERE rut_cedula_cliente = %s
              AND rut_fecha = %s
              AND rut_hora  = %s
            LIMIT 1
            """,
            (cliente["cedula"], fecha, hora),
            fetchone=True
        )
        return self._formatear(row) if row else None

    def obtener_ejercicios(self, cancha, objetivo):
        rows = ejecutar(
            """
            SELECT ejc_nombre_ejercicio AS ejercicio
            FROM ejercicio_catalogo
            WHERE ejc_nombre_escenario = %s
              AND ejc_objetivo = %s
            ORDER BY ejc_id
            """,
            (cancha, objetivo),
            fetchall=True
        )
        return [r["ejercicio"] for r in rows]

    def obtener_objetivos(self, cancha):
        rows = ejecutar(
            """
            SELECT DISTINCT ejc_objetivo AS objetivo
            FROM ejercicio_catalogo
            WHERE ejc_nombre_escenario = %s
            ORDER BY ejc_objetivo
            """,
            (cancha,),
            fetchall=True
        )
        return [r["objetivo"] for r in rows]

    def agregar_rutina(
        self,
        cliente,
        entrenador,
        cancha,
        objetivo,
        ejercicios,
        fecha,
        hora
    ):
        # Insertar rutina y recuperar el ID generado
        resultado = ejecutar(
            """
            INSERT INTO rutina
                (rut_cedula_cliente, rut_cedula_entrenador,
                 rut_nombre_escenario, rut_objetivo, rut_fecha, rut_hora)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING rut_id AS id
            """,
            (
                cliente["cedula"],
                entrenador["cedula"],
                cancha,
                objetivo,
                fecha,
                hora
            ),
            fetchone=True
        )

        rutina_id = resultado["id"]

        for ej in ejercicios:
            ejecutar(
                """
                INSERT INTO rutina_ejercicio
                    (rej_id_rutina, rej_nombre, rej_series, rej_repeticiones)
                VALUES (%s, %s, %s, %s)
                """,
                (rutina_id, ej["nombre"], ej["series"], ej["repeticiones"])
            )

    # ==========================
    # HELPERS
    # ==========================

    def _formatear(self, row):
        ejercicios = ejecutar(
            """
            SELECT rej_nombre        AS nombre,
                   rej_series        AS series,
                   rej_repeticiones  AS repeticiones
            FROM rutina_ejercicio
            WHERE rej_id_rutina = %s
            ORDER BY rej_id
            """,
            (row["id"],),
            fetchall=True
        )

        return {
            "id": row["id"],
            "cliente": {
                "cedula":    row["cliente_cedula"],
                "nombre":    row["cliente_nombre"],
                "telefono":  row["cliente_telefono"],
                "membresia": row["cliente_membresia"]
            },
            "entrenador": {
                "cedula":       row["entrenador_cedula"],
                "nombre":       row["entrenador_nombre"],
                "telefono":     row["entrenador_telefono"],
                "especialidad": row["entrenador_especialidad"]
            },
            "cancha":     row["cancha"],
            "objetivo":   row["objetivo"],
            "fecha":      str(row["fecha"]),
            "hora":       row["hora"],
            "ejercicios": [dict(e) for e in ejercicios]
        }
