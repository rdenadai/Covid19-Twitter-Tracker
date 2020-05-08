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

    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        start_time = time.time()
        contents = list(executor.map(run_hashtag, hashtags, chunksize=1))
        print(f"--- Load tweets: {round(time.time() - start_time, 2)} seconds ---")
        for item in contents:
            print(f"---{item['hashtag']} => {len(item['comments'])}")
        start_time = time.time()
        list(executor.map(run_save_hashtag, contents, chunksize=25))
        print(f"--- Save tweets: {round(time.time() - start_time, 2)} seconds ---")
