from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import sqlite3
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def get_db_connection():
    conn = sqlite3.connect('guides.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    category = request.args.get('category')
    status = request.args.get('status')

    conn = get_db_connection()
    query = "SELECT * FROM guides"
    filters = []
    params = []

    if category:
        filters.append("category = ?")
        params.append(category)

    if status == 'ongoing':
        filters.append("end_date >= ?")
        params.append(datetime.now().isoformat())

    if filters:
        query += " WHERE " + " AND ".join(filters)

    query += " ORDER BY start_date ASC"
    guides = conn.execute(query, params).fetchall()

    categories = conn.execute("SELECT DISTINCT category FROM guides WHERE category != ''").fetchall()
    conn.close()

    return render_template(
        'index.html',
        guides=guides,
        categories=[c['category'] for c in categories],
        selected_category=category,
        status=status
    )

@app.route('/add', methods=['GET', 'POST'])
def add_guide():
    conn = get_db_connection()
    categories = conn.execute("SELECT DISTINCT category FROM guides WHERE category != ''").fetchall()
    conn.close()

    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category'].strip() or request.form.get('new_category', '').strip()
        content = request.form['content']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        image = request.files.get('image')

        filename = None
        if image and image.filename != '':
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO guides (title, category, content, start_date, end_date, image) VALUES (?, ?, ?, ?, ?, ?)",
            (title, category, content, start_date, end_date, filename)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add.html', categories=[c['category'] for c in categories])

@app.route('/edit/<int:guide_id>', methods=['GET', 'POST'])
def edit_guide(guide_id):
    conn = get_db_connection()
    guide = conn.execute("SELECT * FROM guides WHERE id = ?", (guide_id,)).fetchone()
    categories = conn.execute("SELECT DISTINCT category FROM guides WHERE category != ''").fetchall()

    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category'].strip() or request.form.get('new_category', '').strip()
        content = request.form['content']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        image = request.files.get('image')

        filename = guide['image']
        if image and image.filename != '':
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        conn.execute(
            "UPDATE guides SET title = ?, category = ?, content = ?, start_date = ?, end_date = ?, image = ? WHERE id = ?",
            (title, category, content, start_date, end_date, filename, guide_id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit.html', guide=guide, categories=[c['category'] for c in categories])

@app.route('/delete/<int:guide_id>', methods=['POST'])
def delete_guide(guide_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM guides WHERE id = ?", (guide_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Render 배포를 위한 포트 바인딩
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(debug=True, host='0.0.0.0', port=port)
