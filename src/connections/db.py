import psycopg
from psycopg.rows import dict_row

from src.config import settings


def get_db():
    with psycopg.connect(settings.database_url, row_factory=dict_row) as conn:
        yield conn