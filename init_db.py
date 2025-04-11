import sqlite3
from datetime import datetime

conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS guides (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        category TEXT,
        content TEXT NOT NULL,
        image_url TEXT,
        start_date TEXT,
        end_date TEXT
    )
''')

sample_data = [
    ('초보자를 위한 프리코네 가이드', '프리코네 > 이벤트 정보', '프리코네 입문자를 위한 공략입니다.', '/static/images/clan.jpg', '2025-04-10 10:00:00', '2025-04-30 22:00:00'),
    ('아레나 캐릭터 조합 추천', '프리코네 > 픽업 정보', '추천 캐릭터 조합 리스트입니다.', '/static/images/luna.jpg', '2025-04-05 09:30:00', '2025-04-20 21:00:00')
]

c.executemany('''
    INSERT INTO guides (title, category, content, image_url, start_date, end_date)
    VALUES (?, ?, ?, ?, ?, ?)
''', sample_data)

conn.commit()
conn.close()
print("✅ guides 테이블과 샘플 데이터 생성 완료")