from peewee import DoesNotExist

from ..database.models import RawHashtagComments


def run_hashtag(hashtag, client):
    client.start(hashtag)
    return client.results


def run_save_hashtag(content):
    for data in content["data"]:
        hashtag = data["hashtag"]
        for comment in data["comments"]:
            try:
                item = RawHashtagComments.get(
                    RawHashtagComments.hash == comment["hash"]
                )
            except DoesNotExist:
                RawHashtagComments(hashtag=hashtag, **comment).save(force_insert=True)
