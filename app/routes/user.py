from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.forms.user_form import UserForm
from app.models.user import User
from app import db
from werkzeug.security import generate_password_hash
from flask_login import login_required
from functools import wraps

user_bp = Blueprint('user', __name__)

# Requiere rol admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask_login import current_user
        if current_user.role != 'admin':
            flash('Acceso no autorizado.', 'danger')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@user_bp.route('/usuarios')
@login_required
@admin_required
def lista_usuarios():
    rol = request.args.get('rol')
    search = request.args.get('buscar')
    query = User.query

    if rol:
        query = query.filter_by(role=rol)
    if search:
        query = query.filter(User.username.ilike(f'%{search}%'))

    usuarios = query.all()
    return render_template('lista_usuarios.html', usuarios=usuarios)


@user_bp.route('/usuarios/nuevo', methods=['GET', 'POST'])
@login_required
@admin_required
def crear_usuario():
    form = UserForm()
    if form.validate_on_submit():
        nuevo = User(
            username=form.username.data,
            password_hash=generate_password_hash(form.password.data),
            role=form.role.data
        )
        db.session.add(nuevo)
        db.session.commit()
        flash('Usuario creado correctamente.', 'success')
        return redirect(url_for('user.lista_usuarios'))
    return render_template('registrar_usuario.html', form=form)


@user_bp.route('/usuarios/editar/<int:usuario_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_usuario(usuario_id):
    usuario = User.query.get_or_404(usuario_id)
    form = UserForm(obj=usuario)

    if form.validate_on_submit():
        usuario.username = form.username.data
        if form.password.data:  # Solo actualiza si se ingresó nueva contraseña
            usuario.password_hash = generate_password_hash(form.password.data)
        usuario.role = form.role.data
        db.session.commit()
        flash('Usuario actualizado correctamente.', 'success')
        return redirect(url_for('user.lista_usuarios'))

    return render_template('registrar_usuario.html', form=form)


@user_bp.route('/usuarios/eliminar/<int:usuario_id>', methods=['POST'])
@login_required
@admin_required
def eliminar_usuario(usuario_id):
    usuario = User.query.get_or_404(usuario_id)
    
    if usuario.role == 'admin':
        flash('No se puede eliminar un usuario administrador.', 'danger')
        return redirect(url_for('user.lista_usuarios'))

    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario eliminado correctamente.', 'success')
    return redirect(url_for('user.lista_usuarios'))

