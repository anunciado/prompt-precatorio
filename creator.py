import ollama
from guardrails.hub import RegexMatch
from guardrails import Guard
import pandas as pd
import os
import requests

# Configuração do Ollama
conversation_history = [
    {
        "role": "system",
        "content": (
            "Você é um profissional especializado na criação de arquivos .csv, responsável por organizar "
            "e estruturar dados de forma eficiente e padronizada para facilitar seu armazenamento e compartilhamento. "
            "Utiliza ferramentas como planilhas eletrônicas ou scripts de programação para compilar informações "
            "relevantes, garantindo a correta separação por delimitadores, geralmente vírgulas, e mantendo a "
            "consistência no formato dos dados."
        )
    }
]

# URL da API do Banco Central
URL_BANCO_CENTRAL = "http://api.bcb.gov.br/dados/serie/bcdata.sgs.4390/dados?formato=json"
        
class FileCreator:
    """Classe para gerar um arquivo de taxas."""

    def create(self):       
        # Fazer a requisição à API
        response = requests.get(URL_BANCO_CENTRAL)
        if response.status_code == 200:
            # Carregar os dados em um DataFrame
            data = response.json()
            df = pd.DataFrame(data)

            # Converter a coluna 'data' para datetime e a coluna 'valor' para numérico
            df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
            df['valor'] = pd.to_numeric(df['valor'])

            # Extrair ano e mês
            df['ano'] = df['data'].dt.year
            df['mes'] = df['data'].dt.month

            # Reorganizar os dados para formato de tabela com meses como colunas
            tabela = df.pivot_table(index='ano', columns='mes', values='valor', aggfunc='sum')
            tabela.columns = [
                'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
            ]

            # Salvar a tabela em um arquivo CSV
            tabela.to_csv('tabela_selic.csv', index_label='Ano')
        else:
            return (
                "Não foi possível criar o arquivo."
            )

