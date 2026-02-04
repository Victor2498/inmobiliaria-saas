from fastapi import APIRouter, Request, HTTPException, Depends
from app.services.whatsapp import whatsapp_service
from app.db.session import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models.base_entities import Property
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/webhook")
async def whatsapp_webhook(request: Request, session: AsyncSession = Depends(get_session)):
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
                messages = [data] if data.get('key') else []

            for message in messages:
                if message.get('key', {}).get('fromMe'):
                    continue

                remote_jid = message.get('key', {}).get('remoteJid')
                if not remote_jid or '@s.whatsapp.net' not in remote_jid:
                    continue

                msg_body = message.get('message', {})
                content = (
                    msg_body.get('conversation') or 
                    msg_body.get('extendedTextMessage', {}).get('text') or
                    msg_body.get('imageMessage', {}).get('caption')
                )

                if content:
                    sender_name = message.get('pushName', 'Usuario')
                    phone_number = remote_jid.split('@')[0]
                    
                    # 1. Fetch available properties to give context to AI
                    result = await session.execute(select(Property).where(Property.status == "available"))
                    properties = result.scalars().all()
                    
                    prop_context = "Propiedades disponibles:\n"
                    for p in properties:
                        prop_context += f"- {p.address} ({p.city}): {p.type}, ${p.price}\n"
                    
                    # 2. Process with OpenAI
                    from app.services.openai_service import openai_service
                    ai_response = await openai_service.generate_response(
                        content, 
                        context=f"Usuario: {sender_name}\n\n{prop_context}"
                    )
                    
                    # 3. Send response back
                    if ai_response:
                        await whatsapp_service.send_text_message(phone_number, ai_response)

        return {"status": "success", "event": event_type}

    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return {"status": "error", "reason": str(e)}
