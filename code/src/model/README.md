## Modelos de Machine Learning

Os arquivos dentro deste diretório tem por objetivo geral modelos de machine learning para uso na identificação e categorização de textos no idioma português.

O arquivo nomeado **classifier.py** foi utilizado diretamente neste projeto para criar um classificar SVM usando TF-IDF para gerar as variáveis latentes. Para a geração deste classificador é realizada uma busca exaustiva passando alguns parâmetros básicos e o dataset cujo conteúdo é normalizado, removendo acentuação, realizando stemização das palavras dentre outras necessidades do projeto.

Já o seguindo arquivo, nomeado **embedding.py**, permite a geração de modelos de deep learning conhecidos como Word2Vec e Doc2Vec. O uso destes arquivos no projeto é totalmente opcional, e serviram para validação de uma possível melhor classificação dos comentários. Os resultados desse modelo treinado com uma centena de milhares de frases coletadas de diversas fontes (ver todos os extratores dentro do diretório src/data/scraping/embedding) esta apresentado nos notebooks nomeados **alpha_avaliacao_algoritmos_nao_supervisionados_word2vec.ipynb** e **alpha_avaliacao_deep_learning_classificacao_comentarios.ipynb**.

Em termos práticos (e sem excesso de tunning de parâmetros) os resultados de ambas as abordagens foram muito próximos, e em consequencia, a primeira, mais simples de usar fora a escolhida.

Entretanto, os resultados da segunda abordagem usando Deep Learning, pode vir a ser útil em outros projetos futuros, por isso disponibilizado aqui.