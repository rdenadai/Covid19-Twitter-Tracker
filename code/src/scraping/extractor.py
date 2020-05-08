from decouple import config
from functools import partial
import concurrent.futures
import time

from .utils import run_hashtag, run_save_hashtag


if __name__ == "__main__":
    hashtags = [
        "febre",
        "falta de ar",
        "tosse",
        "coriza",
        "tosse febre coriza",
        "estou com covid",
        "peguei covid",
    ]

    n_posts_2_extract = config("N_POSTS_TO_EXTRACT", default=1)
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
                f"--- # of tweets for {item['hashtag']} => {len(contents[i]['comments'])}/{item['salvos']}"
            )
