
import csv
import io
import re
import smtplib
import ssl
from datetime import datetime
from email.message import EmailMessage

import pandas as pd
import streamlit as st

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="AI SEO Email Outreach",
    page_icon="✉️",
    layout="wide"
)

# अपना नया Tool Login Password यहाँ डालें
TOOL_PASSWORD = "Prateek@2028"

# ---------------- DARK BLUE DESIGN ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #06152e, #0b2345);
    color: white;
}
.block-container {
    max-width: 1150px;
    padding-top: 2rem;
}
h1, h2, h3, p, label {
    color: white !important;
}
div[data-testid="stSidebar"] {
    background-color: #071a35;
}
.stButton button {
    background: #0878d1;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: bold;
    min-height: 42px;
}
.stButton button:hover {
    background: #1595f5;
    color: white;
}
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    background-color: #102b4d;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN ----------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 AI SEO Tool Login")
    password = st.text_input("Enter Tool Password", type="password")

    if st.button("Login", type="primary"):
        if TOOL_PASSWORD != "CHANGE_TO_YOUR_NEW_PASSWORD" and password == TOOL_PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password. Check your Tool Password.")

    st.stop()

# ---------------- MAIN APP ----------------
st.title("✉️ AI SEO Email Outreach")
st.caption("Business email outreach manager")

# ---------------- GMAIL SETTINGS ----------------
st.sidebar.title("📧 Gmail Connection")

gmail_address = st.sidebar.text_input(
    "Gmail Address",
    placeholder="yourname@gmail.com"
)

gmail_app_password = st.sidebar.text_input(
    "Gmail App Password",
    type="password",
    placeholder="Enter Gmail App Password"
)

sender_name = st.sidebar.text_input(
    "Sender Name",
    value="SEO Team"
)

st.sidebar.info(
    "Use a Gmail App Password, not your normal Gmail login password. "
    "Do not share it or save it in a public repository."
)

# ---------------- HELPER FUNCTIONS ----------------
def normalize_email(value):
    return str(value).strip().lower().strip(",;")

def valid_email(value):
    return bool(re.fullmatch(
        r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+",
        value.strip()
    ))

def read_email_file(uploaded_file):
    if uploaded_file is None:
        return []

    name = uploaded_file.name.lower()

    try:
        if name.endswith(".csv"):
            df = pd.read_csv(uploaded_file, header=None, dtype=str)
        elif name.endswith(".xlsx") or name.endswith(".xls"):
            df = pd.read_excel(uploaded_file, header=None, dtype=str)
        elif name.endswith(".txt"):
            content = uploaded_file.getvalue().decode(
                "utf-8-sig", errors="replace"
            )
            return re.findall(
                r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+",
                content
            )
        else:
            st.error("Please upload CSV, TXT or Excel file.")
            return []

        found = []
        for cell in df.to_numpy().flatten():
            if pd.isna(cell):
                continue
            text = str(cell)
            found.extend(re.findall(
                r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+",
                text
            ))
        return found

    except Exception as error:
        st.error(f"File reading error: {error}")
        return []

def parse_recipients(raw_text, uploaded_emails, suppressed):
    all_emails = []

    for line in raw_text.splitlines():
        all_emails.extend(re.findall(
            r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+",
            line
        ))

    all_emails.extend(uploaded_emails)

    unique = []
    duplicates = []
    invalid = []
    blocked = []
    seen = set()

    for item in all_emails:
        email = normalize_email(item)

        if not valid_email(email):
            invalid.append(email)
        elif email in seen:
            duplicates.append(email)
        elif email in suppressed:
            blocked.append(email)
        else:
            seen.add(email)
            unique.append(email)

    return unique, duplicates, invalid, blocked

def read_suppression_file(uploaded_file):
    if uploaded_file is None:
        return set()

    content = uploaded_file.getvalue().decode(
        "utf-8-sig", errors="replace"
    )

    found = re.findall(
        r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+",
        content
    )
    return {normalize_email(x) for x in found}

# ---------------- EMAIL COMPOSER ----------------
st.subheader("📝 Email Campaign")

subject = st.text_input(
    "Email Subject",
    placeholder="Quick question about your website"
)

template = st.text_area(
    "Email Template",
    height=220,
    placeholder="Hi,\n\nI noticed your website and wanted to ask..."
)

st.caption("Use {sender} to insert the sender name.")

# ---------------- RECIPIENTS ----------------
st.subheader("📂 Email List")

raw_emails = st.text_area(
    "Paste email addresses (one per line)",
    height=150,
    placeholder="example@company.com"
)

uploaded_file = st.file_uploader(
    "Upload Email List (CSV, TXT or Excel)",
    type=["csv", "txt", "xlsx", "xls"]
)

suppression_upload = st.file_uploader(
    "Upload Do-Not-Email / Unsubscribe List",
    type=["csv", "txt"]
)

uploaded_emails = read_email_file(uploaded_file)
suppressed = read_suppression_file(suppression_upload)

# ---------------- VALIDATE AND PREVIEW ----------------
recipients, duplicates, invalid, blocked = parse_recipients(
    raw_emails,
    uploaded_emails,
    suppressed
)

st.subheader("📊 Email List Summary")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Valid Unique", len(recipients))
col2.metric("Duplicates", len(duplicates))
col3.metric("Invalid", len(invalid))
col4.metric("Suppressed", len(blocked))

if recipients:
    st.success(f"{len(recipients)} unique email addresses ready for review.")
    st.dataframe(
        pd.DataFrame({"Email Address": recipients}),
        use_container_width=True
    )
else:
    st.warning("Add or upload email addresses to continue.")

# ---------------- EMAIL PREVIEW ----------------
st.subheader("👀 Email Preview")

if template:
    preview_body = template.replace("{sender}", sender_name)
    st.markdown("**Subject:** " + subject)
    st.text(preview_body)

# ---------------- SEND EMAILS ----------------
st.divider()
st.subheader("🚀 Send Emails")

st.warning(
    "Only contact relevant business recipients where your outreach is lawful "
    "and appropriate. Respect opt-outs and never email anyone on your "
    "Do-Not-Email list. A successful SMTP send does not guarantee inbox delivery."
)

confirm = st.checkbox(
    "I confirm these recipients are appropriate to contact and the list has been checked."
)

if st.button("Send Emails", type="primary"):
    if not gmail_address or not gmail_app_password:
        st.error("Enter Gmail Address and Gmail App Password in the sidebar.")

    elif not subject.strip() or not template.strip():
        st.error("Enter both Subject and Email Template.")

    elif not recipients:
        st.error("No valid recipients found.")

    elif not confirm:
        st.error("Please confirm the recipient list first.")

    else:
        # Conservative per-run limit
        send_list = recipients[:20]
        results = []

        progress = st.progress(0)
        status = st.empty()

        try:
            context = ssl.create_default_context()

            with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
                server.ehlo()
                server.starttls(context=context)
                server.ehlo()
                server.login(gmail_address, gmail_app_password)

                for index, recipient in enumerate(send_list):
                    status.write(
                        f"Processing {index + 1} of {len(send_list)}"
                    )

                    message = EmailMessage()
                    message["From"] = f"{sender_name} <{gmail_address}>"
                    message["To"] = recipient
                    message["Subject"] = subject

                    body = template.replace("{sender}", sender_name)

                    message.set_content(
                        body
                        + "\n\nIf you do not wish to receive further "
                        "emails from us, please reply with 'unsubscribe'."
                    )

                    try:
                        server.send_message(message)
                        results.append({
                            "Email": recipient,
                            "Status": "Accepted by SMTP",
                            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "Details": ""
                        })

                    except Exception as error:
                        results.append({
                            "Email": recipient,
                            "Status": "Failed",
                            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "Details": str(error)
                        })

                    progress.progress((index + 1) / len(send_list))

            st.success("Sending process finished.")

        except Exception as error:
            st.error(f"Gmail connection error: {error}")

        if results:
            report = pd.DataFrame(results)
            st.session_state["email_report"] = report

# ---------------- REPORT ----------------
if "email_report" in st.session_state:
    st.divider()
    st.subheader("📋 Sending Report")

    report = st.session_state["email_report"]
    st.dataframe(report, use_container_width=True)

    sent_count = int(
        (report["Status"] == "Accepted by SMTP").sum()
    )
    failed_count = int(
        (report["Status"] == "Failed").sum()
    )

    a, b = st.columns(2)
    a.metric("Accepted by SMTP", sent_count)
    b.metric("Failed", failed_count)

    csv_data = report.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        "⬇️ Download CSV Report",
        data=csv_data,
        file_name="email_sending_report.csv",
        mime="text/csv"
    )

# ---------------- FOOTER ----------------
st.divider()
st.caption("AI SEO Email Outreach Tool | Review recipients and follow opt-out requests.")
