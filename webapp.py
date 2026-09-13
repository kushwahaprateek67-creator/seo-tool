import streamlit as st
import pandas as pd
import smtplib
import time
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# हैकर डार्क थीम और नियॉन-ब्लू बॉर्डर कॉन्फ़िगरेशन
st.set_page_config(page_title="Wild Rank Mailer", layout="centered")
st.markdown("""
    <style>
    .stApp {
        background-color: #0a0a0a; /* Deep Dark Background */
        color: #ffffff;
    }
    /* सिंगल-फ्रेम UI - नियॉन ब्लू बॉर्डर और ग्लो इफेक्ट */
    .main-container {
        border: 2px solid #00d2ff;
        box-shadow: 0 0 15px #00d2ff;
        border-radius: 8px;
        padding: 30px;
        background-color: #111111;
        margin-bottom: 20px;
    }
    h1, h2, h3, h4 {
        color: #00d2ff !important;
    }
    /* रेडियो बटन को सेंटर में रखने के लिए */
    div.row-widget.stRadio > div {
        flex-direction: row;
        justify-content: center;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Wild Rank Outreach Tool")

# तरीका चुनने का ऑप्शन (सिंगल फ्रेम के बाहर)
mode = st.radio("Select Targeting Mode:", ["Manual Entry", "CSV Bulk Upload"])

# सिंगल-फ्रेम हैकर UI (नीले बॉर्डर के अंदर)
with st.form("hacker_form"):
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.markdown("#### [1] Authentication")
    sender_email = st.text_input("Your Gmail Address")
    app_password = st.text_input("App Password", type="password")
    
    st.markdown("---")
    st.markdown("#### [2] Payload (Email Content)")
    subject = st.text_input("Subject")
    body = st.text_area("Body", height=150)
    
    st.markdown("---")
    st.markdown("#### [3] Targets")
    
    # जो तरीका ऊपर चुना है, सिर्फ वही यहाँ दिखेगा
    if mode == "Manual Entry":
        manual_emails = st.text_area("Enter Email IDs (comma separated)", placeholder="target1@gmail.com, target2@gmail.com")
        uploaded_file = None
    else:
        manual_emails = ""
        uploaded_file = st.file_uploader("Upload Target CSV", type=["csv"])
        
    submit = st.form_submit_button("EXECUTE [Start Sending]")
    st.markdown('</div>', unsafe_allow_html=True)

# सेंडिंग लॉजिक और रैंडम डिले
if submit:
    if not sender_email or not app_password or not subject or not body:
        st.error("⚠️ All authentication and payload fields are required.")
    else:
        email_list = []
        
        if mode == "Manual Entry":
            if manual_emails.strip():
                email_list = [e.strip() for e in manual_emails.split(",") if e.strip()]
            else:
                st.error("⚠️ Enter at least one target.")
        else:
            if uploaded_file is not None:
                try:
                    df = pd.read_csv(uploaded_file)
                    if 'Email' in df.columns:
                        email_list = df['Email'].dropna().tolist()
                    else:
                        st.error("⚠️ CSV must contain an 'Email' column.")
                except:
                    st.error("⚠️ Error reading CSV.")
            else:
                st.error("⚠️ Upload a CSV file.")
        
        if email_list:
            email_list = list(set(email_list))[:100]
            total = len(email_list)
            st.info(f"🚀 Initializing attack on {total} targets...")
            progress = st.progress(0)
            status = st.empty()
            
            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, app_password)
                
                for i, target in enumerate(email_list):
                    try:
                        msg = MIMEMultipart()
                        msg['From'] = sender_email
                        msg['To'] = target
                        msg['Subject'] = subject
                        msg.attach(MIMEText(body, 'plain'))
                        server.send_message(msg)
                        
                        progress.progress((i + 1) / total)
                        status.success(f"✅ Payload delivered: {target}")
                        
                        # स्पैम फिल्टर से बचने के लिए 12-16 सेकंड और 6-8 सेकंड का कस्टम डिले
                        if i < total - 1:
                            delay = random.choice([random.randint(6, 8), random.randint(12, 16)]) 
                            status.info(f"⏳ Waiting {delay} seconds before next execution...")
                            time.sleep(delay)
                            
                    except Exception as e:
                        st.error(f"❌ Failed for {target}: {e}")
                
                server.quit()
                st.success("🎉 Campaign Executed Successfully!")
            except Exception as e:
                st.error("❌ Connection Failed: Check your App Password.")
