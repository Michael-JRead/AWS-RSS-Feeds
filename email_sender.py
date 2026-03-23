"""
Email composition and delivery via SMTP (Gmail / Outlook / any TLS SMTP).
"""

from __future__ import annotations

import smtplib
import ssl
from datetime import datetime, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any


# ---------------------------------------------------------------------------
# HTML email template (inline styles for broad client compatibility)
# ---------------------------------------------------------------------------

_HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>AWS Service Digest</title>
</head>
<body style="margin:0;padding:0;background:#0d1117;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif;">

<!-- Wrapper -->
<table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#0d1117;">
<tr><td align="center" style="padding:24px 16px;">

  <!-- Email card -->
  <table width="620" cellpadding="0" cellspacing="0" border="0"
         style="max-width:620px;width:100%;background:#161b22;border-radius:12px;overflow:hidden;border:1px solid #30363d;">

    <!-- HEADER -->
    <tr>
      <td style="background:#0d1117;padding:30px 36px;border-bottom:3px solid #ff9900;">
        <table width="100%" cellpadding="0" cellspacing="0" border="0">
          <tr>
            <td>
              <div style="color:#ff9900;font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-bottom:8px;">&#9729; AWS SERVICE DIGEST</div>
              <div style="color:#e6edf3;font-size:26px;font-weight:700;line-height:1.2;">What's New in AWS</div>
              <div style="color:#8b949e;font-size:13px;margin-top:6px;">Covering the last {days_back} day{days_plural}</div>
            </td>
            <td align="right" valign="top" style="white-space:nowrap;">
              <div style="background:#ff9900;color:#0d1117;font-size:12px;font-weight:700;padding:6px 14px;border-radius:20px;display:inline-block;">{date_str}</div>
            </td>
          </tr>
        </table>
      </td>
    </tr>

    <!-- SUMMARY BAR -->
    <tr>
      <td style="background:#ff9900;padding:10px 36px;">
        <span style="color:#0d1117;font-size:14px;font-weight:700;">{total_updates} update{total_plural} across {service_count} service{service_plural}</span>
      </td>
    </tr>

    <!-- SERVICE BLOCKS -->
    <tr>
      <td style="padding:24px 28px 12px;">
        {service_blocks}
      </td>
    </tr>

    <!-- FOOTER -->
    <tr>
      <td style="background:#0d1117;padding:20px 36px;border-top:1px solid #30363d;">
        <table width="100%" cellpadding="0" cellspacing="0" border="0">
          <tr>
            <td style="color:#6e7681;font-size:11px;line-height:1.8;">
              <strong style="color:#8b949e;">AWS RSS Digest</strong> &nbsp;·&nbsp; Generated {generated_at} UTC<br>
              <a href="https://aws.amazon.com/about-aws/whats-new/" style="color:#ff9900;text-decoration:none;">AWS What's New</a>
              &nbsp;·&nbsp;
              <a href="https://aws.amazon.com/blogs/aws/" style="color:#ff9900;text-decoration:none;">AWS Blog</a>
              &nbsp;·&nbsp;
              <a href="https://aws.amazon.com" style="color:#ff9900;text-decoration:none;">aws.amazon.com</a>
            </td>
          </tr>
        </table>
      </td>
    </tr>

  </table>
  <!-- /email card -->

</td></tr>
</table>
</body>
</html>
"""

_SERVICE_BLOCK = """\
<!-- Service: {service_name} -->
<table width="100%" cellpadding="0" cellspacing="0" border="0"
       style="margin-bottom:20px;border-radius:8px;overflow:hidden;border:1px solid #30363d;">
  <!-- Service header -->
  <tr>
    <td style="background:#21262d;padding:11px 18px;">
      <table width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
          <td>
            <span style="color:#ff9900;font-size:14px;font-weight:700;letter-spacing:0.3px;">{service_name}</span>
          </td>
          <td align="right">
            <span style="background:#ff9900;color:#0d1117;font-size:11px;font-weight:700;padding:2px 10px;border-radius:12px;">{item_count} update{plural}</span>
          </td>
        </tr>
      </table>
    </td>
  </tr>
  <!-- Items -->
  <tr>
    <td style="background:#161b22;">
      {item_rows}
    </td>
  </tr>
</table>
"""

_ITEM_ROW = """\
<table width="100%" cellpadding="0" cellspacing="0" border="0"
       style="border-bottom:1px solid #21262d;">
  <tr>
    <td style="width:4px;background:#ff9900;"></td>
    <td style="padding:16px 18px;">
      <!-- Title -->
      <a href="{link}" style="color:#e6edf3;font-size:14px;font-weight:700;text-decoration:none;line-height:1.4;display:block;margin-bottom:6px;">{title}</a>
      <!-- Date badge -->
      <span style="display:inline-block;background:#21262d;color:#8b949e;font-size:11px;font-weight:600;padding:2px 8px;border-radius:8px;margin-bottom:10px;">{date_str}</span>
      <!-- Summary -->
      <div style="color:#8b949e;font-size:13px;line-height:1.6;margin-bottom:12px;">{summary}</div>
      <!-- Read more pill button -->
      <a href="{link}"
         style="display:inline-block;background:#ff9900;color:#0d1117;font-size:12px;font-weight:700;padding:5px 16px;border-radius:20px;text-decoration:none;letter-spacing:0.3px;">
        Read more &rarr;
      </a>
    </td>
  </tr>
</table>
"""

_NO_ITEMS_ROW = """\
<table width="100%" cellpadding="0" cellspacing="0" border="0">
  <tr>
    <td style="padding:16px 20px;color:#6e7681;font-size:13px;font-style:italic;text-align:center;">
      No updates in this time window.
    </td>
  </tr>
</table>
"""


# ---------------------------------------------------------------------------
# Plain-text fallback
# ---------------------------------------------------------------------------

def _build_plain_text(results: dict[str, list[dict]], days_back: int) -> str:
    now = datetime.now(timezone.utc)
    total_updates = sum(len(v) for v in results.values())
    service_count = len(results)
    lines = [
        f"AWS SERVICE DIGEST — {total_updates} update{'s' if total_updates != 1 else ''} across {service_count} service{'s' if service_count != 1 else ''}",
        f"Generated: {now.strftime('%Y-%m-%d %H:%M UTC')}",
        f"Covering last {days_back} day{'s' if days_back != 1 else ''}",
        "=" * 60,
        "",
    ]
    for service_name, items in results.items():
        lines.append(f"## {service_name} ({len(items)} update{'s' if len(items) != 1 else ''})")
        if not items:
            lines.append("  No updates found.")
        for item in items:
            date_str = item["published"].strftime("%Y-%m-%d") if item["published"] else "Unknown"
            lines.append(f"  [{date_str}] {item['title']}")
            if item["summary"]:
                lines.append(f"  {item['summary'][:200]}")
            lines.append(f"  {item['link']}")
            lines.append("")
        lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# HTML builder
# ---------------------------------------------------------------------------

def build_html_email(results: dict[str, list[dict]], days_back: int) -> str:
    """Render the full HTML email from scraped results."""
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%B %d, %Y")
    generated_at = now.strftime("%Y-%m-%d %H:%M")

    total_updates = sum(len(v) for v in results.values())
    service_count = len(results)

    service_blocks_html = ""
    for service_name, items in results.items():
        item_rows_html = ""
        if not items:
            item_rows_html = _NO_ITEMS_ROW
        else:
            for item in items:
                d = item["published"].strftime("%B %d, %Y") if item["published"] else "Unknown date"
                item_rows_html += _ITEM_ROW.format(
                    link=item["link"] or "#",
                    title=_esc(item["title"]),
                    date_str=d,
                    summary=_esc(item["summary"]) if item["summary"] else "",
                )

        service_blocks_html += _SERVICE_BLOCK.format(
            service_name=_esc(service_name),
            item_count=len(items),
            plural="s" if len(items) != 1 else "",
            item_rows=item_rows_html,
        )

    return _HTML_TEMPLATE.format(
        date_str=date_str,
        days_back=days_back,
        days_plural="s" if days_back != 1 else "",
        total_updates=total_updates,
        total_plural="s" if total_updates != 1 else "",
        service_count=service_count,
        service_plural="s" if service_count != 1 else "",
        generated_at=generated_at,
        service_blocks=service_blocks_html,
    )


def _esc(text: str) -> str:
    """Minimal HTML escaping for inline content."""
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
    )


# ---------------------------------------------------------------------------
# SMTP send
# ---------------------------------------------------------------------------

def send_email(
    html_body: str,
    recipients: list[str],
    subject: str,
    smtp_config: dict,
) -> None:
    """
    Send an HTML email via SMTP.

    Raises an exception on failure so the caller can surface the error.
    """
    if not recipients:
        raise ValueError("No recipients specified.")

    plain_body = "Please view this email in an HTML-capable client."

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = smtp_config["username"]
    msg["To"] = ", ".join(recipients)

    msg.attach(MIMEText(plain_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    host = smtp_config["host"]
    port = int(smtp_config.get("port", 587))
    username = smtp_config["username"]
    password = smtp_config["password"]
    use_tls = smtp_config.get("tls", True)

    context = ssl.create_default_context()

    if use_tls:
        with smtplib.SMTP(host, port, timeout=30) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(username, password)
            server.sendmail(username, recipients, msg.as_string())
    else:
        with smtplib.SMTP_SSL(host, port, context=context, timeout=30) as server:
            server.login(username, password)
            server.sendmail(username, recipients, msg.as_string())


def open_in_outlook(html_body: str, recipients: list[str], subject: str) -> None:
    """Open a pre-filled Outlook draft using Windows COM automation (win32com).

    Requires Microsoft Outlook to be installed and pywin32 (pip install pywin32).
    Opens the draft for the user to review — does NOT send automatically.

    COM must be initialised on every thread that uses it. Streamlit runs button
    callbacks on background threads, so we call CoInitialize/CoUninitialize
    explicitly to avoid the "CoInitialize has not been called" error on repeated
    button clicks.

    Args:
        html_body:  Full HTML string for the email body.
        recipients: List of recipient email addresses.
        subject:    Email subject line.

    Raises:
        RuntimeError: If pywin32 is not installed.
        Exception:    If Outlook is not installed or COM dispatch fails.
    """
    try:
        import win32com.client  # type: ignore
        import pythoncom        # type: ignore  (bundled with pywin32)
    except ImportError:
        raise RuntimeError(
            "pywin32 is not installed. Run: pip install pywin32"
        )

    # Initialise COM on the current thread (safe to call even if already initialised)
    pythoncom.CoInitialize()
    try:
        outlook = win32com.client.Dispatch("Outlook.Application")
        mail = outlook.CreateItem(0)       # 0 = olMailItem
        mail.Subject = subject
        mail.HTMLBody = html_body
        mail.To = "; ".join(recipients)
        mail.Display(False)                # False = non-modal, keeps Outlook visible
    finally:
        # Always uninitialise so the thread's COM state is clean for future calls
        pythoncom.CoUninitialize()


def test_smtp_connection(smtp_config: dict) -> tuple[bool, str]:
    """
    Test SMTP credentials without sending a message.
    Returns (success: bool, message: str).
    """
    try:
        host = smtp_config["host"]
        port = int(smtp_config.get("port", 587))
        username = smtp_config["username"]
        password = smtp_config["password"]
        use_tls = smtp_config.get("tls", True)

        if not host or not username or not password:
            return False, "Host, username, and password are required."

        context = ssl.create_default_context()
        if use_tls:
            with smtplib.SMTP(host, port, timeout=15) as server:
                server.ehlo()
                server.starttls(context=context)
                server.ehlo()
                server.login(username, password)
        else:
            with smtplib.SMTP_SSL(host, port, context=context, timeout=15) as server:
                server.login(username, password)

        return True, f"Connected to {host}:{port} successfully."
    except smtplib.SMTPAuthenticationError:
        return False, "Authentication failed. Check your username and password."
    except smtplib.SMTPConnectError as e:
        return False, f"Could not connect to {smtp_config.get('host', '')}:{smtp_config.get('port', 587)} — {e}"
    except Exception as e:
        return False, str(e)


def build_subject(template: str) -> str:
    """Substitute {date} in the subject template."""
    return template.replace("{date}", datetime.now().strftime("%Y-%m-%d"))


def build_teams_message(results: dict[str, list[dict]], days_back: int) -> str:
    """Build a copy-pasteable Microsoft Teams channel message from scraped results."""
    now = datetime.now(timezone.utc)
    header_date = now.strftime("%B %d, %Y")
    total_updates = sum(len(v) for v in results.values())
    service_count = sum(1 for v in results.values() if v)  # only services with items
    total_plural = "s" if total_updates != 1 else ""
    svc_plural = "s" if service_count != 1 else ""
    day_plural = "s" if days_back != 1 else ""

    lines = [
        f"☁️ **AWS SERVICE DIGEST**  |  {header_date}",
        f"📊 **{total_updates} update{total_plural} across {service_count} service{svc_plural}**  ·  Last {days_back} day{day_plural}",
        "",
    ]

    for service_name, items in results.items():
        if not items:
            continue
        plural = "s" if len(items) != 1 else ""
        lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        lines.append(f"🔶 **{service_name}**  ·  {len(items)} update{plural}")
        lines.append("")
        for item in items:
            item_date = item["published"].strftime("%b %d, %Y") if item["published"] else "Unknown date"
            summary = (item["summary"] or "").strip()[:220]
            if summary and not summary.endswith((".", "…", "!")):
                summary += "…"
            lines.append(f"▸ **[{item['title']}]({item['link']})**")
            lines.append(f"  📅 {item_date}")
            if summary:
                lines.append(f"  {summary}")
            lines.append("")

    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append(
        f"_Generated by AWS RSS Digest · "
        f"[What's New](https://aws.amazon.com/about-aws/whats-new/) · "
        f"[AWS Blog](https://aws.amazon.com/blogs/aws/)_"
    )
    return "\n".join(lines)
