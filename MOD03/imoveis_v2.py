#%%
from os import WCONTINUED, link, sep
from typing import AsyncIterator
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
import time
# %%
url = 'https://glue-api.vivareal.com/v2/listings?addressCity=Curitiba&addressLocationId=BR>Parana>NULL>Curitiba&addressNeighborhood&addressState=Paraná&addressCountry=Brasil&addressStreet&addressZone&addressPointLat=-25.437238&addressPointLon=-49.269973&business=SALE&facets=amenities&unitTypes=APARTMENT&unitSubTypes=UnitSubType_NONE,DUPLEX,LOFT,STUDIO,TRIPLEX&unitTypesV3=APARTMENT&usageTypes=RESIDENTIAL&listingType=USED&parentId=null&categoryPage=RESULT&includeFields=search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones),medias,accountLink,link)),totalCount),page,seasonalCampaigns,fullUriFragments,nearby(search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones),medias,accountLink,link)),totalCount)),expansion(search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones),medias,accountLink,link)),totalCount)),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones,phones),developments(search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones),medias,accountLink,link)),totalCount)),owners(search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones),medias,accountLink,link)),totalCount))&size=300&from={}&q&developmentsSize=5&levels=CITY,UNIT_TYPE&ref=/venda/parana/curitiba/apartamento_residencial/&pointRadius&isPOIQuery'

headersList = {
 "Accept": "*/*",
 "User-Agent": "Thunder Client (https://www.thunderclient.io)",
 "x-domain": "www.vivareal.com.br" 
}

payload = ''
#%%
def get_json(url, i, headersList, payload):
    ret = requests.request("GET", url.format(i), data=payload, headers=headersList)
    soup = bs(ret.text, 'html.parser')
    return json.loads(soup.text)
# %%
# obtem os dados do card
df = pd.DataFrame(
    columns=[
        'descricao',
        'endereco',
        'area',
        'quartos',
        'suites',
        'wc',
        'vagas',
        'valor',
        'condominio',
        'wlink'
    ]
)
#%%
imovel_id = 0
json_data = get_json(url, imovel_id, headersList, payload)
while len(json_data['search']['result']['listings']) > 0:
    qtd = len(json_data['search']['result']['listings'])
    print(f"Qtd imóveis: {qtd} | Total: {imovel_id}")

    for i in range(0, qtd):
        try:
            descricao = json_data['search']['result']['listings'][i]['listing']['title']
        except:
            descricao = "-"
        try:
            try:
                endereco = json_data['search']['result']['listings'][i]['listing']['address']['street'] + ", " + json_data['search']['result']['listings'][i]['listing']['address']['streetNumber']
            except:
                endereco = json_data['search']['result']['listings'][i]['listing']['address']['street']
        except:
            endereco = "-"
        try:
            area = json_data['search']['result']['listings'][i]['listing']['totalAreas']
        except:
            area = "-"
        try:
            quartos = json_data['search']['result']['listings'][i]['listing']['bedrooms']
        except:
            quartos = "-"
        try:
            suites = json_data['search']['result']['listings'][i]['listing']['suites']
        except:
            suites = "-"
        try:
            wc = json_data['search']['result']['listings'][i]['listing']['bathrooms']
        except:
            wc = "-"
        try:
            vagas = json_data['search']['result']['listings'][i]['listing']['parkingSpaces']
        except:
            vagas = "-"
        try:
            valor = json_data['search']['result']['listings'][i]['listing']['princingInfos'][0]['price']
        except:
            valor = "-"
        try:
            condominio = json_data['search']['result']['listings'][i]['listing']['princingInfos'][0]['monthlyCondoFee']
        except:
            condominio = "-"
        try:
            wlink = 'https://www.vivareal.com.br/' + json_data['search']['result']['listings'][i]['link']['href']
        except:
            wlink = "-"

        df.loc[df.shape[0]] = [
            descricao,
            endereco,
            area,
            quartos,
            suites,
            wc,
            vagas,
            valor,
            condominio,
            wlink
        ]
        
    imovel_id = imovel_id + qtd
    if imovel_id > 9500:
        break
    time.sleep(1) # evitar erro 429 - muitas requisições...
    json_data = get_json(url, imovel_id, headersList, payload)

# %%
df.to_csv('banco_imoveis.csv', sep=';', index=False)
# %%
