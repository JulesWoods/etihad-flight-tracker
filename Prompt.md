Here's the full detailed prompt:

---

Build a **Middle East Flight Tracker** web app to monitor Etihad Airways flight reliability during the 2026 Iran-UAE conflict recovery period.

---

## Background context

The 2026 Iran-US-Israel war began 28 February 2026. Iran fired 438+ ballistic missiles and 2,000+ drones at the UAE over 42 days, directly striking Abu Dhabi's Zayed International Airport (AUH) on 1 March. A 2-week ceasefire took effect 8 April 2026. Etihad suspended all flights from 28 Feb, resumed limited operations 6 March, and is currently running ~97 daily departures to ~80 destinations as of 11 April 2026. The purpose of this app is to give a passenger (Cat) visibility on whether her specific Etihad flights are operating reliably ahead of her 1 May 2026 travel date: MEL→AUH (EY461) then AUH→BCN (EY111).

---

## Data source

**OpenSky Network REST API** — free, no auth required for anonymous access.

Base URL: `https://opensky-network.org/api`

Endpoint: `GET /flights/departure?airport={icao}&begin={unix}&end={unix}`

- Returns array of flight objects with fields: `callsign`, `firstSeen`, `lastSeen`, `estDepartureAirport`, `estArrivalAirport`
- Max 7 days per query — must chunk requests
- **CORS blocked** — must route through proxy. Try in order:
    1. `https://corsproxy.io/?{encodedUrl}`
    2. `https://api.allorigins.win/raw?url={encodedUrl}`
    3. Show error with manual fallback instructions if both fail

---

## Flights to track

|Tab|Flight|Callsign|Origin ICAO|Dest ICAO|Typical dep time|
|---|---|---|---|---|---|
|1|EY461|ETD461|YMML (Melbourne)|OMAA (Abu Dhabi)|17:10 AEST (UTC+10)|
|2|EY111|ETD111|OMAA (Abu Dhabi)|LEBL (Barcelona)|02:10 GST (UTC+4)|

Match callsigns: `ETD461`, `ETD0461` for EY461. `ETD111`, `ETD0111` for EY111.

When parsing departure timestamps, convert UTC unix time to **local airport time** before assigning to a calendar date:

- YMML = UTC+10 (AEST, no DST in May)
- OMAA = UTC+4 (GST, no DST)

---

## Date range

- Past **30 days** of history
- Next **19 days** of future (covers up to 1 May 2026 — Cat's flight date)
- Highlight 1 May 2026 prominently as "Cat's flight"

---

## Calendar grid UI

- 7-column grid (Sun–Sat headers)
- Pad start to correct weekday
- Each cell shows: date number, month abbr, status label, departure time if available
- Cell states:
    - 🟢 **Flew** — found in ADS-B data, show actual departure time
    - 🔴 **No record** — past day, not in ADS-B (may be cancelled or not scheduled)
    - 🔵 **Scheduled** — future date
    - ⚫ **Gap day** — empty padding cell
    - ⭐ **Cat's flight** — 1 May 2026, special highlight ring/badge

---

## Summary bar

Show above calendar:

- `✓ X flew` (green)
- `✗ X no record` (red)
- `◉ X scheduled` (blue)
- `📅 Operating rate: X%` (flew / (flew + no record) × 100, past days only)

---

## Conflict timeline overlay

Below the calendar, show a compact horizontal timeline bar:

- 28 Feb — War begins / Etihad suspends
- 6 Mar — Etihad resumes limited ops
- 8 Apr — Ceasefire begins
- 1 May — Cat's flight (EY461)
- 2 May — Cat's connection (EY111)

---

## Error handling

- Loading spinner while fetching
- If proxy fails: show message "OpenSky unreachable — check manually at flightaware.com/live/flight/ETD461"
- If data returns 0 results: warn "No flights found — may be API rate limit, try again in 60 seconds"
- Auto-retry button

---

## Disclaimer panel

Show clearly below calendar:

> ⚠️ "No record" days may mean: (1) flight was cancelled, (2) flight not scheduled that day — EY461 operates ~6x weekly, not daily, (3) ADS-B transponder data gap. Cross-reference with Flightradar24 or FlightAware for confirmation. War began 28 Feb 2026 — all red days before that date are expected.

---

## Tech stack

- **React** (hooks only — useState, useEffect, useCallback)
- **Tailwind CSS** (CDN)
- Single `index.html` file, no build step required
- No backend — all API calls client-side via CORS proxy

---

## Additional features

- **Auto-refresh toggle** — re-fetch every 30 minutes
- **Last updated** timestamp shown in header
- Dark mode support via Tailwind dark: classes
- Mobile responsive — calendar cells shrink gracefully on small screens
- Copy-to-clipboard button that exports the calendar as plain text summary

---
