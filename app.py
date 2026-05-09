from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('hotel.db')
    conn.row_factory = sqlite3.Row # Allows accessing columns by name
    return conn

# Initialize Database with prices and descriptions for guests
def init_db():
    db = get_db()
    db.execute('''CREATE TABLE IF NOT EXISTS rooms 
                 (id INTEGER PRIMARY KEY, 
                  room_num TEXT, 
                  type TEXT, 
                  price INTEGER, 
                  status TEXT, 
                  guest_name TEXT)''')
    
    # Check if empty, then add sample data
    if not db.execute("SELECT * FROM rooms").fetchone():
        rooms = [
            ('101', 'Deluxe Suite', 2500, 'Available', ''),
            ('102', 'Standard Room', 1200, 'Available', ''),
            ('103', 'Family Loft', 3500, 'Occupied', 'John Doe')
        ]
        db.executemany("INSERT INTO rooms (room_num, type, price, status, guest_name) VALUES (?,?,?,?,?)", rooms)
        db.commit()
    db.close()

@app.route('/')
def public_home():
    db = get_db()
    # Guests only care about what is available or how it looks
    rooms = db.execute("SELECT * FROM rooms").fetchall()
    db.close()
    return render_template('index.html', rooms=rooms)

@app.route('/admin')
def admin_dashboard():
    db = get_db()
    rooms = db.execute("SELECT * FROM rooms").fetchall()
    db.close()
    return render_template('admin.html', rooms=rooms)

@app.route('/update_room/<int:id>', methods=['POST'])
def update_room(id):
    new_status = request.form.get('status')
    guest = request.form.get('guest_name')
    
    db = get_db()
    db.execute("UPDATE rooms SET status=?, guest_name=? WHERE id=?", (new_status, guest, id))
    db.commit()
    db.close()
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
