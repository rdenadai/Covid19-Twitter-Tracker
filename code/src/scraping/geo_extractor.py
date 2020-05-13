import os
import time
import json
from multiprocessing import cpu_count
from concurrent.futures import ProcessPoolExecutor

import pandas as pd
from peewee import JOIN
from decouple import config

from ..database.conn import db
from ..database.models import RawHashtagComments, UserLocation
from .utils import run_user_geo, run_save_user_location
from ..processing.utils import normalizar, divide_chunks


if __name__ == "__main__":

    json_file = f"{os.getcwd()}/src/scraping/collected_users.json"

    cidades = pd.read_csv(f"{os.getcwd()}/data/brazil_cities_final.csv")
    cidades["nome_norm"] = cidades["nome"].apply(
        lambda nome: normalizar(nome, sort=False)
    )

    with open(json_file) as fh:
        collected_users = json.load(fh)

    N_USER_GEO = int(config("N_USER_GEO", default=100))

    # Carregar todos os usuários que ainda não foram geolocalizados
    results = (
        RawHashtagComments.select(RawHashtagComments.username)
        .distinct()
        .join(
            UserLocation,
            JOIN.LEFT_OUTER,
            on=(RawHashtagComments.username == UserLocation.username),
        )
        .where(UserLocation.username.is_null())
        .order_by(RawHashtagComments.timestamp.asc())
    )

    usernames_d = [
        result.username.replace("@", "")
        for result in results
        if result.username not in collected_users
    ]
    print(f"# of Users without geolocation: {len(usernames_d)}")
    # Carregar apenas uma parcela
    usernames_d = [:N_USER_GEO]

    k = 10
    procs = cpu_count() * 2
    chunk = int(k / procs)
    # Realizar o processo de pesquisa no twitter, extração e gravação na base de dados
    with ProcessPoolExecutor(max_workers=procs) as executor:
        start_time_t = time.time()
        for usernames in divide_chunks(usernames_d, k):
            start_time = time.time()
            contents = list(
                filter(None, executor.map(run_user_geo, usernames, chunksize=1))
            )
            os.system("pkill chrome")
            os.system("pkill chromedriver")
            print(f"--- Load geo took {round(time.time() - start_time, 2)}s ---")

            # Save collected users for history
            collected_users += [f"@{username}" for username in usernames]
            with open(json_file, "w") as fh:
                json.dump(collected_users, fh)
            # ----

            # Normaliza os dados
            norm_geo_users = []
            for i, content in enumerate(contents):
                try:
                    geo = cidades[cidades["nome_norm"] == content[1]]
                    lat, lng = geo[["lat", "lng"]].values.tolist()[0]
                    norm_geo_users += [
                        (
                            f"@{content[0]}",
                            geo["nome"].values[0],
                            geo["estado"].values[0],
                            geo["regiao"].values[0],
                            f"{lat},{lng}",
                        )
                    ]
                except:
                    pass

            start_time = time.time()
            with db.atomic() as txn:
                resultados = list(
                    filter(
                        None,
                        executor.map(
                            run_save_user_location, norm_geo_users, chunksize=chunk
                        ),
                    )
                )
                qtde = len(resultados)
                print(f"Qtde saved usernames : {qtde}")
                txn.commit()
            print(f"--- Save geo took {round(time.time() - start_time, 3)}s ---")
        print(f"--- All process took {round(time.time() - start_time_t, 2)}s ---")
