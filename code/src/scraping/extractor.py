import os
from functools import partial
from multiprocessing import cpu_count
from concurrent.futures import ProcessPoolExecutor
import time

from decouple import config

from ..database.conn import db
from ..processing.utils import divide_chunks
from .utils import run_hashtag, run_save_hashtag


if __name__ == "__main__":

    n_posts_part = int(config("N_POSTS_PART", default=0))

    hashtags = [
        '"peguei covid"',
        '"peguei covid19"',
        '"peguei corona"',
        '"estou com covid"',
        '"estou com covid19"',
        '"estou com corona"',
        '"estou doente" covid',
        '"estou doente" covid19',
        '"estou doente" corona',
        '"dor de cabeça" febre',
        '"dor de cabeça" corona',
        '"dor de cabeça" covid',
        '"dor de cabeça" covid19',
        '"falta de ar" corona',
        '"falta de ar" covid',
        '"falta de ar" covid19',
        '"falta de ar"',
        '"dor de garganta" corona',
        '"dor de garganta" covid',
        '"dor de garganta" covid19',
        '"dor de garganta"',
        '"tosse, febre e coriza"',
        '"testei positivo" covid',
        '"testei positivo" corona',
        '"testei negativo" covid',
        '"testei negativo" corona',
    ]
    if n_posts_part == 1:
        hashtags += [
            "peguei covid",
            "estou com covid",
            "dor de cabeça febre",
            "dor de cabeça corona",
            "dor de cabeça covid",
            "dor de cabeça covid19",
            "diarréia corona",
            "diarréia covid",
            "diarréia covid19",
            "febre corona",
            "febre covid",
            "febre covid19",
            "falta de ar corona",
            "falta de ar covid",
            "falta de ar covid19",
            "tosse corona",
            "tosse covid",
            "tosse covid19",
            "coriza corona",
            "coriza covid",
            "coriza covid19",
            "dor de garganta corona",
            "dor de garganta covid",
            "dor de garganta covid19",
            "febre",
            "falta de ar",
            "tosse",
            "coriza",
            "dor de garganta",
            "tosse febre coriza",
        ]

    qtd = cpu_count() * 2
    n_posts_2_extract = int(config("N_POSTS_TO_EXTRACT", default=1))
    with ProcessPoolExecutor(max_workers=qtd) as executor:
        for hashtags_ in divide_chunks(hashtags, qtd):
            start_time = time.time()
            contents = list(
                executor.map(
                    partial(run_hashtag, n_posts_2_extract), hashtags_, chunksize=1
                )
            )
            os.system("pkill chrome")
            os.system("pkill chromedriver")
            print(f"--- Load tweets took {round(time.time() - start_time, 2)}s ---")
            start_time = time.time()
            with db.atomic() as txn:
                salvos = list(executor.map(run_save_hashtag, contents, chunksize=25))
                txn.commit()
            print(f"--- Save tweets took {round(time.time() - start_time, 2)}s ---")
            for i, item in enumerate(salvos):
                print(
                    f"--- # of tweets for : {item['hashtag']} => {len(contents[i]['comments'])}/{item['salvos']}"
                )
