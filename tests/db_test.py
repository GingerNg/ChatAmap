from utils.flask_sql_utils import init_db_app
db, app = init_db_app(db_url=f"sqlite:///livat_test.sqlite3")

def test_create_db():
    db, app = init_db_app()
    with app.app_context():
        db.create_all()

def test_fetch_tgmsg():
    from common.models.dao import TgMsgDao
    dao = TgMsgDao(db, app)
    items = dao.fetch()
    print(items)
    for item in items:
        print(item.content)


def test_fetch_translatorbotmsg():
    from common.models.dao import TranslatorBotMsgDao
    dao = TranslatorBotMsgDao(db, app)
    items = dao.fetch()
    print(items)
    for item in items:
        print(item.content)