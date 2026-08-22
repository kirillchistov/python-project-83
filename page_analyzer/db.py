import os
from datetime import datetime
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

load_dotenv()


def get_database_url():
    url = os.getenv("DATABASE_URL")
    if url and url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return url


def get_connection():
    return psycopg.connect(get_database_url(), row_factory=dict_row)


def find_url_by_name(name):
    query = "SELECT id, name, created_at FROM urls WHERE name = %s"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (name,))
            return cur.fetchone()


def find_url_by_id(url_id):
    query = "SELECT id, name, created_at FROM urls WHERE id = %s"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (url_id,))
            return cur.fetchone()


def create_url(name):
    query = """
        INSERT INTO urls (name, created_at)
        VALUES (%s, %s)
        RETURNING id
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (name, datetime.now()))
            return cur.fetchone()["id"]


def get_urls():
    query = """
        SELECT id, name, created_at
        FROM urls
        ORDER BY created_at DESC, id DESC
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()


def apply_migrations():
    schema = Path(__file__).resolve().parent.parent / "database.sql"
    with get_connection() as conn:
        conn.execute(schema.read_text())
