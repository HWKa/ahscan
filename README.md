# Icecrown AH — Epic Gem Tracker

Twice-daily automated tracker for WotLK epic gem prices on Warmane Icecrown.  
Scrapes [ah.nerfed.net](https://ah.nerfed.net) and generates:
- A **static website** (hosted free on GitHub Pages)
- An **HTML email report** with executive summary

---

## What it tracks

| Gem | Color | Transmute Mats |
|-----|-------|----------------|
| Cardinal Ruby | 🔴 Red | Scarlet Ruby + Eternal Fire |
| King's Amber | 🟡 Yellow | Autumn's Glow + Eternal Life |
| Majestic Zircon | 🔵 Blue | Sky Sapphire + Eternal Air |
| Dreadstone | 🟣 Purple | Twilight Opal + Eternal Shadow |
| Ametrine | 🟠 Orange | Monarch Topaz + Eternal Shadow |
| Eye of Zul | 🟢 Green | 3× Forest Emerald |

For each gem: all cuts sorted by profit, transmute ROI, side-by-side Horde vs Alliance.

---

## Setup (one-time, ~10 minutes)

### 1. Create GitHub repository

1. Go to github.com → New repository
2. Name it e.g. `ah-tracker`
3. Set to **Public** (required for free GitHub Pages)
4. Push this code:
```bash
git init
git add .
git commit -m "initial"
git remote add origin https://github.com/YOURUSERNAME/ah-tracker.git
git push -u origin main
```

### 2. Enable GitHub Pages

Go to repo **Settings → Pages → Source → GitHub Actions** (or set to `docs/` folder on `main` branch).

### 3. Set up email (Gmail App Password)

1. Go to your Google Account → Security → 2-Step Verification (must be on)
2. Search "App passwords" → create one named "AH Tracker"
3. Copy the 16-character password

In your GitHub repo: **Settings → Secrets and variables → Actions → New repository secret**

| Secret name | Value |
|-------------|-------|
| `SMTP_USER` | your.email@gmail.com |
| `SMTP_PASSWORD` | your 16-char app password |
| `REPORT_EMAIL` | where to send the report (can be same address) |

### 4. That's it

The workflow runs automatically at **07:00 UTC** and **19:00 UTC** daily.  
You can also trigger it manually from the **Actions** tab → Run workflow.

Your website will be at: `https://YOURUSERNAME.github.io/ah-tracker/`

---

## Local usage

```bash
pip install -r requirements.txt

# Full run (generates docs/index.html + sends email if env vars set)
python main.py

# HTML only, no email
python main.py --html-only

# Dry run (console output only)
python main.py --dry-run
```

---

## File structure

```
├── main.py           # Entry point
├── items.py          # All item IDs and transmute recipes
├── scraper.py        # Fetches prices from ah.nerfed.net
├── analysis.py       # Profit calculations and executive summary
├── render_html.py    # Generates docs/index.html
├── render_email.py   # Generates HTML email body
├── mailer.py         # Sends via Gmail SMTP
├── requirements.txt
├── docs/
│   └── index.html    # Generated — served by GitHub Pages
└── .github/
    └── workflows/
        └── update.yml  # GitHub Actions cron job
```

---

## Notes

- All prices are **median buyout** in copper (most stable metric)
- Transmute margin = epic gem median buyout − sum of mat median buyouts
- "Profit vs raw" = cut price − raw uncut gem price
- "Profit vs transmute" = cut price − transmute cost (most relevant if you're an alchemist)
- Data refreshes every ~6 hours on nerfed.net; running this 2×/day is well within that cadence
