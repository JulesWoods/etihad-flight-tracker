#!/usr/bin/env python3
"""
Simple CORS proxy server for OpenSky Network API
Run: python3 proxy.py
Optional: Set OPENSKY_USER and OPENSKY_PASS environment variables for authentication
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import sys
import os

app = Flask(__name__)
CORS(app)

OPENSKY_BASE = "https://opensky-network.org/api"
OPENSKY_USER = os.environ.get('OPENSKY_USER')
OPENSKY_PASS = os.environ.get('OPENSKY_PASS')

@app.route('/flights/departure')
def proxy_flights():
    """Proxy requests to OpenSky Network API"""
    airport = request.args.get('airport')
    begin = request.args.get('begin')
    end = request.args.get('end')

    if not all([airport, begin, end]):
        return jsonify({"error": "Missing required parameters"}), 400

    url = f"{OPENSKY_BASE}/flights/departure"
    params = {
        'airport': airport,
        'begin': begin,
        'end': end
    }

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
        }

        # Add authentication if credentials are provided
        auth = None
        if OPENSKY_USER and OPENSKY_PASS:
            auth = (OPENSKY_USER, OPENSKY_PASS)
            print(f"Using authenticated request for {airport}")

        response = requests.get(url, params=params, headers=headers, auth=auth, timeout=30)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        error_msg = str(e)
        if '403' in error_msg:
            error_msg += " - OpenSky requires authentication. Create free account at https://opensky-network.org and set OPENSKY_USER and OPENSKY_PASS environment variables"
        return jsonify({"error": error_msg}), 500

if __name__ == '__main__':
    try:
        import flask_cors
    except ImportError:
        print("Error: flask-cors not installed")
        print("Run: pip3 install flask flask-cors requests")
        sys.exit(1)

    print("Starting proxy server on http://localhost:5000")
    print("Press Ctrl+C to stop")
    app.run(port=5000, debug=False)
