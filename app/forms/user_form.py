from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Optional, Length

class UserForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired(), Length(min=3)])
    password = PasswordField('Contraseña', validators=[Optional(), Length(min=6)])
    role = SelectField('Rol', choices=[
        ('admin', 'Administrador'),
        ('medico', 'Médico General'),
        ('kinesiologo', 'Kinesiólogo'),
        ('nutricionista', 'Nutricionista'),
        ('psicologo', 'Psicólogo'),
        ('enfermero', 'Enfermero'),
        ('tecnologo_medico', 'Tecnólogo Médico'),
        ('fonoaudiologo', 'Fonoaudiólogo'),
        ('terapeuta_ocupacional', 'Terapeuta Ocupacional'),
        ('matrona', 'Matrona'),
        ('odontologo', 'Odontólogo'),
        ('quimico_farmaceutico', 'Químico Farmacéutico'),
    ])
