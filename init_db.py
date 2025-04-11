import sqlite3

# DB 연결
conn = sqlite3.connect('guides.db')
c = conn.cursor()

# 기존 테이블 삭제 (있을 경우)
c.execute('DROP TABLE IF EXISTS guides')

# 새로운 guides 테이블 생성 (image_url 추가됨)
c.execute('''
CREATE TABLE guides (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT,
    image_url TEXT,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# 샘플 데이터 삽입 (이미지 URL 포함)
c.execute("INSERT INTO guides (title, category, image_url, content) VALUES (?, ?, ?, ?)",
          ('캐러밴 시즌 3', '이벤트', '/static/images/caravan.jpg', '동료와 대련이의 새롭고 짜릿한 공략'))

c.execute("INSERT INTO guides (title, category, image_url, content) VALUES (?, ?, ?, ?)",
          ('루나의 탑', '던전', '/static/images/luna.jpg', '루나의 탑 공략: 적 구성, 추천 조합, 보상 정리'))

c.execute("INSERT INTO guides (title, category, image_url, content) VALUES (?, ?, ?, ?)",
          ('4월 클랜전', '클랜전', '/static/images/clan.jpg', '클랜 보스별 패턴 정리 및 딜 순서'))

# 저장하고 닫기
conn.commit()
conn.close()
