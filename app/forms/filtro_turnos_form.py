# app/forms/filtro_turnos_form.py
from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, SubmitField
from wtforms.validators import Optional

class FiltroTurnosForm(FlaskForm):
    fecha = DateField('Fecha', validators=[Optional()])
    tipo = SelectField('Tipo', choices=[('', 'Todos'), ('presencial', 'Presencial'), ('virtual', 'Virtual')], validators=[Optional()])
    submit = SubmitField('Filtrar')
