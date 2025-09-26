from config import Config
import os

class TestConfig(Config):
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = "sqlite://"
    DB_HOST = "db" if os.environ.get("DOCKER_ENV") == "true" else os.environ.get("DB_HOST", "localhost")
    SQLALCHEMY_DATABASE_URI = (os.environ.get("DATABASE_URL") or
                               f'postgresql+psycopg2://{os.environ.get("POSTGRES_USER")}'
                               f':{os.environ.get("POSTGRES_PASSWORD")}@{DB_HOST}:'
                               f'{os.environ.get("DB_PORT")}/{os.environ.get("POSTGRES_DB")}')