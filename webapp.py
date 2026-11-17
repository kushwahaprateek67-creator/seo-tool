
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
    page_title="AI SEO Email Outreach",
    page_icon="✉️",
    layout="wide"
)


# ==================================================
# DARK BLUE PROFESSIONAL DESIGN
# ==================================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #06152e 0%, #0b2345 55%, #102d50 100%);
    color: #f4f7fb;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3, h4, p, label, span {
    color: #f4f7fb;
}

div[data-testid="stSidebar"] {
    background: #071a35;
    border-right: 1px solid #1d3d63;
}

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    background-color: #102b4d;
    color: #ffffff;
    border: 1px solid #315477;
    border-radius: 8px;
}

div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    border-color: #38a7ff;
    box-shadow: 0 0 0 1px #38a7ff;
}

.stButton button {
    background: linear-gradient(90deg, #0878d1, #1595f5);
    color: white;
    border: none;
    border-radius: 9px;
    font-weight: 700;
    min-height: 43px;
    padding: 0.4rem 1.2rem;
}

.stButton button:hover {
    background: linear-gradient(90deg, #1595f5, #38a7ff);
    color: white;
    border: none;
}

div[data-testid="stMetric"] {
    background: #102b4d;
    border: 1px solid #24496f;
    padding: 15px;
    border-radius: 12px;
}

div[data-testid="stAlert"] {
    border-radius: 10px;
}

hr {
    border-color: #29496b;
}

.email-preview {
    background: #ffffff;
    color: #202938;
    border-radius: 12px;
    padding: 25px;
    line-height: 1.7;
    overflow-wrap: anywhere;
}

.email-preview a {
    color: #0878d1;
    text-decoration: underline;
    font-weight: 600;
}

.small-note {
    color: #b8cce2;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)


# ==================================================
# LOGIN
# ==================================================
TOOL_PASSWORD = st.secrets.get("Prateek@2029", "")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not TOOL_PASSWORD:
    st.title("🔐 AI SEO Tool Setup")
    st.error(
        "Tool login password configure नहीं है। "
        "Streamlit Secrets में tool_password सेट करें।"
    )
    st.code('tool_password = "अपना-नया-लॉगिन-पासवर्ड"')
    st.stop()

if not st.session_state.authenticated:
    st.title("🔐 AI SEO Tool Login")
    st.caption("Prateek@2029")

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
        + "Unsubscribe: mailto:"
        + sender_email
        + "?subject=Unsubscribe"
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
