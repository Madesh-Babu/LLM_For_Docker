import psycopg2
from src.config import Config

def get_connection():
    return psycopg2.connect(Config.PG_URI)
