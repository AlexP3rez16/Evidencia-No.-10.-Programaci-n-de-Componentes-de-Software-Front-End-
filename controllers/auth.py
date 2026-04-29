from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash
import models.usuario as usuario_model

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'usuario' in session:
        return redirect(url_for('libros.index'))

    error = None
    if request.method == 'POST':
        usuario   = request.form.get('usuario', '').strip()
        contrasena = request.form.get('contrasena', '').strip()

        user = usuario_model.get_by_usuario(usuario)

        if user and check_password_hash(user['contrasena'], contrasena):
            session['usuario'] = user['usuario']
            session['nombre']  = user['nombre']
            return redirect(url_for('libros.index'))
        else:
            error = 'Usuario o contraseña incorrectos'

    return render_template('login.html', error=error)


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
