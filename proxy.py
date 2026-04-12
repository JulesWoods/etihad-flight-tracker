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
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import re

app = Flask(__name__)
CORS(app)

OPENSKY_BASE = "https://opensky-network.org/api"
OPENSKY_USER = os.environ.get('OPENSKY_USER')
OPENSKY_PASS = os.environ.get('OPENSKY_PASS')

AVIATIONSTACK_KEY = "8e092a48cae2106ab1d4880d426cffc0"
AVIATIONSTACK_BASE = "http://api.aviationstack.com/v1"

@app.route('/aviationstack/flights')
def aviationstack_flights():
    """Get flight data from AviationStack"""
    flight_iata = request.args.get('flight_iata')  # e.g., "EY461"
    flight_date = request.args.get('flight_date')  # Optional YYYY-MM-DD

    if not flight_iata:
        return jsonify({"error": "Missing flight_iata parameter"}), 400

    try:
        # Note: Free tier only supports current/future flights
        # Historical data requires paid plan
        url = f"{AVIATIONSTACK_BASE}/flights"
        params = {
            'access_key': AVIATIONSTACK_KEY,
            'flight_iata': flight_iata,
            'limit': 100
        }

        if flight_date:
            params['flight_date'] = flight_date

        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        # Convert to format expected by frontend
        flights = []
        if 'data' in data:
            for flight in data['data']:
                if flight.get('departure'):
                    dep = flight['departure']
                    flights.append({
                        'date': flight.get('flight_date'),
                        'time': dep.get('actual') or dep.get('scheduled'),
                        'origin': dep.get('iata'),
                        'destination': flight.get('arrival', {}).get('iata'),
                        'status': 'flew' if dep.get('actual') else 'scheduled'
                    })

        return jsonify({'flights': flights, 'raw': data})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/flightaware/history')
def flightaware_history():
    """Scrape FlightAware for flight history"""
    flight_number = request.args.get('flight')  # e.g., "ETD461"
    days = int(request.args.get('days', 30))

    if not flight_number:
        return jsonify({"error": "Missing flight parameter"}), 400

    flights = []

    try:
        # FlightAware flight history page
        url = f"https://flightaware.com/live/flight/{flight_number}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Look for flight history data in the page
        # FlightAware shows recent flights in a table
        # This is a simplified scraper - may need adjustment based on actual page structure

        # Try to find JSON data embedded in page
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string and 'trackpollBootstrap' in script.string:
                # Extract flight data from the bootstrap JSON
                import json
                match = re.search(r'trackpollBootstrap\s*=\s*({.*?});', script.string, re.DOTALL)
                if match:
                    try:
                        data = json.loads(match.group(1))
                        if 'flights' in data:
                            for flight in data['flights']:
                                flights.append({
                                    'date': flight.get('filed_departuretime'),
                                    'origin': flight.get('origin'),
                                    'destination': flight.get('destination'),
                                    'status': flight.get('status')
                                })
                    except:
                        pass

        return jsonify(flights)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
