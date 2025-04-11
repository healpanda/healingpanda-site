import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import sqlite3
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_db_connection():
    conn = sqlite3.connect('guides.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    filter_option = request.args.get('filter', 'all')
    conn = get_db_connection()

    if filter_option == 'active':
        today = datetime.now().strftime('%Y-%m-%dT%H:%M')
        guides = conn.execute('SELECT * FROM guides WHERE end_date >= ?', (today,)).fetchall()
    else:
        guides = conn.execute('SELECT * FROM guides').fetchall()

    categories = conn.execute('SELECT DISTINCT category FROM guides WHERE category IS NOT NULL').fetchall()
    conn.close()
    return render_template('index.html', guides=guides, filter_option=filter_option, categories=categories)

@app.route('/add', methods=['GET', 'POST'])
def add_guide():
    conn = get_db_connection()
    categories = conn.execute('SELECT DISTINCT category FROM guides WHERE category IS NOT NULL').fetchall()
    conn.close()

    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        new_category = request.form.get('new_category', '').strip()
        content = request.form['content']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        if new_category:
            category = new_category

        image_file = request.files['image']
        image_filename = None
        if image_file and image_file.filename != '':
            image_filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        conn = get_db_connection()
        conn.execute(
            'INSERT INTO guides (title, category, content, start_date, end_date, image) VALUES (?, ?, ?, ?, ?, ?)',
            (title, category, content, start_date, end_date, image_filename)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add.html', categories=categories)

@app.route('/edit/<int:guide_id>', methods=['GET', 'POST'])
def edit_guide(guide_id):
    conn = get_db_connection()
    guide = conn.execute('SELECT * FROM guides WHERE id = ?', (guide_id,)).fetchone()
    categories = conn.execute('SELECT DISTINCT category FROM guides WHERE category IS NOT NULL').fetchall()

    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        new_category = request.form.get('new_category', '').strip()
        content = request.form['content']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        if new_category:
            category = new_category

        image_file = request.files['image']
        image_filename = guide['image']
        if image_file and image_file.filename != '':
            image_filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        conn.execute(
            'UPDATE guides SET title = ?, category = ?, content = ?, start_date = ?, end_date = ?, image = ? WHERE id = ?',
            (title, category, content, start_date, end_date, image_filename, guide_id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit.html', guide=guide, categories=categories)

@app.route('/delete/<int:guide_id>', methods=['POST'])
def delete_guide(guide_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM guides WHERE id = ?', (guide_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
