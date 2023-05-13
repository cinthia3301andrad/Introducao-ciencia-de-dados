import requests
import json
import time
import pandas as pd
import re
# Define a URL base para a requisição GET
base_url = "https://www.webmotors.com.br/api/search/car?url=https://www.webmotors.com.br/carros/estoque/{}"

# Define a lista de marcas desejadas
marcas = ["chevrolet", "fiat", "volkswagen", "ford", "hyundai", "toyota", 
    "mitsubishi", "nissan", "renault", "honda", "kia", "peugeot"]

# Define os parâmetros que serão usados na requisição GET
params = {
    "tipoveiculo": "carros",
    "anunciante": "Pessoa Física",
    "actualPage": 1,
    "displayPerPage": 24,
    "order": 1,
    "showMenu": "true",
    "showCount": "true",
    "showBreadCrumb": "true",
    "testAB": "false",
    "returnUrl": "false",
}

# Define uma lista para armazenar os resultados
resultados = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299',
    'Accept-Language': 'pt-BR',
    'Referer': 'https://www.google.com'
}

# Extrair informações do tipo de combustível usando expressões regulares
padroes_combustivel = r"\b(gasolina|diesel|etanol|elétrico|híbrido|flex|flexflue)\b"

# Executa um loop para cada marca desejada
for marca in marcas:
    # Atualiza a URL base com a marca desejada
    url = base_url.format(marca)
    
    # Executa um loop de 1 a x para realizar as requisições GET
    print("Fazendo a requisição...")
    for page in range(1, 15):
        # Atualiza o valor do parâmetro "actualPage"
        params["actualPage"] = page
        
        # Realiza a requisição GET
        response = requests.get(url, params=params, headers=headers)
    
        # Verifica se a resposta da requisição foi bem sucedida
        if response.status_code == 200:
            # Decodifica o conteúdo da resposta em JSON
            conteudo = json.loads(response.content)
            cars = conteudo["SearchResults"]
            print("Adicionando carros ao dataset...")
            for car in cars:
                # Extrair informações do card
            
                marca = car["Specification"]["Make"]["Value"]
                modelo = car["Specification"]["Model"]["Value"] 
                ano_modelo = car["Specification"]["YearModel"]
                ano_fabr = car["Specification"]["YearFabrication"]
                quilometragem = car["Specification"]["Odometer"] 
                cor =  car["Specification"]["Color"]["Primary"]
                estado =  car["Seller"]["State"].split(" ")[-1].replace("(", "").replace(")", "")
                cambio = car["Specification"]["Version"]["Value"].split()[-1]
                motor = car["Specification"]["Version"]["Value"].split()[0]
                tipo_combustivel_match = re.search(padroes_combustivel, car["Specification"]["Title"], re.IGNORECASE)
                if tipo_combustivel_match:
                    tipo_combustivel = tipo_combustivel_match.group()
                else:
                    tipo_combustivel = "nan"
                preco = car["Prices"]["Price"]
                info_carro = {
                    "marca": marca,
                    "modelo": modelo, 
                    "ano_modelo": ano_modelo,
                    "ano_fabr": ano_fabr,
                    "quilometragem": quilometragem,
                    "cor": cor,
                    "estado": estado,
                    "cambio": cambio,
                    "motor": motor,
                    "preco": preco,
                }
            
                # Adiciona os resultados na lista de resultados
                resultados.append(info_carro)
            print("Carros adicionados!")
            # Aguarda alguns segundos para evitar sobrecarga do servidor
            time.sleep(5)
            
        else:
            # Exibe uma mensagem de erro
            print("Erro ao realizar a requisição GET")
            break
            
# Cria o DataFrame com o dataset_car
df = pd.DataFrame(resultados)

# Salva o DataFrame em um arquivo CSV
df.to_csv('dataset_completo_entrega_final.csv', index=False)
print("Dataset salvo com sucesso!")