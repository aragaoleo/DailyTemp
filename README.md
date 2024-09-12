# Previsão do Tempo por e-mail

Este projeto consiste em dois scripts em Python que obtêm dados meteorológicos da API OpenWeatherMap e os enviam por e-mail. O (`main.py`) busca dados de clima atual e previsão do tempo, processa essas informações e no (`email-sender.py`) envia essas informações por e-mail para algum usuário.

## Ferramentas

- Python
- Bibliotecas principais: `requests`,`pandas`,`email.message`

## Uso

### `main.py`

1. Solicita ao usuário a cidade e o estado.
2. Obtém a latitude e longitude da cidade.
3. Faz uma requisição à API OpenWeatherMap para obter o clima atual e a previsão do tempo.
4. Processa os dados e os armazena em dois DataFrames do Pandas: `dfWeather` e `dfForecast`.

### `email-sender.py`

1. Importa os DataFrames `dfWeather` e `dfForecast` do `main.py`.
2. Converte os DataFrames em HTML.
3. Envia um e-mail com a previsão do tempo atual e a previsão dos próximos dias.

## Observações

O projeto é apenas uma prática para requests de API e a escolhida por mim para esse treino foi a OpenWeatherMap, ele não possui nenhum tipo de estilização ou polimento, foquei apenas nas funções práticas.