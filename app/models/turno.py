from app import db

class Turno(db.Model):
    __tablename__ = 'turno'
    
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    
    paciente = db.relationship('Paciente', backref='turnos', lazy=True)

    # Resto de tus columnas:
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    motivo = db.Column(db.String(255))
    profesional_id = db.Column(db.Integer)
