from datetime import datetime
import logging
import httpx
from sqlalchemy import select
from app.models import ReviewResponse
from app.google_client import get_access_token

# Endpoints de la API de Google Business
REVIEW_URL = "https://mybusiness.googleapis.com/v4/accounts/{accountId}/locations/{locationId}/reviews"
REPLY_URL = "https://mybusiness.googleapis.com/v4/accounts/{accountId}/locations/{locationId}/reviews/{reviewId}/reply"

logger = logging.getLogger("responder")
logger.setLevel(logging.INFO)

# ---------------------------------------
# Utilidades de lógica de negocio
# ---------------------------------------

def generar_respuesta(rating: int) -> str:
    if rating <= 2:
        return "Lamentamos tu experiencia. Gracias por tu comentario, trabajaremos para mejorar."
    elif rating == 3:
        return "Gracias por tus comentarios. Seguimos mejorando cada día."
    else:
        return "¡Gracias por tu calificación positiva! Nos alegra que estés conforme."


def convertir_estrellas(star: str) -> int:
    estrellas = {
        "ONE": 1,
        "TWO": 2,
        "THREE": 3,
        "FOUR": 4,
        "FIVE": 5
    }
    return estrellas.get(star, 0)


async def ya_respondida(db, review_id: str) -> bool:
    query = select(ReviewResponse).where(ReviewResponse.review_id == review_id)
    result = await db.execute(query)
    return result.scalar_one_or_none() is not None


# ---------------------------------------
# Funciones principales del sistema
# ---------------------------------------

async def obtener_reseñas(account_id: str, location_id: str, token: str) -> list:
    url = REVIEW_URL.format(accountId=account_id, locationId=location_id)
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        if resp.status_code != 200:
            raise Exception(f"Error al obtener reseñas: {resp.text}")
        data = resp.json()
        return data.get("reviews", [])


async def responder_reseña(review: dict, account_id: str, location_id: str, token: str, db):
    review_id = review["reviewId"]
    rating_str = review["starRating"]
    estrellas = convertir_estrellas(rating_str)

    if await ya_respondida(db, review_id):
        logger.info(f"Reseña {review_id} ya respondida, se omite.")
        return

    respuesta = generar_respuesta(estrellas)

    reply_url = REPLY_URL.format(
        accountId=account_id,
        locationId=location_id,
        reviewId=review_id
    )
    body = {"comment": respuesta}
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        resp = await client.post(reply_url, headers=headers, json=body)
        if resp.status_code != 200:
            raise Exception(f"Error al responder reseña: {resp.text}")

    nueva = ReviewResponse(
        review_id=review_id,
        user_name=review.get("reviewer", {}).get("displayName"),
        rating=estrellas,
        review_text=review.get("comment", ""),
        response_text=respuesta,
        review_date=datetime.fromisoformat(
            review.get("createTime", "").replace("Z", "+00:00")
        )
    )

    db.add(nueva)
    await db.commit()
    logger.info(f"Reseña {review_id} respondida y guardada.")


async def procesar_reseñas(account_id: str, location_id: str, db):
    try:
        token = await get_access_token()
        reseñas = await obtener_reseñas(account_id, location_id, token)

        for review in reseñas:
            try:
                await responder_reseña(review, account_id, location_id, token, db)
            except Exception as e:
                logger.error(f"Error al procesar reseña {review.get('reviewId')}: {e}")
    except Exception as e:
        logger.error(f"Error general en procesar_reseñas: {e}")
        raise
