from dataclasses import dataclass, asdict
import datetime
from utils.env_utils import db_url
from utils.flask_sql_utils import init_db_app
db, app = init_db_app(db_url=db_url)

@dataclass
class User(db.Model):
    user: str
    token: str
    token_limit: int

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime,
                           default=datetime.datetime.now, nullable=False)
    update_time = db.Column(db.DateTime,
                           default=datetime.datetime.now,
                           onupdate=datetime.datetime.now, nullable=False)
    user = db.Column(db.String(32))
    token = db.Column(db.String(128))
    token_limit = db.Column(db.Integer)

    def __init__(self, user, token, token_limit):
        self.user = user
        self.token = token
        self.token_limit = token_limit

UserTokens = {}
UserTokens["sk-test1"] = User(user="test", token="sk-test1", token_limit=10000)
UserTokens["sk-123456"] = User(user="test", token="sk-123456", token_limit=10000)

if __name__ == "__main__":
    user = User(user="test", token="test", token_limit=100)
    print(user)
    print(asdict(user))