import sqlite3

conn = sqlite3.connect('guides.db')
c = conn.cursor()

c.execute('''
CREATE TABLE guides (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# 예시 데이터 삽입
c.execute("INSERT INTO guides (title, category, content) VALUES (?, ?, ?)", 
          ('초보자용 프리코네 가이드', '프리코네', '프리코네를 처음 시작할 때 참고할 공략입니다.'))

conn.commit()
conn.close()
