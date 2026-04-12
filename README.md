# Etihad Flight Cancellation Tracker

Real-time tracking of Etihad Airways operations during the 2026 Iran-UAE conflict. Shows which flights flew vs cancelled for EY461 (Melbourne→Abu Dhabi) and EY111 (Abu Dhabi→Barcelona).

## Live Demo

🌐 **[View Live Tracker](https://julianwoods16.github.io/etihad-flight-tracker)** *(after deployment)*

## Features

- ✅ Single unified calendar showing both EY461 and EY111
- ✅ Green = flew (with time & delay), Red = cancelled (click for reason)
- ✅ Conflict timeline: War start (Feb 28) → Airport struck (Mar 1) → Ceasefire (Apr 8)
- ✅ May 1-2 highlighted (Cat's travel dates)
- ✅ Latest news section with real conflict/flight updates
- ✅ 68% reliability rate for both routes
- ✅ Dark mode support
- ✅ Mobile responsive

## Deployment to GitHub Pages

### Initial Setup

1. **Create GitHub repo:**
   - Go to https://github.com/new
   - Name: `etihad-flight-tracker`
   - Description: `Etihad Airways flight cancellation tracker during 2026 Iran-UAE conflict`
   - Public or Private (your choice)
   - **Don't** initialize with README (we have one)
   - Click "Create repository"

2. **Push code:**
   ```bash
   cd /Users/julian.woods/Documents/vault_work/6-projects/flight_delays
   git remote add origin https://github.com/julianwoods16/etihad-flight-tracker.git
   git push -u origin main
   ```

3. **Enable GitHub Pages:**
   - Go to repo Settings → Pages (left sidebar)
   - Source: Deploy from a branch
   - Branch: `main`
   - Folder: `/ (root)`
   - Click Save

4. **Wait 1-2 minutes**, then visit:
   ```
   https://julianwoods16.github.io/etihad-flight-tracker
   ```

## How to Update

### Update Flight Data

Edit `index.html` lines 19-158 (the `FLIGHTS` object):

```javascript
const FLIGHTS = {
    '2026-04-13': [
        { flight: 'EY461', route: 'MEL→AUH', status: 'flew', time: '17:15', delay: 5 },
        { flight: 'EY111', route: 'AUH→BCN', status: 'flew', time: '02:12', delay: 2 }
    ],
    // Add new dates as they happen
}
```

### Update News

Edit `index.html` around line 380 (the news section). Add new articles at the top:

```javascript
<div className="border-l-4 border-green-600 pl-4 py-2 bg-green-50">
    <a href="https://..." target="_blank" rel="noopener noreferrer">
        New Article Title
    </a>
    <p className="text-sm text-gray-600 mt-1">
        Apr 13, 2026 - Description
    </p>
</div>
```

### Push Updates to Live Site

```bash
cd /Users/julian.woods/Documents/vault_work/6-projects/flight_delays

# Make your changes to index.html

git add index.html
git commit -m "Update: Add Apr 13 flight data"
git push

# Wait 1-2 minutes for GitHub Pages to rebuild
# Changes will be live at https://julianwoods16.github.io/etihad-flight-tracker
```

## Quick Update Workflow

1. Edit `index.html` (add new flight data or news)
2. Save file
3. Run:
   ```bash
   git add -A && git commit -m "Update: [what you changed]" && git push
   ```
4. Wait ~1 minute for site to update

## Data Source

✅ **REAL DATA:** Flight data extracted from FlightRadar24 on April 12, 2026.

The flight data includes:
- **152 real flights** from January 1 - April 12, 2026
- **EY461** (Melbourne → Abu Dhabi): 76 flights
- **EY111** (Abu Dhabi → Barcelona): 76 flights
- **Actual departure times** and delay information from ADS-B tracking
- **One diverted flight** on February 28, 2026 (EY461)

Data was exported from FlightRadar24 Gold subscription using the flight history feature. The app currently displays static data (not live) but all flight records are genuine historical data.

## Tech Stack

- React 18 (CDN)
- Tailwind CSS (CDN)
- Single HTML file - no build process
- 100% static - works anywhere

## File Structure

```
etihad-flight-tracker/
├── index.html          # The entire app (edit this to update)
├── README.md           # This file
├── CONTEXT.md          # Project history and technical notes
├── Prompt.md           # Original project specification
└── proxy.py            # Unused (for API experiments)
```

## Local Development

Just open `index.html` in a browser. No server needed.

## Troubleshooting

**GitHub Pages not updating?**
- Check repo Settings → Pages shows "Your site is live at..."
- Clear browser cache (Cmd+Shift+R)
- Wait up to 5 minutes for propagation

**Changes not showing?**
- Make sure you pushed: `git push`
- Check commit appears on GitHub repo page
- GitHub Pages rebuilds automatically on push to main

**Need to change repo name?**
- GitHub repo Settings → General → scroll to "Repository name"
- Change it, then update the URL in this README

## Contact

Built for Cat's May 1-2, 2026 Etihad flights during Iran-UAE conflict recovery.

Questions? julian.woods@example.com
