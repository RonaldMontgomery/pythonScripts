# rss_reader/rss_reader.py
# https://medium.com/@jonathanmondaut/fetching-data-from-rss-feeds-in-python-a-comprehensive-guide-a3dc86a5b7bc

import feedparser
import smtplib
from email.message import EmailMessage
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from typing import List
import os

# --- Configuration & Sensitive Data ---

SENDER_EMAIL = os.environ.get("GMAIL_SENDER")
RECEIVER_EMAIL = os.environ.get("GMAIL_RECEIVER")

missing = []
if not SENDER_EMAIL:
    missing.append("GMAIL_SENDER")
if not RECEIVER_EMAIL:
    missing.append("GMAIL_RECEIVER")

try:
    EMAIL_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]
except KeyError:
    missing.append("GMAIL_APP_PASSWORD")
    EMAIL_PASSWORD = None

if missing:
    print("ERROR: Missing required environment variables:", ", ".join(missing))
    print("Email functionality will be skipped.")
    EMAIL_PASSWORD = None  # force-disable email sending


# --- Helper Functions ---

def clean_html(raw_html: str) -> str:
    """
    Strips HTML tags and entities from a string using Beautiful Soup,
    preserving paragraph breaks with double newlines.
    """
    if not raw_html:
        return ""
    
    soup = BeautifulSoup(raw_html, "html.parser")
    clean_text = soup.get_text(separator="\n\n", strip=True)
    return clean_text


def send_notification_email(to: str, subject: str, body: str) -> None:
    """Sends an email using the configured SMTP server."""
    if not EMAIL_PASSWORD or not SENDER_EMAIL:
        return

    try:
        msg = EmailMessage()
        msg["From"] = SENDER_EMAIL
        msg["To"] = to
        msg["Subject"] = subject
        msg.set_content(body)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print(f"\nEmail successfully sent to {to}!")
    except Exception as e:
        print(f"\nFailed to send email. Check credentials/App Password. Error: {e}")


# --- RSS Fetching and Processing ---

def fetch_rss_data(url: str, time_range_days: int) -> str:
    """
    Fetches, filters, and cleans RSS data, returning a formatted string summary.
    Filters entries published within the last 'time_range_days'.
    """
    output_buffer = []

    output_buffer.append("==================================================")
    output_buffer.append(f"| FETCHING FEED: {url}")
    output_buffer.append("==================================================")

    feed = feedparser.parse(url)

    if not feed.feed:
        output_buffer.append(f"Error: Could not parse feed from {url}. Skipping.")
        return "\n".join(output_buffer)

    print(f"Fetching: {feed.feed.title}")
    output_buffer.append(f"Feed Title: {feed.feed.title}")
    output_buffer.append("-" * 30)

    now = datetime.now()
    time_range = timedelta(days=time_range_days)

    found_entries = False

    for entry in feed.entries:
        try:
            entry_date = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %Z")
        except (AttributeError, ValueError):
            continue

        if now - entry_date <= time_range:
            found_entries = True
            clean_summary = clean_html(entry.summary)

            output_buffer.append(f"Entry Title: {entry.title}")
            output_buffer.append(f"Entry Link: {entry.link}")
            output_buffer.append(f"Published Date: {entry.published}")
            output_buffer.append(f"Entry Summary (Cleaned): {clean_summary}")
            output_buffer.append("-" * 25)

    if not found_entries:
        output_buffer.append(f"No new entries found in the last {time_range_days} days.")

    output_buffer.append("\n")
    return "\n".join(output_buffer)


# --- Main Processor ---

def main_rss_processor() -> None:
    """Fetches all feeds, sends collected data via email."""
    rss_feed_urls: List[str] = [
        "https://techcommunity.microsoft.com/t5/s/gxcuf89792/rss/board?board.id=skills-hub-blog",
        # Add more feeds here if you want
    ]

    full_report: List[str] = []

    for url in rss_feed_urls:
        report_section = fetch_rss_data(url, time_range_days=14)
        full_report.append(report_section)

    final_body = "\n".join(full_report)

    if RECEIVER_EMAIL:
        send_notification_email(
            to=RECEIVER_EMAIL,
            subject=f"Automated RSS Digest ({datetime.now().strftime('%Y-%m-%d')})",
            body=final_body,
        )
    else:
        print("No RECEIVER_EMAIL configured; not sending email.")


if __name__ == "__main__":
    main_rss_processor()