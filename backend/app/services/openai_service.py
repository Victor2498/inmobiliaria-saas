from openai import AsyncOpenAI
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        if not self.api_key:
            logger.warning("OPENAI_API_KEY is not set in settings! AI features will be disabled.")
            self.client = None
        else:
            logger.info("OpenAI client initialized with API key.")
            self.client = AsyncOpenAI(api_key=self.api_key)

    async def generate_response(self, user_message: str, context: str = "") -> str:
        """
        Generates a response using OpenAI GPT-4o or GPT-3.5-turbo.
        """
        if not self.client:
            return "Lo siento, mi cerebro de IA no está conectado actualmente."

        system_prompt = f"""
        Eres 'InmoneaBot', un asistente virtual inteligente para una inmobiliaria.
        Tu objetivo es ayudar a inquilinos y clientes potenciales de manera amable, profesional y eficiente.
        
        Contexto del usuario: {context}

        Instrucciones:
        1. Responde preguntas sobre propiedades, alquileres y pagos.
        2. Si un inquilino pregunta por su deuda, intenta responder basándote en el contexto (próximamente conectado a DB).
        3. Sé conciso y directo. Usa emojis ocasionalmente para ser amigable.
        4. Si no sabes la respuesta, ofrece contactar a un humano.
        """

        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo", # Or gpt-4o if available/preferred
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=300,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"OpenAI API Error: {e}")
            return "Tuve un pequeño problema técnico intentando pensar mi respuesta. ¿Podrías intentar de nuevo en un momento?"

openai_service = OpenAIService()
