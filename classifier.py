from telegram import Update
from telegram.ext import CallbackContext
import ollama

# Configuração do Ollama
conversation_history = [
    {
        "role": "system",
        "content": (
            "Você é um classificador de texto. Sua tarefa é classificar os textos fornecidos "
            "em categorias específicas. Responda apenas com o nome da categoria apropriada."
        )
    }
]

# Definir categorias para classificação
CATEGORIES = ["Processo", "Trivialidade"]

class MessageClassifier:
    """Classe para processar mensagens recebidas e gerar respostas em áudio."""
        
    def classify_text(self, input_text):
        """
        Função que usa o Ollama para classificar o texto em categorias fornecidas.

        Args:
            input_text (str): Texto a ser classificado.
            categories (list): Lista de categorias possíveis.

        Returns:
            str: Categoria escolhida ou uma mensagem de erro.
        """
        user_message = (
            f"Texto: {input_text}\n"
            f"Classifique nas categorias: {', '.join(CATEGORIES)}."
        )
        conversation_history.append({"role": "user", "content": user_message})

        try:
            completion = ollama.chat(
                messages=conversation_history,
                model='llama3.2'
            )
            response =  completion['message']['content']
            conversation_history.append({"role": "assistant", "content": response})
            return response
        except Exception as e:
            return f"Erro ao classificar o texto: {e}"
