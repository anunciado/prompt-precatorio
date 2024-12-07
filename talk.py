import ollama

# Configuração do Ollama
conversation_history = [
    {
        "role": "system",
        "content": (
            "Você é uma profissional de conversação, especialista em estabelecer, conduzir e" 
            "facilitar diálogos eficazes, promovendo a troca de informações, ideias e sentimentos "
            "de maneira clara, empática e assertiva. Com sua habilidade, atua em contextos diversos, "
            "como educação, mediação de conflitos, atendimento ao cliente ou desenvolvimento pessoal, " 
            "criando conexões humanas significativas, resolvendo problemas e alcançando metas " 
            "específicas por meio da comunicação."
        )
    }
]

class ProfessionalTalk:
        
    def talk(self, input_text):
        conversation_history.append({"role": "user", "content": input_text})

        try:
            completion = ollama.chat(
                messages=conversation_history,
                model='llama3.2'
            )
            response =  completion['message']['content']
            conversation_history.append({"role": "assistant", "content": response})
            return response
        except Exception as e:
            return f"Erro ao responder o texto: {e}"