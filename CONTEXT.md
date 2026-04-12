# Middle East Flight Tracker - Context

**Created:** 2026-04-12
**Status:** In Development
**Repository:** Local git repo

---

## Overview

**What it does:**
Web app to monitor Etihad Airways flight reliability during the 2026 Iran-UAE conflict recovery period. Tracks two specific flights (EY461 MEL→AUH and EY111 AUH→BCN) to give passenger Cat visibility on whether her 1 May 2026 flights are operating reliably.

**Original idea:**
Created from prompt in 6-projects/flight_delays/Prompt.md on 2026-04-12

---

## Current State

**Latest version:** Initial build
**Last updated:** 2026-04-12
**Main branch:** main
**Active branches:** None

---

## Technical Details

**Tech stack:**
- React 18 (via CDN, no build step)
- Tailwind CSS (via CDN)
- OpenSky Network REST API
- CORS proxy (corsproxy.io primary, allorigins.win fallback)
- Single HTML file deployment

**Key files:**
- `index.html` - Complete single-page React app
- `Prompt.md` - Original specification
- `CONTEXT.md` - This file

**Architecture notes:**
- Client-side only, no backend required
- Uses functional React with hooks (useState, useEffect, useCallback)
- OpenSky Network API provides flight departure data via ADS-B tracking
- Two-tab interface for two flights (EY461 and EY111)
- Calendar grid shows 30 days past + 19 days future (through May 1, 2026)
- Timezone-aware date parsing (converts UTC to local airport time)
- CORS proxy fallback chain for API access
- Dark mode support via Tailwind

**Key implementation details:**
- Date range: 30 days history + 19 days future
- Callsign matching: ETD461/ETD0461 for EY461, ETD111/ETD0111 for EY111
- Timezone conversion: YMML=UTC+10, OMAA=UTC+4
- API chunking: 7-day max per request to OpenSky
- Cell states: 🟢 Flew, 🔴 No record, 🔵 Scheduled, ⭐ Cat's flight (May 1)
- Summary metrics: flights operated, no records, operating rate percentage
- Conflict timeline: War start (Feb 28), Resume ops (Mar 6), Ceasefire (Apr 8), Cat's flights (May 1-2)

---

## Iteration Log

### 2026-04-12 - Initial Creation

**What was built:**
- Complete single-page React app in index.html
- Two-tab interface for EY461 and EY111
- Calendar grid with 7-column layout (Sun-Sat)
- OpenSky Network API integration with CORS proxy fallback
- Summary statistics bar showing operating rate
- Conflict timeline overlay
- Error handling with retry functionality
- Auto-refresh toggle (30 min intervals)
- Dark mode support
- Mobile responsive layout
- Copy-to-clipboard export functionality
- Disclaimer panel explaining "No record" days

**Approach:**
- Single HTML file for maximum portability
- CDN-based dependencies to avoid build tooling
- Timezone-aware date parsing to correctly assign flights to calendar dates
- CORS proxy chain (corsproxy.io → allorigins.win) for API access
- May 1, 2026 highlighted as Cat's critical flight date
- Operating rate calculated only from past days (flew / (flew + no record))

**Git:**
- Branch: main (initial commit)

---

## Known Issues

- [ ] OpenSky API has rate limits for anonymous access - may need to handle 429 responses
- [ ] ADS-B data gaps possible - not all flights guaranteed to be tracked
- [ ] EY461 operates ~6x weekly, not daily - "no record" days expected
- [ ] CORS proxies can be unreliable - fallback to manual FlightAware check documented

---

## Future Ideas

- Add flight status API for real-time scheduled vs actual comparison
- Historical trend chart showing reliability over time
- Email/SMS alerts for flight status changes
- Additional Etihad routes monitoring
- Export to PDF/image for sharing

---

## Notes for Claude

**When working on this project:**
- This is tracking real flights for a passenger named Cat traveling May 1, 2026
- War context: 2026 Iran-US-Israel conflict, Iran attacked UAE (AUH airport struck Mar 1), ceasefire Apr 8
- Dates are critical - verify timezone conversions (YMML=UTC+10, OMAA=UTC+4)
- OpenSky API is free but rate-limited - handle gracefully
- "No record" does NOT mean cancelled - could be not scheduled, ADS-B gap, or actually cancelled
- Single HTML file requirement - keep everything in index.html

---

*Last updated: 2026-04-12*
