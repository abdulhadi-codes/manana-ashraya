from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            budget TEXT,
            bhk TEXT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return jsonify({'status': 'Manana Ashraya API is running'})

@app.route('/submit-lead', methods=['POST'])
def submit_lead():
    data = request.get_json()
    name = data.get('name')
    phone = data.get('phone')
    email = data.get('email')
    budget = data.get('budget')
    bhk = data.get('bhk')
    message = data.get('message')

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO leads (name, phone, email, budget, bhk, message)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, phone, email, budget, bhk, message))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success', 'message': 'Lead saved successfully'})

@app.route('/get-leads', methods=['GET'])
def get_leads():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM leads ORDER BY created_at DESC')
    leads = cursor.fetchall()
    conn.close()

    leads_list = []
    for lead in leads:
        leads_list.append({
            'id': lead[0],
            'name': lead[1],
            'phone': lead[2],
            'email': lead[3],
            'budget': lead[4],
            'bhk': lead[5],
            'message': lead[6],
            'created_at': lead[7]
        })

    return jsonify(leads_list)

if __name__ == '__main__':
    init_db()
    app.run(debug=True) 
