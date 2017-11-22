from peewee import *
import json

db = SqliteDatabase('trading.db')


class TradingBaseClass(Model):
    history = CharField()

    def get_history(self):
        return json.loads(self.history)

    def set_history(self, h):
        self.history = json.dumps(h)

    class Meta:
        database = db


class YobitTrading(TradingBaseClass):
    pass
