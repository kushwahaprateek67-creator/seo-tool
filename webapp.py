import streamlit as st
import pandas as pd
import smtplib
import time
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# डार्क थीम और नियॉन-ब्लू बॉर्डर के लिए कस्टम CSS
st.set_page_config(page_title="Bulk Email Tool", layout="centered")
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: white;
    }
    .main-container {
        border: 2px solid #00d2ff;
        border-radius: 10px;
        padding: 25px;
        background-color: #1a1c24;
        margin-bottom: 20px;
    }
    /* रेडियो बटन को सुंदर बनाने के लिए */
    div.row-widget.stRadio > div {
        flex-direction: row;
        justify-content: center;
        background-color: #1a1c24;
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #00d2ff;
    }
    </style>
""", unsafe_allow_html=True)

st.title("✉️ Bulk Email Outreach Tool")

# ==========================================
# सबसे ऊपर से तरीका चुनने का ऑप्शन (जैसे पहले था)
# ==========================================
mode = st.radio(
    "👇 सबसे पहले ईमेल भेजने का तरीका चुनें:", 
    ["✍️ Manual Entry (बॉक्स में टाइप करें)", "📁 Bulk Send (CSV फाइल अपलोड करें)"]
)

st.markdown("---")

# --- ईमेल भेजने का मुख्य फंक्शन ---
def send_emails_logic(emails, sender_email, app_password, subject, body):
    emails = list(set(emails))[:100] # डुप्लीकेट हटाना और 100 की लिमिट
    
    total_emails = len(emails)
    st.info(f"🚀 Starting campaign for {total_emails} contacts...")
    progress_bar = st.progress(0)
    status_text = st.empty()

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)

        for i, receiver_email in enumerate(emails):
            try:
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = receiver_email
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'plain'))

                server.send_message(msg)

                progress_bar.progress((i + 1) / total_emails)
                status_text.success(f"✅ Sent to: {receiver_email} ({i+1}/{total_emails})")

                # 6-8 या 12-16 सेकंड का डिले
                if i < total_emails - 1:
                    delay = random.choice([random.randint(6, 8), random.randint(12, 16)]) 
                    status_text.info(f"⏳ Waiting {delay} seconds before next email...")
                    time.sleep(delay)

            except Exception as e:
                st.error(f"❌ Failed to send to {receiver_email}: {e}")
                continue

        server.quit()
        status_text.success("🎉 Campaign Completed Successfully!")
        st.balloons()

    except smtplib.SMTPAuthenticationError:
        st.error("❌ SMTP Login Failed. Check your App Password.")
    except Exception as e:
        st.error(f"❌ Error: {e}")


# ==========================================
# तरीका 1: सिर्फ मैनुअल (Old Style)
# ==========================================
if mode == "✍️ Manual Entry (बॉक्स में टाइप करें)":
    st.subheader("✍️ Send Emails Manually")
    
    with st.form("manual_form"):
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        
        sender_email = st.text_input("Your Gmail Address")
        app_password = st.text_input("App Password", type="password")
        
        st.markdown("---")
        subject = st.text_input("Email Subject")
        body = st.text_area("Email Message", height=150)
        
        st.markdown("---")
        manual_emails = st.text_area("Enter Email IDs (separated by comma)", placeholder="test1@gmail.com, test2@yahoo.com")
        
        submit_manual = st.form_submit_button("Send Emails Manually")
        st.markdown('</div>', unsafe_allow_html=True)
        
    if submit_manual:
        if not sender_email or not app_password or not subject or not body or not manual_emails.strip():
            st.error("⚠️ Please fill all details and enter at least one email.")
        else:
            raw_emails = manual_emails.split(",")
            clean_emails = [email.strip() for email in raw_emails if email.strip()]
            if clean_emails:
                send_emails_logic(clean_emails, sender_email, app_password, subject, body)


# ==========================================
# तरीका 2: सिर्फ CSV शीट (बिल्कुल अलग)
# ==========================================
elif mode == "📁 Bulk Send (CSV फाइल अपलोड करें)":
    st.subheader("📁 Send Bulk Emails via CSV")
    
    with st.form("csv_form"):
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        
        sender_email = st.text_input("Your Gmail Address")
        app_password = st.text_input("App Password", type="password")
        
        st.markdown("---")
        subject = st.text_input("Email Subject")
        body = st.text_area("Email Message", height=150)
        
        st.markdown("---")
        uploaded_file = st.file_uploader("Upload CSV (Max 100 Contacts)", type=["csv"])
        
        submit_csv = st.form_submit_button("Send Bulk Emails")
        st.markdown('</div>', unsafe_allow_html=True)
        
    if submit_csv:
        if not sender_email or not app_password or not subject or not body or uploaded_file is None:
            st.error("⚠️ Please fill all details and upload your CSV file.")
        else:
            try:
                df = pd.read_csv(uploaded_file)
                if 'Email' in df.columns:
                    clean_emails = df['Email'].dropna().tolist()
                    if clean_emails:
                        send_emails_logic(clean_emails, sender_email, app_password, subject, body)
                    else:
                        st.error("⚠️ No valid emails found in the CSV.")
                else:
                    st.error("⚠️ CSV file must contain a column named 'Email'.")
            except Exception as e:
                st.error(f"Error reading CSV: {e}")
