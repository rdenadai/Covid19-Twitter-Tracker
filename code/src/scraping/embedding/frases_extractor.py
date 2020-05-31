import os
import sys
import pickle
import asyncio
from itertools import chain

import httpx
from bs4 import BeautifulSoup
from aiomultiprocess import Pool

main_urls = [
    ("https://www.frasesdobem.com.br/frases-engracadas/", 0),
    ("https://www.frasesdobem.com.br/frases-de-dia-dos-namorados", 0),
    ("https://www.frasesdobem.com.br/frases-de-amizade", 0),
    ("https://www.frasesdobem.com.br/frases-de-carinho", 0),
    ("https://www.frasesdobem.com.br/frases-inspiradoras", 0),
    ("https://www.frasesdobem.com.br/frases-de-amor", 0),
    ("https://www.frasesdobem.com.br/frases-apaixonadas", 0),
    ("https://www.frasesdobem.com.br/frases-romanticas", 0),
    ("https://www.frasesdobem.com.br/frases-de-autoestima", 0),
    ("https://www.frasesdobem.com.br/frases-de-superacao", 0),
    ("https://www.frasesdobem.com.br/frases-de-otimismo", 0),
    ("https://www.frasesdobem.com.br/frases-de-positividade", 0),
    ("https://www.frasesdobem.com.br/frases-pensativas", 0),
    ("https://www.frasesdobem.com.br/frases-de-impacto", 0),
    ("https://www.frasesdobem.com.br/frases-filosoficas", 0),
    ("https://www.frasesdobem.com.br/frases-de-sabedoria", 0),
    ("https://www.frasesdobem.com.br/frases-religiosas", 0),
    ("https://www.frasesdobem.com.br/frases-de-motivacao", 0),
    ("https://www.frasesdobem.com.br/frases-legais", 0),
    ("https://www.frasesdobem.com.br/frases-perfeitas", 0),
    ("https://www.frasesdobem.com.br/frases-de-aventura", 0),
    ("https://www.frasesdobem.com.br/frases-de-determinacao", 0),
    ("https://www.frasesdobem.com.br/frases-de-arrependimento", 0),
    ("https://www.frasesdobem.com.br/frases-sobre-cultura", 0),
    ("https://www.frasesdobem.com.br/frases-de-liberdade", 0),
    ("https://www.frasesdobem.com.br/frases-sobre-mentira", 0),
    ("https://www.frasesdobem.com.br/frases-inveja", 0),
    ("https://www.frasesdobem.com.br/frases-ironicas", 0),
    ("https://www.pensador.com/frases_para_ofender/", 1),
    ("https://www.pensador.com/frases_de_amizade/", 1),
    ("https://www.pensador.com/recentes/", 1),
    ("https://www.pensador.com/epigrafe_para_tcc/", 1),
    ("https://www.pensador.com/mensagens_depressao/", 1),
    ("https://www.pensador.com/o_tempo_passa_depressa/", 1),
    ("https://www.pensador.com/autor/dalai_lama/", 1),
    ("https://www.pensador.com/autor/martin_luther_king/", 1),
    ("https://www.pensador.com/autor/sigmund_freud/", 1),
    ("https://www.pensador.com/autor/adolf_hitler/", 1),
    ("https://www.pensador.com/autor/adam_smith/", 1),
    ("https://www.pensador.com/autor/maisa_silva/", 1),
    ("https://www.pensador.com/autor/pabllo_vittar/", 1),
    ("https://www.pensador.com/autor/padre_fabio_de_melo/", 1),
    ("https://www.pensador.com/populares/", 1),
    ("https://www.pensador.com/frases_de_escritores_famosos/", 1),
    ("https://www.pensador.com/autor/pitagoras/", 1),
    ("https://www.pensador.com/autor/voltaire/", 1),
    ("https://www.pensador.com/frases_de_besteira/", 1),
    ("https://www.pensador.com/puta/", 1),
    ("https://www.pensador.com/vagabundo/", 1),
    ("https://www.pensador.com/pinto/", 1),
    ("https://www.pensador.com/cacete/", 1),
    ("https://www.pensador.com/puta_que_pariu/", 1),
    ("https://www.pensador.com/vara/", 1),
    ("https://www.pensador.com/vagina/", 1),
    ("https://www.pensador.com/autor/albert_einstein/", 1),
    ("https://www.pensador.com/frases_de_duvida/", 1),
    ("https://www.pensador.com/frases_para_refletir/", 1),
    ("https://www.pensador.com/frases_positivas/", 1),
    ("https://www.pensador.com/autor/edgar_allan_poe/", 1),
    ("https://www.pensador.com/maca/", 1),
    ("https://www.pensador.com/software/", 1),
    ("https://www.pensador.com/computador/", 1),
    ("https://www.pensador.com/internet/", 1),
    ("https://www.pensador.com/cozinha/", 1),
    ("https://www.pensador.com/gripe/", 1),
    ("https://www.pensador.com/morcego/", 1),
    ("https://www.pensador.com/imagem/", 1),
    ("https://www.pensador.com/guerra/", 1),
]

urls = []
for url, tipo in main_urls:
    urls += [url]
    for i in range(2, 30):
        if tipo == 0:
            urls += [f"{url}page/{i}/"]
        else:
            urls += [f"{url}{i}/"]


async def get_link_content(url):
    phrases = []
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(url, timeout=120)
            if r.status_code == 200:
                html = BeautifulSoup(r.content, "lxml")
                posts = html.findAll("p", {"class": "frase"})
                for post in posts:
                    phrases += (
                        BeautifulSoup(post.get_text(), "lxml")
                        .get_text()
                        .replace("\n", ".")
                        .split(".")
                    )
        except:
            pass
    return phrases


async def carregar(func, urls):
    async with Pool() as pool:
        result = await pool.map(func, urls)
    return result


if __name__ == "__main__":
    phrases = filter(None, chain(*asyncio.run(carregar(get_link_content, urls))))
    phrases = list(set([phrase.strip() for phrase in phrases if len(phrase) > 10]))
    with open(f"{os.getcwd()}/data/embedding/frases.pkl", "wb") as fh:
        pickle.dump(phrases, fh)
