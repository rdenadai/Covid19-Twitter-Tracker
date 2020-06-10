import os
import sys
import time
import pickle
import asyncio
from itertools import chain

import httpx
from bs4 import BeautifulSoup
from aiomultiprocess import Pool
import feedparser


rss = [
    "https://brasil.elpais.com/rss/brasil/portada_completo.xml",
]

urls = [
    "https://brasil.elpais.com/",
    "https://brasil.elpais.com/seccion/economia/",
    "https://brasil.elpais.com/seccion/ciencia/",
    "https://brasil.elpais.com/seccion/tecnologia/",
    "https://brasil.elpais.com/seccion/internacional/",
    "https://brasil.elpais.com/seccion/cultura/",
]


async def get_link_content(url):
    phrases = []
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(url, timeout=120)
            if r.status_code == 200:
                html = BeautifulSoup(r.content, "lxml")
                posts = html.findAll("div", {"class": "article_body"})
                for post in posts:
                    phrases += post.get_text().split(".")
    except Exception as e:
        print(f"2. Erro ao carregar posts: {url}, {str(e)}")
    return phrases


async def get_links_pagina_inicial(url):
    links = []
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(url, timeout=60)
            if r.status_code == 200:
                html = BeautifulSoup(r.content, "lxml")
                links_ = html.findAll("h2", {"class": "headline"})
                for link in links_:
                    links.append(
                        f"https://brasil.elpais.com{link.find('a').get('href')}"
                    )
    except Exception as e:
        print(f"2. Erro ao carregar posts: {url}, {str(e)}")
    return links


async def get_links(url):
    links = []
    try:
        d = feedparser.parse(url)
        links = [item["link"] for item in d["entries"]]
    except Exception as e:
        print(f"1. Erro ao carregar posts: {url}, {str(e)}")
    return links


async def carregar(func, urls):
    async with Pool() as pool:
        result = await pool.map(func, urls)
    return result


if __name__ == "__main__":
    links = list(filter(None, chain(*asyncio.run(carregar(get_links, rss)))))
    links += list(
        filter(None, chain(*asyncio.run(carregar(get_links_pagina_inicial, urls))),)
    )

    print(f"Links carregados... {len(links)}")
    phrases = filter(None, chain(*asyncio.run(carregar(get_link_content, links))))
    phrases = [phrase.strip() for phrase in phrases if len(phrase) > 10]

    sentences = []
    try:
        with open(f"{os.getcwd()}/data/embedding/elpais.pkl", "rb") as fh:
            sentences = pickle.load(fh)
            sentences = [sent.strip() for sent in sentences]
    except:
        pass
    with open(f"{os.getcwd()}/data/embedding/elpais.pkl", "wb") as fh:
        sents = set(sentences + phrases)
        pickle.dump(list(sents), fh)
