from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import os
from config import Config
from database import get_db_connection

app = Flask(__name__)
app.config.from_object(Config)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    if 'user_id' in session:
        if session['role'] == 'teacher':
            return redirect(url_for('teacher_dashboard'))
        else:
            return redirect(url_for('student_dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        conn = get_db_connection()
        if not conn:
            flash('Database connection failed.', 'error')
            return redirect(url_for('login'))

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s AND role = %s", (username, role))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            session['name'] = user['name']
            
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

def fetch_student_data(student_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get user info
    cursor.execute("SELECT name FROM users WHERE id = %s", (student_id,))
    user_info = cursor.fetchone()
    
    # Get marks
    cursor.execute("SELECT subject, internal_marks, external_marks FROM marks WHERE student_id = %s", (student_id,))
    marks = cursor.fetchall()
    
    total_obtained = sum(m['internal_marks'] + m['external_marks'] for m in marks)
    max_total = len(marks) * 100
    total_percentage = round((total_obtained / max_total * 100), 2) if max_total > 0 else 0
    
    # Get certificates
    cursor.execute("SELECT category, points FROM certificates WHERE student_id = %s", (student_id,))
    certificates = cursor.fetchall()
    total_points = sum(c['points'] for c in certificates)
    
    # Get ratings
    cursor.execute("SELECT rating, remarks FROM performance WHERE student_id = %s ORDER BY id DESC LIMIT 1", (student_id,))
    perf = cursor.fetchone()
    performance_rating = perf['rating'] if perf else 0
    remarks = perf['remarks'] if perf else "No remarks yet."
    
    cursor.close()
    conn.close()
    return {
        'name': user_info['name'] if user_info else 'Student',
        'marks': marks,
        'total_percentage': total_percentage,
        'certificates': certificates,
        'total_points': total_points,
        'performance_rating': performance_rating,
        'remarks': remarks
    }

@app.route('/student_dashboard')
def student_dashboard():
    if 'user_id' not in session or session['role'] != 'student':
        return redirect(url_for('login'))
        
    data = fetch_student_data(session['user_id'])
    # Need to override name because session['name'] is used in template directly. 
    # The template references session['name'], so teacher viewing it will see teacher's name.
    # Let's override it in the template variable context but adjust template or just use flashed messages.
    return render_template('student_dashboard.html', **data)

@app.route('/certificate_upload', methods=['GET', 'POST'])
def certificate_upload():
    if 'user_id' not in session or session['role'] != 'student':
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        category = request.form['category']
        file = request.files['file']
        
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Points logic: 10 points for games, 5 points for extra activities
            points = 10 if category == 'games' else 5
            
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO certificates (student_id, category, file_path, points) VALUES (%s, %s, %s, %s)",
                           (session['user_id'], category, filename, points))
            conn.commit()
            cursor.close()
            conn.close()
            
            flash('Certificate uploaded successfully!', 'success')
            return redirect(url_for('student_dashboard'))
            
    return render_template('certificate_upload.html')

@app.route('/teacher_dashboard')
def teacher_dashboard():
    if 'user_id' not in session or session['role'] != 'teacher':
        return redirect(url_for('login'))
        
    class_name = request.args.get('class_name')
    semester = request.args.get('semester')
    students = []
    
    if class_name and semester:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT u.id, u.name, s.class_name, s.semester 
            FROM users u
            JOIN students s ON u.id = s.id
            WHERE s.class_name = %s AND s.semester = %s
        """
        cursor.execute(query, (class_name, int(semester)))
        students = cursor.fetchall()
        cursor.close()
        conn.close()

    return render_template('teacher_dashboard.html', students=students)

@app.route('/marks_entry/<int:student_id>', methods=['GET', 'POST'])
def marks_entry(student_id):
    if 'user_id' not in session or session['role'] != 'teacher':
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        subject = request.form['subject']
        int_marks = request.form['internal_marks']
        ext_marks = request.form['external_marks']
        rating = request.form['rating']
        remarks = request.form['remarks']
        
        # Determine current semester for the student to record marks properly
        cursor.execute("SELECT semester FROM students WHERE id = %s", (student_id,))
        stu = cursor.fetchone()
        sem = stu['semester'] if stu else 1
        
        cursor.execute("""
            INSERT INTO marks (student_id, subject, internal_marks, external_marks, semester) 
            VALUES (%s, %s, %s, %s, %s)
        """, (student_id, subject, int_marks, ext_marks, sem))
        
        cursor.execute("""
            INSERT INTO performance (student_id, teacher_id, rating, remarks) 
            VALUES (%s, %s, %s, %s)
        """, (student_id, session['user_id'], rating, remarks))
        
        conn.commit()
        flash('Evaluation saved successfully!', 'success')
        return redirect(url_for('teacher_dashboard'))
        
    cursor.execute("SELECT u.name, s.class_name FROM users u JOIN students s ON u.id = s.id WHERE u.id = %s", (student_id,))
    student = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return render_template('marks_entry.html', student=student)

@app.route('/student_view/<int:student_id>')
def student_view(student_id):
    if 'user_id' not in session or session['role'] != 'teacher':
        return redirect(url_for('login'))
        
    data = fetch_student_data(student_id)
    return render_template('student_dashboard.html', **data)

if __name__ == '__main__':
    app.run(debug=True)
