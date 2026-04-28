from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from dotenv import load_dotenv
import pymysql
import pymysql.cursors
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = 'ducky_secret_2024'

# ── Config MySQL ─────────────────────────────────────────────────
DB_CONFIG = {
    'host':        os.getenv('DB_HOST', 'localhost'),
    'user':        os.getenv('DB_USER', 'root'),
    'password':    os.getenv('DB_PASSWORD', ''),
    'database':    os.getenv('DB_NAME', 'biblioteca_ducky'),
    'charset':     'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db():
    return pymysql.connect(**DB_CONFIG)


# ── Auth decorator ───────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


# ══════════════════════════════════════════════════════════════════
#  AUTH
# ══════════════════════════════════════════════════════════════════

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'usuario' in session:
        return redirect(url_for('libros'))

    error = None
    if request.method == 'POST':
        usuario    = request.form.get('usuario', '').strip()
        contrasena = request.form.get('contrasena', '').strip()

        con = get_db()
        try:
            with con.cursor() as cur:
                cur.execute("SELECT * FROM usuarios WHERE usuario = %s", (usuario,))
                user = cur.fetchone()
        finally:
            con.close()

        if user and check_password_hash(user['contrasena'], contrasena):
            session['usuario'] = user['usuario']
            session['nombre']  = user['nombre']
            return redirect(url_for('libros'))
        else:
            error = 'Usuario o contraseña incorrectos'

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ══════════════════════════════════════════════════════════════════
#  LIBROS
# ══════════════════════════════════════════════════════════════════

@app.route('/libros')
@login_required
def libros():
    q = request.args.get('q', '').strip()
    con = get_db()
    try:
        with con.cursor() as cur:
            if q:
                like = f'%{q}%'
                cur.execute("""
                    SELECT * FROM libros
                    WHERE titulo LIKE %s OR autor LIKE %s OR isbn LIKE %s
                    ORDER BY fecha_registro DESC
                """, (like, like, like))
            else:
                cur.execute("SELECT * FROM libros ORDER BY fecha_registro DESC")
            books = cur.fetchall()
    finally:
        con.close()
    return render_template('libros.html', books=books, q=q)


@app.route('/libros/<isbn>')
@login_required
def libro_detalle(isbn):
    con = get_db()
    try:
        with con.cursor() as cur:
            cur.execute("SELECT * FROM libros WHERE isbn = %s", (isbn,))
            book = cur.fetchone()
    finally:
        con.close()

    if not book:
        flash('Libro no encontrado', 'error')
        return redirect(url_for('libros'))

    prestados   = max(0, book['num_copias'] - 2)
    disponibles = book['num_copias'] - prestados

    return render_template('libro_detalle.html', book=book,
                           prestados=prestados, disponibles=disponibles)


@app.route('/libros/nuevo', methods=['GET', 'POST'])
@login_required
def libro_nuevo():
    if request.method == 'POST':
        data = _form_to_libro(request.form)
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
            flash('Libro guardado correctamente', 'success')
            return redirect(url_for('libros'))
        except Exception as e:
            flash(f'Error al guardar: {e}', 'error')
        finally:
            con.close()

    return render_template('libro_form.html', book=None, modo='nuevo')


@app.route('/libros/<isbn>/editar', methods=['GET', 'POST'])
@login_required
def libro_editar(isbn):
    con = get_db()
    try:
        with con.cursor() as cur:
            cur.execute("SELECT * FROM libros WHERE isbn = %s", (isbn,))
            book = cur.fetchone()
    finally:
        con.close()

    if not book:
        flash('Libro no encontrado', 'error')
        return redirect(url_for('libros'))

    if request.method == 'POST':
        data = _form_to_libro(request.form)
        data['isbn_original'] = isbn
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
            flash('Libro actualizado correctamente', 'success')
            return redirect(url_for('libros'))
        except Exception as e:
            flash(f'Error al actualizar: {e}', 'error')
        finally:
            con.close()

    return render_template('libro_form.html', book=book, modo='editar')


@app.route('/libros/<isbn>/eliminar', methods=['POST'])
@login_required
def libro_eliminar(isbn):
    con = get_db()
    try:
        with con.cursor() as cur:
            cur.execute("DELETE FROM libros WHERE isbn = %s", (isbn,))
        con.commit()
        flash('Libro eliminado correctamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar: {e}', 'error')
    finally:
        con.close()
    return redirect(url_for('libros'))


# ── Helper ───────────────────────────────────────────────────────
def _form_to_libro(form):
    return {
        'isbn':      form.get('isbn', '').strip(),
        'titulo':    form.get('titulo', '').strip(),
        'autor':     form.get('autor', '').strip(),
        'editorial': form.get('editorial', '').strip(),
        'sinopsis':  form.get('sinopsis', '').strip(),
        'anio':      form.get('anio') or None,
        'paginas':   form.get('paginas') or None,
        'precio':    form.get('precio') or None,
        'ubicacion': form.get('ubicacion', '').strip(),
        'copias':    form.get('copias') or 0,
        'categoria': form.get('categoria', '').strip(),
    }


if __name__ == '__main__':
    app.run(debug=True)