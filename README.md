> Projeto final para a disciplina **Ciência e Visualização de Dados em Saúde** (IA386X) ministrada pelo **prof. André Santanchè** (IC) e **prof. Paula Dornhofer Paro Costa** (FEEC).


# Análise da Disseminação de COVID-19 a partir de redes sociais

## Analysis of the Dissemination of COVID-19 from social networks

## Descrição

O uso das redes sociais no últimos anos efetivamente se espalhou na sociedade moderna, permitindo que diversas pessoas possam ter voz e expressar seus sentimentos (tanto para o bem quanto para o mal). Tendo em vista a quantidade de informações disponíveis nas redes sociais e o momento atual que a sociedade passa (vive-se uma pandemia causada pelo novo Corona Vírus descoberto na China no começo de 2020), levanta-se a ideia da possibilidade de se vincular um aumento na quantidade de comentários nas redes sociais (em especial no Twitter) com o aumento na quantidade de casos confirmados de COVID-19.

Para realizar tal análise, se fez necessário a coleta dos comentários de usuários da rede social Twitter, bem como o posterior pré-processamento e classificação destes comentários, para só então observar através de validações estatísticas, se existe alguma "causalidade" inerente e / ou relação entre o aumento de usuários comunicando que estão doentes (ou possuem sintomas da doença), com um aumento nos casos reportados oficialmente.

Por fim, os resultados apresentados não permitem uma inferência direta de tal relação entre os comentários e os casos, tendo em vista o período estudado e os dados utilizados.

## Abstract

The use of social networks in recent years has effectively spread in modern society, allowing a diversity of people to have a voice and express their feelings (for both good and bad). Given the amount of information available on social networks and the current moment that society is going through (a pandemic caused by the new Corona Virus discovered in China in early 2020), arises the ideia of the possibility of linking a increase in the amount of comments on social networks (especially on Twitter) with the increase in the number of confirmed cases of COVID-19.

In order to carry out such an analysis, it was necessary to collect the comments of users of the social network Twitter, as well as the subsequent pre-processing and classification of those comments, and then to observe through statistical validations, if there is any inherent "causality" and / or relationship between the increase in users reporting that they are sick (or have symptoms of the disease), with an increase in officially reported cases.

Finally, the results presented do not allow a direct inference of such a relationship between the comments and the cases, given the period studied and the data used.

## Equipe

 - [Iliana Burguán Valverde](https://github.com/imburguan) - 163677
 - [Rodolfo de Nadai](https://github.com/rdenadai) - 208911
 - [Victor Leal de Almeida](https://github.com/victorleal) - 104283
 - [Sabrina Beck Angelini](https://github.com/sabrina-beck)


## Vídeo

 - [Link do video]()


## Introdução e Motivação

As redes sociais exercem um papel fundamental na sociedade hoje, e principalmente através delas que as pessoas se informam e discutem sobre notícias. Estudo conduzido com alunos de graduação Social Media as Information Source: Undergraduates Use and Evaluation Behavior[1] mostrou que 97% dos entrevistados usa as redes sociais como fonte de informação.

É também nas redes sociais que as pessoas compartilham informações sobre seu cotidiano. É fácil encontrar comentários sobre o trânsito, problemas no trabalho, dificuldades em alguma tarefa, sintomas de alguma doença. E é especialmente neste último item que está o objeto deste trabalho.

Com o avanço da COVID-19 no mundo (e consequentemente com sua rápida proliferação), várias análises sobre a doença surgem a cada momento. Estas análises vão desde a simples contagem dos casos e óbitos até previsões do aumento nestes números. Como exposto, as pessoas possuem uma tendência a expor nas redes sociais comentários diversos sobre seu cotidiano e possivelmente sobre seu estado de saúde. Dada a atual situação mundial de pandemia de COVID-19, presume-se que comentários relacionados aos principais sintomas de COVID-19 apareçam com maior frequência nas redes sociais.

Tendo em vista essa maior interação das redes sociais e a exposição cada maior de informações dos usuários, questiona-se se existe uma relação entre o número de casos de COVID-19 efetivamente identificado pelas autoridades em saúde do Brasil, com os comentários feitos na rede social Twitter.


### Perguntas de Pesquisa

 - É possível identificar a disseminação da COVID-19 no Brasil, através do conteúdo de redes sociais?
 - Sendo possível, ou existindo alguma relação "causal":
   - Com que grau de certeza a disseminação de COVID-19 é identificada?
   - Com que antecedência podemos identificar a disseminação da doença (em dias/semanas)?
   - Considerando que boa parte do conteúdo extraído não terá informações de geolocalização, é possível verificar essa disseminação por cidades ou estados?


### Objetivo

O projeto tem como principal objetivo avaliar a possibilidade de se identificar, através das redes sociais, a disseminação de doenças, especificamente a COVID-19 no Brasil.

A identificação baseia-se na extração e análise de comentários de usuários das redes sociais (mais especificamente do Twitter), que utilizaram termos relacionados aos sintomas da doenças, tais como “dor de cabeça”, “febre” e entre outros. O conteúdo desta extração, pré processado (usando técnicas de NLP [*Natural Language Processing*]) e classificado como comentário positivo para a doença ou não (usando técnicas convencionais de ML [*Machine Learning*]), será comparado com os dados oficiais de andamento da doença (quantidade de novos casos / mortes). Com isso, procura-se verificar a possibilidade de se melhor prever a disseminação da doença.

A análise, leva em conta a evolução da quantidade de comentários e novos casos da doença ao longo do tempo, e dessa maneira foram inicialmente avaliados como séries temportais. Sendo os resultados sejam concretos, poderia fornecer insumos de possíveis casos ainda não registrados oficialmente nas estatísticas elaboradas pelos órgãos oficiais, melhorando a visão de como a doença está disseminada na sociedade.

## Recursos e Métodos

### Bases de Dados:
 - [Covid-19 : Dados Mundo](https://github.com/CSSEGISandData/COVID-19)
 - [Covid-19 : Ministério da Saúde](https://covid.saude.gov.br/)
 - [Covid-19 : Dados Brasil](https://github.com/wcota/covid19br)
 - [Covid-19 : Dados Brasil : prof. Paula](https://github.com/pdpcosta/COVID-19_Brazil)
 - [IBGE : Dados populacionais](https://www.ibge.gov.br/estatisticas/sociais/populacao.html)
 - [Coronavirus (covid19) Tweets](https://www.kaggle.com/smid80/coronavirus-covid19-tweets#2020-03-00%20Coronavirus%20Tweets%20(pre%202020-03-12).CSV)


### Ferramentas


## Metodologia


### Detalhamento do Projeto


### Evolução do Projeto


## Resultados e Discussão


## Conclusões


## Trabalhos Futuros


### Referências:
 - [1] [Social Media as Information Source: Undergraduates Use and Evaluation Behavior](https://asistdl.onlinelibrary.wiley.com/doi/full/10.1002/meet.2011.14504801283)
 - [2] [Prediction of Infectious Disease Spread Using Twitter: A Case of Influenza](https://ieeexplore.ieee.org/document/6424743)
 - [3] [Towards detecting influenza epidemics by analyzing Twitter messages](https://dl.acm.org/doi/pdf/10.1145/1964858.1964874)
 - [4] [Predicting Flu Trends using Twitter data](https://ieeexplore.ieee.org/abstract/document/5928903)
 - [5] [Forecasting Word Model: Twitter-based Influenza Surveillance and Prediction](https://www.aclweb.org/anthology/C16-1008.pdf)
 - [6] [Analysing Twitter and web queries for flu trend prediction](https://link.springer.com/article/10.1186/1742-4682-11-S1-S6)
 - [7] [Twitter Improves Seasonal Influenza Prediction](https://scitepress.org/papers/2012/37806/37806.pdf)
 - [8] [Real-time disease surveillance using Twitter data: demonstration on flu and cancer](https://dl.acm.org/doi/abs/10.1145/2487575.2487709)
 - [9] [Applying GIS and Machine Learning Methods to Twitter Data for Multiscale Surveillance of Influenza](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4959719/)
 - [10] [Mining Twitter data for influenza detection and surveillance](https://dl.acm.org/doi/abs/10.1145/2897683.2897693)
 - [11] [Defining Facets of Social Distancing during the COVID-19 Pandemic: Twitter Analysis](https://www.medrxiv.org/content/10.1101/2020.04.26.20080937v1)
 - [12] [Predicting crime using Twitter and kernel density estimation](https://www.sciencedirect.com/science/article/pii/S0167923614000268)
 - [13] [Opinion Mining on Twitter Data using Unsupervised Learning Technique](https://www.ijcaonline.org/archives/volume148/number12/unnisa-2016-ijca-911317.pdf)
 - [14] [On the limited memory BFGS method for large scale optimization](https://link.springer.com/article/10.1007/BF01589116)
