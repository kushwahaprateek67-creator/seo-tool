import streamlit as st
import smtplib
import time
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ==========================================
# 🔒 टूल का पासवर्ड
# ==========================================
TOOL_PASSWORD = "Prateek@2026"

st.set_page_config(page_title="Bulk Email Tool", layout="centered")

# पूरा ओरिजिनल फ्रेम और नियॉन-ब्लू CSS
st.markdown("""
    <style>
    .stApp, .stApp > header { background-color: #000000 !important; }
    
    .block-container {
        background-color: #001122 !important;
        border: 3px solid #00bfff !important;
        border-radius: 20px !important;
        box-shadow: 0px 0px 30px rgba(0, 191, 255, 0.5) !important;
        padding: 40px 30px !important;
        margin-top: 40px !important;
        margin-bottom: 40px !important;
        max-width: 900px !important;
    }
    
    h1, h2, h3, label p, .stMarkdown p {
        font-weight: 800 !important;
        color: #00bfff !important; 
        font-size: 16px !important;
    }

    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #000000 !important; 
        color: #00bfff !important; 
        border: 1px solid #0066ff !important; 
        border-radius: 8px !important;
    }

    .stButton>button {
        background-color: #0044cc !important;
        color: white !important;
        border: 2px solid #00bfff !important;
        font-weight: bold;
        border-radius: 8px;
        transition: 0.3s;
        height: 50px;
    }
    
    .stButton>button:hover {
        background-color: #00bfff !important;
        color: black !important;
        box-shadow: 0px 0px 15px #00bfff;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- पासवर्ड वेरिफिकेशन -----------------
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.markdown("<h1 style='text-align: center;'>🔒 ACCESS CONTROL</h1>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid #0066ff;'>", unsafe_allow_html=True)
    
    col_p1, col_p2, col_p3 = st.columns([1, 2, 1])
    with col_p2:
        input_pass = st.text_input("Enter Access Key", type="password", placeholder="Enter tool password...")
        if st.button("Unlock System", use_container_width=True):
            if input_pass == TOOL_PASSWORD:
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("❌ Access Denied: Invalid Password")
    st.stop()

# ----------------- मेन फ्रेम -----------------

st.markdown("<h1 style='text-align: center;'>✉️ Phantom SEO Outreach</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #0066ff;'>", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### 1. अकाउंट डिटेल्स")
    sender_name = st.text_input("Sender Name", placeholder="अपना नाम लिखें")
    gmail_id = st.text_input("Gmail ID", placeholder="your-email@gmail.com")
    app_password = st.text_input("App Password", type="password", placeholder="16 अंकों का ऐप पासवर्ड")

with col2:
    st.markdown("### 2. संदेश और डेटा")
    subject_line = st.text_input("Subject Line", placeholder="ईमेल का विषय")
    email_template = st.text_area("Email Template", height=110, placeholder="Hi Team,\n\nMy name is {sender}...")
    st.caption("*(फॉर्मेट: हर लाइन में सिर्फ एक ईमेल आईडी पेस्ट करें)*")
    data = st.text_area("Data (Email IDs)", height=110, placeholder="info@example.com\ncontact@website.com")

st.markdown("<br>", unsafe_allow_html=True)

col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
with col_b2:
    send_button = st.button("🚀 Send Campaign", use_container_width=True)

# ----------------- ईमेल भेजने का मेन लॉजिक -----------------
if send_button:
    if not sender_name or not gmail_id or not app_password or not data.strip() or not subject_line or not email_template:
        st.error("⚠️ कृपया सभी जानकारी (Name, Gmail ID, Password, Subject, Template और Data) भरें!")
    else:
        # डेटा को प्रोसेस करना (नाम और ईमेल अलग करना)
        raw_lines = data.replace("\r", "").split("\n")
        targets = []
        for line in raw_lines:
            if "," in line and "@" in line:
                name_part, email_part = line.split(",", 1)
                targets.append({"name": name_part.strip(), "email": email_part.strip()})
            elif "@" in line:
                targets.append({"name": "Friend", "email": line.strip()}) # अगर कोई सिर्फ ईमेल डाले
                
        if not targets:
            st.error("⚠️ कोई वैध ईमेल आईडी नहीं मिली! फॉर्मेट चेक करें (Name, Email)")
        else:
            total_emails = len(targets)
            st.info(f"🚀 कुल {total_emails} ईमेल्स भेजना शुरू किया जा रहा है...")
            progress_bar = st.progress(0)
            status_box = st.empty()

            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(gmail_id, app_password)
                
                success_count = 0
                for i, target_data in enumerate(targets):
                    rcv_email = target_data['email']
                    rcv_name = target_data['name']
                    
                    try:
                        # [Name] और {sender} को असली नामों से रिप्लेस करना
                        personalized_body = email_template.replace("{sender}", sender_name).replace("[Name]", rcv_name).replace("[name]", rcv_name)
                        
                        msg = MIMEMultipart()
                        msg['From'] = f"{sender_name} <{gmail_id}>"
                        msg['To'] = rcv_email
                        msg['Subject'] = subject_line
                        msg.attach(MIMEText(personalized_body, 'plain'))
                        
                        server.sendmail(gmail_id, rcv_email, msg.as_string())
                        success_count += 1
                        
                        progress_bar.progress((i + 1) / total_emails)
                        status_box.success(f"✅ Sent ({i+1}/{total_emails}): {rcv_name} ({rcv_email})")
                        
                        # रैंडम स्मार्ट टाइमर (6 से 8 सेकंड) + लाइव काउंटडाउन
                        if i < total_emails - 1:
                            delay = random.randint(6, 8)
                            for sec in range(delay, 0, -1):
                                status_box.warning(f"⏳ Anti-Spam: अगला ईमेल {sec} सेकंड में जाएगा...")
                                time.sleep(1)
                            
                    except Exception as mail_err:
                        st.error(f"❌ Failed for {rcv_email}: {mail_err}")
                        continue
                        
                server.quit()
                
                status_box.empty() # काउंटडाउन बॉक्स हटा देगा
                st.balloons()
                st.success(f"🎉 शानदार! कुल {success_count}/{total_emails} ईमेल सफलतापूर्वक भेज दिए गए!")
                
            except Exception as e:
                st.error(f"❌ SMTP कनेक्शन या ऑथेंटिकेशन एरर (ऐप पासवर्ड चेक करें): {e}")
