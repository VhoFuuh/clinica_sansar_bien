from app import db
from datetime import datetime

class Turno(db.Model):
    __tablename__ = 'turno'
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    paciente = db.relationship('Paciente', backref='turnos', lazy=True)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    motivo = db.Column(db.String(255))

    # Clave foránea al usuario (profesional)
    profesional_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    profesional = db.relationship('User', backref='turnos', lazy=True)

    # Timestamp de creación
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)