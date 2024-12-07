
import ollama
import os
import pandas as pd
import os

FEW_SHOT_PROMPT_1 = """
    Você recebeu um dataframe Pandas chamado df:
    - Colunas: ['Posição', 'Ano', 'Validado', 'Autuado Pelo Chefe', 'Autuado Pelo Juíz', 
                'Baixado', 'Número do Processo', 'Nome do Beneficiário', 'Documento do Beneficiário', 
                'Nome do Ente Devedor', 'Valor', 'Unidade']
    Pergunta do usuário: Quantos processos na lista cronológica do ente devedor {enteDevedor}?
    """
    
FEW_SHOT_ANSWER_1 = """
    lista_cronologica[lista_cronologica['Nome do Ente Devedor'] == {enteDevedor}].shape[0]
    """

FEW_SHOT_PROMPT_2 = """
    Você recebeu um dataframe Pandas chamado df:
    - Colunas: ['Posição', 'Ano', 'Validado', 'Autuado Pelo Chefe', 'Autuado Pelo Juíz', 
                'Baixado', 'Percentual Pago', 'Número do Processo', 'Nome do Beneficiário', 
                'Documento do Beneficiário', 'Nome do Ente Devedor', 'Valor', 'Unidade']
    Pergunta do usuário: Quantos beneficiários na lista prioridade do ente devedor {enteDevedor}?
    """
    
FEW_SHOT_ANSWER_2 = """
    lista_prioridade[lista_prioridade['Nome do Ente Devedor'] == {enteDevedor}].shape[0]
    """

FEW_SHOT_PROMPT_3 = """
    Você recebeu um dataframe Pandas chamado df:
    - Colunas: ['Posição', 'Ano', 'Validado', 'Autuado Pelo Chefe', 'Autuado Pelo Juíz', 
                'Baixado', 'Número do Processo', 'Nome do Beneficiário', 'Documento do Beneficiário', 
                'Nome do Ente Devedor', 'Valor', 'Unidade']
    Pergunta do usuário: Quanto falta ser pago na lista cronológica do ente devedor {enteDevedor}?
    """
    
FEW_SHOT_ANSWER_3 = """
    lista_cronologica[lista_cronologica['Nome do Ente Devedor'] == {enteDevedor}]['Valor'].sum()
    """

FEW_SHOT_PROMPT_4 = """
    Você recebeu um dataframe Pandas chamado df:
    - Colunas: ['Posição', 'Ano', 'Validado', 'Autuado Pelo Chefe', 'Autuado Pelo Juíz', 
                'Baixado', 'Percentual Pago', 'Número do Processo', 'Nome do Beneficiário', 
                'Documento do Beneficiário', 'Nome do Ente Devedor', 'Valor', 'Unidade']
    Pergunta do usuário: Quanto falta ser pago na lista prioridade do ente devedor {enteDevedor}?
    """
    
FEW_SHOT_ANSWER_4 = """
    lista_prioridade[lista_prioridade['Nome do Ente Devedor'] == {enteDevedor}]['Valor'].sum()
    """

# Configuração do Ollama
conversation_history = [
    {
        "role": "system",
        "content": (
            "Você é um analista de dados experiente, capaz de escrever códigos em Python "
            "capazes de extrair informações solicitadas de conjuntos de dados estruturados como arquivo CSV."
            "Escreva o código do pandas para obter a resposta à pergunta do usuário."
        )
    },
    {
        "role": "user",
        "content": FEW_SHOT_PROMPT_1
    },
    {
        "role": "assistant",
        "content": FEW_SHOT_ANSWER_1
    },
    {
        "role": "user",
        "content": FEW_SHOT_PROMPT_2
    },
    {
        "role": "assistant",
        "content": FEW_SHOT_ANSWER_2
    },
    {
        "role": "user",
        "content": FEW_SHOT_PROMPT_3
    },
    {
        "role": "assistant",
        "content": FEW_SHOT_ANSWER_3
    },
    {
        "role": "user",
        "content": FEW_SHOT_PROMPT_4
    },
    {
        "role": "assistant",
        "content": FEW_SHOT_ANSWER_4
    },
]

class DataAnalyst:
    """Classe para processar mensagens recebidas e gerar respostas em áudio."""
        
    def analyze_data(self, query):
        task = (
            f"Você recebeu um dataframe Pandas chamado df:\n"
            f"- Colunas: ['Posição', 'Ano', 'Validado', 'Autuado Pelo Chefe', 'Autuado Pelo Juíz', 'Baixado', 'Número do Processo', 'Nome do Beneficiário', 'Documento do Beneficiário', 'Nome do Ente Devedor', 'Valor', 'Unidade']\n"
            f"Pergunta do usuário: {query}."
        )
        conversation_history.append({"role": "user", "content": task})
        try:
            completion = ollama.chat(
                messages=conversation_history,
                model='codellama:13b'
            )
            response =  completion['message']['content']
            conversation_history.append({"role": "assistant", "content": response})
            lista_cronologica_path = 'lista-cronologica.csv' 
            lista_prioridade_path = 'lista-prioridade.csv' 
            lista_cronologica = pd.read_csv(os.path.abspath(lista_cronologica_path))
            lista_prioridade = pd.read_csv(os.path.abspath(lista_prioridade_path))
            print("Código gerado: \n" + response)

            resultado = pd.eval(response)
            return str(resultado)
        except Exception as e:
            print(e)
            return f"Erro ao analisar os dados: {e}"
