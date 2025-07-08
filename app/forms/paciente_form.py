from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

class PacienteForm(FlaskForm):
    nombre = StringField('Nombre completo', validators=[DataRequired(), Length(min=2, max=100)])
    rut = StringField('RUT', validators=[DataRequired()])
    fecha_nacimiento = DateField('Fecha de nacimiento', validators=[DataRequired()])
    sexo = SelectField('Sexo', choices=[('masculino', 'Masculino'), ('femenino', 'Femenino')], validators=[DataRequired()])
    telefono = StringField('Teléfono')
    email = StringField('Email')
    direccion = StringField('Dirección')
    submit = SubmitField('Registrar Paciente')
