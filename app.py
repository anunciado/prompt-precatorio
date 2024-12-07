import logging
from telegram import Update
from telegram.ext import Application, CallbackContext, CommandHandler, MessageHandler, filters
from processor import MessageProcessor
from dotenv import load_dotenv
import os

load_dotenv()

# Configurar a chave da API da OpenAI
api_key = os.getenv("TELEGRAM_TOKEN")
if not api_key:
    raise ValueError("A chave da API 'TELEGRAM_TOKEN' não foi encontrada. Verifique o arquivo .env.")

# Função de boas-vindas
async def start(update: Update, context: CallbackContext) -> None:
    """Sejam bem vindos ao PrecaBot."""
    await update.message.reply_text("""
        Olá! Eu sou o PrecaBOT, seu assistente virtual no Telegram! 🚀  
        Estou aqui para facilitar sua vida e oferecer uma experiência prática e divertida. Confira abaixo tudo o que posso fazer por você:  

        1️⃣ **Verificar a posição do processo**  
        - Basta enviar um CPF, CNPJ ou número do processo válido.

        2️⃣ **Criar um arquivo de taxas**  
        - Basta pedir com carinho.  

        3️⃣ **Análisar dados das listas cronológica e prioridade**  
        - Pergunte sobre qualquer coisa e eu trarei informações das listas que precisar.  

        4️⃣ **Entretenimento**  
        - Pode conversar comigo sobre diversos temas sempre que quiser.  

        Sou rápido, eficiente e sempre disponível para ajudar. Basta me enviar uma mensagem, e eu estarei pronto para interagir com você. Experimente e descubra tudo o que posso fazer!  

        💬 **Vamos começar?**  
        Envie um texto ou áudio, e eu responderei com um áudio! 😊                        
        """)

# Inicializar o bot
def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)

    application = Application.builder().token(api_key).build()

    # Instância da classe MessageProcessor
    message_processor = MessageProcessor()

    # Handlers para comandos e mensagens
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT | filters.VOICE, message_processor.process_message))

    # Iniciar o bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()