from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import sqlite3
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_db_connection():
    conn = sqlite3.connect('guides.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home_redirect():
    return redirect(url_for('index', main_category='프리코네'))

@app.route('/<main_category>')
def index(main_category):
    conn = get_db_connection()
    cur = conn.cursor()

    category = request.args.get('category', '')
    status = request.args.get('status', 'all')

    query = "SELECT * FROM guides WHERE main_category = ?"
    params = [main_category]

    if category:
        query += " AND category = ?"
        params.append(category)

    if status == 'ongoing':
        query += " AND end_date >= ?"
        params.append(datetime.now().isoformat())

    cur.execute(query, params)
    guides = cur.fetchall()

    cur.execute("SELECT DISTINCT category FROM guides WHERE main_category = ?", (main_category,))
    categories = [row['category'] for row in cur.fetchall()]
    conn.close()

    return render_template('index.html', guides=guides, categories=categories, selected_category=category, status=status)

@app.route('/add', methods=['GET', 'POST'])
def add_guide():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT category FROM guides")
    categories = [row['category'] for row in cur.fetchall()]

    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        new_category = request.form['new_category']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        main_category = '프리코네' if '프리코네' in title else '소녀전선2'

        if new_category:
            category = new_category

        image = request.files['image']
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        cur.execute("""
            INSERT INTO guides (title, category, start_date, end_date, image, main_category)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, category, start_date, end_date, filename, main_category))
        conn.commit()
        conn.close()
        return redirect(url_for('index', main_category=main_category))

    return render_template('add.html', categories=categories)

@app.route('/edit/<int:guide_id>', methods=['GET', 'POST'])
def edit_guide(guide_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM guides WHERE id = ?", (guide_id,))
    guide = cur.fetchone()

    cur.execute("SELECT DISTINCT category FROM guides")
    categories = [row['category'] for row in cur.fetchall()]

    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        new_category = request.form['new_category']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        if new_category:
            category = new_category

        filename = guide['image']
        if 'image' in request.files and request.files['image'].filename != '':
            image = request.files['image']
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        cur.execute("""
            UPDATE guides
            SET title = ?, category = ?, start_date = ?, end_date = ?, image = ?
            WHERE id = ?
        """, (title, category, start_date, end_date, filename, guide_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index', main_category=guide['main_category']))

    conn.close()
    return render_template('edit.html', guide=guide, categories=categories)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete/<int:guide_id>', methods=['POST'])
def delete_guide(guide_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM guides WHERE id = ?", (guide_id,))
    conn.commit()
    conn.close()
    return redirect(request.referrer or url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
