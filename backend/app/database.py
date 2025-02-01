import sqlite3

DB_FILE = "app.db"

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db()
    cur = conn.cursor()

    # 국내/해외 기업 정보 테이블
    cur.execute("""
    CREATE TABLE IF NOT EXISTS companies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        corp_name TEXT,
        stock_code TEXT,
        country TEXT,           -- "KR" or "US" 등의 구분
        industry TEXT,
        market_cap INTEGER      -- 시총(또는 자본금 등) 저장용
    );
    """)

    # 뉴스 정보 테이블
    cur.execute("""
    CREATE TABLE IF NOT EXISTS news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        link TEXT,
        summary TEXT,
        sentiment TEXT,
        companies TEXT,
        industries TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()
