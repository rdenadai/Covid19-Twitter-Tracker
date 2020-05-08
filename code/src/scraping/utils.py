from peewee import DoesNotExist

from .models import TwitterTagsClient
from ..database.models import RawHashtagComments


def run_hashtag(hashtag):
    print(f"- Collecting for {hashtag}...")
    tw = TwitterTagsClient(np_posts=50)
    return tw.load(hashtag)


def run_save_hashtag(item):
    hashtag = item["hashtag"]
    for comment in item["comments"]:
        try:
            existe = RawHashtagComments.get(RawHashtagComments.hash == comment["hash"])
        except DoesNotExist:
            RawHashtagComments(hashtag=hashtag, **comment).save(force_insert=True)
