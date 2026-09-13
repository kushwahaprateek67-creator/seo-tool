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
    div[data-testid="stTabs"] {
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("✉️ Bulk Email Outreach Tool")

# --- ईमेल भेजने का मुख्य फंक्शन (ताकि कोड बार-बार न लिखना पड़े) ---
def send_emails_list(emails):
    if not sender_email or not app_password or not subject or not body:
        st.error("⚠️ Please fill in Sender Details and Email Content first.")
        return
    
    emails = list(set(emails))[:100] # डुप्लीकेट हटाना और 100 की लिमिट
    if not emails:
        st.error("⚠️ No valid emails found.")
        return

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

                # स्पैम से बचने के लिए डिले
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
# 1. सेंडर और ईमेल की जानकारी (कॉमन सेक्शन)
# ==========================================
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.subheader("1. Sender Details & Email Content")

col1, col2 = st.columns(2)
with col1:
    sender_email = st.text_input("Your Gmail Address (e.g., you@gmail.com)")
with col2:
    app_password = st.text_input("App Password", type="password")
    
subject = st.text_input("Email Subject")
body = st.text_area("Email Message", height=150)
st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# 2. ईमेल भेजने के दो अलग-अलग तरीके (टैब में)
# ==========================================
st.subheader("2. Choose Sending Method")

# यहाँ हमने दो टैब बनाए हैं, जो स्क्रीन को दो हिस्सों में बांट देंगे
tab1, tab2 = st.tabs(["✍️ Type Emails Manually", "📁 Upload CSV File"])

# --- पहला तरीका: मैनुअल (सिर्फ बॉक्स) ---
with tab1:
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown("### Send Emails Manually")
    manual_emails = st.text_area("Enter Email IDs (separated by comma)", placeholder="test1@gmail.com, test2@yahoo.com")
    
    if st.button("Send Manually", key="btn_manual"):
        if manual_emails.strip():
            raw_emails = manual_emails.split(",")
            clean_emails = [email.strip() for email in raw_emails if email.strip()]
            send_emails_list(clean_emails)
        else:
            st.error("⚠️ Please enter at least one email address in the box.")
    st.markdown('</div>', unsafe_allow_html=True)


# --- दूसरा तरीका: CSV (सिर्फ फाइल अपलोड) ---
with tab2:
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown("### Send in Bulk (CSV)")
    uploaded_file = st.file_uploader("Upload CSV (Max 100 Contacts)", type=["csv"])
    
    if st.button("Send Bulk (CSV)", key="btn_csv"):
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                if 'Email' in df.columns:
                    clean_emails = df['Email'].dropna().tolist()
                    send_emails_list(clean_emails)
                else:
                    st.error("⚠️ CSV file must contain a column named 'Email'.")
            except Exception as e:
                st.error(f"Error reading CSV: {e}")
        else:
            st.error("⚠️ Please upload a CSV file.")
    st.markdown('</div>', unsafe_allow_html=True)
