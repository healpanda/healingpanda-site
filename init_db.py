import sqlite3

conn = sqlite3.connect('guides.db')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS guides')

cur.execute('''
CREATE TABLE guides (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT,
    start_date TEXT,
    end_date TEXT,
    image TEXT,
    main_category TEXT
)
''')

sample_guides = [
    ('프리코네 이벤트 공략', '이벤트 정보', '2025-04-10 00:00', '2025-04-11 23:59', 'sample1.jpg', '프리코네'),
    ('소녀전선2 초반 공략', '이벤트 정보', '2025-04-12 00:00', '2025-04-22 23:59', 'sample2.jpg', '소녀전선2'),
    ('소녀전선2 발주 정리', '발주 정보', '2025-04-13 00:00', '2025-04-23 23:59', 'sample3.jpg', '소녀전선2')
]

cur.executemany('''
INSERT INTO guides (title, category, start_date, end_date, image, main_category)
VALUES (?, ?, ?, ?, ?, ?)
''', sample_guides)

conn.commit()
conn.close()
