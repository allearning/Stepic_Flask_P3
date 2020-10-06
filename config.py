import os


class Config:
    DEBUG = True
    SECRET_KEY = "randomstring"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
