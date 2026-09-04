import psycopg2
from psycopg2.extras import RealDictCursor

# ==========================
# CONFIGURACIÓN
# Cambia estos valores con
# los datos de tu servidor
# ==========================

DB_CONFIG = {
    "host":     "localhost",
    "port":     5432,
    "dbname":   "centro_deportivo",
    "user":     "postgres",
    "password": "tarzann26"
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def ejecutar(query, params=None, fetchone=False, fetchall=False):
    """
    Ejecuta una consulta y devuelve
    resultados como diccionarios.
    """
    conn = get_connection()
    try:
        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, params)

                if fetchone:
                    resultado = cur.fetchone()
                    return dict(resultado) if resultado else None

                if fetchall:
                    resultados = cur.fetchall()
                    return [dict(r) for r in resultados]

                return None
    finally:
        conn.close()
