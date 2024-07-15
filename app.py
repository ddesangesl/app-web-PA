from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from prediction import get_prediction


app = Flask(__name__)
CORS(app)


@app.route('/api/get_prediction', methods=['POST'])
def get_winner():
    data = request.json
    home_team = data.get('num1')
    away_team = data.get('num2')
    winner = get_prediction(home_team, away_team)
    return jsonify({'result': winner})

@app.route('/')
def serve_index():
    return send_from_directory('.', 'prediction.html')

@app.route('/test')
def serve_test():
    return send_from_directory('.', 'ancienne-prediction.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    app.run(host="0.0.0.0")

