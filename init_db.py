import sqlite3
import os

# 기존 DB 삭제 (선택사항)
if os.path.exists('guides.db'):
    os.remove('guides.db')

# 새 DB 생성 및 테이블 초기화
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

# 초기 데이터 삽입
guides = [
    ('프리코네 이벤트 공략', '이벤트 정보', '이번 이벤트는 탱커 중심으로 구성하세요.', '2025-04-10T00:00', '2025-04-20T23:59', ''),
    ('프리코네 픽업 분석', '픽업 정보', '픽업 캐릭터는 PVP에서 유용합니다.', '2025-04-11T00:00', '2025-04-25T23:59', ''),
    ('소녀전선2 초반 공략', '이벤트 정보', '자원 관리가 핵심입니다.', '2025-04-12T00:00', '2025-04-22T23:59', ''),
    ('소녀전선2 발주 정리', '발주 정보', '최적의 발주 루트를 알려드립니다.', '2025-04-13T00:00', '2025-04-23T23:59', '')
]

conn.executemany('''
INSERT INTO guides (title, category, content, start_date, end_date, image)
VALUES (?, ?, ?, ?, ?, ?)
''', guides)

conn.commit()
conn.close()

print("Database initialized with sample data.")
