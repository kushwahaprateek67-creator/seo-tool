import streamlit as st
import pandas as pd
import smtplib
import time
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 🔥 अल्ट्रा-प्रीमियम 'सेक्सी हैकर' UI
st.set_page_config(page_title="Phantom SEO Mailer", layout="centered")
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at center, #0a0f18 0%, #020202 100%);
        color: #00f3ff;
        font-family: 'Courier New', Courier, monospace;
    }
    [data-testid="stForm"] {
        border: 1px solid rgba(0, 243, 255, 0.4);
        border-radius: 12px;
        background: rgba(5, 8, 15, 0.85);
        padding: 35px;
        box-shadow: 0 0 25px rgba(0, 243, 255, 0.15), inset 0 0 15px rgba(0, 243, 255, 0.05);
        backdrop-filter: blur(5px);
    }
    h1, h2, h3, h4, p, label {
        color: #00f3ff !important;
        text-shadow: 0 0 8px rgba(0, 243, 255, 0.4);
        letter-spacing: 1px;
    }
    .stTextInput input, .stTextArea textarea {
        background-color: #020305 !important;
        color: #ffffff !important;
        border: 1px solid rgba(0, 243, 255, 0.3) !important;
        border-radius: 6px !important;
        box-shadow: inset 0 0 10px rgba(0, 243, 255, 0.05) !important;
        transition: all 0.3s ease-in-out;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border: 1px solid #00f3ff !important;
        box-shadow: 0 0 15px rgba(0, 243, 255, 0.4), inset 0 0 10px rgba(0, 243, 255, 0.2) !important;
    }
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
    [data-testid="stFormSubmitButton"] button:hover {
        background: #00f3ff !important;
        color: #000000 !important;
        box-shadow: 0 0 25px #00f3ff, 0 0 45px #00f3ff !important;
        transform: translateY(-2px);
    }
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

st.title("⚡ PHANTOM_SEO // OUTREACH_NEXUS")

mode = st.radio("SELECT_EXECUTION_PROTOCOL:", ["✍️ // MULTI_TARGET_MANUAL", "📁 // MASS_INJECTION (CSV Bulk)"])

# --- ईमेल भेजने का मेन इंजन ---
def execute_campaign(targets, sender, password, sub, msg_body):
    targets = targets[:100] 
    total = len(targets)
    
    st.info(f"⚙️ SYSTEM_ACTIVE: Initializing sequence for {total} targets...")
    progress = st.progress(0)
    status = st.empty()
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        
        for i, target_data in enumerate(targets):
            target_name = target_data['name']
            target_email = target_data['email']
            
            try:
                personalized_body = msg_body.replace("[Name]", target_name).replace("[name]", target_name)
                
                msg = MIMEMultipart()
                msg['From'] = sender
                msg['To'] = target_email
                msg['Subject'] = sub
                msg.attach(MIMEText(personalized_body, 'plain'))
                
                server.send_message(msg)
                
                progress.progress((i + 1) / total)
                status.success(f"✔️ PAYLOAD_DELIVERED: {target_email} [{i+1}/{total}]")
                
                if i < total - 1:
                    delay = random.choice([random.randint(6, 8), random.randint(12, 16)]) 
                    status.info(f"⏳ STEALTH_MODE: Cooling down for {delay} seconds...")
                    time.sleep(delay)
                    
            except Exception as e:
                st.error(f"❌ CONNECTION_LOST: {target_email} -> {e}")
                
        server.quit()
        st.success("🏁 MISSION_ACCOMPLISHED: All payloads delivered successfully.")
    except Exception as e:
        st.error(f"❌ AUTH_FAILED: Access Denied. Check App Password. -> {e}")

# ==========================================
# फ्रेम 1: मैनुअल तरीका (कॉमा या नंबर/लाइन दोनों सपोर्ट करेगा)
# ==========================================
if mode == "✍️ // MULTI_TARGET_MANUAL":
    with st.form("manual_frame"):
        st.markdown("#### [// SYSTEM_AUTHENTICATION //]")
        sender_email = st.text_input("GMAIL_ID (Operator)")
        app_password = st.text_input("APP_PASSWORD (Secret Key)", type="password")
        
        st.markdown("---")
        st.markdown("#### [// PAYLOAD_CONFIGURATION //]")
        subject = st.text_input("MAIL_SUBJECT")
        st.markdown("*(Hint: Use **[Name]** in the message box below to auto-insert the name. E.g., 'Hi [Name],')*")
        body = st.text_area("MAIL_BODY (Content)", height=150)
        
        st.markdown("---")
        st.markdown("#### [// TARGET_ACQUISITION //]")
        target_name = st.text_input("TARGET_NAME (Applies to all emails below, e.g., 'Webmaster' or 'Admin')")
        
        manual_emails = st.text_area("TARGET_EMAILS (Enter comma separated OR line-by-line / numbered list)", height=100)
        
        submit = st.form_submit_button(">> EXECUTE_PROTOCOL <<")
        
        if submit:
            if not sender_email or not app_password or not subject or not body or not manual_emails.strip():
                st.error("⚠️ ERROR: Missing critical parameters.")
            else:
                final_name = target_name.strip() if target_name.strip() else "Friend"
                
                # यह कोड कॉमा (,) और नई लाइन (\n) दोनों को संभाल लेगा
                import re
                # पहले लाइनों में तोड़ें, फिर कॉमा से तोड़ें
                lines = manual_emails.split("\n")
                extracted_emails = []
                for line in lines:
                    # अगर लाइन में कॉमा है तो उन्हें अलग करें
                    parts = line.split(",")
                    for p in parts:
                        cleaned = p.strip()
                        # नंबर (जैसे 1., 2.) या फालतू चीजें हटाने के लिए बेसिक ईमेल फ़िल्टर
                        # '@' होने पर ही ईमेल मानेगा
                        if "@" in cleaned:
                            extracted_emails.append(cleaned)
                
                targets = []
                for email in extracted_emails:
                    targets.append({"name": final_name, "email": email})
                
                # डुप्लीकेट हटाना
                unique_targets = list({t['email']: t for t in targets}.values())
                
                if unique_targets:
                    execute_campaign(unique_targets, sender_email, app_password, subject, body)
                else:
                    st.error("⚠️ FORMAT_ERROR: No valid emails found. Make sure '@' is included.")

# ==========================================
# फ्रेम 2: CSV तरीका
# ==========================================
elif mode == "📁 // MASS_INJECTION (CSV Bulk)":
    with st.form("csv_frame"):
        st.markdown("#### [// SYSTEM_AUTHENTICATION //]")
        sender_email = st.text_input("GMAIL_ID (Operator)")
        app_password = st.text_input("APP_PASSWORD (Secret Key)", type="password")
        
        st.markdown("---")
        st.markdown("#### [// PAYLOAD_CONFIGURATION //]")
        subject = st.text_input("MAIL_SUBJECT")
        st.markdown("*(Hint: Use **[Name]** in the message box below to auto-insert the name. E.g., 'Hi [Name],')*")
        body = st.text_area("MAIL_BODY (Content)", height=150)
        
        st.markdown("---")
        st.markdown("#### [// CSV_DATABASE_LINK //]")
        st.markdown("*(Required Columns in CSV: **Name** and **Email**)*")
        uploaded_file = st.file_uploader("UPLOAD_DATABASE (.csv format)", type=["csv"])
        
        submit = st.form_submit_button(">> EXECUTE_BULK_PROTOCOL <<")
        
        if submit:
            if not sender_email or not app_password or not subject or not body or uploaded_file is None:
                st.error("⚠️ ERROR: Database or parameters missing.")
            else:
                try:
                    df = pd.read_csv(uploaded_file)
                    if 'Email' in df.columns:
                        targets = []
                        for index, row in df.iterrows():
                            email_val = str(row['Email']).strip()
                            if 'Name' in df.columns and pd.notna(row['Name']):
                                name_val = str(row['Name'].strip())
                            else:
                                name_val = "Friend"
                                
                            if email_val and email_val.lower() != 'nan':
                                targets.append({"name": name_val, "email": email_val})
                                
                        if targets:
                            execute_campaign(targets, sender_email, app_password, subject, body)
                        else:
                            st.error("⚠️ SYSTEM_ERROR: No valid emails found in database.")
                    else:
                        st.error("⚠️ FORMAT_ERROR: 'Email' column not found in database.")
                except Exception as e:
                    st.error(f"⚠️ SYSTEM_ERROR: {e}")
