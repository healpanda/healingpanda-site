import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('guides.db')
    c = conn.cursor()

    # guides 테이블 생성 (main_category, sub_category 추가)
    c.execute('''
        CREATE TABLE IF NOT EXISTS guides (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            image_filename TEXT,
            start_date TEXT,
            end_date TEXT,
            main_category TEXT,
            sub_category TEXT
        )
    ''')

    # 초기 데이터 삽입
    guides = [
        (
            "프리코네 여름 이벤트",
            "수영복 캐릭터들이 등장하는 한정 이벤트!",
            None,
            datetime(2025, 4, 15, 10, 0).isoformat(),
            datetime(2025, 4, 30, 23, 59).isoformat(),
            "프리코네",
            "이벤트 정보"
        ),
        (
            "소녀전선2 발주 개시",
            "신규 장비 발주 이벤트 시작!",
            None,
            datetime(2025, 4, 10, 0, 0).isoformat(),
            datetime(2025, 4, 20, 23, 59).isoformat(),
            "소녀전선2",
            "발주 정보"
        )
    ]

    c.executemany('''
        INSERT INTO guides (title, description, image_filename, start_date, end_date, main_category, sub_category)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', guides)

    conn.commit()
    conn.close()
    print("DB 초기화 완료 및 샘플 데이터 삽입 완료")

if __name__ == "__main__":
    init_db()
