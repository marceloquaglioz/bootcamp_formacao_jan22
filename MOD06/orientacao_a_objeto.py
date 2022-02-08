import datetime
import math

class Pessoa:
    def __init__(self, nome: str, sobrenome: str, data_de_nascimento: datetime.date):
        self.data_de_nascimento = data_de_nascimento
        self.sobrenome = sobrenome
        self.nome = nome

    @property
    def idade(self) -> int:
        return math.floor((datetime.date.today() - self.data_de_nascimento).days / 365.2425)
    
    def __str__(self) -> str:
        return f"{self.nome} {self.sobrenome} tem {self.idade} anos"

# idade é derivado da data de nascimento e é uma propriedade da pessoa.
# se colocamos o @property antes da função, podemos chama-la como um atributo de pessoa
# e não mais como uma função.
# a função __str__ sobrescreve a saida quando damos o print no nome da classe.

marcelo = Pessoa(nome='Marcelo', sobrenome='Quaglioz', data_de_nascimento=datetime.date(1978, 3, 25))

print(marcelo)
print(marcelo.nome)
print(marcelo.sobrenome)
print(marcelo.idade)
