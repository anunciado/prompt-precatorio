
import ollama
import os

# Configuração do Ollama
conversation_history = [
    {
        "role": "system",
        "content": (
            "Você é um analista de dados experiente, capaz de escrever códigos em Python "
            "capazes de extrair informações solicitadas de conjuntos de dados estruturados como arquivo CSV."
        )
    }
]

class DataAnalyst:
    """Classe para processar mensagens recebidas e gerar respostas em áudio."""
        
    def analyze_data(self, query):
        task = """  
                Dada a solicitação delimitada por <query>, crie um código python que  
                irá ler o arquivo exatamente como o código delimitado em <abertura>.
                Você  deve completar o código que começou em abertura de modo a atender a <query>. 
                Em <exemplo> tem um exemplo de um código que você deve gerar. 
                Veja que o exemplo já tem <abertura> nele.  

                <query>  
                colunas=(Posição, Ano,Validado,Autuado Pelo Chefe,Autuado Pelo Juíz,Baixado,Número do Processo,Nome do Beneficiário,Documento do Beneficiário, 
                Nome do Ente Devedor, Valor, Unidade).  
                Com base nas colunas do CSV lista-cronologica.csv escreva um código pandas para essa solicitação:  
                {query}
                </query>  

                <abertura>  
                csv = os.path.join('lista', 'lista-cronologica.csv')  
                df = pd.read_csv(csv)  
                </abertura>

                <exemplo>
                import os
                import pandas as pd

                csv = os.path.join('lista', 'lista-cronologica.csv')  
                # Carregue o arquivo CSV no DataFrame
                df = pd.read_csv(csv)

                # Agrupar os dados por 'Nome do Ente Devedor' e somar o 'Valor' para cada grupo
                processos_por_ente_devedor = df.groupby('Nome do Ente Devedor')['Valor'].sum()

                # Identificar o ente devedor com maior valor devido
                ente_devedor_maior_divida = processos_por_ente_devedor.idxmax()
                valor_maior_divida = processos_por_ente_devedor.max()

                resultado = f'O ente devedor com maior dívida é ' + ente_devedor_maior_divida + ' com um total de R$ ' + valor_maior_divida
                </exemplo>

                No código, sempre atribua a o resultado da variável "resultado" como mostra o <exemplo>.
                Importante, só me responda com o código python executável e nada além disso.
        """
        task = task.replace("{query}", query)
        task = task.replace("lista-cronologica.csv", os.path.abspath('lista-cronologica.csv'))

        conversation_history.append({"role": "user", "content": task})

        try:
            completion = ollama.chat(
                messages=conversation_history,
                model='codellama:13b-python'
            )
            response =  completion['message']['content']
            print("Código gerado: \n" + response)
            conversation_history.append({"role": "assistant", "content": response})
            context = {}   
            exec(response,  context)
            return context['resultado']
        except Exception as e:
            return f"Erro ao analisar os dados: {e}"
