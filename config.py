import os

import mysql.connector
import mysql.connector.pooling


def get_db_config(pool_size=10):
    return {
        "pool_name": os.getenv("IPTV_DB_POOL_NAME", "iptv_pool"),
        "pool_size": pool_size,
        "host": os.getenv("IPTV_DB_HOST", "127.0.0.1"),
        "port": int(os.getenv("IPTV_DB_PORT", "3306")),
        "user": os.getenv("IPTV_DB_USER", "iptv"),
        "password": os.getenv("IPTV_DB_PASSWORD", "iptv"),
        "database": os.getenv("IPTV_DB_NAME", "iptv"),
    }


def create_connection_pool(pool_size=10):
    return mysql.connector.pooling.MySQLConnectionPool(**get_db_config(pool_size))


def get_quake_api_token():
    return os.getenv("QUAKE_API_TOKEN", "")
