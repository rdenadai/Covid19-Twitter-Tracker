# Covid19 Twitter Tracker
---

Projeto final para a disciplina de mestrado ia386x ministrada pelo prof. André Santanchè (IC) e prof. Paula Dornhofer Paro Costa (FEEC).


### Instalação
---

#### Requisitos

 - python 3.7+
 
> Caso não possua o python 3.7+ (sugiro o 3.8), veja como instalar.
Você pode usar o [pyenv](https://github.com/pyenv/pyenv) para instalar várias versões paralelamente.

## Executar

 1. Faça o git clone deste repositório;
 2. Execute os seguintes comandos (depois de ter instalado o python 3.6+)
    ```bash
    $> virtualenv venv
    $> pip install -r requirements.txt
    $> source venv/bin/activate
    $> python -m nltk.downloader stopwords
    $> python -m nltk.downloader punkt
    $> python -m nltk.downloader rslp
    $> python -m nltk.downloader perluniprops
    $> python -m spacy download en
    $> python -m spacy download pt
    ```
 3. Altere as configurações no arquivo settings.ini (não é necessário)
 4. Iniciar o banco de dados:
    ```bash
    $> cd code
    $> python -m src.database.start_db
    ```
 5. Extração de dados:
    ```bash
    $> cd code
    $> python -m src.scraping.extractor
    $> python -m src.scraping.geo_extractor
    ```
 5. Limpeza dos dados extraídos do Twitter:
    ```bash
    $> cd code
    $> python -m src.processing.sanitization
    ```


### Datasets:
---

 - [Covid-19 : Dados Mundo](https://github.com/CSSEGISandData/COVID-19)
 - [Covid-19 : Ministério da Saúde](https://covid.saude.gov.br/)
 - [Covid-19 : Dados Brasil](https://github.com/wcota/covid19br)
 - [Covid-19 : Dados Brasil : prof. Paula](https://github.com/pdpcosta/COVID-19_Brazil)
 - [IBGE : Dados populacionais](https://www.ibge.gov.br/estatisticas/sociais/populacao.html)
 - [Coronavirus (covid19) Tweets](https://www.kaggle.com/smid80/coronavirus-covid19-tweets#2020-03-00%20Coronavirus%20Tweets%20(pre%202020-03-12).CSV)


### Referências:
 - [1] [Prediction of Infectious Disease Spread Using Twitter: A Case of Influenza](https://ieeexplore.ieee.org/document/6424743)
 - [2] [Towards detecting influenza epidemics by analyzing Twitter messages](https://dl.acm.org/doi/pdf/10.1145/1964858.1964874)
 - [3] [Predicting Flu Trends using Twitter data](https://ieeexplore.ieee.org/abstract/document/5928903)
 - [4] [Forecasting Word Model: Twitter-based Influenza Surveillance and Prediction](https://www.aclweb.org/anthology/C16-1008.pdf)
 - [5] [Analysing Twitter and web queries for flu trend prediction](https://link.springer.com/article/10.1186/1742-4682-11-S1-S6)
 - [6] [Twitter Improves Seasonal Influenza Prediction](https://scitepress.org/papers/2012/37806/37806.pdf)
 - [7] [Real-time disease surveillance using Twitter data: demonstration on flu and cancer](https://dl.acm.org/doi/abs/10.1145/2487575.2487709)
 - [8] [Applying GIS and Machine Learning Methods to Twitter Data for Multiscale Surveillance of Influenza](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4959719/)
 - [9] [Mining Twitter data for influenza detection and surveillance](https://dl.acm.org/doi/abs/10.1145/2897683.2897693)
 - [10] [Defining Facets of Social Distancing during the COVID-19 Pandemic: Twitter Analysis](https://www.medrxiv.org/content/10.1101/2020.04.26.20080937v1)
 - [11] [Predicting crime using Twitter and kernel density estimation](https://www.sciencedirect.com/science/article/pii/S0167923614000268)
 - [12] [Opinion Mining on Twitter Data using Unsupervised Learning Technique](https://www.ijcaonline.org/archives/volume148/number12/unnisa-2016-ijca-911317.pdf)
 - [13] [On the limited memory BFGS method for large scale optimization](https://link.springer.com/article/10.1007/BF01589116)
