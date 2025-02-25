from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'  # Change if using cloud MySQL (e.g., Render)
app.config['MYSQL_USER'] = 'root'  # Replace with your MySQL username
app.config['MYSQL_PASSWORD'] = 'password'  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'tektap'

mysql = MySQL(app)


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM employees")
    employees = cur.fetchall()
    return render_template('index.html', employees=employees)


@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        department = request.form['department']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO employees (name, position, department) VALUES (%s, %s, %s)",
                    (name, position, department))
        mysql.connection.commit()
        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM employees WHERE id = %s", (id,))
    employee = cur.fetchone()

    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        department = request.form['department']

        cur.execute("UPDATE employees SET name = %s, position = %s, department = %s WHERE id = %s",
                    (name, position, department, id))
        mysql.connection.commit()
        return redirect(url_for('index'))

    return render_template('edit.html', employee=employee)


@app.route('/delete/<int:id>')
def delete_employee(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM employees WHERE id = %s", (id,))
    mysql.connection.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
