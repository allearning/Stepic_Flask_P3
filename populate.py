import csv

from flask import Flask

from config import Config
from models import Category, Item, db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
app.app_context().push()

USER_ONLY = True

if not USER_ONLY:
    with open("data/delivery_categories.csv") as csv_file:
        rdr = csv.DictReader(csv_file, delimiter=',')
        for row in rdr:
            db.session.add(Category(**row))

    with open("data/delivery_items.csv") as csv_file:
        rdr = csv.DictReader(csv_file, delimiter=',')
        for row in rdr:
            db.session.add(Item(**row))

db.session.commit()
