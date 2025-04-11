import sqlite3

conn = sqlite3.connect('guides.db')
conn.execute('''
CREATE TABLE IF NOT EXISTS guides (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT,
    content TEXT,
    start_date TEXT,
    end_date TEXT,
    image TEXT
)
''')

# 초기 데이터 삽입 예시 (없어도 됨)
conn.execute('''
INSERT INTO guides (title, category, content, start_date, end_date, image)
VALUES (?, ?, ?, ?, ?, ?)
''', ('예시 공략', '이벤트 정보', '공략 내용입니다.', '2025-04-12T00:00', '2025-04-30T23:59', NULL))

conn.commit()
conn.close()
