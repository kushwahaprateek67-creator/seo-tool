import streamlit as st
import pandas as pd
import smtplib
import time
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ⚡ प्योर हैकर लुक - डार्क बैकग्राउंड और सिंगल-फ्रेम UI 
st.set_page_config(page_title="Wild Rank Mailer", layout="centered")
st.markdown("""
    <style>
    /* पूरा बैकग्राउंड डार्क */
    .stApp {
        background-color: #050505; 
        color: #00d2ff;
    }
    /* स्ट्रीमलिट के डिफॉल्ट फॉर्म को ही सिंगल-फ्रेम बना दिया */
    [data-testid="stForm"] {
        border: 2px solid #00d2ff;
        border-radius: 8px;
        background-color: #0f1115;
        padding: 30px;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.3);
    }
    /* टेक्स्ट और लेबल्स का हैकर कलर (नियॉन ब्लू) */
    h1, h2, h3, h4, p, label {
        color: #00d2ff !important;
    }
    /* रेडियो बटन को सेंटर करने के लिए */
    div.row-widget.stRadio > div {
        flex-direction: row;
        justify-content: center;
        background-color: #0f1115;
        padding: 10px;
        border: 1px solid #00d2ff;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Wild Rank Outreach Tool")

# तरीका चुनने का बटन (ऊपर से ही दोनों को अलग कर दिया)
mode = st.radio("Select Execution Mode:", ["✍️ Manual Entry", "📁 CSV Bulk Upload"])

# --- ईमेल भेजने का मेन इंजन ---
def execute_campaign(emails, sender, password, sub, msg_body):
    emails = list(set(emails))[:100]
    total = len(emails)
    
    st.info(f"🚀 Initializing attack... Target Count: {total}")
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
                status.success(f"✅ Payload Delivered: {target} ({i+1}/{total})")
                
                # कस्टम स्लीप टाइमर (6-8 सेकंड या 12-16 सेकंड)
                if i < total - 1:
                    delay = random.choice([random.randint(6, 8), random.randint(12, 16)]) 
                    status.info(f"⏳ Waiting {delay} seconds before next payload...")
                    time.sleep(delay)
                    
            except Exception as e:
                st.error(f"❌ Failed for {target}: {e}")
                
        server.quit()
        st.success("🎉 Campaign Executed Successfully!")
    except Exception as e:
        st.error(f"❌ Authentication Error: {e}")

# ==========================================
# फ्रेम 1: मैनुअल तरीका
# ==========================================
if mode == "✍️ Manual Entry":
    with st.form("manual_frame"):
        st.markdown("### [ AUTHENTICATION ]")
        sender_email = st.text_input("Your Gmail Address")
        app_password = st.text_input("App Password", type="password")
        
        st.markdown("---")
        st.markdown("### [ PAYLOAD ]")
        subject = st.text_input("Email Subject")
        body = st.text_area("Email Message", height=150)
        
        st.markdown("---")
        st.markdown("### [ TARGETS ]")
        manual_emails = st.text_area("Enter Email IDs (comma separated)")
        
        submit = st.form_submit_button("EXECUTE [Manual]")
        
        if submit:
            if not sender_email or not app_password or not subject or not body or not manual_emails.strip():
                st.error("⚠️ All fields are required.")
            else:
                clean_emails = [e.strip() for e in manual_emails.split(",") if e.strip()]
                execute_campaign(clean_emails, sender_email, app_password, subject, body)

# ==========================================
# फ्रेम 2: CSV तरीका (बिल्कुल अलग)
# ==========================================
elif mode == "📁 CSV Bulk Upload":
    with st.form("csv_frame"):
        st.markdown("### [ AUTHENTICATION ]")
        sender_email = st.text_input("Your Gmail Address")
        app_password = st.text_input("App Password", type="password")
        
        st.markdown("---")
        st.markdown("### [ PAYLOAD ]")
        subject = st.text_input("Email Subject")
        body = st.text_area("Email Message", height=150)
        
        st.markdown("---")
        st.markdown("### [ CSV TARGETS ]")
        uploaded_file = st.file_uploader("Upload Target CSV (Max 100 Contacts)", type=["csv"])
        
        submit = st.form_submit_button("EXECUTE [Bulk CSV]")
        
        if submit:
            if not sender_email or not app_password or not subject or not body or uploaded_file is None:
                st.error("⚠️ All fields and CSV file are required.")
            else:
                try:
                    df = pd.read_csv(uploaded_file)
                    if 'Email' in df.columns:
                        clean_emails = df['Email'].dropna().tolist()
                        execute_campaign(clean_emails, sender_email, app_password, subject, body)
                    else:
                        st.error("⚠️ CSV file must contain a column named 'Email'.")
                except Exception as e:
                    st.error(f"⚠️ Error reading CSV: {e}")
