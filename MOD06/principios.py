import datetime
import math
from typing import List

class Pessoa:
    def __init__(self, nome: str, sobrenome: str, data_de_nascimento: datetime.date) -> None:
        self.data_de_nascimento = data_de_nascimento
        self.sobrenome = sobrenome
        self.nome = nome

    @property
    def idade(self) -> int:
        return math.floor((datetime.date.today() - self.data_de_nascimento).days / 365.2425)
    
    def __str__(self) -> str:
        return f"{self.nome} {self.sobrenome} tem {self.idade} anos"

class Curriculo:
    def __init__(self, pessoa: Pessoa, experiencias: List[str]) -> None:
        self.experiencias = experiencias
        self.pessoa = pessoa
    @property
    def quantidade_de_experiencias(self) -> int:
        return len(self.experiencias)

    @property
    def empresa_atual(self) -> str:
        return self.experiencias[-1]

    def adiciona_experiencia(self, experiencia: str) -> None:
        self.experiencias.append(experiencia)
    
    def __str__(self):
        return f"{self.pessoa.nome} {self.pessoa.sobrenome} tem {self.pessoa.idade} anos e já " \
            f"trabalhou em {self.quantidade_de_experiencias} empresas e atualmente trabalha " \
                f"na empresa {self.empresa_atual}"


marcelo = Pessoa(nome='Marcelo', sobrenome='Quaglioz', data_de_nascimento=datetime.date(1978, 3, 25))
print(marcelo)

curriculo_marcelo = Curriculo(pessoa=marcelo, experiencias=['Oi','Serede','Everis','TIM'])
print(curriculo_marcelo.pessoa.idade)

print(curriculo_marcelo)

curriculo_marcelo.adiciona_experiencia("AmbevTech")

print(curriculo_marcelo)


# agora vamos herdar outra classe

class Vivente:
    def __init__(self, nome: str, data_de_nascimento: datetime.date) -> None:
        self.data_de_nascimento = data_de_nascimento
        self.nome = nome

    @property
    def idade(self) -> int:
        return math.floor((datetime.date.today() - self.data_de_nascimento).days / 365.2425)
    
    def emite_ruido(self, ruido: str):
        print(f"{self.nome} fez ruído: {ruido}")


# aqui herda sem inclusão de novos dados
class PessoaHeranca(Vivente):
    def __str__(self) -> str:
        return f"{self.nome} tem {self.idade} anos"

    def fala(self, frase):
        return self.emite_ruido(frase)


# aqui herda com a inclusão de novos dados
class Cachorro(Vivente):
    def __init__(self, nome: str, data_de_nascimento: datetime.date, raca: str) -> None:
        super().__init__(nome, data_de_nascimento)
        self.raca = raca
    
    def __str__(self):
        return f"{self.nome} é da raça {self.raca} e tem {self.idade} anos"
    
    def late(self):
        return self.emite_ruido('Au! Au!')

marcelo2 = PessoaHeranca(nome='Marcelo', data_de_nascimento=datetime.date(1978, 3, 25))
print(marcelo2)

belisco = Cachorro(nome='Belisco', data_de_nascimento=datetime.date(2019, 4, 15), raca='Lhasa Apso')
print(belisco)

belisco.late()
belisco.late()
belisco.late()
marcelo2.fala('Cala a boca Belisco!')
belisco.late()
