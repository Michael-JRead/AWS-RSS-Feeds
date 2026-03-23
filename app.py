"""
AWS RSS Feed Scraper & Email Digest
===================================
Run with:  streamlit run app.py
"""

from __future__ import annotations

import re
import streamlit as st

from aws_services import AWS_SERVICES, CATEGORIES, SERVICE_NAMES
from config import load_config, save_config, update_config
from rss_scraper import scrape_services, total_item_count
from email_sender import build_html_email, send_email, build_subject, test_smtp_connection, open_in_outlook, build_teams_message
from scheduler import apply_schedule, get_next_run, start_scheduler, get_scheduler

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="AWS RSS Digest",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Startup: initialise scheduler if a schedule is saved
# ---------------------------------------------------------------------------
if "scheduler_started" not in st.session_state:
    cfg = load_config()
    sched_cfg = cfg.get("schedule", {})
    if sched_cfg.get("enabled", False):
        start_scheduler()
        apply_schedule(sched_cfg)
    st.session_state["scheduler_started"] = True

# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------
CSS_BLOCK = """<style>
.block-container { padding-top:1rem; max-width:1100px; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { gap:4px; border-bottom:2px solid #232f3e; }
.stTabs [data-baseweb="tab"] { height:46px; padding:0 22px; font-weight:600; font-size:14px; border-radius:6px 6px 0 0; color:#555; }
.stTabs [aria-selected="true"] { background:#232f3e !important; color:#ff9900 !important; }

/* Progress stepper */
.stepper-wrap { display:flex; align-items:center; justify-content:center; padding:14px 0 18px; gap:0; }
.step-item { display:flex; flex-direction:column; align-items:center; min-width:110px; }
.step-circle { width:34px; height:34px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:700; border:2px solid #dee2e6; background:#f8f9fa; color:#999; }
.step-circle.done   { background:#28a745; border-color:#28a745; color:white; }
.step-circle.active { background:#ff9900; border-color:#ff9900; color:white; }
.step-label { font-size:11px; margin-top:5px; color:#777; font-weight:500; text-align:center; }
.step-label.done   { color:#28a745; font-weight:600; }
.step-label.active { color:#ff9900; font-weight:700; }
.step-connector { flex:1; height:2px; background:#dee2e6; margin-top:-20px; min-width:30px; max-width:80px; }
.step-connector.done { background:#28a745; }

/* Service chips */
.chip-wrap { display:flex; flex-wrap:wrap; gap:6px; margin:8px 0; }
.chip        { background:#ff9900; color:white; padding:3px 12px; border-radius:14px; font-size:12px; font-weight:600; }
.chip-custom { background:#232f3e; color:#ff9900; padding:3px 12px; border-radius:14px; font-size:11px; font-weight:500; }

/* Method cards */
.method-card { border:2px solid #dee2e6; border-radius:10px; padding:20px; background:white; margin-bottom:8px; }
.method-card.selected { border-color:#ff9900; background:#fffdf7; }
.method-card-icon { font-size:28px; margin-bottom:6px; }
.method-card-title { font-size:16px; font-weight:700; color:#232f3e; margin-bottom:4px; }
.method-card-desc  { font-size:13px; color:#666; }
.method-card-tag   { display:inline-block; background:#e8f5e9; color:#2e7d32; font-size:11px; font-weight:600; padding:2px 8px; border-radius:8px; margin-top:8px; }
.method-card-tag.warn { background:#fff3e0; color:#e65100; }

/* Badges */
.badge-ok    { display:inline-block; background:#d4edda; color:#155724; font-size:12px; font-weight:600; padding:2px 10px; border-radius:10px; }
.badge-warn  { display:inline-block; background:#fff3cd; color:#856404; font-size:12px; font-weight:600; padding:2px 10px; border-radius:10px; }

/* Callout boxes */
.callout     { border-left:4px solid #ff9900; background:#fff8ee; padding:12px 16px; border-radius:0 6px 6px 0; margin:8px 0 14px; font-size:13px; color:#444; }
.callout-tip { border-left:4px solid #17a2b8; background:#e8f6f8; padding:12px 16px; border-radius:0 6px 6px 0; margin:8px 0 14px; font-size:13px; color:#0c5460; }

/* Stat bar */
.stat-bar { background:#232f3e; color:#ff9900; border-radius:6px; padding:8px 16px; font-size:13px; font-weight:600; display:inline-block; }

/* Section headings */
.section-head { font-size:20px; font-weight:700; color:#232f3e; margin-bottom:2px; }
.section-sub  { font-size:13px; color:#888; margin-bottom:14px; }

/* Preview */
.result-count-badge { display:inline-block; background:#ff9900; color:white; font-size:11px; font-weight:700; padding:1px 8px; border-radius:10px; margin-left:6px; }
.result-zero-badge  { display:inline-block; background:#e9ecef; color:#666; font-size:11px; font-weight:600; padding:1px 8px; border-radius:10px; margin-left:6px; }

/* Checklist */
.check-row { display:flex; align-items:center; gap:10px; padding:6px 0; font-size:14px; }

/* Schedule */
.next-run-box { background:#232f3e; color:#ff9900; border-radius:8px; padding:14px 20px; font-size:15px; font-weight:700; text-align:center; margin:10px 0; }
.next-run-label { font-size:11px; color:#aab3bf; font-weight:400; display:block; margin-bottom:4px; text-transform:uppercase; letter-spacing:1px; }

div[data-testid="stExpander"] details summary p { font-size:14px; font-weight:600; }
</style>"""

st.markdown(CSS_BLOCK, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div style="background:#232f3e;padding:18px 24px;border-radius:8px;margin-bottom:10px;">
      <span style="color:#ff9900;font-size:24px;font-weight:bold;">☁️ AWS RSS Feed Digest</span>
      <span style="color:#aab3bf;font-size:14px;margin-left:16px;">
        Follow the steps below to set up and send your personalised AWS update digest.
      </span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Load config into session state once
# ---------------------------------------------------------------------------
if "cfg" not in st.session_state:
    st.session_state["cfg"] = load_config()

cfg = st.session_state["cfg"]

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _completion_flags(cfg: dict) -> dict:
    smtp = cfg.get("smtp", {})
    return {
        "services":    bool(cfg.get("selected_services") or cfg.get("custom_feeds")),
        "recipients":  bool(cfg.get("recipients")),
        "send_method": bool(smtp.get("host") and smtp.get("username") and smtp.get("password")),
        "schedule":    cfg.get("schedule", {}).get("enabled", False),
        "ready":       bool(
            (cfg.get("selected_services") or cfg.get("custom_feeds"))
            and cfg.get("recipients")
        ),
    }


def _step_badge(complete: bool, ok_label: str = "Complete", warn_label: str = "Incomplete") -> str:
    if complete:
        return f'<span class="badge-ok">✅ {ok_label}</span>'
    return f'<span class="badge-warn">⚠️ {warn_label}</span>'


def _service_chips(names: list, custom_feeds: list) -> str:
    parts = ['<div class="chip-wrap">']
    for n in names:
        parts.append(f'<span class="chip">{n}</span>')
    for url in custom_feeds:
        short = url if len(url) <= 40 else url[:37] + "…"
        parts.append(f'<span class="chip-custom" title="{url}">{short}</span>')
    parts.append('</div>')
    return "".join(parts)


def _render_progress(cfg: dict) -> None:
    flags = _completion_flags(cfg)
    steps = [
        ("1", "Pick<br>Services",       flags["services"]),
        ("2", "Add<br>Recipients",      flags["recipients"]),
        ("3", "Schedule<br>(Optional)", flags["schedule"]),
        ("4", "Ready<br>to Send",       flags["ready"]),
    ]
    html = ['<div class="stepper-wrap">']
    for i, (num, label, done) in enumerate(steps):
        if i > 0:
            prev_done = steps[i - 1][2]
            html.append(f'<div class="step-connector {"done" if prev_done else ""}"></div>')
        if done:
            c_cls, l_cls, inner = "done", "done", "✓"
        elif i > 0 and all(s[2] for s in steps[:i]):
            c_cls, l_cls, inner = "active", "active", num
        else:
            c_cls, l_cls, inner = "", "", num
        html.append(
            f'<div class="step-item">'
            f'<div class="step-circle {c_cls}">{inner}</div>'
            f'<div class="step-label {l_cls}">{label}</div>'
            f'</div>'
        )
    html.append('</div>')
    st.markdown("".join(html), unsafe_allow_html=True)


# Render stepper before tabs
_render_progress(cfg)

# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "① Pick Services",
    "② Recipients",
    "③ Schedule",
    "④ Preview & Send",
])


# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — Pick Services
# ════════════════════════════════════════════════════════════════════════════

# Seed the multiselect session-state key from config the very first time.
# All subsequent mutations go through st.session_state["svc_ms"] so the
# widget always reflects the true selection regardless of how it was changed.
_MS_KEY  = "svc_ms"          # multiselect widget key
_CAT_KEY = "svc_cat"         # category selectbox key

if _MS_KEY not in st.session_state:
    st.session_state[_MS_KEY] = cfg.get("selected_services", [])

def _set_services(new_list: list) -> None:
    """Update both the widget session state and cfg in one call."""
    st.session_state[_MS_KEY] = new_list
    cfg["selected_services"] = new_list
    save_config(cfg)

with tab1:
    flags = _completion_flags(cfg)
    n_selected = len(cfg.get("selected_services", [])) + (1 if cfg.get("custom_feeds") else 0)
    ok_label = f"{n_selected} service{'s' if n_selected != 1 else ''} selected"
    st.markdown(
        '<p class="section-head">What AWS services do you want to track?</p>'
        '<p class="section-sub">Choose from 300+ services. Add one, a category, or everything.</p>',
        unsafe_allow_html=True,
    )
    st.markdown(_step_badge(flags["services"], ok_label=ok_label), unsafe_allow_html=True)
    st.markdown("")

    col_left, col_right = st.columns([2, 1])

    with col_left:
        # ── Select All / Clear All / Category ────────────────────────────
        btn_col1, btn_col2, btn_col3 = st.columns(3)

        if btn_col1.button("✅ Select All", use_container_width=True):
            _set_services(SERVICE_NAMES.copy())

        if btn_col2.button("❌ Clear All", use_container_width=True):
            _set_services([])

        cat_options = ["— add entire category —"] + CATEGORIES
        chosen_cat = btn_col3.selectbox(
            "Add entire category",
            cat_options,
            key=_CAT_KEY,
            label_visibility="collapsed",
        )
        if chosen_cat and chosen_cat != "— add entire category —":
            _cat_svcs = [s["name"] for s in AWS_SERVICES if s["category"] == chosen_cat]
            _new_sel  = list(dict.fromkeys(list(st.session_state[_MS_KEY]) + _cat_svcs))
            _set_services(_new_sel)
            # Reset the selectbox to placeholder so it doesn't re-fire on next render
            st.session_state[_CAT_KEY] = cat_options[0]
            st.rerun()

        st.divider()

        # ── Main searchable multiselect ───────────────────────────────────
        st.markdown("**Or search & select by name:**")
        selected = st.multiselect(
            "Services",
            options=SERVICE_NAMES,
            key=_MS_KEY,          # drives the widget value; no `default` needed
            placeholder="Type to search (e.g. Lambda, S3, Bedrock, CloudFront…)",
            label_visibility="collapsed",
        )
        # Sync widget output → config whenever the user edits via the dropdown
        if selected != cfg.get("selected_services", []):
            cfg["selected_services"] = selected
            save_config(cfg)

        st.divider()

        # ── Custom feed URLs ──────────────────────────────────────────────
        with st.expander("➕ Add custom RSS feed URLs"):
            st.caption("One URL per line. Useful for third-party AWS community blogs or private feeds.")
            custom_raw = st.text_area(
                "Custom feed URLs",
                value="\n".join(cfg.get("custom_feeds", [])),
                height=100,
                placeholder="https://example.com/feed.rss",
                label_visibility="collapsed",
            )
            custom_feeds = [u.strip() for u in custom_raw.splitlines() if u.strip()]
            if custom_feeds != cfg.get("custom_feeds", []):
                cfg["custom_feeds"] = custom_feeds
                save_config(cfg)

    # Read final values for the right-hand summary column
    custom_feeds = cfg.get("custom_feeds", [])
    selected     = cfg.get("selected_services", [])

    with col_right:
        st.markdown("**Your selection**")
        if not selected and not custom_feeds:
            st.markdown(
                '<div class="callout">Nothing selected yet — use the popular picks or search on the left.</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(_service_chips(selected, custom_feeds), unsafe_allow_html=True)
            unique_cats = len({s["category"] for s in AWS_SERVICES if s["name"] in selected})
            st.markdown(
                f'<div class="stat-bar">📊 {len(selected) + len(custom_feeds)} sources'
                f'{f" · {unique_cats} categories" if unique_cats else ""}</div>',
                unsafe_allow_html=True,
            )


# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — Recipients
# ════════════════════════════════════════════════════════════════════════════
with tab2:
    flags = _completion_flags(cfg)
    n_recip = len(cfg.get("recipients", []))
    st.markdown(
        '<p class="section-head">Who should get this digest?</p>'
        '<p class="section-sub">Add one or more email addresses. Each person receives their own copy.</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        _step_badge(flags["recipients"], ok_label=f"{n_recip} recipient{'s' if n_recip != 1 else ''} configured"),
        unsafe_allow_html=True,
    )
    st.markdown("")

    col_a, col_b = st.columns([3, 2])

    with col_a:
        st.markdown("**Recipient email addresses — one per line**")
        recipients_raw = st.text_area(
            "Recipients",
            value="\n".join(cfg.get("recipients", [])),
            height=160,
            placeholder="alice@example.com\nbob@example.com",
            label_visibility="collapsed",
        )
        recipients = [r.strip() for r in recipients_raw.splitlines() if r.strip()]

        invalid = [r for r in recipients if not re.match(r"[^@]+@[^@]+\.[^@]+", r)]
        if invalid:
            st.warning(f"⚠️ Invalid email format: {', '.join(invalid)}")
        elif recipients:
            st.success(f"✅ {len(recipients)} valid recipient{'s' if len(recipients) != 1 else ''}")

        if recipients != cfg.get("recipients", []):
            cfg["recipients"] = recipients
            save_config(cfg)

    with col_b:
        st.markdown("**Email subject line**")
        st.markdown(
            '<div class="callout-tip">💡 Use <strong>{date}</strong> and it\'s automatically replaced with today\'s date.</div>',
            unsafe_allow_html=True,
        )
        subject_template = st.text_input(
            "Subject",
            value=cfg.get("subject", "AWS Service Updates — {date}"),
            label_visibility="collapsed",
        )
        st.caption(f"Preview: **{build_subject(subject_template)}**")
        if subject_template != cfg.get("subject"):
            cfg["subject"] = subject_template
            save_config(cfg)

        st.markdown("")
        st.markdown("**How far back should the digest look?**")
        days_back = st.slider(
            "Days back",
            min_value=1,
            max_value=30,
            value=cfg.get("days_back", 7),
            label_visibility="collapsed",
        )
        # Human-readable label
        if days_back == 1:
            preset_label = "1 day"
        elif days_back == 7:
            preset_label = "1 week"
        elif days_back == 14:
            preset_label = "2 weeks"
        elif days_back == 30:
            preset_label = "1 month"
        else:
            preset_label = f"{days_back} days"
        st.caption(f"Covering: **{preset_label}** · Tip: match this to your send frequency.")
        if days_back != cfg.get("days_back"):
            cfg["days_back"] = days_back
            save_config(cfg)


# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — Schedule
# ════════════════════════════════════════════════════════════════════════════
with tab3:
    flags = _completion_flags(cfg)
    sched_cfg = cfg.get("schedule", {})

    st.markdown(
        '<p class="section-head">Automatic delivery schedule</p>'
        '<p class="section-sub">Optional. You can always send manually from ④ Preview &amp; Send.</p>',
        unsafe_allow_html=True,
    )
    st.markdown("")

    sched_enabled = st.toggle(
        "Enable automatic schedule",
        value=sched_cfg.get("enabled", False),
    )

    if not sched_enabled:
        st.markdown(
            '<div class="callout">Scheduling is off. You can send manually from <strong>④ Preview &amp; Send</strong> anytime.</div>',
            unsafe_allow_html=True,
        )

    col_s1, col_s2 = st.columns([3, 2])

    with col_s1:
        _freq_saved = sched_cfg.get("frequency", "daily")
        _freq_opts  = ["daily", "weekly", "monthly"]
        frequency = st.radio(
            "How often?",
            _freq_opts,
            index=_freq_opts.index(_freq_saved) if _freq_saved in _freq_opts else 0,
            horizontal=True,
            captions=["Every day", "Once a week", "Once a month"],
            disabled=not sched_enabled,
        )

        time_str = sched_cfg.get("time", "08:00")
        time_hour, time_min = (int(x) for x in time_str.split(":"))

        t_col1, t_col2 = st.columns(2)
        send_hour = t_col1.selectbox(
            "Hour (UTC)",
            list(range(24)),
            index=time_hour,
            format_func=lambda h: f"{h:02d}:00",
            disabled=not sched_enabled,
        )
        send_minute = t_col2.selectbox(
            "Minute",
            [0, 15, 30, 45],
            index=[0, 15, 30, 45].index(time_min) if time_min in [0, 15, 30, 45] else 0,
            format_func=lambda m: f":{m:02d}",
            disabled=not sched_enabled,
        )

        dow_options = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        day_of_week = st.selectbox(
            "Day of week",
            dow_options,
            index=dow_options.index(sched_cfg.get("day_of_week", "monday")),
            disabled=(not sched_enabled or frequency != "weekly"),
            help="Only applies to weekly schedules.",
        )

        dom_options = list(range(1, 29))
        _dom_saved  = sched_cfg.get("day_of_month", 1)
        day_of_month = st.selectbox(
            "Day of month",
            dom_options,
            index=dom_options.index(_dom_saved) if _dom_saved in dom_options else 0,
            format_func=lambda d: f"{d}{('st' if d == 1 else 'nd' if d == 2 else 'rd' if d == 3 else 'th')} of each month",
            disabled=(not sched_enabled or frequency != "monthly"),
            help="Only applies to monthly schedules. Max 28 to avoid missing February.",
        )

    with col_s2:
        next_run = get_next_run()
        if sched_cfg.get("enabled") and next_run:
            st.markdown(
                f'<div class="next-run-box">'
                f'<span class="next-run-label">Next scheduled run</span>'
                f'{next_run}'
                f'</div>',
                unsafe_allow_html=True,
            )
            st.caption("⚠️ Scheduler runs while this browser tab is open.")
        elif sched_enabled:
            st.info("Set a time above and save to activate the schedule.")
        else:
            st.info("Enable the schedule above, set a time, then save.")

    st.markdown("")
    if st.button("💾 Save Schedule", type="primary"):
        new_sched = {
            "enabled": sched_enabled,
            "frequency": frequency,
            "time": f"{send_hour:02d}:{send_minute:02d}",
            "day_of_week": day_of_week,
            "day_of_month": day_of_month,
        }
        cfg["schedule"] = new_sched
        save_config(cfg)
        next_run_str = apply_schedule(new_sched)
        if next_run_str:
            st.success(f"✅ Schedule saved. Next run: **{next_run_str}**")
        else:
            st.info("Schedule saved (disabled).")
        st.rerun()


# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — Preview & Send
# ════════════════════════════════════════════════════════════════════════════
with tab4:
    flags = _completion_flags(cfg)

    selected_services = cfg.get("selected_services", [])
    custom_feeds = cfg.get("custom_feeds", [])
    recipients = cfg.get("recipients", [])
    days_back = cfg.get("days_back", 7)
    smtp = cfg.get("smtp", {})
    smtp_ok = bool(smtp.get("host") and smtp.get("username") and smtp.get("password"))

    st.markdown(
        '<p class="section-head">Preview &amp; Send Your Digest</p>'
        '<p class="section-sub">Configure how to send, fetch the latest updates, then deliver.</p>',
        unsafe_allow_html=True,
    )
    st.markdown("")

    # ── Readiness checklist ───────────────────────────────────────────────
    has_services   = bool(selected_services or custom_feeds)
    has_recipients = bool(recipients)

    svc_icon  = "✅" if has_services   else "⚠️"
    rec_icon  = "✅" if has_recipients else "⚠️"
    smtp_icon = "✅" if smtp_ok        else "ℹ️"

    svc_text  = (f"{len(selected_services)} service{'s' if len(selected_services) != 1 else ''} selected"
                 + (f" + {len(custom_feeds)} custom feed{'s' if len(custom_feeds) != 1 else ''}" if custom_feeds else "")
                 ) if has_services else "No services selected — go to ① Pick Services"
    rec_text  = (f"{len(recipients)} recipient{'s' if len(recipients) != 1 else ''} configured"
                 ) if has_recipients else "No recipients — go to ② Recipients"
    smtp_text = "SMTP configured" if smtp_ok else "SMTP not configured — Outlook available, or configure below"

    st.markdown(
        f'<div style="background:#f8f9fa;border:1px solid #e9ecef;border-radius:8px;padding:14px 20px;margin-bottom:16px;">'
        f'<div class="check-row">{svc_icon} &nbsp; {svc_text}</div>'
        f'<div class="check-row">{rec_icon} &nbsp; {rec_text}</div>'
        f'<div class="check-row">{smtp_icon} &nbsp; {smtp_text}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── Send method ───────────────────────────────────────────────────────
    smtp_cls = "selected" if smtp_ok else ""
    smtp_tag_cls = "" if smtp_ok else "warn"
    smtp_tag_txt = "✅ Configured" if smtp_ok else "⚠️ Setup required"
    card_col1, card_col2 = st.columns(2)
    with card_col1:
        st.markdown(
            f'<div class="method-card {smtp_cls}">'
            f'<div class="method-card-icon">📨</div>'
            f'<div class="method-card-title">Send via Email (SMTP)</div>'
            f'<div class="method-card-desc">Connect Gmail, Outlook 365, or any SMTP provider. Required for auto-scheduling.</div>'
            f'<span class="method-card-tag {smtp_tag_cls}">{smtp_tag_txt}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with card_col2:
        st.markdown(
            '<div class="method-card">'
            '<div class="method-card-icon">📧</div>'
            '<div class="method-card-title">Open in Outlook</div>'
            '<div class="method-card-desc">Opens a pre-filled draft in your local Outlook app. Review and edit before sending — no SMTP needed.</div>'
            '<span class="method-card-tag">✅ No setup needed</span>'
            '</div>',
            unsafe_allow_html=True,
        )

    with st.expander("⚙️ Configure SMTP Settings", expanded=not smtp_ok):
        st.caption("Credentials are saved locally in config.json — never transmitted to anyone except your SMTP server.")
        with st.form("smtp_form"):
            col1, col2 = st.columns(2)
            with col1:
                host_presets = {
                    "Gmail":             ("smtp.gmail.com", 587),
                    "Outlook / Hotmail": ("smtp.office365.com", 587),
                    "Yahoo Mail":        ("smtp.mail.yahoo.com", 587),
                    "Custom":            ("", 587),
                }
                preset = st.selectbox(
                    "Provider preset",
                    list(host_presets.keys()),
                    index=0,
                    help="Select a preset to auto-fill host/port, or choose Custom.",
                )
                default_host, default_port = host_presets[preset]
                smtp_host = st.text_input("SMTP Host", value=smtp.get("host") or default_host, placeholder="smtp.gmail.com")
                smtp_port = st.number_input("SMTP Port", value=smtp.get("port") or default_port, min_value=1, max_value=65535)
                smtp_tls  = st.checkbox("Use STARTTLS (recommended)", value=smtp.get("tls", True))
            with col2:
                smtp_user = st.text_input("Username / Email", value=smtp.get("username", ""), placeholder="you@gmail.com")
                smtp_pass = st.text_input(
                    "Password / App Password", value=smtp.get("password", ""), type="password",
                    help="For Gmail: use an App Password. Go to Google Account → Security → App Passwords.",
                )
            btn_row1, btn_row2 = st.columns(2)
            test_btn = btn_row1.form_submit_button("🔌 Test Connection", use_container_width=True)
            save_btn = btn_row2.form_submit_button("💾 Save SMTP Settings", use_container_width=True, type="primary")
            if save_btn:
                cfg["smtp"] = {"host": smtp_host, "port": int(smtp_port), "username": smtp_user, "password": smtp_pass, "tls": smtp_tls}
                save_config(cfg)
                st.success("✅ SMTP settings saved.")
                st.rerun()
            if test_btn:
                with st.spinner("Testing connection…"):
                    ok, msg = test_smtp_connection({"host": smtp_host, "port": int(smtp_port), "username": smtp_user, "password": smtp_pass, "tls": smtp_tls})
                (st.success if ok else st.error)(f"{'✅' if ok else '❌'} {msg}")

    with st.expander("💡 Gmail & Outlook setup tips"):
        st.markdown(
            """
**Gmail:** Enable 2-Step Verification → Google Account → Security → App Passwords → create one for "Mail".
Use your Gmail address + the 16-character app password. Host: `smtp.gmail.com`, Port: `587`, TLS: ✅

**Outlook / Microsoft 365:** Full email address as username. Host: `smtp.office365.com`, Port: `587`, TLS: ✅
If MFA is enabled, create an App Password in Microsoft account security settings.
            """
        )

    st.divider()

    # ── Fetch button ──────────────────────────────────────────────────────
    if st.button(
        "🔍 Fetch Latest Updates",
        use_container_width=True,
        type="secondary",
        disabled=not has_services,
    ):
        with st.spinner("Fetching feeds… this may take a moment."):
            results = scrape_services(selected_services, custom_feeds, days_back)
        st.session_state["preview_results"] = results
        total = total_item_count(results)
        if total:
            st.success(
                f"✅ Fetched **{total} update{'s' if total != 1 else ''}** "
                f"across {len(results)} service{'s' if len(results) != 1 else ''}."
            )
        else:
            st.info(f"No updates found in the last {days_back} day{'s' if days_back != 1 else ''}. Try increasing the time window in ② Recipients.")

    # ── Send pair ─────────────────────────────────────────────────────────
    base_issues = ([] if has_services else ["no services"]) + ([] if has_recipients else ["no recipients"])
    smtp_issues = base_issues + ([] if smtp_ok else ["smtp"])

    send_col, outlook_col = st.columns(2)

    with send_col:
        send_btn = st.button(
            "📨 Send via SMTP",
            use_container_width=True,
            type="primary",
            disabled=bool(smtp_issues),
            help="Configure SMTP above first." if not smtp_ok else "",
        )

    with outlook_col:
        outlook_btn = st.button(
            "📧 Open in Outlook",
            use_container_width=True,
            type="secondary",
            disabled=bool(base_issues),
        )

    # ── Send actions ──────────────────────────────────────────────────────
    if send_btn and not smtp_issues:
        with st.spinner("Fetching feeds and sending email…"):
            try:
                results = scrape_services(selected_services, custom_feeds, days_back)
                st.session_state["preview_results"] = results
                html = build_html_email(results, days_back)
                subject = build_subject(cfg.get("subject", "AWS Service Updates — {date}"))
                send_email(html, recipients, subject, cfg["smtp"])
                total = total_item_count(results)
                st.success(
                    f"✅ Email sent to **{len(recipients)} recipient{'s' if len(recipients) != 1 else ''}** "
                    f"with **{total} update{'s' if total != 1 else ''}** across {len(results)} service{'s' if len(results) != 1 else ''}."
                )
            except Exception as e:
                st.error(f"❌ Failed to send email: {e}")

    if outlook_btn and not base_issues:
        with st.spinner("Building digest and opening Outlook draft…"):
            try:
                results = scrape_services(selected_services, custom_feeds, days_back)
                st.session_state["preview_results"] = results
                html = build_html_email(results, days_back)
                subject = build_subject(cfg.get("subject", "AWS Service Updates — {date}"))
                open_in_outlook(html, recipients, subject)
                total = total_item_count(results)
                st.info(
                    f"📧 Outlook draft opened with **{total} update{'s' if total != 1 else ''}** across "
                    f"{len(results)} service{'s' if len(results) != 1 else ''} — review and send from Outlook."
                )
            except RuntimeError as e:
                st.error(f"❌ {e}")
            except Exception as e:
                st.error(f"❌ Could not open Outlook: {e}")

    # ── Preview results ───────────────────────────────────────────────────
    if "preview_results" in st.session_state:
        results = st.session_state["preview_results"]
        st.divider()
        total = total_item_count(results)
        st.markdown(
            f"### Preview — {total} item{'s' if total != 1 else ''} across {len(results)} service{'s' if len(results) != 1 else ''}",
        )

        if not results:
            st.info(
                f"No items found for the selected services in the last {days_back} day{'s' if days_back != 1 else ''}. "
                "Try increasing the 'Days back' slider in ② Recipients."
            )
        else:
            for service_name, items in results.items():
                with st.expander(
                    f"**{service_name}** — {len(items)} update{'s' if len(items) != 1 else ''}",
                    expanded=len(items) > 0,
                ):
                    if not items:
                        st.caption("No updates found in this time window.")
                    else:
                        for item in items:
                            date_str = item["published"].strftime("%Y-%m-%d") if item["published"] else "Unknown"
                            st.markdown(
                                f"**[{item['title']}]({item['link']})**  \n"
                                f"<span style='color:#888;font-size:12px;'>{date_str}</span>",
                                unsafe_allow_html=True,
                            )
                            if item["summary"]:
                                st.caption(item["summary"][:300])
                            st.divider()

    # ── Teams message ─────────────────────────────────────────────────────
    if "preview_results" in st.session_state and st.session_state["preview_results"]:
        with st.expander("💬 Copy Teams Message", expanded=False):
            st.markdown(
                '<div class="callout-tip">'
                '📋 Paste this directly into a <strong>Microsoft Teams</strong> channel. '
                'Teams renders the bold text, links, and emoji automatically.'
                '</div>',
                unsafe_allow_html=True,
            )
            teams_msg = build_teams_message(
                st.session_state["preview_results"],
                cfg.get("days_back", 7),
            )
            st.code(teams_msg, language=None)

    # ── Test email ────────────────────────────────────────────────────────
    with st.expander("📮 Send a test email (SMTP only)"):
        st.caption("Sends a minimal test message to verify your SMTP configuration. No feed content included.")
        test_recipient = st.text_input("Test recipient email", placeholder="you@example.com")
        if st.button("Send Test Email"):
            if not test_recipient:
                st.warning("Enter a recipient address above.")
            elif not smtp_ok:
                st.error("Configure SMTP settings above first.")
            else:
                with st.spinner("Sending test email…"):
                    try:
                        test_html = """
                        <html><body style="font-family:Arial,sans-serif;padding:20px;">
                        <h2 style="color:#232f3e;">&#9729; AWS RSS Digest — Test Email</h2>
                        <p>Your SMTP configuration is working correctly! 🎉</p>
                        <p style="color:#888;font-size:12px;">Sent from AWS RSS Digest app.</p>
                        </body></html>
                        """
                        send_email(test_html, [test_recipient], "AWS RSS Digest — Test", cfg["smtp"])
                        st.success(f"✅ Test email sent to {test_recipient}")
                    except Exception as e:
                        st.error(f"❌ {e}")
