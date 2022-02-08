#%%
import requests
# %%
url = 'https://portalcafebrasil.com.br/todos/podcasts/'
# %%
ret = requests.get(url)
# %%
ret.text
# %%
# podemos usar o BeautifulSoup para ajudar
from bs4 import BeautifulSoup as bs
# %%
soup = bs(ret.text)
# no terminal ele retorno qual o melhor parser 
# a se usado, que será o html
# %%
soup
# o texto ainda esta ruim, mas já esta visualmente 
# melhor que os dados brutos
# %%
# usando o inspector (F12) do navegador, podemos
# identificar as tags html que nos interessam
# nesse exemplo, a tag "h5" é o que queremos
soup.find("h5")
# retorna a primeira ocorrência. (tem como trazer todos)
# %%
# mas podemos ser mais objetivos na obtenção
soup.find("h5").text
# somente o texto
# %%
soup.find("h5").a['href']
# somente o link
# %%
# podemos agora obter vários epsódios
lst_podcast = soup.find_all("h5")
# %%
for item in lst_podcast:
    print(f"EP: {item.text} - Link: {item.a['href']}")
# mas não vieram todos...
# %%
# quando a pagina carrega o restante do conteúdo,
# ela faz uma chamada em outra url
url = 'https://portalcafebrasil.com.br/todos/podcasts/page/{}/?ajax=true'
# podemos incluir os valores das paginas dinamicamente
url.format(5)
# %%
def get_podcast(url):
    ret = requests.get(url)
    soup = bs(ret.text)
    return soup.find_all("h5")
# %%
get_podcast(url.format(4))
#%%
# criar log para a função
import logging
#%%
log = logging.getLogger()
log.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)
# %%
# com a função dinâmica, vamos para a paginação
i = 1
lst_podcast = []
lst_get = get_podcast(url.format(i))
log.debug(f"Coletado {len(lst_get)} espisódios do link: {url.format(i)}")

while len(lst_get) > 0:
    lst_podcast = lst_podcast + lst_get
    i += 1
    lst_get = get_podcast(url.format(i))
    log.debug(f"Coletado {len(lst_get)} espisódios do link: {url.format(i)}")
# %%
len(lst_podcast)
# %%
# criar um dataframe a partir da lista coletada
import pandas as pd
# %%
# cria um dataframe vazio com as colunas
df = pd.DataFrame(columns=['nome','link'])
# %%
# percorre a lista e grava na ultima posição do df
for item in lst_podcast:
    df.loc[df.shape[0]] = [item.text, item.a['href']]
# %%
df.shape
# %%
df
# %%
df.to_csv('banco_de_podcast.csv', sep=';', index=False)
# %%
