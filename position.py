import ollama
from guardrails.hub import RegexMatch
from guardrails import Guard
import pandas as pd
import os

# Configuração do Ollama
conversation_history = [
    {
        "role": "system",
        "content": (
            "Você é uma profissional corretora de texto, responsável por revisar, ajustar e " 
            "aprimorar conteúdos para garantir clareza, correção gramatical, coesão e coerência, "
            "alinhando-os às normas linguísticas e ao objetivo comunicativo pretendido. "
        )
    }
]

# Patterns pra busca
CPF_PATTERN = r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b'
CNPJ_PATTERN = r'\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b'
PROCESS_PATTERN = r'\b\d{7}-\d{2}\.\d{4}\.\d{1}\.\d{2}\.\d{4}\b'
        
class PositionChecker:
    """Classe para procurar um processo em uma lista com base no CPF, CNPJ ou número do processo."""
    def __init__(self):
        # Definir regex para CPF, CNPJ e número de processo usando RegexMatch
        self.cpf_validator = Guard().use(RegexMatch(CPF_PATTERN))
        self.cnpj_validator = Guard().use(RegexMatch(CNPJ_PATTERN))
        self.process_validator = Guard().use(RegexMatch(PROCESS_PATTERN))
        lista_cronologica_path = 'lista-cronologica.csv' 
        lista_prioridade_path = 'lista-prioridade.csv' 
        self.lista_cronologica = pd.read_csv(os.path.abspath(lista_cronologica_path))
        self.lista_prioridade = pd.read_csv(os.path.abspath(lista_prioridade_path))

    def check(self, input_text):       
        cpf_validation = self.cpf_validator.validate(input_text)
        cnpj_validation = self.cnpj_validator.validate(input_text)
        process_validation = self.process_validator.validate(input_text)
        coluna = ''

        if cpf_validation.validation_passed or cnpj_validation.validation_passed:
            coluna = 'Documento do Beneficiário'

        elif process_validation.validation_passed:
            coluna = 'Número do Processo'
            
        else: 
            return (
                "A mensagem enviada não contém um CPF, CNPJ ou número de processo válido. "
                "Por favor, revise e envie novamente."
            )
            
        # Filtrar as linhas com o número do processo
        linhas_cronologica_encontradas = self.lista_cronologica[self.lista_cronologica[coluna] == input_text]
        linhas_prioridade_encontradas = self.lista_prioridade[self.lista_prioridade[coluna] == input_text]

        user_message = (
            f"Escreva um texto resumido com o resultados abaixo informando a posição, o valor e o número do processo. \n"
            f"Resultados Cronológico: {linhas_cronologica_encontradas.astype(str)}\n"
            f"Resultados Prioridade: {linhas_prioridade_encontradas.astype(str)}\n"
        )
        
        conversation_history.append({"role": "user", "content": user_message})

        try:
            completion = ollama.chat(
                messages=conversation_history,
                model='llama3.2'
            )
            response =  completion['message']['content']
            conversation_history.append({"role": "assistant", "content": response})
            print(response)
            return response
        except Exception as e:
            return f"Erro ao classificar o texto: {e}"


