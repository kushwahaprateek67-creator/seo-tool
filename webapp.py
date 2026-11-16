import csv
import io
import re
import smtplib
import ssl
import time
from datetime import datetime, timezone
from email.message import EmailMessage

import streamlit as st

# IMPORTANT:
# Store credentials in .streamlit/secrets.toml, never in this source file.
# Example:
# [gmail]
# address = "youraddress@gmail.com"
# app_password = "your-16-character-app-password"

st.set_page_config(page_title="AI SEO Email Outreach", page_icon="✉️", layout="wide")

# TOOL LOGIN PASSWORD: replace the placeholder below with your own password.
# This is separate from your Gmail App Password.
TOOL_PASSWORD = "Prateek@2026"

if "tool_authenticated" not in st.session_state:
    st.session_state.tool_authenticated = False

if not st.session_state.tool_authenticated:
    st.title("🔐 Tool Login")
    entered_password = st.text_input("Enter tool password", type="Prateek@2026")
    if st.button("Login", type="primary"):
        if TOOL_PASSWORD != "CHANGE_THIS_TO_YOUR_OWN_PASSWORD" and entered_password == TOOL_PASSWORD:
            st.session_state.tool_authenticated = True
            st.rerun()
        else:
            st.error("Password incorrect, or the default password has not been changed in app.py.")
    st.stop()

st.title("✉️ AI SEO Email Outreach")
st.caption("A controlled Gmail sender for relevant business contacts. It does not guarantee inbox placement.")

with st.sidebar:
    st.subheader("Gmail connection")
    st.write("Credentials are read from Streamlit secrets.")
    gmail_address = st.secrets.get("gmail", {}).get("address", "")
    gmail_app_password = st.secrets.get("gmail", {}).get("app_password", "")
    if gmail_address and gmail_app_password:
        st.success(f"Configured: {gmail_address}")
    else:
        st.warning("Gmail credentials are not configured.")
    st.markdown(
        "Create `.streamlit/secrets.toml` with:\n\n"
        '```toml\n[gmail]\naddress = "youraddress@gmail.com"\n'
        'app_password = "your-app-password"\n```'
    )
    st.caption("Do not paste passwords into the chat or commit secrets.toml to GitHub.")

def normalize_email(value: str) -> str:
    return value.strip().lower()

def valid_email(value: str) -> bool:
    # Syntax check only; it does not prove that a mailbox exists or accepts mail.
    return bool(re.fullmatch(r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+", value.strip()))

def read_suppression(uploaded_file) -> set[str]:
    if uploaded_file is None:
        return set()
    raw = uploaded_file.getvalue().decode("utf-8-sig", errors="replace")
    values = set()
    for row in csv.reader(io.StringIO(raw)):
        for cell in row:
            candidate = normalize_email(cell)
            if valid_email(candidate):
                values.add(candidate)
    return values

def parse_recipients(raw: str, suppressed: set[str]):
    unique, duplicates, invalid, blocked = [], [], [], []
    seen = set()
    for line in raw.splitlines():
        item = normalize_email(line.strip().strip(",;"))
        if not item:
            continue
        if not valid_email(item):
            invalid.append(item)
        elif item in seen:
            duplicates.append(item)
        elif item in suppressed:
            blocked.append(item)
        else:
            seen.add(item)
            unique.append(item)
    return unique, duplicates, invalid, blocked

suppression_upload = st.file_uploader(
    "Upload Do-Not-Email / unsubscribe list (CSV or TXT; one email per line)",
