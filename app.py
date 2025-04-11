from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
        category = request.form['category']
        custom_category = request.form.get('custom_category')
        final_category = custom_category if category == 'custom' and custom_category else category
        content = request.form['content']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        image = request.files['image']
        image_url = ''
        if image:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(image_path)
            image_url = '/' + image_path.replace('\\', '/')

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO guides (title, category, content, image_url, start_date, end_date) VALUES (?, ?, ?, ?, ?, ?)",
                  (title, final_category, content, image_url, start_date, end_date))
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
        category = request.form['category']
        custom_category = request.form.get('custom_category')
        final_category = custom_category if category == 'custom' and custom_category else category
        content = request.form['content']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        image = request.files['image']
        image_url = request.form['existing_image_url']
        if image:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(image_path)
            image_url = '/' + image_path.replace('\\', '/')

        c.execute("UPDATE guides SET title=?, category=?, content=?, image_url=?, start_date=?, end_date=? WHERE id=?",
                  (title, final_category, content, image_url, start_date, end_date, guide_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    c.execute("SELECT * FROM guides WHERE id=?", (guide_id,))
    guide = c.fetchone()
    conn.close()
    return render_template('edit.html', guide=guide)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))  # Render는 환경변수 PORT를 사용
    app.run(host='0.0.0.0', port=port)
