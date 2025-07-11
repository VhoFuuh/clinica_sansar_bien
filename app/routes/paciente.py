from flask import Blueprint, request, redirect, url_for, flash
from app.forms.paciente_form import PacienteForm
from app import db
from app.models.paciente import Paciente
from flask_login import login_required
from flask import render_template  
from app.models.examen import Examen

def limpiar_rut(rut):
    return rut.replace(".", "").replace("-", "").strip()

def formatear_rut(rut):
    rut = rut.upper().replace(".", "").replace("-", "").strip()
    if len(rut) < 2:
        return rut

    cuerpo = rut[:-1]
    dv = rut[-1]
    cuerpo = cuerpo[::-1]  # Revertimos para insertar puntos desde atrás

    bloques = [cuerpo[i:i+3] for i in range(0, len(cuerpo), 3)]
    cuerpo_formateado = ".".join(bloques)[::-1]
    return f"{cuerpo_formateado}-{dv}"



paciente_bp = Blueprint('paciente', __name__)

@paciente_bp.route('/registrar_paciente', methods=['GET', 'POST'])
@login_required
def registrar_paciente():
    form = PacienteForm()
    if request.method == 'POST' and form.validate_on_submit():
        rut_limpio = limpiar_rut(form.rut.data)

        existente = Paciente.query.filter(
            db.func.replace(db.func.replace(Paciente.rut, '.', ''), '-', '') == rut_limpio
        ).first()
        if existente:
            flash('Ya existe un paciente con ese RUT.', 'danger')
            return redirect(url_for('paciente.registrar_paciente'))

        nuevo = Paciente(
            nombre=form.nombre.data,
            rut=rut_limpio,
            fecha_nacimiento=form.fecha_nacimiento.data,
            sexo=form.sexo.data,
            telefono=form.telefono.data,
            email=form.email.data,
            direccion=form.direccion.data
        )
        db.session.add(nuevo)
        db.session.commit()
        flash('Paciente registrado correctamente.', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('registrar_paciente.html', form=form)

@paciente_bp.route('/pacientes')
@login_required
def lista_pacientes():
    sexo = request.args.get('sexo')
    buscar = request.args.get('buscar')

    query = Paciente.query

    if sexo:
        query = query.filter(Paciente.sexo == sexo)
    
    if buscar:
        query = query.filter(Paciente.nombre.ilike(f"%{buscar}%"))

    pacientes = query.all()

    # Formatear los RUTs para mostrar con puntos y guión
    for p in pacientes:
     p.rut = formatear_rut(p.rut)

    return render_template('lista_pacientes.html', pacientes=pacientes)


@paciente_bp.route('/pacientes/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    form = PacienteForm(obj=paciente)

    if form.validate_on_submit():
        rut_limpio = limpiar_rut(form.rut.data)

        # Verificar si otro paciente ya tiene ese RUT
        existente = Paciente.query.filter(
            db.func.replace(db.func.replace(Paciente.rut, '.', ''), '-', '') == rut_limpio,
            Paciente.id != paciente.id  # Excluir al mismo paciente
        ).first()
        if existente:
            flash('Ya existe otro paciente con ese RUT.', 'danger')
            return redirect(url_for('paciente.editar_paciente', id=paciente.id))

        paciente.nombre = form.nombre.data
        paciente.rut = rut_limpio
        paciente.fecha_nacimiento = form.fecha_nacimiento.data
        paciente.sexo = form.sexo.data
        paciente.telefono = form.telefono.data
        paciente.email = form.email.data
        paciente.direccion = form.direccion.data

        db.session.commit()
        flash('Paciente actualizado correctamente.', 'success')
        return redirect(url_for('paciente.lista_pacientes'))

    return render_template(
        'registrar_paciente.html',
        form=form,
        editar=True,
        paciente=paciente       
    )



@paciente_bp.route('/pacientes/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    db.session.delete(paciente)
    db.session.commit()
    flash('Paciente eliminado correctamente.', 'success')
    return redirect(url_for('paciente.lista_pacientes'))


@paciente_bp.route('/pacientes/<int:id>')
@login_required
def detalle_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    # Exámenes ordenados de más reciente a más antiguo
    examenes = (
        paciente.examenes
                .order_by(Examen.fecha_subida.desc())
                .all()
    )
    return render_template(
        'detalle_paciente.html',
        paciente=paciente,
        examenes=examenes
    )

