from fastapi_mail import FastMail, MessageSchema
from app.config import mail_config
import logging

logger = logging.getLogger("mailer")

fm = FastMail(mail_config)

async def enviar_alerta_mail(asunto: str, cuerpo: str, destino: str):
    mensaje = MessageSchema(
    	subject=asunto,
    	recipients=[destino],
    	body=cuerpo,
    	subtype="plain"
	)

    try:
        await fm.send_message(mensaje)
        logger.info("✉️ Alerta enviada por mail")
    except Exception as e:
        logger.error(f"No se pudo enviar alerta por mail: {e}")

