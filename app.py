import sqlite3
import os
import pprint

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
app = Flask(__name__)

DATABASE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'bartender.db')
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static', 'img')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

try:
    conn = sqlite3.connect(DATABASE)
    conn.execute('CREATE TABLE IF NOT EXISTS drinks (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, image_name TEXT, drink_info TEXT)')
    conn.close()
except sqlite3.Error as e:
    print(e, flush=True)

def query_database(query):
    try:
        with sqlite3.connect(DATABASE) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            return rows
    except sqlite3.Error as e:
        print(e, flush=True)
        conn.rollback()
        return []
    finally:
        conn.close()

def insert_into_database(query):
    try:
        with sqlite3.connect(DATABASE) as conn:
            cur = conn.cursor()
            cur.execute(query)
            conn.commit()
    except sqlite3.Error as e:
        print(e, flush=True)
        conn.rollback()
    finally:
        conn.close()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    drink_list = query_database('SELECT name, image_name, drink_info FROM drinks')
    pprint.pprint(drink_list)
    return render_template('index.html', drink_list=drink_list)

@app.route('/add')
def add_drinks():
    return render_template('add.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    name = request.form.get('drink_name')
    drink_info = request.form.get('drink_info')
    file = request.files.get('drink_image')

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_DIR, 'up_' + filename))
        image_name = 'up_' + file.filename
    else:
        image_name = 'cocktail.jpg'

    insert_query = "INSERT INTO drinks (name, image_name, drink_info) VALUES ('%s', '%s', '%s')" % (name, image_name, drink_info)
    insert_into_database(insert_query)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
