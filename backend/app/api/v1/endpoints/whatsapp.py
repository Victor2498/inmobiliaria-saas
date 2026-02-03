from fastapi import APIRouter, Request, HTTPException
from app.services.whatsapp import whatsapp_service
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/webhook")
async def whatsapp_webhook(request: Request):
    """
    Receives webhook events from Evolution API.
    """
    try:
        payload = await request.json()
        logger.info(f"Received webhook: {payload}")
        
        # Basic validation (Evolution API structure)
        data = payload.get('data')
        if not data:
            return {"status": "ignored", "reason": "no data"}

        # Handle text messages
        message_type = data.get('messageType')
        if message_type == 'conversation' or message_type == 'extendedTextMessage':
             # Here we will eventually integrate OpenAI
             # For now, let's just log it and maybe echo simple response if needed
             sender = data.get('pushName')
             msg_content = data.get('message', {}).get('conversation') or data.get('message', {}).get('extendedTextMessage', {}).get('text')
             remote_jid = data.get('key', {}).get('remoteJid')
             
             print(f"New Message from {sender} ({remote_jid}): {msg_content}")
             
             if msg_content:
                 # 1. Process with OpenAI
                 from app.services.openai_service import openai_service
                 ai_response = await openai_service.generate_response(msg_content, context=f"Usuario: {sender}")
                 
                 # 2. Send response back via WhatsApp
                 # Extract phone number from JID (e.g., 549379...@s.whatsapp.net -> 549379...)
                 phone_number = remote_jid.split('@')[0]
                 await whatsapp_service.send_text_message(phone_number, ai_response)

             
        return {"status": "received"}

    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return {"status": "error", "reason": str(e)}
