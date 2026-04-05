import os
import json
import httpx
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# --- TUS CREDENCIALES DIRECTAS ---
TELEGRAM_TOKEN = "8688750839:AAFkQgo3Wq262lU6gmYjmHwm1TEvtOH96nc"
GEMINI_API_KEY = "AIzaSyBt1a1hnFkenWtcSXeYzZFliiA5micTcVM"

async def procesar_todo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto_usuario = update.message.text
    
    # Aviso inmediato para que el chamo sepa que el bot recibió la orden
    await update.message.reply_text("🎧 Sisi DJ: Conectando con el motor de audio... Aguanta un pelo, Cristian.")

    # URL del motor de Google
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    # Instrucción de "Choque" para que no se ponga a hablar y genere audio
    instruccion = (
        f"ACTÚA COMO UN MOTOR DE GENERACIÓN DE AUDIO NATIVO PROFESIONAL. "
        f"Tu misión es crear un archivo de audio real (.mp3) de 15 a 30 segundos. "
        f"Estilo solicitado: {texto_usuario}. "
        f"No escribas introducciones. Entrega directamente el link de descarga del audio "
        f"o el objeto binario del sonido generado."
    )

    payload = {
        "contents": [{"parts": [{"text": instruccion}]}],
        "safetySettings": [
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"}
        ]
    }

    # Tiempo de espera largo (120 seg) por si el internet de Caracas se pone pesado
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            response = await client.post(url, json=payload)
            data = response.json()
            
            # Extraemos la respuesta de la IA
            if 'candidates' in data:
                respuesta = data['candidates'][0]['content']['parts'][0]['text']
                await update.message.reply_text(respuesta)
            else:
                await update.message.reply_text("⚠️ Google está ocupado. Intenta de nuevo en un minuto.")
                
        except Exception as e:
            await update.message.reply_text(f"❌ Error de conexión en la nube: {e}")

if __name__ == '__main__':
    # Configuración de arranque para Railway
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # Filtro: Todo lo que NO sea un comando (/), Sisi lo procesa como música
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), procesar_todo))
    
    print("🚀 SISTEMA CRISTIAN TORRES: ¡Laboratorio Online!")
    app.run_polling()
