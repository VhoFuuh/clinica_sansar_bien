import os
from flask import Blueprint, request, redirect, url_for, flash, render_template, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db, mail
from flask_mail import Message
from app.models.examen import Examen
from app.models.paciente import Paciente
from app.forms.examen_form import ExamenForm

examen_bp = Blueprint('examen', __name__)

@examen_bp.route('/examenes/subir', methods=['GET', 'POST'])
@login_required
def subir_examen():
    form = ExamenForm()
# Si llega ?paciente_id en la URL, setea el valor del select
    if request.args.get('paciente_id'):
        form.paciente_id.data = int(request.args['paciente_id'])

    form.paciente_id.choices = [
        (p.id, p.nombre) for p in Paciente.query.order_by(Paciente.nombre).all()
    ]

    if form.validate_on_submit():
        archivo = form.archivo.data
        if archivo:
            filename = secure_filename(archivo.filename)
            # Carpeta absoluta dentro de static
            upload_folder = os.path.join(
                current_app.root_path,
                'static',
                'archivos_examenes'
            )
            os.makedirs(upload_folder, exist_ok=True)
            path = os.path.join(upload_folder, filename)
            archivo.save(path)

            paciente = Paciente.query.get(form.paciente_id.data)

            # Crear y guardar el examen
            nuevo_examen = Examen(
                paciente_id=paciente.id,
                nombre=form.nombre.data,
                archivo=filename
            )
            db.session.add(nuevo_examen)
            db.session.commit()

            # Enviar correo con adjunto
            try:
                msg = Message(
                    'Nuevo Examen Disponible',
                    sender=current_app.config['MAIL_USERNAME'],
                    recipients=[paciente.email]
                )
                msg.body = f"""Estimado/a {paciente.nombre},

Se ha subido un nuevo examen a su ficha médica.

Nombre del examen: {form.nombre.data}

Saludos cordiales,
Clínica Sansar Bien
"""
                # Adjuntar el archivo
                file_path = os.path.join(upload_folder, filename)
                with open(file_path, 'rb') as fp:
                    file_data = fp.read()
                    msg.attach(
                        filename,
                        form.archivo.data.mimetype,
                        file_data
                    )

                mail.send(msg)
                flash('Examen subido y correo enviado con éxito.', 'success')
            except Exception as e:
                print('❌ Error al enviar correo:', e)
                flash('Examen subido, pero falló el envío del correo.', 'warning')

            return redirect(url_for('examen.subir_examen'))

    return render_template('subir_examen.html', form=form)


@examen_bp.route('/lista_examenes')
@login_required
def lista_examenes():
    examenes = Examen.query.all()
    return render_template('lista_examenes.html', examenes=examenes)


@examen_bp.route('/examenes/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_examen(id):
    examen = Examen.query.get_or_404(id)

    if request.method == 'POST':
        examen.nombre = request.form['nombre']

        if current_user.role == 'admin':
            archivo = request.files.get('archivo')
            if archivo and archivo.filename != '':
                filename = secure_filename(archivo.filename)
                upload_folder = os.path.join(
                    current_app.root_path,
                    'static',
                    'archivos_examenes'
                )
                os.makedirs(upload_folder, exist_ok=True)
                # Eliminar archivo anterior
                antiguo = os.path.join(upload_folder, examen.archivo)
                if os.path.exists(antiguo):
                    os.remove(antiguo)
                # Guardar nuevo archivo
                nuevo_path = os.path.join(upload_folder, filename)
                archivo.save(nuevo_path)
                examen.archivo = filename

        db.session.commit()
        flash('Examen actualizado correctamente.', 'success')
        return redirect(url_for('examen.lista_examenes'))

    return render_template('editar_examen.html', examen=examen)


@examen_bp.route('/examenes/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_examen(id):
    examen = Examen.query.get_or_404(id)
    upload_folder = os.path.join(
        current_app.root_path,
        'static',
        'archivos_examenes'
    )
    path = os.path.join(upload_folder, examen.archivo)
    if os.path.exists(path):
        os.remove(path)
    db.session.delete(examen)
    db.session.commit()
    flash('Examen eliminado correctamente.', 'success')
    return redirect(url_for('examen.lista_examenes'))
