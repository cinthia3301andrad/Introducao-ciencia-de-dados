


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth

from bs4 import BeautifulSoup
import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

s = Service('/home/sindyme/Downloads/chromedriver')
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")

# options.add_argument("--headless")

options.add_argument("--headless")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
""" options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
options.add_argument("Accept: application/json, text/plain, */*")
options.add_argument("Accept-Language: pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3")
options.add_argument("Accept-Encoding: gzip, deflate, br")
options.add_argument("X-Channel-Id: webmotors.buyer.desktop.ui")
options.add_argument("Connection: keep-alive")
options.add_argument("Upgrade-Insecure-Requests: 1") """
options.add_argument("--enable-javascript") # habilita o javascript


driver = webdriver.Chrome(service=s, options=options)

stealth(driver,
       user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.105 Safari/537.36',
       languages=["en-US", "en"],
       vendor="Google Inc.",
       platform="Win32",
       webgl_vendor="Intel Inc.",
       renderer="Intel Iris OpenGL Engine",
       fix_hairline=True,
       )

        
# Lista de carros que serão pesquisados
carros = [
    {'marca': 'chevrolet', 'modelo': 'corsa'},
    {'marca': 'volkswagen', 'modelo': 'gol'},
    {'marca': 'ford', 'modelo': 'fiesta'},
]

# Lista para armazenar os resultados
dataset_car = [] 

for carro in carros:
    # Montando a URL de pesquisa
    marca = carro['marca']
    modelo = carro['modelo']
    url = f'https://www.webmotors.com.br/carros/estoque/{marca}?tipoveiculo=carros&marca1={marca.upper()}'

    # Acessando a página
    driver.get(url)
    print("Aguardando o carregamento da página...")
    # Aguardando o carregamento da página
    time.sleep(10)
    print("Carregou!")

    html = driver.page_source
    # Analisando o HTML com BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Localizando o elemento que contem os dados dos carros
    container = soup.find_all('div', {'class': 'ContainerCardVehicle'})
    if(len(container) == 0):
        print("Não achamos o conteúdo")
    else:
        print("Achamos o conteúdo! Aguarde o dataset ser montado!")
        
    cards = soup.find_all('div', {'data-qa': lambda x: x and x.startswith('vehicle_card_')})

    for card in cards:
        # Extrair informações do card
        name_car = card.select_one('div div:nth-of-type(2) a h2').text
        preco_div = card.find("div", {"id": "valorVerParcelas"})
        preco = preco_div.select_one("strong").text
        preco_value = preco.split(" ")[0].replace("R$", "").replace("\xa0", "").replace(".", "")
        ano = card.select_one('div div:nth-of-type(2) a:nth-of-type(2) div:nth-of-type(2) div span').text

        info_carro = {
            "name": name_car,
            "preco": preco_value,
            "ano": ano,
            "marca": marca
        }
        dataset_car.append(info_carro)
    time.sleep(10)
    print("ESPERANDO")
print('dataset de carros', dataset_car)
# Fechando o navegador
driver.quit()

# Cria o DataFrame com o dataset_car
df = pd.DataFrame(dataset_car)

# Salva o DataFrame em um arquivo CSV
df.to_csv('dataset_car_tentativa1.csv', index=False)
print("Dataset salvo com sucesso!")