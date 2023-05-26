import datetime
from dataclasses import dataclass

from utils.env_utils import db_url
from utils.flask_sql_utils import init_db_app
db, app = init_db_app(db_url=db_url)

# ***************************************************** Shanbay
class ShanbayMsg(db.Model):
    words: str
    story: str
    role: str
    role_type: str

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime,
                           default=datetime.datetime.now, nullable=False)
    update_time = db.Column(db.DateTime,
                           default=datetime.datetime.now,
                           onupdate=datetime.datetime.now, nullable=False)
    words = db.Column(db.Text())
    story = db.Column(db.Text())
    role = db.Column(db.String(32), index=True)
    role_type = db.Column(db.String(32), index=True)

    def __init__(self, words, story, role="G", role_type="G"):
        self.words = words
        self.story = story
        self.role = role
        self.role_type = role_type

# ***************************************************** TranslatorBot
class TranslatorBotMsg(db.Model):
    content: str
    role: str
    role_type: str

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime,
                           default=datetime.datetime.now, nullable=False)
    update_time = db.Column(db.DateTime,
                           default=datetime.datetime.now,
                           onupdate=datetime.datetime.now, nullable=False)
    content = db.Column(db.Text())
    role = db.Column(db.String(32), index=True)
    role_type = db.Column(db.String(32), index=True)

    def __init__(self, content, role="G", role_type="G"):
        self.content = content
        self.role = role
        self.role_type = role_type

# ***************************************************** Tg UserMgs
class Dialog(db.Model):
    content: str
    role: str
    role_type: str
    round: int
    session_id: str
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime,
                           default=datetime.datetime.now, nullable=False)
    update_time = db.Column(db.DateTime,
                           default=datetime.datetime.now,
                           onupdate=datetime.datetime.now, nullable=False)
    content = db.Column(db.Text())
    role = db.Column(db.String(32))
    role_type = db.Column(db.String(32))
    session_id = db.Column(db.String(64))
    round = db.Column(db.Integer)

    def __init__(self, content, round, session_id="tg", role="G", role_type="G"):
        self.content = content
        self.role = role  # chat_id/user_id
        self.role_type = role_type  # user(tg)/gpt/model_id
        self.round = round
        self.session_id = session_id


class TgMsg(db.Model):
    content: str
    role: str
    role_type: str
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime,
                           default=datetime.datetime.now, nullable=False)
    update_time = db.Column(db.DateTime,
                           default=datetime.datetime.now,
                           onupdate=datetime.datetime.now, nullable=False)
    content = db.Column(db.Text())
    role = db.Column(db.String(32), index=True)
    role_type = db.Column(db.String(32), index=True)

    def __init__(self, content, role="G", role_type="G"):
        self.content = content
        self.role = role
        self.role_type = role_type


# ***************************************************** RSS
class Subscription(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime,
                           default=datetime.datetime.now, nullable=False)
    update_time = db.Column(db.DateTime,
                           default=datetime.datetime.now,
                           onupdate=datetime.datetime.now, nullable=False)

@dataclass
class RssMsg(db.Model):
    # __tablename__ = "rss_msg"
    source: str
    title: str
    link: str
    summary: str
    published: str

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime,
                           default=datetime.datetime.now, nullable=False)
    update_time = db.Column(db.DateTime,
                           default=datetime.datetime.now,
                           onupdate=datetime.datetime.now, nullable=False)

    source = db.Column(db.String(256))
    title = db.Column(db.Text())
    link = db.Column(db.String(512))
    summary = db.Column(db.Text())
    published = db.Column(db.DateTime, nullable=False)

    def __init__(self, source, title, link, summary, published):
        self.source = source
        self.title = title
        self.link = link
        self.summary = summary
        self.published = published