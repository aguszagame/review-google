from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.responder import procesar_reseñas
from app.database import get_db
from fastapi import Depends
import asyncio
import logging

from app.utils.mailer import enviar_alerta_mail

logger = logging.getLogger("scheduler")

scheduler = AsyncIOScheduler()

def start_scheduler(app):

    @scheduler.scheduled_job(IntervalTrigger(hours=3))
    def job():
        logger.info("⏳ Ejecutando tarea automática para procesar reseñas...")

        async def _run():
            try:
                async for db in get_db():
                    await procesar_reseñas(
                    	account_id=app.state.account_id,
                    	location_id=app.state.location_id,
                    	db=db,
                	)
            except Exception as e:
                logger.error(f"Error en tarea programada: {e}")
            	
                await enviar_alerta_mail(
                        asunto="🚨 Error en procesador de reseñas",
                        cuerpo=str(e),
                        destino="destinatario@dominio.com"
                    )


        asyncio.create_task(_run())

    scheduler.start()
