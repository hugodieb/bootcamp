#Importar as libs

from selenium import webdriver #pacote permite abrir o navegador no caso chrome que escolhi
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager #pacote ligação python com navegador
import time
import pandas as pd

from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.headless = False  # Garante que não está em modo headless

#cria um robo que abre o chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options) 


try:
  driver.get('https://www.etfsbrasil.com.br/rankings')
  time.sleep(5)  # Tempo para carregar o javascript da pagina e poder encontrar os elementos do html
  
  path_btn_mostrar = "/html/body/div/main/div[2]/div/div[1]/div[2]/div[2]/div[3]/div/div[2]/button"
  btn_mostrar = driver.find_element("xpath",
                                  path_btn_mostrar)
  btn_mostrar.click()

  #driver.execute_script("arguments[0].click();", btn_mostrar) #**usar esse metodo quando não funcionar o .click()

  input("Pressione Enter para fechar o navegador...") # fiz isso p manter o navegador aberto 

except Exception as e:
  print(f"Ocorreu um erro: {e}")
finally:
  driver.quit()



# **exemplo se tivesse que clicar no maximo de paginas

# numero_paginas = driver.find_element("xpath", "//*[@id='totalPages']")
# numero_paginas = numero_paginas.text.replace("of de", "")
# numero_paginas = int(numero_paginas)===>um total de 32 paginas por exemplo

# **agora vamos ler a tabela com os dados

# lista_tabela_por_pagina = []
# elemento = driver.find_elements("xpath", '//*[@id="finderTable"]')
# 
# for pagina in range(1, numero_paginas + 1)
#  html_tabela = elemento.get_atribute('outerHTML')
#  tabela = pd.read_html(str(html_tabela))[0]
#  lista_tabela_por_pagina.append(tabela)
#  btn_avancar_pagina = driver.find_element("xpath", '//*[@id="nextPage"]')
#  btn_avancar_pagina.click() ** aqui estou avançando para a próxima página

# tabela_cadastro_etfs = pd.concat(lista_tabela_por_pagina) **aqui junta todas as tabelas

# Agora vamos voltar para a pagina 1 buscando pelo elemento dentro do html que é digitavel

# formulario_voltar_pagina = driver.find_element("xpath", '//*[@id="goToPage"]') 
# formulario_voltar_pagina.clear() limpar o campo
# formulario_voltar_pagina.send_keys("1") digitar 1 que seria a pagina 1
# formulario_voltar_pagina.send_keys(u'\ue007') tecla enter

# ** Pegar os dados da tabela rentabilidade que seria a mesma tabela mas em outra aba

# btn_renatabilidade = driver.find_element("xpath", '//*[@id="rentabilidade"]')

# Repete a mesma coisa porem só muda o nome lista p rentabilidade

# lista_tabela_por_pagina = []
# elemento = driver.find_elements("xpath", '//*[@id="finderTable"]')
# 
# for pagina in range(1, numero_paginas + 1)
#  html_tabela = elemento.get_atribute('outerHTML')
#  tabela = pd.read_html(str(html_tabela))[0]
#  lista_tabela_por_pagina.append(tabela)
#  btn_avancar_pagina = driver.find_element("xpath", '//*[@id="nextPage"]')
#  btn_avancar_pagina.click() ** aqui estou avançando para a próxima página

# tabela_rentabilidade_etfs = pd.concat(lista_tabela_por_pagina) **aqui junta todas as tabelas

# Agora vamos voltar para a pagina 1 buscando pelo elemento dentro do html que é digitavel

# formulario_voltar_pagina = driver.find_element("xpath", '//*[@id="goToPage"]') 
# formulario_voltar_pagina.clear() limpar o campo
# formulario_voltar_pagina.send_keys("1") digitar 1 que seria a pagina 1
# formulario_voltar_pagina.send_keys(u'\ue007') tecla enter

# ** Vamos juntar as tabelas cada cadastro etfs com a tabela rentabilidade das etfs numa só

# tabela_cadastro_etfs = tabela_cadastro_etfs.set_index("Ticker") estou definindo a chave primaria sql 
# tabela_rentabilidade_etfs = tabela_rentabilidade_etfs.set_index("Ticker") aqui tbm

# **aqui estou pegando os dados da colunas da tabela que me interessam
# tabela_rentabilidade_etfs = tabela_rentabilidade_etfs[[' Year', '3 years', '5 Years']] 

# Juntar a 2 tabelas com as colunas tendo o Ticker como chave primaria
# O inner vai juntar somente as linhas que tiverem a mesma chave primaria iguais

# tabela_dados_final = tabela_cadastro_etfs.join(tabela_rentabilidade_etfs, how='inner')

