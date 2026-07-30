import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# पेज सेटिंग
st.set_page_config(page_title="Bulk Email Tool", layout="wide")

# बैकग्राउंड, डार्क लेबल्स और शानदार "सफ़ेद बॉक्स" (Box) के लिए CSS
st.markdown("""
    <style>
    /* पूरे ऐप का हल्का बैकग्राउंड */
    .stApp {
        background-color: #eef2f5; 
    }
    
    /* बॉक्स का डिज़ाइन (White Box with Shadow) */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff !important;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.08);
        border: 1.5px solid #d1d5db !important;
    }
    
    /* सभी नाम (Labels) को डार्क और बोल्ड करने के लिए */
    label p {
        font-weight: 800 !important;
        color: #111827 !important;
        font-size: 16px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("✉️ Bulk Email Tool")
st.markdown("---")

# लेआउट को दो भागों (कॉलम) में बाँटना
col1, col2 = st.columns(2, gap="large")

# पहला बॉक्स - अकाउंट की जानकारी
with col1:
    with st.container(border=True):  
        st.subheader("1. अकाउंट डिटेल्स")
        sender_name = st.text_input("**Sender Name**", placeholder="अपना नाम लिखें")
        gmail_id = st.text_input("**Gmail ID**", placeholder="your-email@gmail.com")
        app_password = st.text_input("**App Password**", type="password", placeholder="16 अंकों का पासवर्ड")

# दूसरा बॉक्स - ईमेल मैसेज और डेटा
with col2:
    with st.container(border=True):  
        st.subheader("2. संदेश और डेटा")
        subject_line = st.text_input("**Subject Line**", placeholder="ईमेल का विषय")
        email_template = st.text_area("**Email Template**", height=110, placeholder="अपना मैसेज यहाँ लिखें...")
        data = st.text_area("**Data (Email IDs - हर लाइन में एक)**", height=110, placeholder="example1@gmail.com\nexample2@gmail.com")

st.markdown("<br>", unsafe_allow_html=True)

# सेंड बटन सेंटर में
col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
with col_b2:
    send_button = st.button("🚀 Send Mail", use_container_width=True)

# ईमेल भेजने का लॉजिक
if send_button:
    if not sender_name or not gmail_id or not app_password or not data:
        st.error("⚠️ कृपया सभी बॉक्स की ज़रूरी जानकारी (Sender Name, Gmail ID, Password और Data) भरें!")
    else:
        emails_list = [email.strip() for email in data.split('\n') if email.strip()]
        
        with st.spinner("ईमेल भेजे जा रहे हैं, कृपया प्रतीक्षा करें..."):
            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(gmail_id, app_password)
                
                success_count = 0
                for rcv_email in emails_list:
                    personalized_body = email_template.replace("{sender}", sender_name)
                    
                    msg = MIMEMultipart()
                    msg['From'] = f"{sender_name} <{gmail_id}>"
                    msg['To'] = rcv_email
                    msg['Subject'] = subject_line
                    msg.attach(MIMEText(personalized_body, 'plain'))
                    
                    server.sendmail(gmail_id, rcv_email, msg.as_string())
                    success_count += 1
                    
                server.quit()
                
                # सफलतापूर्वक मेल जाने पर एनिमेशन
                st.balloons() 
                
                # सक्सेस का ऑप्शन
                st.success(f"✅ शानदार! कुल {success_count} ईमेल सफलतापूर्वक भेज दिए गए!")
            except Exception as e:
                st.error(f"❌ ईमेल भेजने में समस्या आई। एरर: {e}")
