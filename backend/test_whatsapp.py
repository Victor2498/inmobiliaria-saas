import asyncio
import sys
import os

# Add backend to sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.services.whatsapp import whatsapp_service
import logging

# Configure logging to see errors
logging.basicConfig(level=logging.INFO)


async def test_send():
    print("--- Test de Envio de WhatsApp (Evolution API) ---")
    # number = input("Ingrese el numero de destino (formato internacional ej: 54911...): ")
    number = "5493794352784" # Added 9 for Argentina mobile if needed, usually 54 + 9 + area + num. User gave 54 379... let's try 5493794352784 or 543794352784. Evolution API often needs the 9 for AR. Let's try as provided first stripped of spaces? Or standard AR format.
    # User input: 54 3794352784. 
    # If it is Argentina Corrientes (379), it usually needs 9 between 54 and area code for WhatsApp.
    # Let's clean it.
    raw_input = "54 3794352784"
    number = raw_input.replace(" ", "")
    if len(number) == 12 and number.startswith("54"): # 54 379 435 2784
       # It might be missing the 9. WhatsApp usually requires 549...
       # Let's try adding it if it looks like an AR mobile without it.
       # Actually, let's try exactly what the user gave first (cleaned), or maybe the user knows best.
       # But for automation safety, I will assume 549 is safer for AR.
       pass 
    
    number = "5493794352784" # forcing the standard format just in case


    print(f"Enviando mensaje de prueba a {number}...", flush=True)
    result = await whatsapp_service.send_text_message(number, "Hola! Esta es una prueba de Inmonea System 🚀")
    print(f"Result: {result}", flush=True)

    
    if result:
        print("✅ Mensaje enviado con exito!")
        print("Respuesta API:", result)
    else:
        print("❌ Fallo el envio. Verifique el log o las credenciales.")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(test_send())
