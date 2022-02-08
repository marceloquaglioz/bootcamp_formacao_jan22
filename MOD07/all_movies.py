#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd
#%%
s = Service('./src/chromedriver')
driver = webdriver.Chrome(service=s)
driver.implicitly_wait(15) # aguarda 15 segundos se não localizar o item e tenta novamente
#%%
driver.get('https://pt.wikipedia.org/wiki/Nicolas_Cage')
#time.sleep(3)
#%%
tabela = driver.find_element(By.XPATH, '/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/table[2]')
# %%
df = pd.read_html('<table>' + tabela.get_attribute('innerHTML') + '</table>')[0]
# %%
with open('print.png', 'wb') as f:
    f.write(driver.find_element(By.XPATH, '/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/table[2]').screenshot_as_png)
# %%
driver.close()
# %%
df[df['Ano']==1984]
# %%
df.to_csv('filmes_Nicolas_Cage.csv', sep=';', index=False)

# %%
