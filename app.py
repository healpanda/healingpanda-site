from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import sqlite3
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    category = request.args.get('category', '전체')
    status = request.args.get('status', '전체')
    conn = get_db_connection()
    guides = conn.execute('SELECT * FROM guides ORDER BY start_date DESC').fetchall()
    conn.close()

    now = datetime.now()
    if category != '전체':
        guides = [g for g in guides if g['category'] == category]
    if status == '진행중':
        guides = [g for g in guides if datetime.strptime(g['end_date'], '%Y-%m-%d %H:%M') >= now]

    categories = sorted(set(g['category'] for g in guides))
    return render_template('index.html', guides=guides, categories=categories, selected_category=category, selected_status=status)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/add', methods=('GET', 'POST'))
def add_guide():
    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        new_category = request.form.get('new_category')
        content = request.form['content']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        if new_category:
            category = new_category.strip()

        file = request.files['image']
        filename = ''
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        conn = get_db_connection()
        conn.execute('INSERT INTO guides (title, category, content, start_date, end_date, image) VALUES (?, ?, ?, ?, ?, ?)',
                     (title, category, content, start_date, end_date, filename))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn = get_db_connection()
    categories = conn.execute('SELECT DISTINCT category FROM guides').fetchall()
    conn.close()
    return render_template('add.html', categories=categories)

@app.route('/edit/<int:guide_id>', methods=('GET', 'POST'))
def edit_guide(guide_id):
    conn = get_db_connection()
    guide = conn.execute('SELECT * FROM guides WHERE id = ?', (guide_id,)).fetchone()

    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        new_category = request.form.get('new_category')
        content = request.form['content']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        file = request.files['image']
        filename = guide['image']

        if new_category:
            category = new_category.strip()
        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        conn.execute('UPDATE guides SET title = ?, category = ?, content = ?, start_date = ?, end_date = ?, image = ? WHERE id = ?',
                     (title, category, content, start_date, end_date, filename, guide_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    categories = conn.execute('SELECT DISTINCT category FROM guides').fetchall()
    conn.close()
    return render_template('edit.html', guide=guide, categories=categories)

@app.route('/delete/<int:guide_id>', methods=('POST',))
def delete_guide(guide_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM guides WHERE id = ?', (guide_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
