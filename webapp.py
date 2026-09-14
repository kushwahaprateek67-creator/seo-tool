import streamlit as st
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ==========================================
# 🔒 टूल का पासवर्ड यहाँ सेट करें
# ==========================================
TOOL_PASSWORD = "Prateek@2026"

# पेज सेटिंग
st.set_page_config(page_title="Bulk Email Tool", layout="centered")

# पूरा ओरिजिनल फ्रेम और नियॉन-ब्लू CSS
st.markdown("""
    <style>
    /* 1. स्क्रीन का बाहरी हिस्सा (पूरा ब्लैक) */
    .stApp, .stApp > header {
        background-color: #000000 !important; 
    }
    
    /* 2. आपका मेन फ्रेम */
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
    
    /* 3. टेक्स्ट और हेडर्स का रंग */
    h1, h2, h3, label p, .stMarkdown p {
        font-weight: 800 !important;
        color: #00bfff !important; 
        font-size: 16px !important;
    }

    /* 4. इनपुट बॉक्स का डिज़ाइन */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #000000 !important; 
        color: #00bfff !important; 
        border: 1px solid #0066ff !important; 
        border-radius: 8px !important;
    }

    /* 5. सेंड बटन का डिज़ाइन */
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

# ----------------- पासवर्ड वेरिफिकेशन गेट -----------------
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

# ----------------- फ्रेम के अंदर का मुख्य कंटेंट -----------------

st.markdown("<h1 style='text-align: center;'>✉️ Bulk Email Tool</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #0066ff;'>", unsafe_allow_html=True)

# लेआउट को दो भागों में बाँटना
col1, col2 = st.columns(2, gap="large")

# पहला हिस्सा - अकाउंट की जानकारी
with col1:
    st.markdown("### 1. अकाउंट डिटेल्स")
    sender_name = st.text_input("Sender Name", placeholder="अपना नाम लिखें")
    gmail_id = st.text_input("Gmail ID", placeholder="your-email@gmail.com")
    app_password = st.text_input("App Password", type="password", placeholder="16 अंकों का पासवर्ड")

# दूसरा हिस्सा - ईमेल मैसेज और डेटा
with col2:
    st.markdown("### 2. संदेश और डेटा")
    subject_line = st.text_input("Subject Line", placeholder="ईमेल का विषय")
    email_template = st.text_area("Email Template", height=110, placeholder="अपना मैसेज यहाँ लिखें... (Use {sender} for your name)")
    data = st.text_area("Data (Email IDs - हर लाइन में एक या कॉमा से)", height=110, placeholder="example1@gmail.com\nexample2@gmail.com")

st.markdown("<br>", unsafe_allow_html=True)

# सेंड बटन को बीच में करने के लिए
col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
with col_b2:
    send_button = st.button("🚀 Send Mail", use_container_width=True)

# ईमेल भेजने का लॉजिक (6 सेकंड टाइमर + प्रोग्रेस + एनिमेशन)
if send_button:
    if not sender_name or not gmail_id or not app_password or not data.strip() or not subject_line or not email_template:
        st.error("⚠️ कृपया सभी ज़रूरी जानकारी (Sender Name, Gmail ID, Password, Subject, Template और Data) भरें!")
    else:
        # कॉमा और लाइन-ब्रेक दोनों को प्रोसेस करना
        raw_lines = data.replace(",", "\n").split("\n")
        emails_list = list(dict.fromkeys([e.strip() for e in raw_lines if "@" in e.strip()]))
        
        if not emails_list:
            st.error("⚠️ कोई वैध ईमेल आईडी नहीं मिली!")
        else:
            total_emails = len(emails_list)
            st.info(f"🚀 कुल {total_emails} ईमेल्स भेजना शुरू किया जा रहा है...")
            progress_bar = st.progress(0)
            status_box = st.empty()

            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(gmail_id, app_password)
                
                success_count = 0
                for i, rcv_email in enumerate(emails_list):
                    try:
                        personalized_body = email_template.replace("{sender}", sender_name)
                        
                        msg = MIMEMultipart()
                        msg['From'] = f"{sender_name} <{gmail_id}>"
                        msg['To'] = rcv_email
                        msg['Subject'] = subject_line
                        msg.attach(MIMEText(personalized_body, 'plain'))
                        
                        server.sendmail(gmail_id, rcv_email, msg.as_string())
                        success_count += 1
                        
                        progress_bar.progress((i + 1) / total_emails)
                        status_box.success(f"✅ Sent ({i+1}/{total_emails}): {rcv_email}")
                        
                        # हर मेल के बाद 6 सेकंड का फिक्स डिले
                        if i < total_emails - 1:
                            time.sleep(6)
                            
                    except Exception as mail_err:
                        st.error(f"❌ Failed for {rcv_email}: {mail_err}")
                        continue
                        
                server.quit()
                
                # सफल होने पर एनिमेशन
                st.balloons()
                st.snow()
                st.success(f"🎉 शानदार! कुल {success_count}/{total_emails} ईमेल सफलतापूर्वक भेज दिए गए!")
                
            except Exception as e:
                st.error(f"❌ SMTP कनेक्शन या ऑथेंटिकेशन एरर: {e}")
