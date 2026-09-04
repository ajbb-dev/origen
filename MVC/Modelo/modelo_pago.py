from Database.conexion import ejecutar
from datetime import datetime


class ModeloPago:

    def obtener_pagos(self):
        rows = ejecutar(
            """
            SELECT
                pag_membresia               AS membresia,
                pag_monto                   AS monto,
                pag_fecha::text             AS fecha,
                cli_cedula                  AS cliente_cedula,
                cli_nombre                  AS cliente_nombre,
                cli_telefono                AS cliente_telefono,
                cli_membresia               AS cliente_membresia
            FROM pago
            JOIN cliente ON cli_cedula = pag_cedula_cliente
            ORDER BY pag_fecha DESC, pag_id DESC
            """,
            fetchall=True
        )
        return [self._formatear(r) for r in rows]

    def obtener_pagos_cliente(self, cliente):
        rows = ejecutar(
            """
            SELECT
                pag_membresia               AS membresia,
                pag_monto                   AS monto,
                pag_fecha::text             AS fecha,
                cli_cedula                  AS cliente_cedula,
                cli_nombre                  AS cliente_nombre,
                cli_telefono                AS cliente_telefono,
                cli_membresia               AS cliente_membresia
            FROM pago
            JOIN cliente ON cli_cedula = pag_cedula_cliente
            WHERE pag_cedula_cliente = %s
            ORDER BY pag_fecha DESC
            """,
            (cliente["cedula"],),
            fetchall=True
        )
        return [self._formatear(r) for r in rows]

    def registrar_pago(self, cliente, membresia, monto):

        ejecutar(
            """
            INSERT INTO pago
                (pag_cedula_cliente, pag_membresia, pag_monto, pag_fecha)
            VALUES (%s, %s, %s, %s)
            """,
            (
                cliente["cedula"],
                membresia["nombre"],
                membresia["monto"],
                datetime.now().strftime("%Y-%m-%d")
            )
        )

        ejecutar(
            """
            UPDATE cliente
            SET cli_membresia = %s
            WHERE cli_cedula = %s
            """,
            (membresia["nombre"], cliente["cedula"])
        )

        # Reflejar cambio en el dict para la vista
        cliente["membresia"] = membresia["nombre"]

    # ==========================
    # HELPERS
    # ==========================

    def _formatear(self, row):
        return {
            "cliente": {
                "cedula":    row["cliente_cedula"],
                "nombre":    row["cliente_nombre"],
                "telefono":  row["cliente_telefono"],
                "membresia": row["cliente_membresia"]
            },
            "membresia": row["membresia"],
            "monto":     float(row["monto"]),
            "fecha":     str(row["fecha"])
        }
