from app import db
from datetime import datetime

class Examen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)      # ← antes era nombre_examen
    archivo = db.Column(db.String(255), nullable=False)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    fecha_subida = db.Column(db.DateTime, default=datetime.utcnow)
