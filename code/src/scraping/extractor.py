from decouple import config
from functools import partial
import concurrent.futures
import time

from .utils import run_hashtag, run_save_hashtag


if __name__ == "__main__":
    hashtags = [
        "estou com covid",
        "peguei covid",
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

    n_posts_2_extract = int(config("N_POSTS_TO_EXTRACT", default=1))
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        start_time = time.time()
        contents = list(
            executor.map(partial(run_hashtag, n_posts_2_extract), hashtags, chunksize=1)
        )
        print(f"--- Load tweets took {round(time.time() - start_time, 2)} seconds ---")
        start_time = time.time()
        salvos = list(executor.map(run_save_hashtag, contents, chunksize=25))
        print(f"--- Save tweets took {round(time.time() - start_time, 2)} seconds ---")
        for i, item in enumerate(salvos):
            print(
                f"--- # of tweets for : {item['hashtag']} => {len(contents[i]['comments'])}/{item['salvos']}"
            )
