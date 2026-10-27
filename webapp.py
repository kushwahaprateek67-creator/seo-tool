from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import smtplib
import time
import re
import streamlit as st

# Apna fixed password yahan set karein
MY_FIXED_PASSWORD = "Prateek@2026"

# Password System
login_box = st.empty()
user_password = login_box.text_input("Tool open karne ke liye password dalein:", type="password")

if user_password != MY_FIXED_PASSWORD:
    st.warning("Kripya sahi password enter karein.")
    st.stop()
else:
    login_box.empty()

st.set_page_config(page_title="Bulk Email Tool (Anti-Spam Spintax)", layout="centered")

st.markdown(
    """
    <style>
    .stApp, .stApp > header { background-color: #000000 !important; }
    .block-container {
        background-color: #001122 !important; border: 3px solid #00bfff !important;
        border-radius: 20px !important; box-shadow: 0px 0px 30px rgba(0, 191, 255, 0.5) !important;
        padding: 40px 30px !important; margin-top: 40px !important; margin-bottom: 40px !important;
        max-width: 900px !important;
    }
    h1, h2, h3, label p, .stMarkdown p { font-weight: 800 !important; color: #00bfff !important; font-size: 16px !important; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #000000 !important; color: #00bfff !important; 
        border: 1px solid #0066ff !important; border-radius: 8px !important;
    }
    .stButton>button {
        background-color: #0044cc !important; color: white !important;
        border: 2px solid #00bfff !important; font-weight: bold;
        border-radius: 8px; transition: 0.3s; height: 50px;
    }
    .stButton>button:hover { background-color: #00bfff !important; color: black !important; box-shadow: 0px 0px 15px #00bfff; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>✉️ Bulk Email Tool (Spintax Edition)</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #0066ff;'>", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### 1. अकाउंट्स पूल डिटेल्स")
    sender_name = st.text_input("Sender Name (Signature ke liye)", value="Prateek Kushwaha")
    accounts_data = st.text_area(
        "Gmail Accounts Pool (email:password)",
        height=280,
        placeholder="id1@gmail.com:app_password_1\nid2@gmail.com:app_password_2",
    )

with col2:
    st.markdown("### 2. संदेश और टारगेट डेटा")
    
    default_subjects = "Quick question about your content\nContent performance review\nAEO Strategy for your brand\nQuick question"
    subject_data = st.text_area("Subject Lines (हर लाइन में अलग)", value=default_subjects, height=80)

    # Naya Spintax Template! Dhyan se dekhiye [] brackets ko.
    default_template = """[Hello|Hi|Hey],

I was [reviewing|looking at] websites in your space and wanted to [ask|inquire] how your business currently tracks mentions inside AI-driven search tools.

I work with teams looking to establish a [strong|solid] presence across Google AI Overviews and generative engines methodically.

I would be happy to share a [couple of|few] key observations that could help [elevate|improve] your profile.

Would you be interested in a [brief chat|quick chat]?

[Best regards|Best|Regards],
{sender}"""

    email_template = st.text_area("Email Template (Spintax Supported)", value=default_template, height=180)
    data = st.text_area("Target Recipients", height=100)

    recipients_list = []
    if data:
        raw_recipients = data.replace(',', '\n').replace(' ', '\n').split('\n')
        recipients_list = [email.strip() for email in raw_recipients if email.strip() and '@' in email]
        if len(recipients_list) > 0:
            required_ids = (len(recipients_list) + 9) // 10  
            st.info(f"📊 **{len(recipients_list)}** वैलिड ईमेल। आज **{required_ids} Gmail IDs** लगेंगी।")

st.markdown("<br>", unsafe_allow_html=True)

col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
with col_b2:
    send_button = st.button("🚀 Start Inbox Campaign", use_container_width=True)

# Spintax Function
def spin_text(text):
    pattern = re.compile(r'\[([^\[\]]*)\]')
    while pattern.search(text):
        text = pattern.sub(lambda m: random.choice(m.group(1).split('|')), text)
    return text

if send_button:
    if not sender_name or not accounts_data or not data or not subject_data:
        st.error("⚠️ कृपया सभी जानकारी भरें!")
    else:
        subjects_list = [s.strip() for s in subject_data.split('\n') if s.strip()]
        raw_accounts = [acc.strip() for acc in accounts_data.split("\n") if acc.strip()]
        account_pool = [{"email": a.split(":", 1)[0].strip(), "password": a.split(":", 1)[1].strip()} for a in raw_accounts if ":" in a]

        if not account_pool or not recipients_list or not subjects_list:
            st.error("❌ डेटा सही फॉर्मेट में नहीं है।")
        else:
            active_accounts = random.sample(account_pool, min(130, len(account_pool)))
            total_recipients = len(recipients_list)
            recipient_index = 0
            success_count = 0

            progress_bar = st.progress(0)
            status_text = st.empty()

            for account in active_accounts:
                if recipient_index >= total_recipients:
                    break

                sender_email = account["email"]
                app_password = account["password"]
                sent_with_this_id = 0

                try:
                    server = smtplib.SMTP("smtp.gmail.com", 587)
                    server.starttls()
                    server.login(sender_email, app_password)

                    while sent_with_this_id < 10 and recipient_index < total_recipients:
                        rcv_email = recipients_list[recipient_index]
                        current_subject = random.choice(subjects_list)

                        # Apply Spintax and replace sender
                        base_body = email_template.replace("{sender}", sender_name)
                        spun_body = spin_text(base_body)

                        msg = MIMEMultipart()
                        # Header se custom name hata diya, taaki mismatch na ho
                        msg["From"] = sender_email
                        msg["To"] = rcv_email
                        msg["Subject"] = current_subject
                        msg.attach(MIMEText(spun_body, "plain"))

                        server.sendmail(sender_email, rcv_email, msg.as_string())
                        success_count += 1
                        sent_with_this_id += 1
                        recipient_index += 1

                        progress_bar.progress(min(recipient_index / total_recipients, 1.0))

                        if recipient_index < total_recipients:
                            delay_seconds = random.randint(5, 8)
                            for remaining in range(delay_seconds, 0, -1):
                                status_text.info(f"📨 ID: {sender_email} | Sent: {sent_with_this_id}/10 | Next email in {remaining}s...")
                                time.sleep(1)

                    server.quit()

                except Exception as e:
                    status_text.warning(f"⚠️ ID {sender_email} error: {e}. Moving to next ID...")
                    time.sleep(2)
                    continue

            status_text.empty()
            progress_bar.empty()
            st.balloons()
            st.success(f"✅ शानदार! कुल {success_count} ईमेल Spintax के साथ सफलतापूर्वक भेज दिए गए!")
