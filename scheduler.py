"""
Background scheduling via APScheduler.

The scheduler runs inside the Streamlit process. On app startup, if a
schedule is saved and enabled in config.json, it starts the background job
automatically.

Usage from app.py:
    from scheduler import get_scheduler, start_scheduler, stop_scheduler
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

log = logging.getLogger(__name__)

_scheduler: BackgroundScheduler | None = None
_JOB_ID = "aws_digest_job"


# ---------------------------------------------------------------------------
# Scheduled job callable
# ---------------------------------------------------------------------------

def _run_job() -> None:
    """
    Executed on schedule: load config, scrape feeds, send email.
    Runs in the APScheduler thread pool — keep imports local to avoid
    Streamlit session-state access.
    """
    try:
        from config import load_config
        from rss_scraper import scrape_services
        from email_sender import build_html_email, send_email, build_subject

        cfg = load_config()

        selected = cfg.get("selected_services", [])
        custom = cfg.get("custom_feeds", [])
        days_back = cfg.get("days_back", 7)
        recipients = cfg.get("recipients", [])
        smtp = cfg.get("smtp", {})
        subject_template = cfg.get("subject", "AWS Service Updates — {date}")

        if not selected and not custom:
            log.warning("Scheduled job: no services selected, skipping.")
            return
        if not recipients:
            log.warning("Scheduled job: no recipients configured, skipping.")
            return

        results = scrape_services(selected, custom, days_back)
        html = build_html_email(results, days_back)
        subject = build_subject(subject_template)
        send_email(html, recipients, subject, smtp)
        log.info("Scheduled digest sent to %s recipient(s) at %s UTC",
                 len(recipients), datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"))
    except Exception:
        log.exception("Scheduled job failed")


# ---------------------------------------------------------------------------
# Scheduler lifecycle
# ---------------------------------------------------------------------------

def get_scheduler() -> BackgroundScheduler:
    global _scheduler
    if _scheduler is None:
        _scheduler = BackgroundScheduler(timezone="UTC", job_defaults={"misfire_grace_time": 300})
    return _scheduler


def start_scheduler() -> None:
    sched = get_scheduler()
    if not sched.running:
        sched.start()
        log.info("APScheduler started.")


def stop_scheduler() -> None:
    global _scheduler
    if _scheduler and _scheduler.running:
        _scheduler.shutdown(wait=False)
        log.info("APScheduler stopped.")
    _scheduler = None


# ---------------------------------------------------------------------------
# Schedule management
# ---------------------------------------------------------------------------

def _make_trigger(schedule_cfg: dict) -> CronTrigger:
    """Build an APScheduler CronTrigger from a schedule config dict."""
    time_str = schedule_cfg.get("time", "08:00")
    hour, minute = (int(p) for p in time_str.split(":"))

    if schedule_cfg.get("frequency") == "weekly":
        day_map = {
            "monday": "mon", "tuesday": "tue", "wednesday": "wed",
            "thursday": "thu", "friday": "fri", "saturday": "sat", "sunday": "sun",
        }
        dow = day_map.get(schedule_cfg.get("day_of_week", "monday").lower(), "mon")
        return CronTrigger(day_of_week=dow, hour=hour, minute=minute)
    else:
        # daily
        return CronTrigger(hour=hour, minute=minute)


def apply_schedule(schedule_cfg: dict) -> str | None:
    """
    Add or replace the scheduled job based on config.
    Returns the next run time as a string, or None if disabled.
    """
    sched = get_scheduler()
    start_scheduler()

    # Remove existing job if present
    if sched.get_job(_JOB_ID):
        sched.remove_job(_JOB_ID)

    if not schedule_cfg.get("enabled", False):
        return None

    trigger = _make_trigger(schedule_cfg)
    job = sched.add_job(_run_job, trigger=trigger, id=_JOB_ID, replace_existing=True)
    next_run = job.next_run_time
    if next_run:
        return next_run.strftime("%Y-%m-%d %H:%M %Z")
    return "scheduled"


def get_next_run() -> str | None:
    """Return the next scheduled run time string, or None."""
    sched = get_scheduler()
    if not sched.running:
        return None
    job = sched.get_job(_JOB_ID)
    if job and job.next_run_time:
        return job.next_run_time.strftime("%Y-%m-%d %H:%M %Z")
    return None


def remove_schedule() -> None:
    """Remove the scheduled job (keeps scheduler running)."""
    sched = get_scheduler()
    if sched.running and sched.get_job(_JOB_ID):
        sched.remove_job(_JOB_ID)
