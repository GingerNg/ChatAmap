
class Dao(object):
    def __init__(self) -> None:
        pass

class FsaDao(Dao):
    # falsk sqlac dao
    def __init__(self, db, app) -> None:
        self.app = app
        self.db = db
        self._create_db()

    def save_obj(self, obj):
        with self.app.app_context():
            self.db.session.add(obj)
            self.db.session.commit()

    # def query(self, obj):
    #     session = self.db.session
    #     hotels = session.query(obj).filter_by(source_id=source_id, hotel_id=hotel_id).first()

    def _create_db(self):
        with self.app.app_context():
            self.db.create_all()

from .msgs import RssMsg, TranslatorBotMsg
class RssMsgDao(FsaDao):
    def __init__(self, db, app) -> None:
        super().__init__(db, app)

    def query_by_link(self, link):
        # print(link)
        with self.app.app_context():
            item = RssMsg.query.filter_by(link=link).first()
        return item

    def insert(self, rss_msg: RssMsg):
        # print(rss_msg)
        if not self.query_by_link(rss_msg.link):
            self.save_obj(rss_msg)
            return True
        else:
            return False


class TranslatorBotMsgDao(FsaDao):
    def __init__(self, db, app) -> None:
        super().__init__(db, app)

    def fetch(self, limit=1):
        with self.app.app_context():
            item = TranslatorBotMsg.query.order_by(TranslatorBotMsg.id.desc()).limit(limit).all()
        return item