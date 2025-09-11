from flask import Flask, request, jsonify
from varsha.simulation import simulate_projectile

app = Flask(__name__)

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.get_json()
    x = data.get('x')
    y = data.get('y')

    if x is None or y is None:
        return jsonify({'error': 'Missing x or y in request body'}), 400

    result = simulate_projectile(x, y)
    
    if result is None:
        return jsonify({'error': 'No valid solution'}), 400

    return jsonify(result)

def handler(environ, start_response):
    from werkzeug.wrappers import Request, Response
    request = Request(environ)
    response = app.full_dispatch_request()
    return response(environ, start_response)
