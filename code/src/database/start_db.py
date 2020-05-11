from .conn import db
from .models import RawHashtagComments, UserLocation
from peewee import *
from playhouse.migrate import *


if __name__ == "__main__":
    db.connect()
    db.create_tables(
        [RawHashtagComments, UserLocation,]
    )

    # Exemplo, caso da necessidade de atualizar alguma tabela
    # with db.atomic():
    #     migrator = SqliteMigrator(db)
    #     migrate(
    #         migrator.add_column('raw_hashtag_comments', 'clean_comment', TextField(default='')),
    #     )
