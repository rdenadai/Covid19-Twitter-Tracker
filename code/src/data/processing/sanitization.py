import os
import sys

sys.path.append("../..")  # Adds higher directory to python modules path.

import math
import asyncio
import time
import re

from joblib import load

import uvloop
from peewee import SQL
from aiomultiprocess import Pool
from multiprocessing import cpu_count

from ...database.conn import db
from ...database.models import RawHashtagComments
from .utils import CleanUp, SNOWBALL_STEMMER


clean_up = CleanUp(remove_stopwords=True)
sanitization = CleanUp(stemmer=SNOWBALL_STEMMER)
clf = load(f"{os.getcwd()}/models/tweets_classifier.model")


async def run_model_update(md_table):
    # run filter?? .where(SQL("length(sanitized_comment) = 0"))
    N = 5000
    total = math.ceil(md_table.select().count() / N) + 1
    print(f"Total pag para {md_table.__name__}: {total-1}")
    for tt in range(total):
        start_time = time.time()
        with db.atomic() as txn:
            rows = [
                (row.hash, row.comment) for row in md_table.select().paginate(tt, N)
            ]
            for hashy, comment in rows:
                clean_up_comment = clean_up.fit(comment)
                sanitized_comment = sanitization.fit(comment)
                pred = clf.predict([sanitized_comment])
                pred = "positivo" if pred == 1 else "negativo"
                query = md_table.update(
                    clean_comment=clean_up_comment,
                    sanitized_comment=sanitized_comment,
                    classify=pred,
                ).where(md_table.hash == hashy)
                query.execute()
            txn.commit()
        print(
            f"{md_table.__name__} pag. {tt} de {total-1} --- {round(time.time() - start_time, 2)}s ---"
        )


async def main():
    md_tables = (RawHashtagComments,)

    start = time.time()
    # async with Pool(processes=cpu_count() * 2) as pool:
    #     await pool.map(run_model_update, md_tables)
    for md_table in md_tables:
        await run_model_update(md_table)
    print(f"Total : {round(time.time() - start, 2)}")


if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    asyncio.run(main())
