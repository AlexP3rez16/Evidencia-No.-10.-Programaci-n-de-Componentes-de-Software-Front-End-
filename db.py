import os
import pymysql
import pymysql.cursors

DB_CONFIG = {
    'host':        os.getenv('DB_HOST', 'localhost'),
    'user':        os.getenv('DB_USER', 'biblioteca_ducky'),
    'password':    os.getenv('DB_PASSWORD', '1730'),
    'database':    os.getenv('DB_NAME', 'biblioteca_arqui'),
    'charset':     'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}

def get_db():
    return pymysql.connect(**DB_CONFIG)
