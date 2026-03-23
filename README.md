# AWS RSS Feed Digest

A Streamlit application that lets you select AWS services, scrapes their official RSS feeds, and delivers a formatted HTML email digest to any recipients — on demand or on a schedule.

## Features

- **50+ pre-configured AWS services** across Compute, Storage, Database, Networking, Security, ML/AI, DevOps, Analytics, and more
- **Searchable multi-select UI** — type to filter, click to add
- **Category quick-select** — add all services in a category at once
- **Custom RSS feeds** — add any feed URL not in the built-in list
- **HTML email digest** — AWS-branded, grouped by service, with titles, dates, summaries, and links
- **Daily or weekly schedule** — auto-send while the app is running
- **SMTP support** — works with Gmail, Outlook, Yahoo, or any SMTP provider
- **Local config** — all settings (including credentials) stored only on your machine in `config.json`

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the app

```bash
streamlit run app.py
```

The app opens at **http://localhost:8501** in your browser.

### 3. Configure & send

| Tab | What to do |
|-----|-----------|
| 🛠️ Service Selection | Search/select AWS services or add custom feed URLs |
| 📧 Email Recipients | Add recipient addresses, set subject & days-back range |
| 🔑 SMTP Config | Enter your SMTP host, port, and credentials |
| 🕐 Schedule | Enable daily or weekly automatic delivery |
| 🚀 Preview & Send | Fetch a live preview, then click "Send Email Now" |

## Gmail Setup

Gmail requires an **App Password** (not your regular password):

1. Enable **2-Step Verification** on your Google account
2. Go to **Google Account → Security → App Passwords**
3. Create an App Password for "Mail"
4. Use the 16-character password in the SMTP Config tab
5. Settings: Host `smtp.gmail.com`, Port `587`, TLS ✅

## Outlook / Microsoft 365

- Host: `smtp.office365.com`, Port: `587`, TLS ✅
- If MFA is enabled, create an App Password in Microsoft account security settings

## Project Structure

```
├── app.py              # Streamlit UI (5 tabs)
├── aws_services.py     # AWS service → feed URL + keyword registry
├── rss_scraper.py      # RSS fetching, filtering, deduplication
├── email_sender.py     # HTML email builder + SMTP delivery
├── scheduler.py        # APScheduler background scheduling
├── config.py           # config.json load/save helpers
├── requirements.txt
├── .env.example
├── .gitignore
└── config.json         # Created on first run (gitignored — contains credentials)
```

## Feed Sources

The app uses two official AWS feed sources:

- **What's New** — `https://aws.amazon.com/about-aws/whats-new/recent/feed/`
  Fetched once and filtered per-service by keyword matching.

- **AWS Blog feeds** — `https://aws.amazon.com/blogs/{topic}/feed/`
  Per-topic feeds (security, database, machine-learning, devops, etc.)

## Scheduling Notes

The APScheduler background thread runs **inside the Streamlit process**. The schedule is active as long as the app tab is open. For unattended/headless scheduling, consider running `streamlit run app.py --server.headless true` as a background service or scheduled task.
