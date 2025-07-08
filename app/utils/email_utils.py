from flask_mail import Message
from app import mail
from flask import current_app

def enviar_correo(destinatario, asunto, cuerpo):
    msg = Message(asunto, recipients=[destinatario])
    msg.body = cuerpo

    try:
        with current_app.app_context():
            mail.send(msg)
            print("✅ Correo enviado a:", destinatario)
    except Exception as e:
        print("❌ Error al enviar correo:", e)
