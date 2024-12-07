from telegram import Update, Voice
from telegram.ext import CallbackContext
from speech_recognition import Recognizer, AudioFile
from pydub import AudioSegment
from gtts import gTTS
from dotenv import load_dotenv
import os
import time

from analyst import DataAnalyst
from classifier import MessageClassifier
from creator import FileCreator
from position import PositionChecker
from talk import ProfessionalTalk

class MessageProcessor:
    """Classe para processar mensagens recebidas e gerar respostas em áudio."""
    
    def __init__(self):
        self.recognizer = Recognizer()
    
    async def process_voice_message(self, voice: Voice, context: CallbackContext, user_id: int) -> str:
        """Processa uma mensagem de voz e retorna o texto transcrito."""
        file_path = ""
        wav_path = ""
        timestr = time.strftime("%Y%m%d_%H%M%S")
        try:
            # Baixar o arquivo de áudio enviado pelo usuário
            file = await context.bot.get_file(voice.file_id)
            file_path = f"{user_id}_{timestr}_input.ogg"
            await file.download_to_drive(file_path)

            # Converter o áudio de OGG para WAV
            audio = AudioSegment.from_file(os.path.abspath(file_path))
            wav_path = f"{user_id}_{timestr}_input.wav"
            audio.export(wav_path, format="wav")

            # Transcrever o áudio usando SpeechRecognition
            with AudioFile(wav_path) as source:
                audio_data = self.recognizer.record(source)
                user_text = self.recognizer.recognize_google(audio_data, language="pt-BR")
            
            return user_text
        finally:
            # Limpar arquivos temporários
            if os.path.exists(file_path):
                os.remove(file_path)
            if os.path.exists(wav_path):
                os.remove(wav_path)

    def generate_audio_response(self, text: str, user_id: int) -> str:
        """Gera um arquivo de áudio para a resposta e retorna o caminho do arquivo."""
        response_audio_path = f"{user_id}_response.mp3"
        tts = gTTS(text, lang="pt")
        tts.save(response_audio_path)
        return response_audio_path

    async def process_message(self, update: Update, context: CallbackContext) -> None:
        """Processa a mensagem do usuário, seja texto ou áudio, e responde com áudio."""
        user_id = update.message.from_user.id
        input_text = ""
        response_text = ""
        response_audio_path = ""
        file_taxa_path = "tabela_selic.csv"
        
        try:
            if update.message.voice:
                # Processar mensagem de áudio
                input_text = await self.process_voice_message(update.message.voice, context, user_id)
            elif update.message.text:
                # Processar mensagem de texto
                input_text = update.message.text
            
            # Classificar a mensagem
            message_classifier = MessageClassifier()
            tipo = message_classifier.classify_text(input_text)
            print(f"A mensagem foi classificada em: {tipo}.")
            
            # Encaminhar pro agente responsável
            if tipo == "Número do Processo":
                position_checker = PositionChecker()
                response_text = position_checker.check(input_text);
            elif tipo ==  "Lista Cronológica" or tipo ==  "Lista Prioridade":
                data_analyst = DataAnalyst()
                response_text = data_analyst.analyze_data(input_text);
            elif tipo == "Criação de Taxas":
                file_creator = FileCreator()
                response_text = file_creator.create();
            else:
                profissional_talk = ProfessionalTalk()
                response_text = profissional_talk.talk(input_text);
                
            if tipo == "Criação de Taxas": 
                with open(file_taxa_path, "rb") as file:
                    await context.bot.send_document(chat_id=update.effective_chat.id, document=file)
            else:
                # Gerar resposta em áudio
                response_audio_path = self.generate_audio_response(response_text, user_id)

                # Enviar resposta em áudio
                await context.bot.send_voice(chat_id=update.effective_chat.id, voice=open(response_audio_path, "rb"))
        
        except Exception as e:
            await update.message.reply_text(f"Desculpe, ocorreu um erro ao processar sua mensagem: {e}")
        
        finally:
            # Limpar arquivo temporário do áudio de resposta
            if os.path.exists(response_audio_path):
                os.remove(response_audio_path)
                
            # Limpar arquivo temporário de taxa
            if os.path.exists(file_taxa_path):
                os.remove(file_taxa_path)