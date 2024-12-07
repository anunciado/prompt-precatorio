
import ollama
import os

FEW_SHOT_PROMPT_1 = """
    Você recebeu um dataframe Pandas chamado lista_cronologica_df:
    - Colunas: ['Posição', 'Ano', 'Validado', 'Autuado Pelo Chefe', 'Autuado Pelo Juíz', 
                'Baixado', 'Número do Processo', 'Nome do Beneficiário', 'Documento do Beneficiário', 
                'Nome do Ente Devedor', 'Valor', 'Unidade']
    Pergunta do usuário: Quantos processos na lista cronológica do ente devedor {enteDevedor}?
    """
    
FEW_SHOT_ANSWER_1 = """
    resultado = lista_cronologica_df[lista_cronologica_df['Nome do Ente Devedor'] == {enteDevedor} & lista_cronologica_df['Posição'] != 0].shape[0]
    """

FEW_SHOT_PROMPT_2 = """
    Você recebeu um dataframe Pandas chamado lista_prioridade_df:
    - Colunas: ['Posição', 'Ano', 'Validado', 'Autuado Pelo Chefe', 'Autuado Pelo Juíz', 
                'Baixado', 'Percentual Pago', 'Número do Processo', 'Nome do Beneficiário', 
                'Documento do Beneficiário', 'Nome do Ente Devedor', 'Valor', 'Unidade']
    Pergunta do usuário: Quantos beneficiários na lista prioridade do ente devedor {enteDevedor}?
    """
    
FEW_SHOT_ANSWER_2 = """
    resultado = lista_prioridade_df[lista_prioridade_df['Nome do Ente Devedor'] == {enteDevedor} & lista_prioridade_df['Posição'] != 0].shape[0]
    """

FEW_SHOT_PROMPT_3 = """
    Você recebeu um dataframe Pandas chamado lista_cronologica_df:
    - Colunas: ['Posição', 'Ano', 'Validado', 'Autuado Pelo Chefe', 'Autuado Pelo Juíz', 
                'Baixado', 'Número do Processo', 'Nome do Beneficiário', 'Documento do Beneficiário', 
                'Nome do Ente Devedor', 'Valor', 'Unidade']
   Pergunta do usuário: Quanto falta ser pago na lista cronológica do ente devedor {enteDevedor}?
    """
    
FEW_SHOT_ANSWER_3 = """
    resultado = lista_cronologica_df[lista_cronologica_df['Nome do Ente Devedor'] == {enteDevedor} & lista_cronologica_df['Posição'] != 0]['Valor'].sum()
    """

FEW_SHOT_PROMPT_4 = """
    Você recebeu um dataframe Pandas chamado lista_prioridade_df:
    - Colunas: ['Posição', 'Ano', 'Validado', 'Autuado Pelo Chefe', 'Autuado Pelo Juíz', 
                'Baixado', 'Percentual Pago', 'Número do Processo', 'Nome do Beneficiário', 
                'Documento do Beneficiário', 'Nome do Ente Devedor', 'Valor', 'Unidade']
    Pergunta do usuário: Quanto falta ser pago na lista prioridade do ente devedor {enteDevedor}?
    """
    
FEW_SHOT_ANSWER_4 = """
    resultado = lista_prioridade_df[lista_prioridade_df['Nome do Ente Devedor'] == {enteDevedor} & lista_prioridade_df['Posição'] != 0]['Valor'].sum()]
    """

# Configuração do Ollama
conversation_history = [
    {
        "role": "system",
        "content": (
            "Você é um analista de dados experiente, capaz de escrever códigos em Python "
            "capazes de extrair informações solicitadas de conjuntos de dados estruturados como arquivo CSV."
            "Escreva o código do pandas para obter a resposta à pergunta do usuário. armazene a resposta em "
            "uma variável chamada `resultado`. Não inclua importações. Envolva sua resposta de código usando ```."
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
            f"Você recebeu um dataframe Pandas chamado lista_cronologica_df:\n"
            f"- Colunas: ['Posição', 'Ano', 'Validado', 'Autuado Pelo Chefe', 'Autuado Pelo Juíz', 'Baixado', 'Número do Processo', 'Nome do Beneficiário', 'Documento do Beneficiário', 'Nome do Ente Devedor', 'Valor', 'Unidade']\n"
            f"Pergunta do usuário: {query}."
        )
        conversation_history.append({"role": "user", "content": task})
        try:
            completion = ollama.chat(
                messages=conversation_history,
                model='codellama'
            )
            response =  completion['message']['content']
            print("Código gerado: \n" + response)
            conversation_history.append({"role": "assistant", "content": response})
            
            query = """  
                import os
                import pandas as pd

                csv = os.path.join('lista', 'lista-cronologica.csv')  
                # Carregue o arquivo CSV no DataFrame
                df = pd.read_csv(csv)
                        
                {resultado}
                """

            query = query.replace("{resultado}", response)
            query = query.replace("lista-cronologica.csv", os.path.abspath('lista-cronologica.csv'))
            context = {}   
            exec(query,  context)
            return context['resultado']
        except Exception as e:
            return f"Erro ao analisar os dados: {e}"
