
import csv
import io
import re
import ssl
import time
import smtplib
import html
from datetime import datetime
from email.message import EmailMessage
from email.utils import formataddr
from urllib.parse import quote

import pandas as pd
import streamlit as st


# ==================================================
# PAGE SETTINGS
# ==================================================
st.set_page_config(
    page_title="SEO Email Outreach",
    page_icon="✉️",
    layout="wide"
)


# ==================================================
# DARK BLUE PROFESSIONAL DESIGN
# ==================================================
st.markdown("""
<style>
/* Cyber / hacker-inspired terminal theme */
.stApp {
    background: radial-gradient(circle at 50% 0%, #10251c 0%, #050b08 48%, #020503 100%) !important;
    color: #d9ffe5 !important;
}
.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div,
[data-testid="stSidebar"] section,
[data-testid="stSidebarContent"] {
    background: #050d09 !important;
    color: #d9ffe5 !important;
}
[data-testid="stSidebar"] { border-right: 1px solid #1c6b3a !important; }
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
h1, h2, h3, h4, p, label,
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label {
    color: #d9ffe5 !important;
}
/* Terminal green headings */
h1, h2, h3 { text-shadow: 0 0 10px rgba(0, 255, 100, .22); }
/* Inputs */
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea,
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] textarea {
    background: #07160e !important;
    color: #b8ffca !important;
    border: 1px solid #237a43 !important;
    border-radius: 6px !important;
}
div[data-testid="stTextInput"] input::placeholder,
div[data-testid="stTextArea"] textarea::placeholder,
[data-testid="stSidebar"] input::placeholder,
[data-testid="stSidebar"] textarea::placeholder {
    color: #6e9d7b !important;
    opacity: 1;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    border-color: #39ff75 !important;
    box-shadow: 0 0 0 1px #39ff75, 0 0 12px rgba(57,255,117,.18) !important;
}
.stButton button {
    background: linear-gradient(90deg, #087a35, #19c653) !important;
    color: #031108 !important;
    border: 1px solid #39ff75 !important;
    border-radius: 6px !important;
    font-weight: 800 !important;
    min-height: 43px;
    padding: 0.4rem 1.2rem;
    box-shadow: 0 0 12px rgba(57,255,117,.15);
}
.stButton button:hover {
    background: #39ff75 !important;
    color: #031108 !important;
    box-shadow: 0 0 18px rgba(57,255,117,.35) !important;
}
div[data-testid="stMetric"] {
    background: #07160e !important;
    border: 1px solid #1c6b3a !important;
    padding: 15px;
    border-radius: 8px;
}
div[data-testid="stAlert"] {
    background: #0b1d12 !important;
    border: 1px solid #237a43 !important;
    border-radius: 8px;
}
hr { border-color: #1c6b3a !important; }
.email-preview {
    background: #f7fff9;
    color: #15251a;
    border: 1px solid #39c96b;
    border-radius: 8px;
    padding: 25px;
    line-height: 1.7;
    overflow-wrap: anywhere;
}
.email-preview a { color: #087a35; text-decoration: underline; font-weight: 700; }
.small-note { color: #91c6a0; font-size: 13px; }
/* Keep form controls readable */
[data-baseweb="select"] > div { background: #07160e !important; border-color: #237a43 !important; color: #d9ffe5 !important; }
[data-testid="stCheckbox"] label, [data-testid="stRadio"] label { color: #d9ffe5 !important; }
</style>
""", unsafe_allow_html=True)


# ==================================================
# LOGIN
# ==================================================
TOOL_PASSWORD = st.secrets.get("tool_password", "")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not TOOL_PASSWORD:
    st.title("🔐 email tool")
    st.error(
        "Tool login password configure नहीं है। "
        "Streamlit Secrets में tool_password सेट करें।"
    )
    st.code('tool_password = "अपना-नया-लॉगिन-पासवर्ड"')
    st.stop()

if not st.session_state.authenticated:
    st.title("🔐 AI SEO Tool Login")
    st.caption("Please enter your private tool password.")

    password = st.text_input(
        "Enter Tool Password",
        type="password"
    )

    if st.button("Login", type="primary"):
        if password == TOOL_PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password. Please try again.")

    st.stop()


# ==================================================
# HEADER
# ==================================================
st.title("✉️ AI SEO Email Outreach")
st.caption("Professional business email outreach manager")


# ==================================================
# GMAIL SETTINGS
# ==================================================
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
    "Gmail App Password इस्तेमाल करें, "
    "अपना सामान्य Gmail password नहीं।"
)

st.sidebar.caption(
    "अपना App Password किसी के साथ साझा न करें।"
)


# ==================================================
# HELPER FUNCTIONS
# ==================================================
EMAIL_PATTERN = (
    r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+"
    r"@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+"
)


def normalize_email(value):
    return str(value).strip().lower().strip(",; ")


def valid_email(value):
    return bool(re.fullmatch(EMAIL_PATTERN, value.strip()))


def extract_emails(raw_text):
    return re.findall(EMAIL_PATTERN, raw_text or "")


def parse_recipients(raw_text, suppression_text):
    pasted_emails = extract_emails(raw_text)
    suppressed_emails = {
        normalize_email(x)
        for x in extract_emails(suppression_text)
    }

    unique = []
    duplicates = []
    invalid = []
    blocked = []
    seen = set()

    for item in pasted_emails:
        email = normalize_email(item)

        if not valid_email(email):
            invalid.append(email)

        elif email in seen:
            duplicates.append(email)

        elif email in suppressed_emails:
            blocked.append(email)

        else:
            seen.add(email)
            unique.append(email)

    return unique, duplicates, invalid, blocked


def make_email_html(body, sender, sender_email):
    safe_body = html.escape(body).replace("\n", "<br>")

    unsubscribe_url = (
        "mailto:"
        + quote(sender_email, safe="@.+-_")
        + "?subject=Unsubscribe"
    )

    return f"""
    <!DOCTYPE html>
    <html>
    <body style="
        margin:0;
        padding:20px;
        font-family:Arial,sans-serif;
        color:#222222;
        background:#ffffff;
        line-height:1.7;
    ">
        <div style="max-width:650px;margin:auto;">
            <div>{safe_body}</div>

            <br><br>

            <div style="color:#222222;">
                {html.escape(sender)}
                <br>
                <a href="mailto:{html.escape(sender_email)}"
                   style="color:#0878d1;text-decoration:none;">
                    {html.escape(sender_email)}
                </a>
                <br>
                <a href="{html.escape(unsubscribe_url, quote=True)}"
                   style="color:#0878d1;text-decoration:underline;">
                    Unsubscribe
                </a>
            </div>
        </div>
    </body>
    </html>
    """


def make_plain_body(body, sender, sender_email):
    return (
        body
        + "\n\n"
        + sender
        + "\n"
        + sender_email
        + "\n"
        + "Unsubscribe"
    )


# ==================================================
# EMAIL COMPOSER
# ==================================================
st.divider()
st.subheader("📝 Email Campaign")

subject = st.text_input(
    "Email Subject",
    placeholder="Quick question about your website"
)

template = st.text_area(
    "Email Template",
    height=220,
    placeholder=(
        "Hi,\n\n"
        "I noticed your website and wanted to ask...\n\n"
        "Regards,"
    )
)

st.caption("Use {sender} in your email template to insert your sender name.")


# ==================================================
# EMAIL LIST
# ==================================================
st.divider()
st.subheader("📋 Email List")

raw_emails = st.text_area(
    "Paste email addresses (one per line)",
    height=180,
    placeholder=(
        "example1@company.com\n"
        "example2@company.com\n"
        "example3@company.com"
    )
)

suppression_text = st.text_area(
    "Do-Not-Email / Unsubscribe List",
    height=100,
    placeholder=(
        "Paste email addresses that must not receive emails.\n"
        "One email per line."
    )
)


# ==================================================
# VALIDATE RECIPIENTS
# ==================================================
recipients, duplicates, invalid, blocked = parse_recipients(
    raw_emails,
    suppression_text
)


# ==================================================
# EMAIL LIST SUMMARY
# ==================================================
st.divider()
st.subheader("📊 Email List Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Valid Unique", len(recipients))
col2.metric("Duplicates", len(duplicates))
col3.metric("Invalid", len(invalid))
col4.metric("Suppressed", len(blocked))

if recipients:
    st.success(
        f"{len(recipients)} unique email addresses ready for review."
    )

    st.dataframe(
        pd.DataFrame({"Email Address": recipients}),
        use_container_width=True,
        hide_index=True
    )
else:
    st.warning("Paste email addresses to continue.")

if duplicates:
    with st.expander("View Duplicate Emails"):
        st.write(duplicates)

if invalid:
    with st.expander("View Invalid Entries"):
        st.write(invalid)

if blocked:
    with st.expander("View Suppressed Emails"):
        st.write(blocked)


# ==================================================
# EMAIL PREVIEW
# ==================================================
st.divider()
st.subheader("👀 Email Preview")

preview_body = template.replace("{sender}", sender_name)

if template.strip():
    st.markdown("**Subject:** " + subject)

    preview_html = make_email_html(
        preview_body,
        sender_name,
        gmail_address if gmail_address else "yourname@gmail.com"
    )

    st.markdown(
        f'<div class="email-preview">{preview_html}</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Preview shows the sender signature and clickable Unsubscribe link."
    )


# ==================================================
# SEND EMAILS
# ==================================================
st.divider()
st.subheader("🚀 Send Emails")

st.warning(
    "Only contact relevant recipients where your outreach is lawful "
    "and appropriate. Respect unsubscribe requests and never email "
    "addresses on your Do-Not-Email list. SMTP acceptance does not "
    "guarantee inbox delivery."
)

confirm = st.checkbox(
    "I confirm that these recipients are appropriate to contact "
    "and that the list has been checked."
)

if st.button("🚀 Send Emails", type="primary"):

    if not gmail_address or not gmail_app_password:
        st.error(
            "Enter Gmail Address and Gmail App Password in the sidebar."
        )

    elif not valid_email(gmail_address):
        st.error("Please enter a valid Gmail address.")

    elif not subject.strip() or not template.strip():
        st.error("Enter both Email Subject and Email Template.")

    elif not recipients:
        st.error("No valid recipients found.")

    elif not confirm:
        st.error("Please confirm the recipient list first.")

    else:
        # Maximum 20 recipients per run
        send_list = recipients[:20]

        results = []

        progress = st.progress(0)
        status = st.empty()

        try:
            context = ssl.create_default_context()

            with smtplib.SMTP(
                "smtp.gmail.com",
                587,
                timeout=30
            ) as server:

                server.ehlo()
                server.starttls(context=context)
                server.ehlo()

                server.login(
                    gmail_address,
                    gmail_app_password
                )

                for index, recipient in enumerate(send_list):

                    status.write(
                        f"Processing {index + 1} of {len(send_list)}"
                    )

                    message = EmailMessage()

                    message["From"] = formataddr(
                        (sender_name, gmail_address)
                    )
                    message["To"] = recipient
                    message["Subject"] = subject

                    # Email client unsubscribe hint
                    message["List-Unsubscribe"] = (
                        f"<mailto:{gmail_address}?subject=Unsubscribe>"
                    )

                    body = template.replace(
                        "{sender}",
                        sender_name
                    )

                    message.set_content(
                        make_plain_body(
                            body,
                            sender_name,
                            gmail_address
                        )
                    )

                    message.add_alternative(
                        make_email_html(
                            body,
                            sender_name,
                            gmail_address
                        ),
                        subtype="html"
                    )

                    try:
                        server.send_message(message)

                        results.append({
                            "Email": recipient,
                            "Status": "Accepted by SMTP",
                            "Time": datetime.now().strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                            "Details": ""
                        })

                    except Exception as error:
                        results.append({
                            "Email": recipient,
                            "Status": "Failed",
                            "Time": datetime.now().strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                            "Details": str(error)
                        })

                    progress.progress(
                        (index + 1) / len(send_list)
                    )

                    # Small pause between messages
                    time.sleep(1)

            status.success("Sending process finished.")

        except Exception as error:
            st.error(f"Gmail connection error: {error}")

        if results:
            report = pd.DataFrame(results)
            st.session_state["email_report"] = report


# ==================================================
# SENDING REPORT
# ==================================================
if "email_report" in st.session_state:

    st.divider()
    st.subheader("📋 Sending Report")

    report = st.session_state["email_report"]

    st.dataframe(
        report,
        use_container_width=True,
        hide_index=True
    )

    sent_count = int(
        (report["Status"] == "Accepted by SMTP").sum()
    )

    failed_count = int(
        (report["Status"] == "Failed").sum()
    )

    a, b = st.columns(2)

    a.metric("Accepted by SMTP", sent_count)
    b.metric("Failed", failed_count)

    csv_data = report.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        "⬇️ Download CSV Report",
        data=csv_data,
        file_name="email_sending_report.csv",
        mime="text/csv"
    )


# ==================================================
# FOOTER
# ==================================================
st.divider()

st.caption(
    "AI SEO Email Outreach Tool | Review recipients and respect opt-out requests."
)
