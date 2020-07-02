## Extratores de frases

Todos os arquivos dentro deste diretório foram criados para a extração de frases de diversas fontes da língua portuguesa.

Cada fonte gera um arquivo em separado com os dados que vão crescendo conforme novas execuções são realizadas.

Todos os arquivos devem ser unidos em um único nomeado **corpus.txt** usando para isso o algoritmo implementado no arquivo **compress.py**.

Posteriormente este arquivo pode ser utilizado para o treinamento de um modelo Word2Vec ou Doc2Vec conforme implementado dentro do diretório **src/model/embedding.py**.

## Como executar

Adicionar quais fontes, por exemplo:
```bash
$> python -m src.data.scraping.g1_extractor
$> python -m src.data.scraping.r7_extractor
$> python -m src.data.scraping.super_extractor
$> python -m src.data.scraping.uol_extractor
$> python -m src.data.scraping.wiki_extractor
```

Realizar a compressão de todas as fontes no **corpus.txt**:
```bash
$> python -m src.data.scraping.compress
```

Para treinar **Word2Vec**:
```bash
$> python -m src.model.embedding --model 0
```

Para treinar **Doc2Vec**:
```bash
$> python -m src.model.embedding --model 1
```