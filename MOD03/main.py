#%%
# imports
import requests
import json

#%%
url = 'https://economia.awesomeapi.com.br/json/last/USD-BRL'

ret = requests.get(url)

# %%
if ret:
    print(ret)
else:
    print('Falhou')

# %%
dolar = json.loads(ret.text)['USDBRL']

# %%
print(f"20 dolares hoje custam {float(dolar['bid']) * 20} reais")

# %%
# criando uma função para obter a cotação
def cotacao(valor, moeda):
    url = f'https://economia.awesomeapi.com.br/json/last/{moeda}'
    ret = requests.get(url)
    dolar = json.loads(ret.text)[moeda.replace('-','')]
    print(f"{valor} {moeda[:3]} hoje custam {float(dolar['bid']) * valor} {moeda[-3:]}")

# %%
cotacao(20, 'USD-BRL')
# %%
cotacao(20, 'JPY-BRL')
# %%
# mas se ocorrer um erro, podemos usar o try except 
try:
    cotacao(20, 'marcelo')
except:
    pass # passa e não retorna nada

# %%
try:
    cotacao(20, 'marcelo')
except Exception as e:
    print(e) # retorna apena o que deu erro, que foi a chave inválida
else:
    print('Ok') # esse aqui retorna se não der erro

# %%
try:
    10/0 # divisão por zero
except Exception as e:
    print(e) # retorna apena o que deu erro, que foi a chave inválida
else:
    print('Ok') # esse aqui retorna se não der erro

    
# %%
# uma função pode gerar error em vários momentos diferentes

def multi_moeda(valor):
    lst_money = [
        "USD-BRL",
        "EUR-BRL",
        "BTC-BRL",
        "RPL-BRL",
        "JPY-BRL",
    ]

    valor = 20

    for moeda in lst_money:
        url = f'https://economia.awesomeapi.com.br/json/last/{moeda}'
        ret = requests.get(url)
        dolar = json.loads(ret.text)[moeda.replace('-','')]
        print(f"{valor} {moeda[:3]} hoje custam {float(dolar['bid']) * valor} {moeda[-3:]}")


# %%
multi_moeda(20)
# %%
# para isso podemos usar um "decorador"
def error_check(func):
    def inner_func(*args, **kargs):
        try:
            func(*args, **kargs)
        except:
            print(f"{func.__name__} falhou")
    return inner_func

@error_check # inicia o decorador
def multi_moeda(valor, moeda):
    url = f'https://economia.awesomeapi.com.br/json/last/{moeda}'
    ret = requests.get(url)
    dolar = json.loads(ret.text)[moeda.replace('-','')]
    print(f"{valor} {moeda[:3]} hoje custam {float(dolar['bid']) * valor} {moeda[-3:]}")
# %%
multi_moeda(20, "USD-BRL")
multi_moeda(20, "EUR-BRL")
multi_moeda(20, "BTC-BRL")
multi_moeda(20, "RPL-BRL")
multi_moeda(20, "JPY-BRL")
# %%
# A solução acima pode ficar um pouco pesada, 
# para isso existe um pacote para essas tratativas
import backoff
import random

# uma função para simular as falhas
# inicia o decorador do pacote, e se falhar ele pode tentar novamente ou por um certo tempo
@backoff.on_exception(backoff.expo, (ConnectionAbortedError, ConnectionRefusedError, TimeoutError), max_tries=2)
def test_func(*args, **kargs):
    rnd = random.random()
    print(f"""
        RND: {rnd}
        args: {args if args else 'sem args'}
        kargs: {kargs if kargs else 'sem kargs'}
    """)
    if rnd < .2:
        raise ConnectionAbortedError('Conexão foi finalizada')
    elif rnd < .4:
        raise ConnectionRefusedError('Conexão foi recusada')
    elif rnd < .6:
        raise TimeoutError('Tempo de espera excedido')
    else:
        return "OK!"

# %%
test_func()
# %%
test_func(42)
# %%
test_func(42, 51, nome='Marcelo')
# %%
# é importante fazer o log das rotinas
# para isso usamos uma biblioteca
import logging
# %%
# Configurando logging para exibir no terminal
log = logging.getLogger()
log.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)

# %%
@backoff.on_exception(backoff.expo, (ConnectionAbortedError, ConnectionRefusedError, TimeoutError), max_tries=2)
def test_func(*args, **kargs):
    rnd = random.random()
    log.debug(f"RND: {rnd}")
    log.info(f"args: {args if args else 'sem args'}")
    log.info(f"kargs: {kargs if kargs else 'sem kargs'}")

    if rnd < .2:
        log.error('Conexão foi finalizada')
        raise ConnectionAbortedError('Conexão foi finalizada')
    elif rnd < .4:
        log.error('Conexão foi recusada')
        raise ConnectionRefusedError('Conexão foi recusada')
    elif rnd < .6:
        log.error('Tempo de espera excedido')
        raise TimeoutError('Tempo de espera excedido')
    else:
        return "OK!"

# %%
test_func()
# %%

# %%
