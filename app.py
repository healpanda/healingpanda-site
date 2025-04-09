from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('guides.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    guides = conn.execute('SELECT * FROM guides ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('index.html', guides=guides)

@app.route('/guide/<int:guide_id>')
def guide(guide_id):
    conn = get_db_connection()
    guide = conn.execute('SELECT * FROM guides WHERE id = ?', (guide_id,)).fetchone()
    conn.close()
    return render_template('guide.html', guide=guide)
