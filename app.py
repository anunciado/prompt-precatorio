import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters
from processor import MessageProcessor
from dotenv import load_dotenv
import os

load_dotenv()

# Configurar a chave da API da OpenAI
api_key = os.getenv("TELEGRAM_TOKEN")
if not api_key:
    raise ValueError("A chave da API 'TELEGRAM_TOKEN' não foi encontrada. Verifique o arquivo .env.")

# Inicializar o bot
def main():


    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)

    application = Application.builder().token(api_key).build()

    # Instância da classe MessageProcessor
    message_processor = MessageProcessor()

    # Handlers para comandos e mensagens
    application.add_handler(MessageHandler(filters.TEXT | filters.VOICE, message_processor.process_message))

    # Iniciar o bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()