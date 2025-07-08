import httpx
import logging
from app.config import settings

logger = logging.getLogger("google")

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"

async def get_access_token():
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
            	GOOGLE_TOKEN_URL,
            	data={
                	"client_id": settings.GOOGLE_CLIENT_ID,
                	"client_secret": settings.GOOGLE_CLIENT_SECRET,
                	"refresh_token": settings.GOOGLE_REFRESH_TOKEN,
                	"grant_type": "refresh_token",
            	},
            	timeout=10
        	)
        response.raise_for_status()
        return response.json()["access_token"]


    except Exception as e:
        logger.error(f"Error al obtener access_token: {e}")
        raise
	