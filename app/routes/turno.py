from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.forms.turno_form import TurnoForm
from app import db
from app.models.turno import Turno
from app.models.paciente import Paciente
from flask import render_template  
from app import mail
from app.utils.email_utils import enviar_correo
from app.models.paciente import Paciente 
from app.utils.auth import admin_required

turno_bp = Blueprint('turno', __name__)  

@turno_bp.route('/asignar_turno', methods=['GET', 'POST'])  # define la URL
@login_required
def asignar_turno():
    form = TurnoForm()
    form.paciente_id.choices = [(p.id, p.nombre) for p in Paciente.query.all()]

    if request.method == 'POST' and form.validate_on_submit():
        nuevo_turno = Turno(
            paciente_id=form.paciente_id.data,
            profesional_id=current_user.id,
            fecha=form.fecha.data,
            hora=form.hora.data,
            especialidad=form.especialidad.data
        )
        db.session.add(nuevo_turno)
        db.session.commit()
        flash('Turno asignado correctamente.', 'success')
        return redirect(url_for('dashboard'))

    return f"Formulario de turno (simulado). Método: {request.method}. Errores: {form.errors}"

from app.forms.turno_form import TurnoForm  # Asegúrate de tener este import


@turno_bp.route('/turnos')
@login_required
@admin_required
def lista_turnos():
    # Sólo administradores llegan aquí
    turnos = Turno.query.all()
    return render_template('lista_turnos.html', turnos=turnos)

from app.utils.email_utils import enviar_correo
from app.models.paciente import Paciente  # si no lo tienes ya importado

from flask_mail import Message
from app import mail
from app.models.paciente import Paciente

@turno_bp.route('/registrar_turno', methods=['GET', 'POST'])
@login_required
def registrar_turno():
    form = TurnoForm()
    form.paciente_id.choices = [(p.id, p.nombre) for p in Paciente.query.all()]

    if form.validate_on_submit():
        nuevo_turno = Turno(
            paciente_id=form.paciente_id.data,
            fecha=form.fecha.data,
            hora=form.hora.data,
            motivo=form.motivo.data
        )
        db.session.add(nuevo_turno)
        db.session.commit()

        # Obtener paciente y enviar correo
        paciente = Paciente.query.get(form.paciente_id.data)
        cuerpo = f"""
        Hola {paciente.nombre},

        Tu hora médica ha sido agendada para el {form.fecha.data.strftime('%d/%m/%Y')} a las {form.hora.data.strftime('%H:%M')}.

        Saludos,
        Clínica Sansar Bien
        """
        enviar_correo(paciente.email, "Confirmación de hora médica", cuerpo)

        flash('Hora médica registrada y correo enviado.', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('registrar_turno.html', form=form)

@turno_bp.route('/mis_turnos')
@login_required
def mis_turnos():
    # Solo los turnos del usuario/profesional conectado
    turnos = (
        Turno.query
            .filter_by(profesional_id=current_user.id)
            .order_by(Turno.fecha.desc(), Turno.hora.desc())
            .all()
    )
    return render_template('mis_turnos.html', turnos=turnos)

@turno_bp.route('/turnos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_turno(id):
    turno = Turno.query.get_or_404(id)
    form = TurnoForm(obj=turno)
    form.paciente_id.choices = [(p.id, p.nombre) for p in Paciente.query.all()]

    if form.validate_on_submit():
        turno.paciente_id    = form.paciente_id.data
        turno.fecha          = form.fecha.data
        turno.hora           = form.hora.data
        turno.motivo         = getattr(form, 'motivo', type('m', (), {'data':turno.motivo})) .data
        # si en tu TurnoForm tienes campo profesional_id:
        if hasattr(form, 'profesional_id'):
            turno.profesional_id = form.profesional_id.data
        db.session.commit()
        flash('Turno actualizado correctamente.', 'success')
        return redirect(url_for('turno.lista_turnos'))

    return render_template('editar_turno.html', form=form, turno=turno)


@turno_bp.route('/turnos/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_turno(id):
    turno = Turno.query.get_or_404(id)
    db.session.delete(turno)
    db.session.commit()
    flash('Turno eliminado correctamente.', 'success')
    return redirect(url_for('turno.lista_turnos'))