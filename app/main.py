import os
import json
import logging
from datetime import datetime
import requests
import psycopg2
from psycopg2.extras import execute_values

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Параметры подключения к БД
DB_PARAMS = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": "db",
    "port": "5432"
}

API_URL_USERS = "https://jsonplaceholder.typicode.com/users"
API_URL_POSTS = "https://jsonplaceholder.typicode.com/posts"
API_URL_COMMENTS = "https://jsonplaceholder.typicode.com/comments"

def get_data_from_api(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Ошибка при получении данных из API: {e}")
        return None

def insert_users(conn, users):
    with conn.cursor() as cur:
        query = """
        INSERT INTO users (name, username, email, phone, website)
        VALUES %s
        ON CONFLICT (username) DO UPDATE
        SET name = EXCLUDED.name,
            email = EXCLUDED.email,
            phone = EXCLUDED.phone,
            website = EXCLUDED.website
        """
        user_data = [(
            user['name'],
            user['username'],
            user['email'],
            user['phone'],
            user['website']
        ) for user in users]
        execute_values(cur, query, user_data)

def insert_posts(conn, posts):
    with conn.cursor() as cur:
        query = """
        INSERT INTO posts (id, user_id, title, body)
        VALUES %s
        ON CONFLICT (id) DO UPDATE
        SET user_id = EXCLUDED.user_id,
            title = EXCLUDED.title,
            body = EXCLUDED.body
        """
        post_data = [(
            post['id'],
            post['userId'],
            post['title'],
            post['body']
        ) for post in posts]
        execute_values(cur, query, post_data)

def insert_comments(conn, comments):
    with conn.cursor() as cur:
        query = """
        INSERT INTO comments (id, post_id, name, email, body)
        VALUES %s
        ON CONFLICT (id) DO UPDATE
        SET post_id = EXCLUDED.post_id,
            name = EXCLUDED.name,
            email = EXCLUDED.email,
            body = EXCLUDED.body
        """
        comment_data = [(
            comment['id'],
            comment['postId'],
            comment['name'],
            comment['email'],
            comment['body']
        ) for comment in comments]
        execute_values(cur, query, comment_data)

def log_load_status(conn, start_time, status, records_processed, error_message=None):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO load_logs (start_time, end_time, status, records_processed, error_message) "
            "VALUES (%s, %s, %s, %s, %s)",
            (start_time, datetime.now(), status, records_processed, error_message)
        )

def main():
    start_time = datetime.now()
    conn = None
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        conn.autocommit = True

        logging.info("Получение данных из API")
        users = get_data_from_api(API_URL_USERS)
        posts = get_data_from_api(API_URL_POSTS)
        comments = get_data_from_api(API_URL_COMMENTS)

        if users is None or posts is None or comments is None:
            raise Exception("Не удалось получить данные из API")

        logging.info(f"Получено {len(users)} пользователей, {len(posts)} постов, {len(comments)} комментариев")

        logging.info("Вставка данных в базу")
        insert_users(conn, users)
        insert_posts(conn, posts)
        insert_comments(conn, comments)

        logging.info("Данные успешно загружены")
        log_load_status(conn, start_time, "SUCCESS", len(users) + len(posts) + len(comments))

    except Exception as e:
        logging.error(f"Ошибка при загрузке данных: {e}")
        if conn:
            log_load_status(conn, start_time, "ERROR", 0, str(e))

    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()
