from flask import Flask, render_template, request, jsonify
from .simulation import simulate_projectile

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.get_json()
    x, y = data['x'], data['y']
    result = simulate_projectile(x, y)
    if result is None:
        return jsonify({'error': 'No valid solution'}), 400
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
