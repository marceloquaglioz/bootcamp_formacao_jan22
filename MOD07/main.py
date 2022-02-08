#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import sys
import time
#%%
cep = sys.argv[1]

#%%
if cep:
    # %%
    s = Service('./src/chromedriver')
    driver = webdriver.Chrome(service=s)
    # %%
    # driver.get('https://howedu.com.br')
    # driver.find_element_by_xpath('//*[@id="post-37"]/div/div/div/section[9]/div/div/div/div[3]/div/div/a').click()
    # %%
    driver.get('https://buscacepinter.correios.com.br/app/endereco/index.php?t')
    elem_cep = driver.find_element(By.NAME, "endereco")
    # %%
    elem_cep.clear()
    # %%
    elem_cep.send_keys(cep)
    # %%
    elem_cmb = driver.find_element(By.NAME, "tipoCEP")
    # %%
    # elem_cmb.click()
    # %%
    elem_cmb = driver.find_element(By.XPATH, '//*[@id=\"formulario\"]/div[2]/div/div[2]/select/option[6]').click()
    # %%
    driver.find_element(By.ID, "btn_pesquisar").click()

    # %%
    time.sleep(3)
    # %%
    logradouro = driver.find_element(By.XPATH, '//*[@id="resultado-DNEC"]/tbody/tr/td[1]').text
    bairro = driver.find_element(By.XPATH, '//*[@id="resultado-DNEC"]/tbody/tr/td[2]').text
    localidade = driver.find_element(By.XPATH, '//*[@id="resultado-DNEC"]/tbody/tr/td[3]').text
    # %%
    driver.close()

    # %%
    print("""
    Para o CEP {} temos:
    Endereço: {}
    Bairro: {}
    Localidade: {}
    """.format(
        cep,
        logradouro.split(' - ')[0],
        bairro,
        localidade
    ))

# %%
