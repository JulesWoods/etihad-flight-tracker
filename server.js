require('dotenv').config();
const express = require('express');
const cors = require('cors');
const fetch = require('node-fetch');

const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.static('.'));

const FR24_API_TOKEN = process.env.FR24_API_TOKEN;
const FR24_API_URL = 'https://fr24api.flightradar24.com/api/flight-summary/light';

// Endpoint to fetch flights by airport (for map)
app.get('/api/flights/airport', async (req, res) => {
    try {
        const { airport, days = 7 } = req.query;

        if (!airport) {
            return res.status(400).json({
                error: 'Missing required parameter: airport (ICAO code like OMAA)'
            });
        }

        // Calculate date range for last N days
        const endDate = new Date();
        const startDate = new Date();
        startDate.setDate(startDate.getDate() - parseInt(days));

        const dateTimeFrom = startDate.toISOString().split('.')[0];
        const dateTimeTo = endDate.toISOString().split('.')[0];

        console.log(`Fetching FR24 flights for airport ${airport} from ${dateTimeFrom} to ${dateTimeTo}`);

        const params = new URLSearchParams({
            airports: airport,
            flight_datetime_from: dateTimeFrom,
            flight_datetime_to: dateTimeTo,
            limit: 500
        });

        const response = await fetch(`${FR24_API_URL}?${params}`, {
            headers: {
                'Authorization': `Bearer ${FR24_API_TOKEN}`,
                'Accept': 'application/json',
                'Accept-Version': 'v1'
            }
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error(`FR24 API error: ${response.status} ${response.statusText}`, errorText);
            return res.status(response.status).json({
                error: `FR24 API error: ${response.statusText}`,
                details: errorText
            });
        }

        const data = await response.json();
        console.log(`Received ${data?.data?.length || 0} flights for ${airport}`);

        res.json(data);
    } catch (error) {
        console.error('Server error:', error);
        res.status(500).json({
            error: 'Server error',
            message: error.message
        });
    }
});

// Endpoint to fetch flight data from FR24
app.get('/api/flights', async (req, res) => {
    try {
        const { callsign, startDate, endDate } = req.query;

        if (!callsign || !startDate || !endDate) {
            return res.status(400).json({
                error: 'Missing required parameters: callsign, startDate, endDate'
            });
        }

        // Format dates as ISO 8601 with time
        const dateTimeFrom = `${startDate}T00:00:00`;
        const dateTimeTo = `${endDate}T23:59:59`;

        console.log(`Fetching FR24 flight summaries for ${callsign} from ${dateTimeFrom} to ${dateTimeTo}`);

        // Build query with correct parameters for flight summary endpoint
        // Note: Use 'flights' parameter (not 'callsigns'), and API has 14-day max range limit
        const params = new URLSearchParams({
            flights: callsign,
            flight_datetime_from: dateTimeFrom,
            flight_datetime_to: dateTimeTo,
            limit: 500
        });

        const response = await fetch(`${FR24_API_URL}?${params}`, {
            headers: {
                'Authorization': `Bearer ${FR24_API_TOKEN}`,
                'Accept': 'application/json',
                'Accept-Version': 'v1'
            }
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error(`FR24 API error: ${response.status} ${response.statusText}`, errorText);
            return res.status(response.status).json({
                error: `FR24 API error: ${response.statusText}`,
                details: errorText
            });
        }

        const data = await response.json();
        console.log(`Received ${data?.data?.length || 0} records for ${callsign}`);

        res.json(data);
    } catch (error) {
        console.error('Server error:', error);
        res.status(500).json({
            error: 'Server error',
            message: error.message
        });
    }
});

app.listen(PORT, () => {
    console.log(`FR24 proxy server running on http://localhost:${PORT}`);
    console.log(`API token loaded: ${FR24_API_TOKEN ? 'YES' : 'NO'}`);
});
