from db import get_db


def get_by_usuario(usuario):
    con = get_db()
    try:
        with con.cursor() as cur:
            cur.execute(
                "SELECT * FROM usuarios WHERE usuario = %s", (usuario,)
            )
            return cur.fetchone()
    finally:
        con.close()
