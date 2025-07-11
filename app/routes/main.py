from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.forms.turno_form import TurnoForm
from werkzeug.security import generate_password_hash
from app.models.turno import Turno
from app.models.paciente import Paciente
from app.forms.user_form import UserForm
from app.models.user import User
from app import db
from flask_mail import Message
from app import mail

main_bp = Blueprint('main', __name__)

@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@main_bp.route('/registrar_turno', methods=['GET', 'POST'])
@login_required
def registrar_turno():
    form = TurnoForm()

    if request.method == 'POST' and form.validate_on_submit():
        nuevo_turno = Turno(
            paciente_id=form.paciente_id.data,
            fecha=form.fecha.data,
            hora=form.hora.data,
            motivo=form.motivo.data,
            tipo=form.tipo.data
        )
        db.session.add(nuevo_turno)
        db.session.commit()
        flash('Turno registrado con éxito.', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('registrar_turno.html', form=form)

@main_bp.route('/ver_turnos')
@login_required
def ver_turnos():
    turnos = Turno.query.all()
    return render_template('ver_turnos.html', turnos=turnos)

from app.forms.filtro_turnos_form import FiltroTurnosForm  

@main_bp.route('/lista_turnos', methods=['GET', 'POST'])
@login_required
def lista_turnos():
    form = FiltroTurnosForm()
    query = Turno.query.join(Paciente)

    if form.validate_on_submit():
        if form.fecha.data:
            query = query.filter(Turno.fecha == form.fecha.data)
        if form.tipo.data:
            query = query.filter(Turno.tipo == form.tipo.data)

    turnos = query.all()
    return render_template('lista_turnos.html', turnos=turnos, form=form)



@main_bp.route('/editar_turno/<int:turno_id>', methods=['GET', 'POST'])
@login_required
def editar_turno(turno_id):
    turno = Turno.query.get_or_404(turno_id)
    form = TurnoForm(obj=turno)

    if form.validate_on_submit():
        turno.paciente_id = form.paciente_id.data
        turno.fecha = form.fecha.data
        turno.hora = form.hora.data
        turno.motivo = form.motivo.data
        turno.tipo = form.tipo.data
        db.session.commit()
        flash('Turno actualizado correctamente.', 'success')
        return redirect(url_for('main.lista_turnos'))

    return render_template('editar_turno.html', form=form)


@main_bp.route('/eliminar_turno/<int:turno_id>', methods=['GET'])
@login_required
def eliminar_turno(turno_id):
    turno = Turno.query.get_or_404(turno_id)
    db.session.delete(turno)
    db.session.commit()
    flash('Turno eliminado correctamente.', 'success')
    return redirect(url_for('main.lista_turnos'))

@main_bp.route('/registrar_usuario', methods=['GET', 'POST'])
@login_required
def registrar_usuario():
    form = UserForm()
    if form.validate_on_submit():
        # Verificar si el usuario ya existe
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Ya existe un usuario con ese nombre.', 'warning')
            return redirect(url_for('main.registrar_usuario'))
        
        nuevo_usuario = User(
            username=form.username.data,
            password_hash=generate_password_hash(form.password.data),
            role=form.role.data
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('Usuario registrado con éxito.', 'success')
        return redirect(url_for('main.lista_usuarios'))
    return render_template('registrar_usuario.html', form=form)

# Ruta para listar los usuarios registrados
@main_bp.route('/lista_usuarios')
@login_required
def lista_usuarios():
    usuarios = User.query.all()
    return render_template('lista_usuarios.html', usuarios=usuarios)
