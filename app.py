from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

DB_PATH = 'guides.db'

# DB 연결 함수
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# 공략 작성 페이지
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        image_url = request.form['image_url']
        content = request.form['content']

        conn = get_db_connection()
        conn.execute('INSERT INTO guides (title, category, image_url, content) VALUES (?, ?, ?, ?)',
                     (title, category, image_url, content))
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
