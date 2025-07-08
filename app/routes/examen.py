import os
from flask import Blueprint, request, redirect, url_for, flash, render_template, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename
from app import db
from app.models.examen import Examen
from app.models.paciente import Paciente
from app.forms.examen_form import ExamenForm
from flask_login import current_user
from app import mail
from flask_mail import Message

examen_bp = Blueprint('examen', __name__)
UPLOAD_FOLDER = 'app/static/archivos_examenes'

@examen_bp.route('/examenes/subir', methods=['GET', 'POST'])
@login_required
def subir_examen():
    form = ExamenForm()
    form.paciente_id.choices = [(p.id, p.nombre) for p in Paciente.query.order_by(Paciente.nombre).all()]

    if form.validate_on_submit():
        archivo = form.archivo.data
        if archivo:
            filename = secure_filename(archivo.filename)
            path = os.path.join(UPLOAD_FOLDER, filename)
            archivo.save(path)

            examen = Examen(
                nombre=form.nombre.data,
                archivo=filename,
                paciente_id=form.paciente_id.data
            )
            db.session.add(examen)
            db.session.commit()

            # ✉️ Enviar correo al paciente
            paciente = Paciente.query.get(form.paciente_id.data)
            mensaje = Message(
                subject="Nuevo examen disponible",
                recipients=[paciente.email],
                body=f"Hola {paciente.nombre},\n\nSe ha subido un nuevo examen con el nombre '{form.nombre.data}'. Puedes revisarlo en la clínica.\n\nSaludos,\nClínica Sansar Bien"
            )
            mail.send(mensaje)

            flash('Examen subido correctamente y correo enviado.', 'success')
            return redirect(url_for('main.dashboard'))

    return render_template('subir_examen.html', form=form)


@examen_bp.route('/lista_examenes')
@login_required
def lista_examenes():
    from app.models.examen import Examen
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

                # Eliminar el archivo anterior si existe
                archivo_antiguo = os.path.join(UPLOAD_FOLDER, examen.archivo)
                if os.path.exists(archivo_antiguo):
                    os.remove(archivo_antiguo)

                path_nuevo = os.path.join(UPLOAD_FOLDER, filename)
                archivo.save(path_nuevo)
                examen.archivo = filename

        db.session.commit()
        flash('Examen actualizado correctamente.', 'success')
        return redirect(url_for('examen.lista_examenes'))

    return render_template('editar_examen.html', examen=examen)

@examen_bp.route('/examenes/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_examen(id):
    examen = Examen.query.get_or_404(id)
    archivo_path = os.path.join(UPLOAD_FOLDER, examen.archivo)
    
    # Eliminar archivo físico si existe
    if os.path.exists(archivo_path):
        os.remove(archivo_path)
    
    db.session.delete(examen)
    db.session.commit()
    flash('Examen eliminado correctamente.', 'success')
    return redirect(url_for('examen.lista_examenes'))