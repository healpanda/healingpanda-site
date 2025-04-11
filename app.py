from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

@app.route('/')
def index():
    filter_type = request.args.get('filter', 'all')
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    if filter_type == 'ongoing':
        today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute("SELECT * FROM guides WHERE end_date >= ?", (today,))
    else:
        c.execute("SELECT * FROM guides")
    guides = c.fetchall()
    conn.close()
    return render_template('index.html', guides=guides)

@app.route('/add', methods=['GET', 'POST'])
def add_guide():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form['custom_category'] or request.form['category']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        image = request.files['image']
        image_url = ''
        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            image_url = '/' + image_path

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO guides (title, category, content, image_url, start_date, end_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, category, content, image_url, start_date, end_date))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/edit/<int:guide_id>', methods=['GET', 'POST'])
def edit_guide(guide_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form['custom_category'] or request.form['category']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        image = request.files['image']
        if image and image.filename != '':
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            image_url = '/' + image_path
            c.execute('''
                UPDATE guides
                SET title=?, category=?, content=?, image_url=?, start_date=?, end_date=?
                WHERE id=?
            ''', (title, category, content, image_url, start_date, end_date, guide_id))
        else:
            c.execute('''
                UPDATE guides
                SET title=?, category=?, content=?, start_date=?, end_date=?
                WHERE id=?
            ''', (title, category, content, start_date, end_date, guide_id))

        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    c.execute("SELECT * FROM guides WHERE id=?", (guide_id,))
    guide = c.fetchone()
    conn.close()
    return render_template('edit.html', guide=guide)

@app.route('/delete/<int:guide_id>', methods=['POST'])
def delete_guide(guide_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM guides WHERE id=?", (guide_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)