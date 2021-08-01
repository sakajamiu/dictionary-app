from flask import Flask, render_template, url_for, request,flash, current_app
from flaskext.mysql import MySQL
import pymysql.cursors
import json
import os
 
app = Flask(__name__)
app.secret_key = 'secret'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_DB'] = 'dictionary'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''

mysql = MySQL(app, cursorclass= pymysql.cursors.DictCursor)

@app.route('/', methods = ['GET','POST'])
def index():
    user_response = ''
    if request.method =='POST':
       user_response = request.form['word']
       if user_response == '':
           flash('you did not enter any word, please try again', 'flash_err')
       else:
            conn = mysql.get_db()
            cur = conn.cursor()
            cur.execute('select meaning from word where word =%s',{user_response})
            rv = cur.fetchall()
            if (len (rv) >0):
                user_response = rv[0]['meaning']
            else:
                user_response = ' the word cannot be found in this dictionary, try again with another word'
     
    return render_template('index.html', user_response = user_response)

@app.route('/dashboard')
def dashboard():
    conn = mysql.get_db()
    cur = conn.cursor()
    cur.execute('select * from word')
    rv = cur.fetchall()
    return render_template('dashboard.html', words = rv)
@app.route('/word', methods=['POST'])
def add_world():
    req = request.get_json()
    word = req['word']
    meaning = req['meaning']
    if word =='' or meaning =='':
        flash('please fill in the field to add new word','flash_err')
    else:
        conn = mysql.get_db()
        cur = conn.cursor()
        cur.execute('insert into word(word,meaning)values(%s,%s)',(word,meaning))
        conn.commit()
        cur.close()
        flash('word added successfully','flash_success')

    return json.dumps('success')
@app.route('/word/<id>/delete', methods=['POST'])
def delete_world(id):
    word_id = id
    conn = mysql.get_db()
    cur = conn.cursor()
    cur.execute('delete from word where id = %s', ( word_id))
    conn.commit()
    cur.close()
    flash('word deleted successfully','flash_success')
    return json.dumps('success')
@app.route('/word/<id>/edit', methods=['POST'])
def edit_world(id):
    word_id = id
    req = request.get_json()
    word = req['word']
    meaning = req['meaning']
    if word =='' or meaning =='':
        flash('please fill in the field correctly to edit word','flash_err')
    else:
        conn = mysql.get_db()
        cur = conn.cursor()
        cur.execute('update word set word =%s, meaning = %s  where id = %s', (word, meaning, word_id))
        conn.commit()
        cur.close()
        flash('word updated successfully', 'flash_success')
    
    return json.dumps('success')

@app.route('/add_logo', methods=['POST'])
def add_logo():
    
    image = request.files['file']
    if image :
        filepath = os.path.join(current_app.root_path,'static/images/logo.png')
        image.save(filepath)
        flash('sucess')
    else:
        flash('error')
    return 'success'
    

if __name__ == "__main__":
    app.run( debug = True)

