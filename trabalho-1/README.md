# Trabalho 1 de Introdução à Ciência de Dados

Este repositório contém os arquivos relacionados ao Trabalho 1 da disciplina de Introdução à Ciência de Dados. O objetivo do trabalho era criar um dataset de carros a partir do site da Web Motors, utilizando técnicas de web scraping.

## Tentativa Inicial - tentativa1-codigo-nao-oficial.py

O arquivo `tentativa1-codigo-nao-oficial.py` foi minha tentativa inicial de realizar o web scraping no site da Web Motors utilizando a biblioteca Selenium. No entanto, durante o processo, percebi que o acesso à página era bloqueado a partir da segunda requisição, impossibilitando a criação do meu dataset.

## Solução Final - web_dataset_carros-codigo-oficial.py

No arquivo `web_dataset_carros-codigo-oficial.py`, você encontrará a solução final para a criação do dataset de carros. Nesse código, utilizo a biblioteca `requests` para fazer várias requisições à API da Web Motors e manipular o retorno para obter todas as informações necessárias. O resultado é um dataset completo que está disponível no arquivo `dataset_completo_entrega_final.csv`.

## Execução

Para executar o código, certifique-se de ter as seguintes bibliotecas instaladas:

- requests
- json
- time
- pandas
- re

Em seguida, basta rodar o seguinte comando no terminal:
~~~python
python3 web_dataset_carros-codigo-oficial.py
~~~
