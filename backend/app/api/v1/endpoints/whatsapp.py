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
        event_type = payload.get('event')
        data = payload.get('data', {})
        
        logger.info(f"Received webhook event: {event_type}")
        
        # Evolution API sends messages in 'messages.upsert' event
        if event_type == 'messages.upsert':
            messages = data.get('messages', [])
            if not messages:
                # Fallback to direct data if it's a legacy or single message payload
                messages = [data] if data.get('key') else []

            for message in messages:
                # Avoid processing our own messages
                if message.get('key', {}).get('fromMe'):
                    continue

                remote_jid = message.get('key', {}).get('remoteJid')
                if not remote_jid or '@s.whatsapp.net' not in remote_jid:
                    continue

                # Extract content from different possible locations
                msg_body = message.get('message', {})
                content = (
                    msg_body.get('conversation') or 
                    msg_body.get('extendedTextMessage', {}).get('text') or
                    msg_body.get('imageMessage', {}).get('caption')
                )

                if content:
                    sender_name = message.get('pushName', 'Usuario')
                    phone_number = remote_jid.split('@')[0]
                    
                    print(f"DEBUG: Processing message from {sender_name} ({phone_number}): {content}")
                    
                    # 1. Process with OpenAI
                    from app.services.openai_service import openai_service
                    ai_response = await openai_service.generate_response(content, context=f"Usuario: {sender_name}")
                    
                    # 2. Send response back
                    if ai_response:
                        await whatsapp_service.send_text_message(phone_number, ai_response)

        return {"status": "success", "event": event_type}

    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        import traceback
        traceback.print_exc()
        return {"status": "error", "reason": str(e)}
