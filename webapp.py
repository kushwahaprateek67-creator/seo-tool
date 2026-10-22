import streamlit as st
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.title("📧 Outlook-Style Cold Email Dashboard (SMTP/IMAP)")

# Sidebar for Account Credentials Configuration
with st.sidebar:
    st.markdown("### ⚙️ Account Settings")
    sender_email = st.text_input("Your Email", "outreach@wildrank.com")
    app_password = st.text_input("Email App Password", type="password")
    
    st.markdown("---")
    folder = st.radio("Folders", ["📥 Inbox", "📤 Send Email"])

# Function to Send Email via SMTP
def send_mail(to_addr, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_addr
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        # Gmail SMTP Server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, to_addr, msg.as_string())
        server.quit()
        return True, "Email sent successfully!"
    except Exception as e:
        return False, str(e)

# Function to Fetch Inbox via IMAP
def fetch_inbox():
    inbox_list = []
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(sender_email, app_password)
        mail.select('inbox')
        
        status, messages = mail.search(None, 'ALL')
        email_ids = messages[0].split()[-10:] # Last 10 emails
        
        for e_id in reversed(email_ids):
            res, msg_data = mail.fetch(e_id, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    inbox_list.render = {
                        "subject": msg["Subject"],
                        "from": msg["From"],
                        "date": msg["Date"]
                    }
                    inbox_list.append(inbox_list.render)
        mail.logout()
        return inbox_list
    except Exception as e:
        return []

# Main Layout Handling
if folder == "📤 Send Email":
    st.subheader("Compose & Send New Message")
    with st.form("compose_form"):
        to_email = st.text_input("To:")
        subject = st.text_input("Subject:")
        body = st.text_area("Message Body", height=150)
        submitted = st.form_submit_button("🚀 Send via SMTP")
        
        if submitted:
            if not app_password:
                st.error("Please enter your App Password in the sidebar first!")
            else:
                success, msg = send_mail(to_email, subject, body)
                if success:
                    st.success(msg)
                else:
                    st.error(f"Error: {msg}")

else:
    st.subheader("📥 Inbox (Live via IMAP)")
    if not app_password:
        st.warning("Please enter your Email and App Password in the sidebar to load your inbox.")
    else:
        with st.spinner("Fetching emails..."):
            emails = fetch_inbox()
            if emails:
                for em in emails:
                    st.markdown(f"**From:** {em['from']}  \n**Subject:** {em['subject']}  \n*Date:* {em['date']}")
                    st.markdown("---")
            else:
                st.info("No emails found or check your App Password.")
