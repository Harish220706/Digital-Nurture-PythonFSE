"""
API Gateway - single entry point (port 5000) that proxies requests to the
correct backend service based on the URL prefix.
"""
from flask import Flask, request, Response
import requests

app = Flask(__name__)

SERVICE_MAP = {
    'courses': 'http://localhost:5001',
    'students': 'http://localhost:5002',
}


@app.route('/api/<resource>', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/api/<resource>/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(resource, path):
    base_url = SERVICE_MAP.get(resource)
    if base_url is None:
        return {'error': f'No service registered for /api/{resource}'}, 404

    target_url = f'{base_url}/api/{resource}/{path}'
    try:
        upstream = requests.request(
            method=request.method,
            url=target_url,
            headers={k: v for k, v in request.headers if k.lower() != 'host'},
            json=request.get_json(silent=True),
            params=request.args,
            timeout=5,
        )
    except requests.exceptions.ConnectionError:
        return {'error': f'{resource} service unavailable'}, 503

    return Response(upstream.content, status=upstream.status_code, content_type=upstream.headers.get('Content-Type'))


if __name__ == '__main__':
    app.run(port=5000, debug=True)
