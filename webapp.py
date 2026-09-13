import streamlit as st
import pandas as pd
import smtplib
import time
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 🔥 अल्ट्रा-प्रीमियम 'सेक्सी हैकर' UI
st.set_page_config(page_title="Wild Rank Mailer", layout="centered")
st.markdown("""
    <style>
    /* एकदम डीप डार्क हैकर बैकग्राउंड */
    .stApp {
        background: radial-gradient(circle at center, #0a0f18 0%, #020202 100%);
        color: #00f3ff;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* फॉर्म कंटेनर - ग्लास इफेक्ट और हैवी ग्लो */
    [data-testid="stForm"] {
        border: 1px solid rgba(0, 243, 255, 0.4);
        border-radius: 12px;
        background: rgba(5, 8, 15, 0.85);
        padding: 35px;
        box-shadow: 0 0 25px rgba(0, 243, 255, 0.15), inset 0 0 15px rgba(0, 243, 255, 0.05);
        backdrop-filter: blur(5px);
    }

    /* सभी हेडिंग्स और टेक्स्ट */
    h1, h2, h3, h4, p, label {
        color: #00f3ff !important;
        text-shadow: 0 0 8px rgba(0, 243, 255, 0.4);
        letter-spacing: 1px;
    }

    /* इनपुट बॉक्स का डिज़ाइन */
    .stTextInput input, .stTextArea textarea {
        background-color: #020305 !important;
        color: #ffffff !important;
        border: 1px solid rgba(0, 243, 255, 0.3) !important;
        border-radius: 6px !important;
        box-shadow: inset 0 0 10px rgba(0, 243, 255, 0.05) !important;
        transition: all 0.3s ease-in-out;
    }
    
    /* जब बॉक्स पर क्लिक करें तो ग्लो करे */
    .stTextInput input:focus, .stTextArea textarea:focus {
        border: 1px solid #00f3ff !important;
        box-shadow: 0 0 15px rgba(0, 243, 255, 0.4), inset 0 0 10px rgba(0, 243, 255, 0.2) !important;
    }

    /* 🔥 सुपर सेक्सी EXECUTE बटन 🔥 */
    [data-testid="stFormSubmitButton"] button {
        background: transparent !important;
        color: #00f3ff !important;
        border: 2px solid #00f3ff !important;
        border-radius: 8px !important;
        font-size: 18px !important;
        font-weight: 900 !important;
        letter-spacing: 3px !important;
        width: 100%;
        padding: 10px !important;
        transition: all 0.3s ease-in-out !important;
        box-shadow: 0 0 10px rgba(0, 243, 255, 0.2) !important;
    }
    
    /* बटन पर माउस ले जाने पर लाइट-अप इफ़ेक्ट */
    [data-testid="stFormSubmitButton"] button:hover {
        background: #00f3ff !important;
        color: #000000 !important;
        box-shadow: 0 0 25px #00f3ff, 0 0 45px #00f3ff !important;
        transform: translateY(-2px);
    }

    /* रेडियो बटन (ऑप्शन चुनने वाला) */
    div.row-widget.stRadio > div {
        flex-direction: row;
        justify-content: center;
        background-color: rgba(0, 243, 255, 0.05);
        padding: 12px;
        border: 1px solid rgba(0, 243, 255, 0.3);
        border-radius: 10px;
        margin-bottom: 25px;
        box-shadow: 0 0 15px rgba(0, 243, 255, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ WILD_RANK_SYSTEM // MAIL_BOT")

# तरीका चुनने का बटन
mode = st.radio("SELECT_EXECUTION_PROTOCOL:", ["✍️ // MANUAL_OVERRIDE", "📁 // CSV_BULK_INJECTION"])

# --- ईमेल भेजने का मेन इंजन ---
def execute_campaign(emails, sender, password, sub, msg_body):
    emails = list(set(emails))[:100]
    total = len(emails)
    
    st.info(f"⚙️ SYSTEM_ACTIVE: Initializing sequence for {total} targets...")
    progress = st.progress(0)
    status = st.empty()
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        
        for i, target in enumerate(emails):
            try:
                msg = MIMEMultipart()
                msg['From'] = sender
                msg['To'] = target
                msg['Subject'] = sub
                msg.attach(MIMEText(msg_body, 'plain'))
                
                server.send_message(msg)
                
                progress.progress((i + 1) / total)
                status.success(f"✔️ DATA_SENT_TO: {target} [{i+1}/{total}]")
                
                # कस्टम डिले
                if i < total - 1:
                    delay = random.choice([random.randint(6, 8), random.randint(12, 16)]) 
                    status.info(f"⏳ STEALTH_MODE: Cooling down for {delay} seconds...")
                    time.sleep(delay)
                    
            except Exception as e:
                st.error(f"❌ CONNECTION_LOST: {target} -> {e}")
                
        server.quit()
        st.success("🏁 MISSION_ACCOMPLISHED: All payloads delivered successfully.")
    except Exception as e:
        st.error(f"❌ AUTH_FAILED: Access Denied. Check App Password. -> {e}")

# ==========================================
# फ्रेम 1: मैनुअल तरीका
# ==========================================
if mode == "✍️ // MANUAL_OVERRIDE":
    with st.form("manual_frame"):
        st.markdown("#### [// SYSTEM_AUTHENTICATION //]")
        sender_email = st.text_input("GMAIL_ID (Operator)")
        app_password = st.text_input("APP_PASSWORD (Secret Key)", type="password")
        
        st.markdown("---")
        st.markdown("#### [// PAYLOAD_CONFIGURATION //]")
        subject = st.text_input("MAIL_SUBJECT")
        body = st.text_area("MAIL_BODY (Content)", height=150)
        
        st.markdown("---")
        st.markdown("#### [// TARGET_ACQUISITION //]")
        manual_emails = st.text_area("TARGET_EMAILS (Comma separated)")
        
        submit = st.form_submit_button(">> EXECUTE_PROTOCOL <<")
        
        if submit:
            if not sender_email or not app_password or not subject or not body or not manual_emails.strip():
                st.error("⚠️ ERROR: Missing parameters.")
            else:
                clean_emails = [e.strip() for e in manual_emails.split(",") if e.strip()]
                execute_campaign(clean_emails, sender_email, app_password, subject, body)

# ==========================================
# फ्रेम 2: CSV तरीका
# ==========================================
elif mode == "📁 // CSV_BULK_INJECTION":
    with st.form("csv_frame"):
        st.markdown("#### [// SYSTEM_AUTHENTICATION //]")
        sender_email = st.text_input("GMAIL_ID (Operator)")
        app_password = st.text_input("APP_PASSWORD (Secret Key)", type="password")
        
        st.markdown("---")
        st.markdown("#### [// PAYLOAD_CONFIGURATION //]")
        subject = st.text_input("MAIL_SUBJECT")
        body = st.text_area("MAIL_BODY (Content)", height=150)
        
        st.markdown("---")
        st.markdown("#### [// CSV_DATABASE_LINK //]")
        uploaded_file = st.file_uploader("UPLOAD_DATABASE (.csv format)", type=["csv"])
        
        submit = st.form_submit_button(">> EXECUTE_BULK_PROTOCOL <<")
        
        if submit:
            if not sender_email or not app_password or not subject or not body or uploaded_file is None:
                st.error("⚠️ ERROR: Database or parameters missing.")
            else:
                try:
                    df = pd.read_csv(uploaded_file)
                    if 'Email' in df.columns:
                        clean_emails = df['Email'].dropna().tolist()
                        execute_campaign(clean_emails, sender_email, app_password, subject, body)
                    else:
                        st.error("⚠️ FORMAT_ERROR: 'Email' column not found in database.")
                except Exception as e:
                    st.error(f"⚠️ SYSTEM_ERROR: {e}")
