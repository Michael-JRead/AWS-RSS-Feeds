"""
Handles loading and saving the user configuration to config.json.
All settings (SMTP, recipients, schedule, selected services) live here.
"""

import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

DEFAULT_CONFIG = {
    "smtp": {
        "host": "smtp.gmail.com",
        "port": 587,
        "username": "",
        "password": "",
        "tls": True,
    },
    "recipients": [],
    "subject": "AWS Service Updates — {date}",
    "days_back": 7,
    "selected_services": [],
    "custom_feeds": [],
    "schedule": {
        "enabled": False,
        "frequency": "daily",   # "daily" | "weekly"
        "time": "08:00",        # HH:MM  24-hour local time
        "day_of_week": "monday",
    },
}


def load_config() -> dict:
    """Load config from disk, falling back to defaults for missing keys."""
    if not os.path.exists(CONFIG_PATH):
        return json.loads(json.dumps(DEFAULT_CONFIG))  # deep copy

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        stored = json.load(f)

    # Merge top-level keys so new defaults are respected
    merged = json.loads(json.dumps(DEFAULT_CONFIG))
    for key, value in stored.items():
        if isinstance(value, dict) and key in merged:
            merged[key].update(value)
        else:
            merged[key] = value
    return merged


def save_config(config: dict) -> None:
    """Persist config dict to disk as JSON."""
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)


def update_config(partial: dict) -> dict:
    """Load, merge partial updates, save, and return updated config."""
    config = load_config()
    for key, value in partial.items():
        if isinstance(value, dict) and key in config and isinstance(config[key], dict):
            config[key].update(value)
        else:
            config[key] = value
    save_config(config)
    return config
