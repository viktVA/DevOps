from flask import Flask, request, render_template, redirect, url_for
import pyodbc

app = Flask(__name__)

# Настройки базы данных
server = 'WIN-PIDNO9RPUUS\SQLEXPRESS'
database = 'barbiee'
conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
@app.route('/')
def index():
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return render_template('index.html', users=users)

@app.route('/add', methods=['POST'])
def add_user():
    username = request.form['username']
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_user(id):
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
