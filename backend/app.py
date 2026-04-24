from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

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

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO leads (name, phone, email, budget, bhk, message)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (name, phone, email, budget, bhk, message))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'status': 'success', 'message': 'Lead saved successfully'})

@app.route('/get-leads', methods=['GET'])
def get_leads():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM leads ORDER BY created_at DESC')
    leads = cursor.fetchall()
    cursor.close()
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
            'created_at': str(lead[7])
        })

    return jsonify(leads_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)