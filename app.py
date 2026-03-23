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
from email_sender import build_html_email, send_email, build_subject, test_smtp_connection
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
# Styles
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .block-container { padding-top: 1.5rem; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        height: 42px;
        padding: 0 20px;
        font-weight: 600;
    }
    div[data-testid="stExpander"] details summary p { font-size: 14px; }
    .service-badge {
        background: #ff9900;
        color: white;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 13px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div style="background:#232f3e;padding:18px 24px;border-radius:8px;margin-bottom:18px;">
      <span style="color:#ff9900;font-size:24px;font-weight:bold;">☁️ AWS RSS Feed Digest</span>
      <span style="color:#aab3bf;font-size:14px;margin-left:16px;">
        Select services → configure email → send or schedule your digest
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
# Tabs
# ---------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🛠️  Service Selection",
    "📧  Email Recipients",
    "🔑  SMTP Config",
    "🕐  Schedule",
    "🚀  Preview & Send",
])


# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — Service Selection
# ════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("Select AWS Services to Monitor")
    st.caption(
        "Start typing to search. Select one or more services — the digest will include "
        "their What's New announcements and blog posts."
    )

    col_left, col_right = st.columns([2, 1])

    with col_left:
        # Quick-select buttons
        btn_col1, btn_col2, btn_col3 = st.columns(3)
        if btn_col1.button("✅ Select All", use_container_width=True):
            cfg["selected_services"] = SERVICE_NAMES.copy()
            save_config(cfg)
        if btn_col2.button("❌ Clear All", use_container_width=True):
            cfg["selected_services"] = []
            save_config(cfg)

        # Category quick-select
        cat_options = ["— pick a category —"] + CATEGORIES
        chosen_cat = btn_col3.selectbox(
            "Add entire category",
            cat_options,
            label_visibility="collapsed",
        )
        if chosen_cat and chosen_cat != "— pick a category —":
            cat_services = [s["name"] for s in AWS_SERVICES if s["category"] == chosen_cat]
            new_sel = list(dict.fromkeys(cfg["selected_services"] + cat_services))
            cfg["selected_services"] = new_sel
            save_config(cfg)
            st.rerun()

        st.divider()

        # Main multiselect — searchable
        selected = st.multiselect(
            "Search & select AWS services:",
            options=SERVICE_NAMES,
            default=cfg.get("selected_services", []),
            placeholder="Type to search (e.g. Lambda, S3, Bedrock...)",
            help="Type a service name to filter. Click to add to your selection.",
        )
        if selected != cfg.get("selected_services", []):
            cfg["selected_services"] = selected
            save_config(cfg)

        st.divider()

        # Custom feed URLs
        st.markdown("**Add custom RSS feed URLs** *(one per line)*")
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

    with col_right:
        st.markdown("**Selected services**")
        if not selected and not custom_feeds:
            st.info("No services selected yet.")
        else:
            for name in selected:
                svc = next((s for s in AWS_SERVICES if s["name"] == name), None)
                cat = svc["category"] if svc else "Custom"
                st.markdown(
                    f"<span style='font-size:12px;color:#888;'>{cat}</span><br>"
                    f"<span style='font-size:14px;font-weight:600;'>{name}</span>",
                    unsafe_allow_html=True,
                )
                st.divider()
            for url in custom_feeds:
                st.markdown(
                    f"<span style='font-size:12px;color:#888;'>Custom</span><br>"
                    f"<span style='font-size:11px;word-break:break-all;'>{url}</span>",
                    unsafe_allow_html=True,
                )
            total = len(selected) + (1 if custom_feeds else 0)
            st.success(f"{total} source{'s' if total != 1 else ''} selected")


# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — Email Recipients
# ════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("Email Recipients & Content Settings")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("**Recipient email addresses** *(one per line)*")
        recipients_raw = st.text_area(
            "Recipients",
            value="\n".join(cfg.get("recipients", [])),
            height=150,
            placeholder="alice@example.com\nbob@example.com",
            label_visibility="collapsed",
        )
        recipients = [r.strip() for r in recipients_raw.splitlines() if r.strip()]

        # Validate email format
        invalid = [r for r in recipients if not re.match(r"[^@]+@[^@]+\.[^@]+", r)]
        if invalid:
            st.warning(f"Invalid email format: {', '.join(invalid)}")

        if recipients != cfg.get("recipients", []):
            cfg["recipients"] = recipients
            save_config(cfg)

    with col_b:
        st.markdown("**Email subject line**")
        subject_template = st.text_input(
            "Subject",
            value=cfg.get("subject", "AWS Service Updates — {date}"),
            help="Use {date} as a placeholder for today's date (YYYY-MM-DD).",
            label_visibility="collapsed",
        )
        st.caption(f"Preview: *{build_subject(subject_template)}*")
        if subject_template != cfg.get("subject"):
            cfg["subject"] = subject_template
            save_config(cfg)

        st.markdown("**Days back to include**")
        days_back = st.slider(
            "Days back",
            min_value=1,
            max_value=30,
            value=cfg.get("days_back", 7),
            help="How many days of updates to include in the digest.",
            label_visibility="collapsed",
        )
        if days_back != cfg.get("days_back"):
            cfg["days_back"] = days_back
            save_config(cfg)

    st.divider()
    st.markdown(f"**{len(recipients)} recipient{'s' if len(recipients) != 1 else ''} configured**")
    if recipients:
        for r in recipients:
            st.markdown(f"- {r}")


# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — SMTP Configuration
# ════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("SMTP Email Configuration")
    st.caption("Your credentials are stored **locally** in config.json and never transmitted except to your SMTP server.")

    smtp = cfg.get("smtp", {})

    with st.form("smtp_form"):
        col1, col2 = st.columns(2)

        with col1:
            host_presets = {
                "Gmail": ("smtp.gmail.com", 587),
                "Outlook / Hotmail": ("smtp.office365.com", 587),
                "Yahoo Mail": ("smtp.mail.yahoo.com", 587),
                "Custom": ("", 587),
            }
            preset = st.selectbox(
                "Provider preset",
                list(host_presets.keys()),
                index=0,
                help="Select a preset to auto-fill host/port, or choose Custom.",
            )
            default_host, default_port = host_presets[preset]

            smtp_host = st.text_input(
                "SMTP Host",
                value=smtp.get("host") or default_host,
                placeholder="smtp.gmail.com",
            )
            smtp_port = st.number_input(
                "SMTP Port",
                value=smtp.get("port") or default_port,
                min_value=1,
                max_value=65535,
            )
            smtp_tls = st.checkbox(
                "Use STARTTLS (recommended)",
                value=smtp.get("tls", True),
            )

        with col2:
            smtp_user = st.text_input(
                "Username / Email",
                value=smtp.get("username", ""),
                placeholder="you@gmail.com",
            )
            smtp_pass = st.text_input(
                "Password / App Password",
                value=smtp.get("password", ""),
                type="password",
                help="For Gmail: use an App Password (not your account password). "
                     "Go to Google Account → Security → App Passwords.",
            )

        save_smtp = st.form_submit_button("💾 Save SMTP Settings", use_container_width=True)
        if save_smtp:
            cfg["smtp"] = {
                "host": smtp_host,
                "port": int(smtp_port),
                "username": smtp_user,
                "password": smtp_pass,
                "tls": smtp_tls,
            }
            save_config(cfg)
            st.success("SMTP settings saved.")

    if st.button("🔌 Test Connection", use_container_width=False):
        with st.spinner("Testing connection..."):
            ok, msg = test_smtp_connection(cfg["smtp"])
        if ok:
            st.success(f"✅ {msg}")
        else:
            st.error(f"❌ {msg}")

    st.divider()
    with st.expander("💡 Gmail setup tips"):
        st.markdown(
            """
**Step-by-step for Gmail:**

1. Enable **2-Step Verification** on your Google account.
2. Go to **Google Account → Security → App Passwords**.
3. Create an App Password for "Mail" / "Other".
4. Use your Gmail address as the username and the 16-character app password.
5. Host: `smtp.gmail.com`, Port: `587`, TLS: ✅

**Step-by-step for Outlook / Microsoft 365:**

1. Use your full email address as the username.
2. Host: `smtp.office365.com`, Port: `587`, TLS: ✅
3. If MFA is enabled, create an App Password in the Microsoft account security settings.
            """
        )


# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — Schedule
# ════════════════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("Automatic Digest Schedule")
    st.caption("The scheduler runs while this app is open in your browser. For unattended scheduling, leave the app running.")

    sched_cfg = cfg.get("schedule", {})

    col_s1, col_s2 = st.columns(2)

    with col_s1:
        sched_enabled = st.toggle(
            "Enable automatic schedule",
            value=sched_cfg.get("enabled", False),
        )

        frequency = st.radio(
            "Frequency",
            ["daily", "weekly"],
            index=0 if sched_cfg.get("frequency", "daily") == "daily" else 1,
            horizontal=True,
            disabled=not sched_enabled,
        )

        time_str = sched_cfg.get("time", "08:00")
        time_hour, time_min = (int(x) for x in time_str.split(":"))

        send_hour = st.selectbox(
            "Hour (24h)",
            list(range(24)),
            index=time_hour,
            disabled=not sched_enabled,
        )
        send_minute = st.selectbox(
            "Minute",
            [0, 15, 30, 45],
            index=[0, 15, 30, 45].index(time_min) if time_min in [0, 15, 30, 45] else 0,
            disabled=not sched_enabled,
        )

        dow_options = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        day_of_week = st.selectbox(
            "Day of week (weekly only)",
            dow_options,
            index=dow_options.index(sched_cfg.get("day_of_week", "monday")),
            disabled=(not sched_enabled or frequency == "daily"),
        )

    with col_s2:
        next_run = get_next_run()
        if sched_cfg.get("enabled") and next_run:
            st.success(f"**Scheduler is active**\n\nNext run: {next_run}")
        elif sched_cfg.get("enabled"):
            st.info("Scheduler enabled — saving will activate it.")
        else:
            st.info("Scheduler is **off**. Enable and save to activate.")

        st.divider()
        st.markdown("**Current schedule settings**")
        st.json(sched_cfg)

    if st.button("💾 Save Schedule", use_container_width=False, type="primary"):
        new_sched = {
            "enabled": sched_enabled,
            "frequency": frequency,
            "time": f"{send_hour:02d}:{send_minute:02d}",
            "day_of_week": day_of_week,
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
# TAB 5 — Preview & Send
# ════════════════════════════════════════════════════════════════════════════
with tab5:
    st.subheader("Preview Feed & Send Digest")

    selected_services = cfg.get("selected_services", [])
    custom_feeds = cfg.get("custom_feeds", [])
    recipients = cfg.get("recipients", [])
    days_back = cfg.get("days_back", 7)

    # Validation summary
    issues = []
    if not selected_services and not custom_feeds:
        issues.append("No services selected (Tab 1)")
    if not recipients:
        issues.append("No recipients added (Tab 2)")
    if not cfg["smtp"].get("host"):
        issues.append("SMTP not configured (Tab 3)")
    if not cfg["smtp"].get("username"):
        issues.append("SMTP username missing (Tab 3)")
    if not cfg["smtp"].get("password"):
        issues.append("SMTP password missing (Tab 3)")

    if issues:
        st.warning("**Before sending, complete the following:**\n" + "\n".join(f"- {i}" for i in issues))
    else:
        st.success("All settings look good — ready to fetch and send!")

    col_f1, col_f2 = st.columns([1, 1])

    # ── Fetch preview ────────────────────────────────────────────────────────
    with col_f1:
        if st.button("🔍 Fetch Feed Preview", use_container_width=True, type="secondary"):
            if not selected_services and not custom_feeds:
                st.error("Please select at least one service in Tab 1 first.")
            else:
                with st.spinner("Fetching feeds... this may take a moment."):
                    results = scrape_services(selected_services, custom_feeds, days_back)
                st.session_state["preview_results"] = results
                total = total_item_count(results)
                st.success(f"Fetched **{total} total item{'s' if total != 1 else ''}** across {len(results)} service{'s' if len(results) != 1 else ''}.")

    # ── Send now ─────────────────────────────────────────────────────────────
    with col_f2:
        send_btn = st.button(
            "📨 Send Email Now",
            use_container_width=True,
            type="primary",
            disabled=bool(issues),
        )

    if send_btn and not issues:
        with st.spinner("Fetching feeds and sending email..."):
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

    # ── Preview results ───────────────────────────────────────────────────────
    if "preview_results" in st.session_state:
        results = st.session_state["preview_results"]
        st.divider()
        st.markdown(f"### Preview ({total_item_count(results)} items)")

        if not results:
            st.info("No items found for the selected services in the last {days_back} days. Try increasing the 'Days back' slider.")
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

    # ── Test email (single recipient) ────────────────────────────────────────
    st.divider()
    st.markdown("#### Send Test Email")
    st.caption("Sends a minimal test message to verify your SMTP configuration, no feed content included.")
    test_recipient = st.text_input("Test recipient email", placeholder="you@example.com")
    if st.button("📮 Send Test Email"):
        if not test_recipient:
            st.warning("Enter a recipient address above.")
        elif not cfg["smtp"].get("host"):
            st.error("Configure SMTP settings in Tab 3 first.")
        else:
            with st.spinner("Sending test email..."):
                try:
                    test_html = """
                    <html><body>
                    <h2 style="color:#232f3e;">AWS RSS Digest — Test Email</h2>
                    <p>Your SMTP configuration is working correctly!</p>
                    <p style="color:#888;font-size:12px;">Sent from AWS RSS Digest app.</p>
                    </body></html>
                    """
                    send_email(test_html, [test_recipient], "AWS RSS Digest — Test", cfg["smtp"])
                    st.success(f"✅ Test email sent to {test_recipient}")
                except Exception as e:
                    st.error(f"❌ {e}")
