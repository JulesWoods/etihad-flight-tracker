# Middle East Flight Tracker

Web app to monitor Etihad Airways flight reliability during the 2026 Iran-UAE conflict recovery period.

## Quick Start

1. Open `index.html` in a web browser
2. Select tab for flight to track:
   - EY461: Melbourne → Abu Dhabi
   - EY111: Abu Dhabi → Barcelona
3. View calendar showing flight history and scheduled future dates

## Purpose

Tracks whether Etihad flights EY461 and EY111 are operating reliably ahead of passenger Cat's May 1, 2026 travel date.

## Context

- **War began:** Feb 28, 2026 (Iran-US-Israel conflict)
- **AUH airport struck:** Mar 1, 2026
- **Etihad resumed ops:** Mar 6, 2026
- **Ceasefire began:** Apr 8, 2026
- **Cat's flights:** May 1 (EY461) and May 2 (EY111)

## Features

- 30-day flight history + 19-day future view
- Real-time ADS-B data from OpenSky Network
- Operating rate statistics
- Conflict timeline overlay
- Auto-refresh option
- Dark mode support
- Mobile responsive
- Copy-to-clipboard export

## Data Source

OpenSky Network REST API (free, anonymous access)

## Tech Stack

- React 18 (CDN)
- Tailwind CSS (CDN)
- Single HTML file, no build required

## Notes

- "No record" days may indicate: flight cancelled, not scheduled that day, or ADS-B data gap
- EY461 operates ~6x weekly, not daily
- Cross-reference with FlightAware or Flightradar24 for confirmation
