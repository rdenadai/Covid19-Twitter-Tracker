from peewee import DoesNotExist

from .models import TwitterTagsClient, TwitterGeoClient
from ..database.models import RawHashtagComments, UserLocation


def run_hashtag(n_posts_2_extract, hashtag):
    print(f"- Collecting hashtag : {hashtag}")
    tw = TwitterTagsClient(n_posts_2_extract=n_posts_2_extract)
    return tw.load_tags(hashtag)


def run_save_hashtag(item):
    salvos = 0
    hashtag = item["hashtag"]
    for comment in item["comments"]:
        try:
            existe = RawHashtagComments.get(RawHashtagComments.hash == comment["hash"])
        except DoesNotExist:
            try:
                RawHashtagComments(hashtag=hashtag, **comment).save(force_insert=True)
                salvos += 1
            except:
                pass
    return {"hashtag": hashtag, "salvos": salvos}


def run_user_geo(username):
    tw = TwitterGeoClient()
    return tw.load_user_geo(username)


def run_save_user_location(item):
    try:
        geo = UserLocation.get(UserLocation.username == item[0])
    except DoesNotExist:
        try:
            UserLocation(
                **{
                    "username": item[0],
                    "city": item[1],
                    "state": item[2],
                    "region": item[3],
                    "geo": item[4],
                }
            ).save(force_insert=True)
            return item[0]
        except Exception as e:
            pass  # print(e)
    return None
