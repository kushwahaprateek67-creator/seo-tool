import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# पेज सेटिंग
st.set_page_config(page_title="Bulk Email Tool", layout="wide")

# हल्का बैकग्राउंड रंग और लेबल्स को डार्क (Bold & Black) करने के लिए CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #eef2f5; 
    }
    label p {
        font-weight: 800 !important;
        color: #000000 !important;
        font-size: 16px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("✉️ Bulk Email Tool")
st.markdown("---")

# लेआउट को दो भागों (कॉलम) में बाँटना
col1, col2 = st.columns(2)

# पहला भाग - अकाउंट की जानकारी
with col1:
    with st.container(border=True):  # बॉक्स के लिए
        st.subheader("1. अकाउंट डिटेल्स")
        # लेबल्स को ** लगाकर डार्क किया गया है
        sender_name = st.text_input("**Sender Name**")
        gmail_id = st.text_input("**Gmail ID**")
        app_password = st.text_input("**App Password**", type="password")

# दूसरा भाग - ईमेल मैसेज और डेटा
with col2:
    with st.container(border=True):  # बॉक्स के लिए
        st.subheader("2. संदेश और डेटा")
        subject_line = st.text_input("**Subject Line**")
        email_template = st.text_area("**Email Template**", height=100)
        data = st.text_area("**Data (Email IDs - हर लाइन में एक)**", height=100)

st.markdown("<br>", unsafe_allow_html=True)

# सेंड बटन
if st.button("🚀 Send Mail"):
    if not sender_name or not gmail_id or not app_password or not data:
        # फील्ड खाली होने पर एरर मैसेज
        st.error("⚠️ कृपया सभी ज़रूरी जानकारी (Sender Name, Gmail ID, Password और Data) भरें!")
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
                
                # यहाँ लास्ट में एनिमेशन जोड़ दिया गया है
                st.balloons() 
                
                # सक्सेस का ऑप्शन
                st.success(f"✅ शानदार! कुल {success_count} ईमेल सफलतापूर्वक भेज दिए गए!")
            except Exception as e:
                # फेल होने पर स्पष्ट एरर फील्ड
                st.error(f"❌ ईमेल भेजने में समस्या आई। एरर: {e}")
