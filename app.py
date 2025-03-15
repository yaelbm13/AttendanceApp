from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
@app.route("/")
def home():
    return "Welcome to the Attendance App!"

# רשימת הדיירים
tenants = [
    "אורנה", "איילה", "טליה", "שרית", "דורית", "ליאור", "רותי", "מיכל", "מירב", "תמר",
    "מישל", "אילנה", "וורן", "אורן", "יונתן", "יוני", "דביר", "דוד", "נועם", "אודי",
    "שחר", "נתי", "פראג'י", "תומר", "גור"
]

# יצירת מסד נתונים אם לא קיים
def init_db():
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            shift TEXT,
            tenant TEXT,
            present TEXT,
            notes TEXT,
            event TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def attendance():
    if request.method == 'POST':
        date = request.form['date']
        shift = request.form['shift']
        
        conn = sqlite3.connect("attendance.db")
        cursor = conn.cursor()
        
        for tenant in tenants:
            present = request.form.get(f'present_{tenant}', 'לא')
            notes = request.form.get(f'notes_{tenant}', '')
            event = request.form.get(f'event_{tenant}', '')
            
            cursor.execute('''INSERT INTO attendance (date, shift, tenant, present, notes, event)
                              VALUES (?, ?, ?, ?, ?, ?)''', (date, shift, tenant, present, notes, event))
        
        conn.commit()
        conn.close()
        
        return redirect(url_for('attendance'))
    
    today = datetime.today().strftime('%Y-%m-%d')
    return render_template('attendance.html', tenants=tenants, today=today)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# עמוד צפייה בנתונים עם אפשרות סינון
@app.route('/view')
def view():
    date_filter = request.args.get('date', '')
    tenant_filter = request.args.get('tenant', '')

    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()

    query = "SELECT date, shift, tenant, present, notes, event FROM attendance WHERE 1=1"
    params = []

    if date_filter:
        query += " AND date = ?"
        params.append(date_filter)
    
    if tenant_filter:
        query += " AND tenant = ?"
        params.append(tenant_filter)

    cursor.execute(query, params)
    records = cursor.fetchall()
    conn.close()

    tenants = ["אורנה", "איילה", "טליה", "שרית", "דורית", "ליאור", "רותי", "מיכל", "מירב", "תמר", 
               "מישל", "אילנה", "וורן", "אורן", "יונתן", "יוני", "דביר", "דוד", "נועם", "אודי", 
               "שחר", "נתי", "פראג'י", "תומר", "גור"]

    return render_template("view.html", records=records, tenants=tenants)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
