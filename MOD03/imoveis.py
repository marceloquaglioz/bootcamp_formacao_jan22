#%%
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
# %%
url = 'https://www.vivareal.com.br/venda/parana/curitiba/apartamento_residencial/?pagina={}'
# %%
i = 1
ret = requests.get(url.format(i))
soup = bs(ret.text)
# %%
# vamos obter 2 informações: os dados do card e a quantidade de imóveis
# filtramos os elementos html que queremos pelo nomes das classes
houses = soup.find_all('a', {'class': 'property-card__content-link js-card-title'})
qtd_imoveis = float(soup.find('strong', {'class': 'results-summary__count js-total-records'}).text.replace('.',''))
# %%
len(houses)
# %%
qtd_imoveis
# %%
# quantidade de paginas para pesquisar
qtd_imoveis / len(houses)
# %%
# obtem o primeiro item
house = houses[0]
# %%
# obtem os dados do card
df = pd.DataFrame(
    columns=[
        'descricao',
        'endereco',
        'area',
        'quartos',
        'wc',
        'vagas',
        'valor',
        'condominio',
        'wlink'
    ]
)
#%%
i = 0
while qtd_imoveis > df.shape[0]:
    i += 1
    print(f"Valor i: {i}\t\t qtd_imoveis: {df.shape[0]}")
    ret = requests.get(url.format(i))
    soup = bs(ret.text)
    houses = soup.find_all('a', {'class': 'property-card__content-link js-card-title'})

    for house in houses:
        try:
            descricao = house.find('span', {'class': 'property-card__title js-cardLink js-card-title'}).text.strip() # strip remove espaços
        except:
            descricao = None
        try:
            endereco = house.find('span', {'class': 'property-card__address'}).text.strip() # strip remove espaços
        except:
            endereco = None
        try:
            area = house.find('span', {'class': 'property-card__detail-value js-property-card-value property-card__detail-area js-property-card-detail-area'}).text.strip() # strip remove espaços
        except:
            area = None
        try:
            quartos = house.find('li', {'class': 'property-card__detail-item property-card__detail-room js-property-detail-rooms'}).span.text.strip() # strip remove espaços
        except:
            quartos = None
        try:
            wc = house.find('li', {'class': 'property-card__detail-item property-card__detail-bathroom js-property-detail-bathroom'}).span.text.strip() # strip remove espaços
        except:
            wc = None
        try:
            vagas = house.find('li', {'class': 'property-card__detail-item property-card__detail-garage js-property-detail-garages'}).span.text.strip() # strip remove espaços
        except:
            vagas = None
        try:
            valor = house.find('div', {'class': 'property-card__price js-property-card-prices js-property-card__price-small'}).p.text.strip() # strip remove espaços
        except:
            valor = None
        try:
            condominio = house.find('strong', {'class': 'js-condo-price'}).text.strip() # strip remove espaços
        except:
            condominio = None
        try:
            wlink = 'https://www.vivareal.com.br' + house['href']
        except:
            wlink = None

        df.loc[df.shape[0]] = [
            descricao,
            endereco,
            area,
            quartos,
            wc,
            vagas,
            valor,
            condominio,
            wlink
        ]


# %%
df.to_csv('banco_imoveis.csv', sep=';', index=False)
# %%
