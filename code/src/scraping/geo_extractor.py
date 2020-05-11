import os
from multiprocessing import cpu_count
from concurrent.futures import ProcessPoolExecutor
import time

import pandas as pd
from peewee import JOIN

from ..database.models import RawHashtagComments, UserLocation
from .utils import run_user_geo, run_save_user_location
from ..processing.utils import normalizar


if __name__ == "__main__":

    cidades = pd.read_csv(f"{os.getcwd()}/data/brazil_cities.csv")
    cidades["nome_norm"] = cidades["nome"].apply(
        lambda nome: normalizar(nome, sort=False)
    )

    # Carregar todos os usuários que ainda não foram geolocalizados
    results = (
        RawHashtagComments.select(RawHashtagComments.username)
        .join(
            UserLocation,
            JOIN.LEFT_OUTER,
            on=(RawHashtagComments.username == UserLocation.username),
        )
        .distinct()
        .order_by(RawHashtagComments.username.asc())
    )
    usernames_d = [result.username.replace("@", "") for result in results]
    print(f"# of Users without geolocation: {len(usernames)}")

    # Realizar o processo de pesquisa no twitter, extração e gravação na base de dados
    with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        start_time_t = time.time()
        for usernames in divide_chunks(usernames_d, 20):
            start_time = time.time()
            contents = list(
                filter(None, executor.map(run_user_geo, usernames, chunksize=5))
            )
            print(f"--- Load geo took {round(time.time() - start_time, 2)} seconds ---")

            # Normaliza os dados
            start_time = time.time()
            norm_geo_users = []
            for i, content in enumerate(contents):
                try:
                    geo = cidades[cidades["nome_norm"] == content[1]]
                    lat, lng = geo[["LATITUDE", "LONGITUDE"]].values.tolist()[0]
                    norm_geo_users += [
                        (f"@{content[0]}", geo["nome"].values[0], f"{lat},{lng}")
                    ]
                except:
                    pass
            print(
                f"--- Data norm took {round(time.time() - start_time, 2)} seconds ---"
            )

            start_time = time.time()
            executor.map(run_save_user_location, norm_geo_users, chunksize=5)
            print(f"--- Save geo took {round(time.time() - start_time, 2)} seconds ---")
        print(
            f"--- All process took {round(time.time() - start_time_t, 2)} seconds ---"
        )
