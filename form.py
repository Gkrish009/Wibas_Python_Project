from flask import Flask, render_template, url_for, redirect, request
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)
Bootstrap(app)

#configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
mysql = MySQL(app)

#server route
@app.route('/', methods=['GET', 'POST'])
def index():
    #post method to server to avoid displaying the detail in the URL
    if request.method == 'POST':
        form = request.form
        #key values
        name = form['name']
        age = form['age']
        #mysql connection
        cur = mysql.connection.cursor()
        #placeholder to store values
        cur.execute("INSERT INTO employee VALUES(%s, %s)", (name, age))
        #committing the data to sql
        mysql.connection.commit()

    return render_template('form.html')

@app.route('/employee')
def employees():
    cur = mysql.connection.cursor()
    employees = cur.fetchall()


    return render_template('employees.html',employees = employees)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
