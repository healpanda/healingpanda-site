import sqlite3
from datetime import datetime

# DB 연결
conn = sqlite3.connect('database.db')
c = conn.cursor()

# guides 테이블 생성
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

# 예시 공략 데이터 삽입
sample_data = [
    (
        '초보자를 위한 프리코네 가이드',
        '프리코네',
        '이 공략은 프리코네를 처음 시작하는 유저를 위한 팁들을 모았습니다.',
        '/static/images/clan.jpg',  # static 폴더에 이미지가 있다고 가정
        '2025-04-10 10:00:00',
        '2025-04-30 22:00:00'
    ),
    (
        '아레나 공략 - 캐릭터 조합 추천',
        '아레나',
        '강력한 캐릭터 조합을 통해 아레나에서 승리하는 법!',
        '/static/images/luna.jpg',
        '2025-04-05 09:30:00',
        '2025-04-20 21:00:00'
    )
]

# 데이터 삽입
c.executemany('''
    INSERT INTO guides (title, category, content, image_url, start_date, end_date)
    VALUES (?, ?, ?, ?, ?, ?)
''', sample_data)

# 저장 및 종료
conn.commit()
conn.close()

print("✅ guides 테이블과 초기 데이터가 성공적으로 생성되었습니다.")
