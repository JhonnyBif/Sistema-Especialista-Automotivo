import pandas as pd
from experta import *

## Install pip install experta

## Caso não funcioned dê os seguintes comandos:
### python -m site
### procure por: Python\\Python312\\Lib\\site-packages
### Acesse a pasta e procure por frozendict entre e abre o arquivo __init__.py
### substituia import collections por import collections \n from collections.abc import Mapping 
### Procure e substituia class frozendict(collections.Mapping) por from collections.abc import Mapping \n class frozendict(Mapping)
## Salve e feche o arquivo

def carregar_dados_carros(arquivo_excel):
    return pd.read_excel(arquivo_excel)

class SistemaRecomendacaoCarro(KnowledgeEngine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.carros = carregar_dados_carros('./BaseDadosRevenda.xlsx')  # Carregar dados de carros
        
    @DefFacts()
    def _initial_facts(self):
        yield Fact(action="começar")
    
    @Rule(Fact(action='começar'), NOT(Fact(orcamento=W())), salience=10)
    def pedir_orcamento(self):
        while True:
            try:
                orcamento = input("Qual é o seu orcamento para o carro? R$ ").strip()
                # Verifica se o valor inserido é um número e converte para inteiro
                orcamento = int(orcamento)
                if orcamento <= 0:
                    print("Orçamento inválido. Por favor, insira um valor maior que zero.")
                else:
                    # Se o orcamento é válido, declara o fato e sai do loop
                    self.declare(Fact(orcamento=orcamento))
                    break
            except ValueError:
                print("Orçamento inválido. Por favor, insira um valor numérico válido.")
    
    @Rule(Fact(orcamento=W()), NOT(Fact(uso=W())), salience=9)
    def pedir_uso(self):
        uso = input("Qual é o uso principal do carro? (cidade/estrada) ").strip().lower()
        if uso in ['cidade', 'estrada']:
            self.declare(Fact(uso=uso))
        else:
            print("Uso inválido. Por favor, responda 'cidade' ou 'estrada'.")
            self.pedir_uso()

    @Rule(Fact(uso=W()), NOT(Fact(tipo=W())), salience=8)
    def pedir_tipo(self):
        tipo = input("Qual tipo de carro você prefere? (sedan/SUV/esportivo) ").strip().lower()
        if tipo in ['sedan', 'suv', 'esportivo']:
            self.declare(Fact(tipo=tipo))
        else:
            print("Tipo inválido. Por favor, responda 'sedan', 'suv' ou 'esportivo'.")
            self.pedir_tipo()

    @Rule(Fact(uso=W()), Fact(tipo=W()), Fact(orcamento=W()), Fact(condicao=W()))
    def recomendar_carro(self):
        orcamento = next((fact['orcamento'] for fact in self.facts.values() if 'orcamento' in fact), 0)
        uso = next((fact['uso'] for fact in self.facts.values() if 'uso' in fact), '')
        tipo = next((fact['tipo'] for fact in self.facts.values() if 'tipo' in fact), '')
        condicao = next((fact['condicao'] for fact in self.facts.values() if 'condicao' in fact), '')

        # Filtrar carros com base no tipo e uso
        carros_filtrados = self.carros[
            (self.carros['CATEGORIA'].str.lower() == tipo) &
            (self.carros['TIPO'].str.lower() == uso)
        ]

        # Verificar se há carros disponíveis
        if carros_filtrados.empty:
            print("Infelizmente, não temos opções que atendem aos seus critérios.")
            return
        
        # Ajustar filtragem com base na condição e orcamento
        if condicao == 'novo':
            carros_filtrados = carros_filtrados[carros_filtrados['ANO'] >= 2022]  # Considerando ano 2022 como mínimo para novo
        
        carros_recomendados = carros_filtrados[carros_filtrados['VALOR'] <= orcamento]
        
        if carros_recomendados.empty:
            print(f"Infelizmente, não temos {tipo} {condicao} que caibam no seu orcamento. Recomendamos opções usadas ou um orcamento maior.")
        else:
            print("Aqui estão algumas recomendações com base em suas preferências:")
            for _, carro in carros_recomendados.iterrows():
                print(f"Marca: {carro['MARCA']}, Modelo: {carro['MODELO']}, Tipo: {carro['CATEGORIA']}, Ano: {carro['ANO']}, Cor: {carro['COR']}, Preço: R$ {carro['VALOR']}")


if __name__ == "__main__":
    engine = SistemaRecomendacaoCarro()
    
    # Coletar informações do usuário
    engine.reset()  # Prepare o motor de regras
    
    # Recolher detalhes do usuário
    uso = input("Qual é o uso principal do carro? (cidade/estrada) ").strip().lower()
    tipo = input("Qual tipo de carro você prefere? (sedan/SUV/esportivo) ").strip().lower()
    condicao = input("Você prefere um carro novo ou usado? (novo/usado) ").strip().lower()
    
    engine.declare(Fact(uso=uso))
    engine.declare(Fact(tipo=tipo))
    engine.declare(Fact(condicao=condicao))
    
    # Rodar o sistema
    engine.run()

