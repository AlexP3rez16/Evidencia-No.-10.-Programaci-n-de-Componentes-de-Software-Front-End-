from db import get_db

ESTADOS = ['disponible', 'prestado', 'mantenimiento', 'perdido']

def get_all(q=None, categoria=None, estado=None, editorial=None):
    con = get_db()
    try:
        with con.cursor() as cur:
            conditions, params = [], []

            if q:
                conditions.append("(titulo LIKE %s OR autor LIKE %s OR isbn LIKE %s)")
                like = f'%{q}%'
                params += [like, like, like]
            if categoria:
                conditions.append("categoria = %s")
                params.append(categoria)
            if estado:
                conditions.append("estado = %s")
                params.append(estado)
            if editorial:
                conditions.append("editorial = %s")
                params.append(editorial)

            where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
            cur.execute(
                f"SELECT * FROM libros {where} ORDER BY fecha_registro DESC",
                params
            )
            return cur.fetchall()
    finally:
        con.close()

def get_categorias():
    con = get_db()
    try:
        with con.cursor() as cur:
            cur.execute(
                "SELECT DISTINCT categoria FROM libros WHERE categoria IS NOT NULL AND categoria != '' ORDER BY categoria"
            )
            return [row['categoria'] for row in cur.fetchall()]
    finally:
        con.close()

def get_editoriales():
    con = get_db()
    try:
        with con.cursor() as cur:
            cur.execute(
                "SELECT DISTINCT editorial FROM libros WHERE editorial IS NOT NULL AND editorial != '' ORDER BY editorial"
            )
            return [row['editorial'] for row in cur.fetchall()]
    finally:
        con.close()

def get_by_isbn(isbn):
    con = get_db()
    try:
        with con.cursor() as cur:
            cur.execute("SELECT * FROM libros WHERE isbn = %s", (isbn,))
            return cur.fetchone()
    finally:
        con.close()

def crear(data):
    con = get_db()
    try:
        with con.cursor() as cur:
            cur.execute("""
                INSERT INTO libros
                  (isbn, titulo, autor, editorial, sinopsis,
                   anio_publicacion, num_paginas, precio,
                   ubicacion, num_copias, categoria, estado)
                VALUES
                  (%(isbn)s, %(titulo)s, %(autor)s, %(editorial)s, %(sinopsis)s,
                   %(anio)s, %(paginas)s, %(precio)s,
                   %(ubicacion)s, %(copias)s, %(categoria)s, 'disponible')
            """, data)
        con.commit()
    finally:
        con.close()

def editar(data):
    con = get_db()
    try:
        with con.cursor() as cur:
            cur.execute("""
                UPDATE libros SET
                  isbn=%(isbn)s, titulo=%(titulo)s, autor=%(autor)s,
                  editorial=%(editorial)s, sinopsis=%(sinopsis)s,
                  anio_publicacion=%(anio)s, num_paginas=%(paginas)s,
                  precio=%(precio)s, ubicacion=%(ubicacion)s,
                  num_copias=%(copias)s, categoria=%(categoria)s
                WHERE isbn=%(isbn_original)s
            """, data)
        con.commit()
    finally:
        con.close()

def eliminar(isbn):
    con = get_db()
    try:
        with con.cursor() as cur:
            cur.execute("DELETE FROM libros WHERE isbn = %s", (isbn,))
        con.commit()
    finally:
        con.close()
