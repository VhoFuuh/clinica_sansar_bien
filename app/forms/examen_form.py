from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FileField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed
from app.models.paciente import Paciente

class ExamenForm(FlaskForm):
    nombre = StringField('Nombre del Examen', validators=[DataRequired()])
    archivo = FileField('Archivo', validators=[
        FileAllowed(['pdf', 'jpg', 'png', 'jpeg'], 'Solo archivos PDF o imagen')
    ])
    paciente_id = SelectField('Paciente', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Subir Examen')
