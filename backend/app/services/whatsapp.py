import httpx
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class WhatsAppService:
    def __init__(self):
        self.base_url = f"{settings.EVOLUTION_API_URL}/message"
        self.headers = {
            "apikey": settings.EVOLUTION_API_TOKEN,
            "Content-Type": "application/json"
        }
        self.instance = settings.INSTANCE_NAME

    async def send_text_message(self, phone: str, message: str):
        """
        Sends a text message using Evolution API.
        Phone should be in international format (e.g. 54911...)
        """
        url = f"{self.base_url}/sendText/{self.instance}"
        payload = {
            "number": phone,
            "text": message
        }
        print(f"DEBUG: Envio a URL: {url} con Headers: {self.headers}")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, headers=self.headers, timeout=10.0)
                response.raise_for_status()
                logger.info(f"WhatsApp message sent to {phone}")
                return response.json()
        except Exception as e:
            print(f"DEBUG: CRITICAL ERROR: {type(e)} - {e}")
            logger.error(f"Failed to send WhatsApp message: {e}")
            return None

whatsapp_service = WhatsAppService()
