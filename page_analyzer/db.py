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
        SELECT
            urls.id,
            urls.name,
            urls.created_at,
            last_checks.created_at AS last_check_at,
            last_checks.status_code AS last_status_code
        FROM urls
        LEFT JOIN LATERAL (
            SELECT created_at, status_code
            FROM url_checks
            WHERE url_checks.url_id = urls.id
            ORDER BY url_checks.id DESC
            LIMIT 1
        ) AS last_checks ON true
        ORDER BY urls.created_at DESC, urls.id DESC
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()


def create_check(url_id, status_code):
    query = """
        INSERT INTO url_checks (url_id, status_code, created_at)
        VALUES (%s, %s, %s)
        RETURNING id
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (url_id, status_code, datetime.now()))
            return cur.fetchone()["id"]


def get_checks(url_id):
    query = """
        SELECT id, url_id, status_code, h1, title, description, created_at
        FROM url_checks
        WHERE url_id = %s
        ORDER BY id DESC
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (url_id,))
            return cur.fetchall()


def apply_migrations():
    schema = Path(__file__).resolve().parent.parent / "database.sql"
    statements = [
        part.strip()
        for part in schema.read_text().split(";")
        if part.strip()
    ]
    with get_connection() as conn:
        for statement in statements:
            conn.execute(statement)
