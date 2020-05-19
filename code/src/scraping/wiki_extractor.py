import os
import pickle

import wikipediaapi

from ..processing.utils import normalizar


if __name__ == "__main__":

    wiki_wiki = wikipediaapi.Wikipedia(
        "pt", extract_format=wikipediaapi.ExtractFormat.WIKI
    )

    termos = sorted(
        list(
            set(
                [
                    "doença",
                    "febre",
                    "dor de cabeça",
                    "tosse",
                    "coriza",
                    "covid-19",
                    "pandemia",
                    "epidemia",
                    "economia",
                    "presidente",
                    "parlamento",
                    "medicina",
                    "medico",
                    "diarreia",
                    "virus",
                    "influenza",
                    "gripe",
                    "sistema imunitário",
                    "imunologia",
                    "dengue",
                    "célula",
                    "coração",
                    "pulmão",
                    "rim",
                    "remédio",
                    "medicamento",
                    "cloroquina",
                    "hidroxicloroquina",
                    "medicação antimalárica",
                    "anvisa",
                    "parlamento",
                    "presidencialismo",
                    "deputado",
                    "ministro",
                    "infusão",
                    "xarope",
                    "alquimia",
                    "farmacologia",
                    "carbocisteína",
                    "náuseas",
                    "doutor",
                    "tontura",
                    "palpitação",
                    "insônia",
                    "stresse psicológico",
                    "insuficiência cardíaca",
                    "demência",
                    "hipnótico",
                    "transtorno de ansiedade",
                    "ansiedade",
                    "corpo humano",
                    "fenomenologia",
                    "inflamação",
                    "infecção",
                    "toxina",
                    "hospital",
                    "hospital psiquiátrico",
                    "placebo",
                    "analgésico",
                    "comprimido",
                    "inalação",
                    "via respiratória",
                    "coronavírus",
                    "vírus_ebola",
                    "doença_por_vírus_ébola",
                    "organização_mundial_da_saúde",
                    "índice_de_massa_corporal",
                    "exercício_físico",
                    "transtorno_mental",
                    "neurocirurgia",
                    "biópsia",
                    "asma",
                    "bronquite",
                    "pneumonia",
                    "tuberculose",
                    "sputum",
                    "sono",
                    "alergia",
                ]
            )
        )
    )

    phrases = []
    for term in termos:
        page_py = wiki_wiki.page(term)
        if page_py.exists():
            paragrafos = page_py.text.split("\n")
            for parag in paragrafos:
                phrases += [normalizar(frase) for frase in parag.split(".")]
        else:
            print(f"Impossível carregar {term}")

    phrases = [phrase for phrase in phrases if len(phrase) > 10]

    with open(f"{os.getcwd()}/data/wikipedia.pkl", "wb") as fh:
        pickle.dump(phrases, fh)
    # with open(f"{os.getcwd()}/data/wikipedia.pkl", "rb") as fh:
    #     phrases = pickle.load(fh)
