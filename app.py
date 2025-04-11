import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.template_filter('format_datetime')
def format_datetime(value):
    if not value:
        return ''
    dt = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    return dt.strftime("%Y년 %m월 %d일 %H:%M")

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM guides ORDER BY start_date DESC")
    guides = c.fetchall()
    conn.close()
    return render_template('index.html', guides=guides)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        content = request.form['content']
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        start_dt = datetime.strptime(start_date, "%Y-%m-%dT%H:%M") if start_date else None
        end_dt = datetime.strptime(end_date, "%Y-%m-%dT%H:%M") if end_date else None

        image_url = ''
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            image_url = url_for('static', filename=f'uploads/{filename}')

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("""
            INSERT INTO guides (title, category, content, image_url, start_date, end_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, category, content, image_url, start_dt, end_dt))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/edit/<int:guide_id>', methods=['GET', 'POST'])
def edit(guide_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM guides WHERE id=?", (guide_id,))
    guide = c.fetchone()
    conn.close()

    if not guide:
        return "Guide not found", 404

    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        content = request.form['content']
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        start_dt = datetime.strptime(start_date, "%Y-%m-%dT%H:%M") if start_date else None
        end_dt = datetime.strptime(end_date, "%Y-%m-%dT%H:%M") if end_date else None

        image_url = guide[4]  # 기존 이미지
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            image_url = url_for('static', filename=f'uploads/{filename}')

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("""
            UPDATE guides SET title=?, category=?, content=?, image_url=?, start_date=?, end_date=? WHERE id=?
        """, (title, category, content, image_url, start_dt, end_dt, guide_id))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    guide_data = {
        'id': guide[0],
        'title': guide[1],
        'category': guide[2],
        'content': guide[3],
        'image_url': guide[4],
        'start_date': guide[5],
        'end_date': guide[6]
    }

    return render_template('edit.html', guide=guide_data)

if __name__ == '__main__':
    import os
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    port = int(os.environ.get('PORT', 5000))  # Render는 환경변수 PORT를 사용
    app.run(host='0.0.0.0', port=port)
