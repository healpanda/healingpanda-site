from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import sqlite3
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_db_connection():
    conn = sqlite3.connect('guides.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.template_filter('format_datetime')
def format_datetime(value):
    try:
        dt = datetime.fromisoformat(value)
        return dt.strftime('%Y-%m-%d %H:%M')
    except Exception:
        return value

@app.route('/')
def index():
    conn = get_db_connection()
    filter_type = request.args.get('filter', 'all')

    if filter_type == 'active':
        today = datetime.now().isoformat()
        guides = conn.execute('SELECT * FROM guides WHERE end_date >= ?', (today,)).fetchall()
    else:
        guides = conn.execute('SELECT * FROM guides').fetchall()

    # 중복 없는 main/sub 카테고리 리스트 (선택적 사용 가능)
    main_categories = list(set([g['main_category'] for g in guides if g['main_category']]))
    conn.close()
    return render_template('index.html', guides=guides, filter_type=filter_type, main_categories=main_categories)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/add', methods=('GET', 'POST'))
def add_guide():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        main_category = request.form['main_category']
        sub_category = request.form['sub_category']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        image = request.files.get('image')

        image_filename = None
        if image and image.filename != '':
            image_filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO guides (title, description, image_filename, start_date, end_date, main_category, sub_category)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (title, description, image_filename, start_date, end_date, main_category, sub_category))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/edit/<int:guide_id>', methods=('GET', 'POST'))
def edit_guide(guide_id):
    conn = get_db_connection()
    guide = conn.execute('SELECT * FROM guides WHERE id = ?', (guide_id,)).fetchone()

    if not guide:
        return "해당 공략을 찾을 수 없습니다.", 404

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        main_category = request.form['main_category']
        sub_category = request.form['sub_category']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        image = request.files.get('image')

        image_filename = guide['image_filename']
        if image and image.filename != '':
            image_filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        conn.execute('''
            UPDATE guides
            SET title = ?, description = ?, image_filename = ?, start_date = ?, end_date = ?, main_category = ?, sub_category = ?
            WHERE id = ?
        ''', (title, description, image_filename, start_date, end_date, main_category, sub_category, guide_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit.html', guide=guide)

@app.route('/delete/<int:guide_id>', methods=['POST'])
def delete_guide(guide_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM guides WHERE id = ?', (guide_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
