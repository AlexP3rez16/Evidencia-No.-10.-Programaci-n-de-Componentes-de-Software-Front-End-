from functools import wraps

from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, session
)

import models.libro as libro_model

libros_bp = Blueprint('libros', __name__, url_prefix='/libros')


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


@libros_bp.route('/')
@login_required
def index():
    q = request.args.get('q', '').strip()
    categoria = request.args.get('categoria', '').strip()
    estado = request.args.get('estado', '').strip()
    editorial = request.args.get('editorial', '').strip()

    books = libro_model.get_all(q, categoria, estado, editorial)
    categorias = libro_model.get_categorias()
    editoriales = libro_model.get_editoriales()

    return render_template(
        'libros.html',
        books=books,
        q=q,
        categorias=categorias,
        editoriales=editoriales,
        estados=libro_model.ESTADOS,
        filtros={
            'categoria': categoria,
            'estado': estado,
            'editorial': editorial,
        },
    )


@libros_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo():
    if request.method == 'POST':
        data = _form_to_libro(request.form)
        try:
            libro_model.crear(data)
            flash('Libro guardado correctamente', 'success')
            return redirect(url_for('libros.index'))
        except Exception as e:
            flash(f'Error al guardar: {e}', 'error')
    return render_template('libro_form.html', book=None, modo='nuevo')


@libros_bp.route('/<isbn>')
@login_required
def detalle(isbn):
    book = libro_model.get_by_isbn(isbn)
    if not book:
        flash('Libro no encontrado', 'error')
        return redirect(url_for('libros.index'))

    prestados = max(0, book['num_copias'] - 2)
    disponibles = book['num_copias'] - prestados
    return render_template(
        'libro_detalle.html',
        book=book,
        prestados=prestados,
        disponibles=disponibles,
    )


@libros_bp.route('/<isbn>/editar', methods=['GET', 'POST'])
@login_required
def editar(isbn):
    book = libro_model.get_by_isbn(isbn)
    if not book:
        flash('Libro no encontrado', 'error')
        return redirect(url_for('libros.index'))

    if request.method == 'POST':
        data = _form_to_libro(request.form)
        data['isbn_original'] = isbn
        try:
            libro_model.editar(data)
            flash('Libro actualizado correctamente', 'success')
            return redirect(url_for('libros.index'))
        except Exception as e:
            flash(f'Error al actualizar: {e}', 'error')

    return render_template('libro_form.html', book=book, modo='editar')


@libros_bp.route('/<isbn>/eliminar', methods=['POST'])
@login_required
def eliminar(isbn):
    try:
        libro_model.eliminar(isbn)
        flash('Libro eliminado correctamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar: {e}', 'error')
    return redirect(url_for('libros.index'))


def _form_to_libro(form):
    return {
        'isbn': form.get('isbn', '').strip(),
        'titulo': form.get('titulo', '').strip(),
        'autor': form.get('autor', '').strip(),
        'editorial': form.get('editorial', '').strip(),
        'sinopsis': form.get('sinopsis', '').strip(),
        'anio': form.get('anio') or None,
        'paginas': form.get('paginas') or None,
        'precio': form.get('precio') or None,
        'ubicacion': form.get('ubicacion', '').strip(),
        'copias': form.get('copias') or 0,
        'categoria': form.get('categoria', '').strip(),
    }
