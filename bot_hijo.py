import os
import json
import httpx
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# --- LEER VARIABLES DE RAILWAY ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

async def procesar_todo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto_usuario = update.message.text
    await update.message.reply_text("🎧 Sisi DJ en la nube: Procesando tu beat...")

    # Forzamos el modo generador de audio
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    instruccion = (
        f"Eres un productor de Trap Dark. Genera un ARCHIVO DE AUDIO (.mp3) "
        f"de 15 segundos con este estilo: {texto_usuario}. "
        f"Responde SOLO con el link de descarga directa o el objeto de audio nativo."
    )

    payload = {
        "contents": [{"parts": [{"text": instruccion}]}],
        "safetySettings": [{"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}]
    }

    async with httpx.AsyncClient(timeout=120.0) as client: # Tiempo extra por si el server está lento
        try:
            response = await client.post(url, json=payload)
            data = response.json()
            respuesta = data['candidates'][0]['content']['parts'][0]['text']
            await update.message.reply_text(respuesta)
        except Exception as e:
            await update.message.reply_text(f"⚠️ Error en el laboratorio: {e}")

if __name__ == '__main__':
    # Railway usa el worker del Procfile, pero esto asegura el arranque
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), procesar_todo))
    print("🚀 SISTEMA CRISTIAN ONLINE EN RAILWAY")
    app.run_polling()
