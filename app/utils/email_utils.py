from flask_mail import Message
from app import mail

def enviar_correo(destinatario, asunto, nombre_paciente, nombre_examen):
    msg = Message(asunto, recipients=[destinatario])
    msg.body = f"""Estimado/a {nombre_paciente},

Se ha subido un nuevo examen a su ficha médica.

Nombre del examen: {nombre_examen}

Saludos cordiales,
Clínica Sansar Bien"""
    try:
        mail.send(msg)
        print("✅ Correo enviado a:", destinatario)
    except Exception as e:
        print("❌ Error al enviar correo:", e)
