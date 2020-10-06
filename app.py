import locale

from flask import Flask
from flask_migrate import Migrate

from config import Config
from models import db

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

from views import *

if __name__ == '__main__':
    app.run()
