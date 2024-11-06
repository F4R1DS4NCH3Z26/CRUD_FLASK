from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_HOST'] = '127.0.0.1' # localhost
app.config['MYSQL_DB'] = 'practica'
mysql = MySQL(app) 

app.secret_key = 'mysecretkey'


@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios")
    data = cur.fetchall()
    return render_template('/index.html', usuarios = data)

@app.route('/add_contact', methods=['POST'])
def add_contcat():
    if request.method == 'POST':
        fullname = request.form['nombre']
        email = request.form['email']
        lastname = request.form['apellido']

        cur = mysql.connection.cursor()
        response = cur.execute("INSERT INTO usuarios (nombre, apellido, email) VALUES (%s,%s,%s)", (fullname, lastname, email))
        if response:
            flash("Guardo exitosamente")

        mysql.connection.commit()
    return redirect(url_for('Index'))

@app.route('/edit_contact/<id>' , methods=['POST'])
def edit_contact(id):
    fullname = request.form['nombre']
    email = request.form['email']
    lastname = request.form['apellido']
    cur = mysql.connection.cursor()
    response = cur.execute(f"UPDATE usuarios SET nombre = '{fullname}', apellido = '{lastname}', email = '{email}' WHERE id = {id}")
    if response:
        flash("Se actualizo exitosamente")

    mysql.connection.commit()
    return redirect(url_for('Index'))

@app.route('/data_edit_contact/<id>')
def data_edit_contact(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios WHERE id = {0}".format(id))
    data = cur.fetchall()
    return render_template('/edit_contact.html', usuarios = data[0])

@app.route('/delete_contact/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    response = cur.execute("DELETE FROM usuarios WHERE id = {0}".format(id))
    if response:
        flash("Eliminación exitosamente")

    mysql.connection.commit()
    return redirect(url_for('Index'))


if __name__ == '__main__':
    app.run(port = 3000, debug=True)