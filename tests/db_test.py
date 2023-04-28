from utils.flask_sql_utils import init_db_app


def test_create_db():
    db, app = init_db_app()
    with app.app_context():
        db.create_all()


def test_fetch():
    db, app = init_db_app()
    from common.models.dao import TranslatorBotMsgDao
    dao = TranslatorBotMsgDao(db, app)
    items = dao.fetch()
    print(items)
    for item in items:
        print(item.content)