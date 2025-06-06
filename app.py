from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime
import pytz

app = Flask(__name__)
CORS(app)

DATA_FILE = 'history.json'
TZ = pytz.timezone('Asia/Ho_Chi_Minh')

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/api/history', methods=['GET', 'POST'])
def history():
    if request.method == 'POST':
        data = request.json
        data['time'] = datetime.now(TZ).strftime("%I:%M:%S %p")
        history = load_history()
        history.insert(0, data)
        history = history[:30]
        with open(DATA_FILE, 'w') as f:
            json.dump(history, f, ensure_ascii=False)
        return jsonify(success=True)
    else:
        return jsonify(load_history())

def load_history():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

@app.route('/api/ping')
def ping():
    return jsonify(status='ok')

if __name__ == '__main__':
    app.run(debug=True)
