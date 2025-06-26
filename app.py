from flask import Flask, render_template, request, redirect, session, url_for, send_from_directory
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'


# Ruta de inicio: redirige según rol
@app.route('/')
def home():
    if 'role' in session:
        if session['role'] == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif session['role'] == 'user':
            return redirect(url_for('user_dashboard'))
    return redirect(url_for('login'))


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('complaints.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['username'] = user[1]
            session['role'] = user[3]
            if user[3] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            return "Credenciales inválidas"

    return render_template('login.html')


# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# Página de selección de servicio
@app.route('/service_menu')
def service_menu():
    return render_template('service_menu.html')


# Página principal del usuario, recibe el servicio seleccionado
@app.route('/user_home', methods=['GET'])
def user_home():
    if 'role' not in session or session['role'] != 'user':
        return redirect(url_for('login'))
    selected_service = request.args.get('service')
    return render_template('user_home.html', selected_service=selected_service)


# Cambia la ruta de user_dashboard para redirigir al menú de servicios
@app.route('/user')
def user_dashboard():
    if 'role' not in session or session['role'] != 'user':
        return redirect(url_for('login'))
    return redirect(url_for('service_menu'))


# Registrar reclamo
@app.route('/submit', methods=['POST'])
def submit():
    if 'username' not in session:
        return redirect(url_for('login'))
    name = request.form['name']
    service = request.form['service']
    description = request.form['description']
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    username = session['username']

    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO complaints (name, username, service, description, date)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, username, service, description, date))
    conn.commit()
    conn.close()

    return redirect(url_for('user_dashboard'))


# Consultar estado de reclamos
@app.route('/status', methods=['GET'])
def status():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM complaints WHERE username = ?", (username,))
    complaints = cursor.fetchall()
    conn.close()
    return render_template('status.html', complaints=complaints)


# Panel de administración
@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))

    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        complaint_id = request.form['id']
        new_status = request.form['status']
        response_text = request.form['response']
        cursor.execute('''
            UPDATE complaints
            SET status = ?, response = ?
            WHERE id = ?
        ''', (new_status, response_text, complaint_id))
        conn.commit()

    cursor.execute('SELECT * FROM complaints')
    complaints = cursor.fetchall()
    conn.close()
    return render_template('admin_home.html', complaints=complaints)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        conn = sqlite3.connect('complaints.db')
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO users (username, password, role)
                VALUES (?, ?, ?)
            ''', (username, password, role))
            conn.commit()
            conn.close()
            return redirect('/login')
        except sqlite3.IntegrityError:
            conn.close()
            return "El nombre de usuario ya existe. Intenta con otro."

    return render_template('register.html')


# Servir imágenes desde la carpeta images
@app.route('/images/<path:filename>')
def images(filename):
    return send_from_directory('images', filename)


if __name__ == '__main__':
    app.run(debug=True)
