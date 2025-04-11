from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_PATH = 'guides.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# 메인 페이지 - 공략 목록
@app.route('/')
def index():
    conn = get_db_connection()
    guides = conn.execute('SELECT * FROM guides ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('index.html', guides=guides)

# 공략 상세 페이지
@app.route('/guide/<int:guide_id>')
def guide(guide_id):
    conn = get_db_connection()
    guide = conn.execute('SELECT * FROM guides WHERE id = ?', (guide_id,)).fetchone()
    conn.close()
    return render_template('guide.html', guide=guide)

# 공략 작성 페이지
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        image_url = request.form['image_url']
        content = request.form['content']
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = get_db_connection()
        conn.execute('INSERT INTO guides (title, category, image_url, content, created_at) VALUES (?, ?, ?, ?, ?)',
                     (title, category, image_url, content, created_at))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('create.html')

# 공략 수정 페이지
@app.route('/edit/<int:guide_id>', methods=['GET', 'POST'])
def edit(guide_id):
    conn = get_db_connection()
    guide = conn.execute('SELECT * FROM guides WHERE id = ?', (guide_id,)).fetchone()

    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        image_url = request.form['image_url']
        content = request.form['content']

        conn.execute('UPDATE guides SET title = ?, category = ?, image_url = ?, content = ? WHERE id = ?',
                     (title, category, image_url, content, guide_id))
        conn.commit()
        conn.close()
        return redirect(url_for('guide', guide_id=guide_id))

    conn.close()
    return render_template('edit.html', guide=guide)

if __name__ == '__main__':
    app.run(debug=True)
