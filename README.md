# Covid19-Twitter-Tracker

Projeto final para a disciplina de mestrado ia386x.


### Instalação

#### Requisitos

 - python 3.7+
 
> Caso não possua o python 3.7+ (sugiro o 3.8), veja como instalar.
Você pode usar o [pyenv](https://github.com/pyenv/pyenv) para instalar várias versões paralelamente.

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
## Executar

