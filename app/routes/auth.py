from flask import Blueprint, request, redirect, url_for, flash
from app.forms.auth_forms import RegisterForm, LoginForm
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from flask_login import login_user, logout_user
from flask import render_template
from flask_login import login_required, current_user

from app.routes import user

# app/routes/auth.py
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    # Solo permitir a usuarios con rol "admin"
    if current_user.role != 'admin':
        flash('No tienes permiso para acceder a esta página.', 'danger')
        return redirect(url_for('main.dashboard'))

    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Ese nombre de usuario ya está registrado.', 'danger')
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(form.password.data)
        new_user = User(
            username=form.username.data,
            password_hash=hashed_password,
            role=form.role.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Usuario registrado con éxito.', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('Has iniciado sesión con éxito.', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Credenciales inválidas.', 'danger')
            return redirect(url_for('auth.login'))
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('auth.login'))
