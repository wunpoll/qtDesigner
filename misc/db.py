import sqlite3

DB_PATH = "settings.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS env_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            param_name TEXT UNIQUE NOT NULL,
            param_value TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def get_env_settings():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT param_name, param_value FROM env_settings")
    data = cursor.fetchall()
    conn.close()
    return data


def set_env_param(param_name, param_value):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO env_settings (param_name, param_value)
        VALUES (?, ?) 
        ON CONFLICT(param_name) 
        DO UPDATE SET param_value=excluded.param_value
    """, (param_name, param_value))
    conn.commit()
    conn.close()

init_db()
