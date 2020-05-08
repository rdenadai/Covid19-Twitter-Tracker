from peewee import DoesNotExist

from .models import TwitterTagsClient
from ..database.models import RawHashtagComments


def run_hashtag(n_posts_2_extract, hashtag):
    print(f"- Collecting hashtag : {hashtag}")
    tw = TwitterTagsClient(n_posts_2_extract=n_posts_2_extract)
    return tw.load(hashtag)


def run_save_hashtag(item):
    salvos = 0
    hashtag = item["hashtag"]
    for comment in item["comments"]:
        try:
            existe = RawHashtagComments.get(RawHashtagComments.hash == comment["hash"])
        except DoesNotExist:
            RawHashtagComments(hashtag=hashtag, **comment).save(force_insert=True)
            salvos += 1
    return {"hashtag": hashtag, "salvos": salvos}
