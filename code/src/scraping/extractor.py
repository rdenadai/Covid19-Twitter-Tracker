import functools
import concurrent.futures
import time

from .models import TwitterTagsClient
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

    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        start_time = time.time()
        tw = TwitterTagsClient(np_posts=40)
        contents = list(
            executor.map(
                functools.partial(run_hashtag, client=tw), hashtags, chunksize=2
            )
        )
        list(executor.map(run_save_hashtag, contents, chunksize=25))
        print(f"--- {round(time.time() - start_time, 2)} seconds ---")
