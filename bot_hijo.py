import os
import requests
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- CONFIGURACIÓN ---
GEMINI_API_KEY = "AIzaSyC8h_cKzZPAjk3gw4I9KOk9ZT_u4GDZAMk"
TELEGRAM_TOKEN = "8688750839:AAFkQgo3Wq262lU6gmYjmHwm1TEvtOH96nc"

# --- FUNCIÓN PARA SEPARAR VOCES ---
async def separar_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎧 Recibido. Iniciando extracción de voces... esto puede tardar un poco, Jefe.")
    
    # 1. Descargar el archivo que envió el usuario
    file = await context.bot.get_file(update.message.audio.file_id)
    input_path = "pista_original.mp3"
    await file.download_to_drive(input_path)

    # 2. Comando de Spleeter (Separa en 2 pistas: vocals.wav y accompaniment.wav)
    # Usamos subprocess para llamar al motor de audio del sistema
    try:
        subprocess.run(["spleeter", "separate", "-p", "spleeter:2stems", "-o", "output", input_path])
        
        # 3. Enviar los resultados de vuelta al usuario
        vocals = "output/pista_original/vocals.wav"
        pista = "output/pista_original/accompaniment.wav"
        
        await update.message.reply_audio(audio=open(vocals, 'rb'), caption="🎤 Aquí tiene solo la VOZ, Jefe.")
        await update.message.reply_audio(audio=open(pista, 'rb'), caption="🎸 Aquí tiene la PISTA (Instrumental).")
        
    except Exception as e:
        await update.message.reply_text(f"💥 Error en el procesador de audio: {e}")

# --- AGREGAR EL HANDLER AL ARRANQUE ---
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # Maneja mensajes de texto (Gemini)
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), responder_manual))
    
    # NUEVO: Maneja archivos de audio para separar pistas
    app.add_handler(MessageHandler(filters.AUDIO, separar_audio))
    
    print("🚀 SISI DJ CON SEPARADOR DE PISTAS ACTIVO")
    app.run_polling()
