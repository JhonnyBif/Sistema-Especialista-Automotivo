from experta import *

## Install pip install experta

## Caso não funcioned dê os seguintes comandos:
### python -m site
### procure por: Python\\Python312\\Lib\\site-packages
### Acesse a pasta e procure por frozendict entre e abre o arquivo __init__.py
### substituia import collections por import collections \n from collections.abc import Mapping 
### Procure e substituia class frozendict(collections.Mapping) por from collections.abc import Mapping \n class frozendict(Mapping)
## Salve e feche o arquivo

class SistemaRecomendacaoCarro(KnowledgeEngine):
    
    @DefFacts()
    def _initial_facts(self):
        yield Fact(action="começar")
    
    @Rule(Fact(action='começar'), NOT(Fact(orçamento=W())), salience=10)
    def pedir_orcamento(self):
        self.declare(Fact(orçamento=int(input("Qual é o seu orçamento para o carro? R$ "))))
    
    @Rule(Fact(orçamento=W()), NOT(Fact(uso=W())), salience=9)
    def pedir_uso(self):
        uso = input("Qual é o uso principal do carro? (cidade/estrada) ").strip().lower()
        if uso in ['cidade', 'estrada']:
            self.declare(Fact(uso=uso))
        else:
            print("Uso inválido. Por favor, responda 'cidade' ou 'estrada'.")
            self.pedir_uso()

    @Rule(Fact(uso='cidade'), NOT(Fact(tipo=W())), salience=8)
    def pedir_tipo_cidade(self):
        tipo = input("Qual tipo de carro você prefere? (sedan/SUV/esportivo) ").strip().lower()
        if tipo in ['sedan', 'suv', 'esportivo']:
            self.declare(Fact(tipo=tipo))
        else:
            print("Tipo inválido. Por favor, responda 'sedan', 'suv' ou 'esportivo'.")
            self.pedir_tipo_cidade()
    
    @Rule(Fact(orçamento=W()), Fact(uso='cidade'), Fact(tipo='sedan'))
    def recomendar_sedan(self):
        if self.facts.get('orçamento', 0) >= 30000:
            print("Recomendação: Um sedan novo pode ser uma boa opção.")
        else:
            print("Recomendação: Um sedan usado pode ser mais adequado ao seu orçamento.")

    @Rule(Fact(orçamento=W()), Fact(uso='cidade'), Fact(tipo='suv'))
    def recomendar_suv(self):
        if self.facts.get('orçamento', 0) >= 40000:
            print("Recomendação: Um SUV novo pode ser uma boa opção.")
        else:
            print("Recomendação: Um SUV usado pode ser mais adequado ao seu orçamento.")
    
    @Rule(Fact(orçamento=W()), Fact(uso='cidade'), Fact(tipo='esportivo'))
    def recomendar_esportivo(self):
        if self.facts.get('orçamento', 0) >= 50000:
            print("Recomendação: Um carro esportivo novo pode ser uma boa opção.")
        else:
            print("Recomendação: Um carro esportivo usado pode ser mais adequado ao seu orçamento.")
    
    @Rule(Fact(orçamento=W()), Fact(uso='estrada'), Fact(tipo='suv'))
    def recomendar_suv_estrada(self):
        if self.facts.get('orçamento', 0) >= 50000:
            print("Recomendação: Um SUV novo é ideal para viagens longas.")
        else:
            print("Recomendação: Um SUV usado pode ser mais adequado ao seu orçamento.")
    
    @Rule(Fact(orçamento=W()), Fact(uso='estrada'), Fact(tipo='sedan'))
    def recomendar_sedan_estrada(self):
        if self.facts.get('orçamento', 0) >= 30000:
            print("Recomendação: Um sedan novo pode ser adequado para viagens na estrada.")
        else:
            print("Recomendação: Um sedan usado pode ser mais adequado ao seu orçamento.")

if __name__ == "__main__":
    engine = SistemaRecomendacaoCarro()
    engine.reset()  # Prepare o motor de regras
    engine.run()    # Execute o motor de regras

