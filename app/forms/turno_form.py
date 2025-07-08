from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, TimeField, SubmitField
from wtforms.validators import DataRequired
from app.models.paciente import Paciente

class TurnoForm(FlaskForm):
    paciente_id = SelectField('Paciente', coerce=int, validators=[DataRequired()])
    fecha = DateField('Fecha', validators=[DataRequired()])
    hora = TimeField('Hora', validators=[DataRequired()])
    motivo = SelectField('Motivo', choices=[('consulta', 'Consulta'), ('control', 'Control')], validators=[DataRequired()])
    tipo = SelectField('Tipo', choices=[('presencial', 'Presencial'), ('virtual', 'Virtual')], validators=[DataRequired()])
    submit = SubmitField('Asignar Turno')

    def __init__(self, *args, **kwargs):
        super(TurnoForm, self).__init__(*args, **kwargs)
        self.paciente_id.choices = [(p.id, p.nombre) for p in Paciente.query.all()]
