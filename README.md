> Projeto final para a disciplina **Ciência e Visualização de Dados em Saúde** (IA386X) ministrada pelo **prof. André Santanchè** (IC) e **prof. Paula Dornhofer Paro Costa** (FEEC).


# Análise da Disseminação de COVID-19 a partir de redes sociais

## Analysis of the Dissemination of COVID-19 from social networks

## Descrição

O uso das redes sociais no últimos anos efetivamente se espalhou na sociedade moderna, permitindo que diversas pessoas possam ter voz e expressar seus sentimentos. Tendo em vista a quantidade de informações disponíveis nas redes sociais e a atual crise sanitária causada pela pandemia do novo Coronavírus, descoberto na China no começo de 2020, levanta-se a possibilidade de que um aumento na quantidade de comentários nas redes sociais (em especial no Twitter), relacionados à doença, esteja vinculado a um aumento na quantidade de casos confirmados de COVID-19.

Para realizar tal análise, foi realizada a coleta dos comentários de usuários da rede social Twitter. A partir desta coleta, realizou-se a classificação destes comentários, para só então observar, através de validações estatísticas, se existe alguma "causalidade" inerente ou relação entre o aumento de usuários comunicando que estão doentes (ou que possuem sintomas da doença), com um aumento nos casos reportados oficialmente.

Os resultados apresentados não permitem uma inferência direta de tal relação entre os comentários e os casos, tendo em vista o período estudado e os dados utilizados.

## Abstract

The use of social networks in recent years has effectively spread in modern society, allowing a diversity of people to have a voice and express their feelings. Given the amount of information available on social networks and the current health crisis caused by the new Coronavirus pandemic, discovered in China in early 2020, the idea of linking an increase in the amount of comments on social networks (especially on Twitter) with the increase in the number of confirmed cases of COVID-19 arises.

In order to carry out such analysis, it was necessary to collect the comments of Twitter users. All those comments were processed and labeled, making possible to observe, through statistical validations, if there is any inherent "causality" or relationship between the increase in users reporting that they are sick (or have symptoms of the disease), with an increase in officially reported cases.

The final results do not allow a direct inference of such relationship between the comments and the cases, given the period studied and the data used.

## Equipe

 - [Iliana Burguán Valverde](https://github.com/imburguan) - 163677
 - [Rodolfo de Nadai](https://github.com/rdenadai) - 208911
 - [Victor Leal de Almeida](https://github.com/victorleal) - 104283
 - [Sabrina Beck Angelini](https://github.com/sabrina-beck)


## Vídeo

 - [Link do video]()


## Introdução e Motivação

As redes sociais exercem um papel fundamental na sociedade hoje, e é principalmente através delas que as pessoas se informam e discutem sobre notícias. Estudo conduzido com alunos de graduação (Social Media as Information Source: Undergraduates Use and Evaluation Behavior[1]) mostrou que 97% dos entrevistados usa as redes sociais como fonte de informação.

É também nas redes sociais que as pessoas compartilham informações sobre seu cotidiano. É fácil encontrar comentários sobre o trânsito, problemas no trabalho, dificuldades em alguma tarefa, sintomas de alguma doença. E é especialmente neste último item que está o objeto deste trabalho.

Com o avanço da COVID-19 no mundo (e consequentemente com sua rápida proliferação), várias análises sobre a doença surgem a cada momento. Estas análises vão desde a simples contagem dos casos e óbitos até previsões do aumento nestes números. Como exposto, as pessoas possuem uma tendência a expor nas redes sociais comentários diversos sobre seu cotidiano e possivelmente sobre seu estado de saúde. Dada a atual situação mundial de pandemia de COVID-19, presume-se que comentários relacionados aos principais sintomas de COVID-19 apareçam com maior frequência nas redes sociais.

Tendo em vista essa maior interação das redes sociais e a exposição cada maior de informações dos usuários, questiona-se a existência de uma relação entre o número de casos de COVID-19 efetivamente identificado pelas autoridades em saúde do Brasil, com os comentários feitos na rede social Twitter.

Este trabalho se inspira em outras tentativas de analisar comentários realizados em redes sociais e eventuais epidemias, especialmente as de Gripe. Um dos trabalhos mais conhecidos nesse sentido é o realizado pela Google, que criou a plataforma *Google Flu Trends*, cujo objetivo era prever o número de casos de Gripe nos Estados Unidos com base nas pesquisas com termos relacionados a Gripe, realizadas pelos usuários. Há de se observar que essa plataforma, entretanto, não foi capaz de fazer as previsões corretamente, por diversos motivos, e acabou sendo desativada pela empresa.

Este trabalho está organizado na seguinte forma:
1. Objetivo: elicita o objetivo da análise realizada sobre os comentários relacionados à COVID-19;
2. Recursos e métodos: elenca as bases de dados e as ferramentas utilizadas;
3. Metodologia: detalha os métodos de classificação dos comentários, bem como as análises estatísticas realizadas;
4. Resultados e discussão: apresenta os resultados encontrados com as análises estatísticas;
5. Conclusões: explicita as conclusões com bases nos resultados;
6. Trabalhos futuros: sugere novas análises e formas de tratar o problema em questão.


### Perguntas de Pesquisa

 - É possível identificar a disseminação da COVID-19 no Brasil, através do conteúdo de redes sociais?
 - Sendo possível, ou existindo alguma relação "causal":
   - Com que grau de certeza a disseminação de COVID-19 é identificada?
   - Com que antecedência podemos identificar a disseminação da doença (em dias/semanas)?
   - Considerando que boa parte do conteúdo extraído não terá informações de geolocalização, é possível verificar essa disseminação por cidades ou estados?


### Objetivo

O projeto tem como principal objetivo avaliar a possibilidade de se identificar, através das redes sociais, a disseminação de doenças, especificamente a COVID-19 no Brasil.

A identificação baseia-se na extração e análise de comentários de usuários das redes sociais (mais especificamente do Twitter), que utilizaram termos relacionados aos sintomas da doenças, tais como “dor de cabeça”, “febre”, entre outros. O conteúdo desta extração, pré processado (usando técnicas de NLP - *Natural Language Processing*) e classificado como comentário positivo para a doença ou não (usando técnicas convencionais de ML - *Machine Learning*), será comparado com os dados oficiais de andamento da doença (quantidade de novos casos / mortes). Com isso, procura-se verificar a possibilidade de prever a disseminação da doença.

A análise leva em conta a evolução da quantidade de comentários e novos casos da doença ao longo do tempo, e dessa maneira foram inicialmente avaliados como séries temporais. Sendo os resultados concretos, isso forneceria informações sobre possíveis casos ainda não registrados oficialmente nas estatísticas elaboradas pelos órgãos oficiais, melhorando a visão de como a doença está disseminada na sociedade.

## Recursos e Métodos

### Bases de Dados:
Para esta análise, foi criada uma base de dados com os comentários realizados no Twitter. Juntamente a esta base, foram utilizadas bases de dados oficiais sobre os casos de COVID-19 no Brasil.

Base de Dados | Endereço na Web | Resumo descritivo e uso
----- | ----- | -----
Comentários Twitter | <não disponível online> | Base de dados com os comentários do Twitter, processados e classificados.
Covid-19 : Dados Brasil | https://github.com/wcota/covid19br | Informações sobre a evolução diária da COVID-19 no Brasil, com os números de casos e óbitos em todas as cidades


 - [Covid-19 : Dados Mundo](https://github.com/CSSEGISandData/COVID-19)
 - [Covid-19 : Ministério da Saúde](https://covid.saude.gov.br/)
 - [Covid-19 : Dados Brasil](https://github.com/wcota/covid19br)
 - [Covid-19 : Dados Brasil : prof. Paula](https://github.com/pdpcosta/COVID-19_Brazil)
 - [IBGE : Dados populacionais](https://www.ibge.gov.br/estatisticas/sociais/populacao.html)
 - [Coronavirus (covid19) Tweets](https://www.kaggle.com/smid80/coronavirus-covid19-tweets#2020-03-00%20Coronavirus%20Tweets%20(pre%202020-03-12).CSV)


### Ferramentas
Ferramenta | Endereço na Web | Resumo descritivo e uso
----- | ----- | -----
Python | https://www.python.org/ | Linguagem de Programação Python, usada para os scripts de análise
SQLite | https://www.sqlite.org/index.html | Sistema Gerenciador de Banco de Dados simples, usado para armazenamento dos comentários do Twitter
Scikit-Learn | https://scikit-learn.org/stable/ | Biblioteca com algoritmos de Machine Learning, utilizada na tarefa de classificação dos comentários
Statsmodels | https://www.statsmodels.org/stable/index.html | Biblioteca com modelos e testes estatísticos, utilizados nas análises estatísticas entre comentários e casos
Selenium WebDriver | https://www.selenium.dev/ | Biblioteca para automatização de tarefas em navegadores web. Utilizada para automação da coleta de comentários do Twitter
NTLK | https://www.nltk.org/ | Biblioteca com funções específicas para processamento de texto. Utilizada para classificação dos comentários

## Metodologia
Como já especificado, o objetivo deste trabalho está em tentar correlacionar comentários relacionados à COVID-19 com o número de casos da doença no Brasil. Para tanto, faz-se necessária a coleta de tais comentários, o processamento destes comentários, de forma que sejam contabilizados, dentro do possível, apenas os comentários efetivamente relacionados a doença, e a posterior análise estatística com os dados oficiais sobre a COVID-19 no país.

Dado o alto número de comentários, optou-se pela classificação destes através de um algoritmo de *Machine Learning*. Feita esta classificação, o problema passou a ser tratado como uma série temporal: tanto o número de comentários como de casos variavam em função do tempo. Portanto, as análises foram feitas considerando essa especificidade.

### Detalhamento do Projeto
Nesta seção é detalhado todo o processo, desde a definição dos termos de pesquisa, classficação dos comentários e análises estatísticas.

#### Definição dos termos de busca
Para a coleta dos comentários do Twitter, havia a necessidade de se definir os termos para os quais seria feita a busca. A rede social possui um mecanismo de busca avançada que permite que apenas textos contendo tais termos sejam retornados. Por exemplo, pode-se definir a busca pelo termo "COVID" de forma que apenas comentários contendo "COVID" sejam retornados.

Para este trabalho, optou-se por, além dos termos que especificam a doença, utilizar termos de sintomas da doença, especificados pela Organização Mundial da Saúde. A lista de termos utilizada é a seguinte:
- peguei covid,
- peguei covid19,
- peguei corona,
- estou com covid,
- estou com covid19,
- estou com corona,
- estou doente covid,
- estou doente covid19,
- estou doente corona,
- dor de cabeça febre,
- dor de cabeça corona,
- dor de cabeça covid,
- dor de cabeça covid19,
- falta de ar corona,
- falta de ar covid,
- falta de ar covid19,
- falta de ar,
- dor de garganta corona,
- dor de garganta covid,
- dor de garganta covid19,
- dor de garganta,
- tosse, febre e coriza,
- testei positivo covid,
- testei positivo corona,
- testei negativo covid,
- testei negativo corona,
- dor de cabeça febre,
- dor de cabeça corona,
- dor de cabeça covid,
- dor de cabeça covid19,
- diarréia corona,
- diarréia covid,
- diarréia covid19,
- febre corona,
- febre covid,
- febre covid19,
- falta de ar corona,
- falta de ar covid,
- falta de ar covid19,
- tosse corona,
- tosse covid,
- tosse covid19,
- coriza corona,
- coriza covid,
- coriza covid19,
- dor de garganta corona,
- dor de garganta covid,
- dor de garganta covid19,
- febre,
- falta de ar,
- tosse,
- coriza,
- dor de garganta,
- tosse febre coriza

Optou-se ainda por restringir os resultados da busca a partir do dia 01/01/2020, de forma que apenas comentários feitos a partir desta data fossem coletados. Isso foi feito considerando que a doença teve maior conhecimento mundial no início de 2020.

#### Coleta dos comentários
A coleta dos comentários foi feita fazendo uso da ferramenta Selenium WebDriver, que permite a automação de tarefas feitas em um navegador web.

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
