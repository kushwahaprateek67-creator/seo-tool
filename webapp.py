import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# पेज सेटिंग
st.set_page_config(page_title="Bulk Email Tool", layout="wide")

# ब्लैक बैकग्राउंड और ब्लू बॉक्सेस/टेक्स्ट के लिए CSS
st.markdown("""
    <style>
    /* पूरे ऐप का बैकग्राउंड ब्लैक */
    .stApp, .stApp > header {
        background-color: #000000 !important; 
    }
    
    /* बॉक्स का डिज़ाइन (Dark Blue Box with Neon Blue Shadow/Border) */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #001122 !important; /* गहरा नीला बैकग्राउंड */
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0px 4px 15px rgba(0, 162, 255, 0.3); /* ब्लू शैडो */
        border: 2px solid #0066ff !important; /* ब्लू बॉर्डर */
    }
    
    /* सभी नाम (Labels), हेडर्स और टेक्स्ट को ब्लू और डार्क (Bold) करने के लिए */
    h1, h2, h3, label p, .stMarkdown p {
        font-weight: 800 !important;
        color: #00bfff !important; /* ब्राइट ब्लू (Cyan) कलर */
        font-size: 16px !important;
    }

    /* इनपुट फील्ड्स (टेक्स्ट बॉक्स) का रंग */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #000000 !important; /* अंदर से ब्लैक */
        color: #00bfff !important; /* लिखते समय ब्लू रंग का टेक्स्ट */
        border: 1px solid #0066ff !important; /* ब्लू बॉर्डर */
    }

    /* बटन का डिज़ाइन */
    .stButton>button {
        background-color: #0044cc !important;
        color: white !important;
        border: 2px solid #00bfff !important;
        font-weight: bold;
        border-radius: 8px;
        transition: 0.3s;
    }
    
    /* बटन पर माउस ले जाने पर रंग (Hover) */
    .stButton>button:hover {
        background-color: #00bfff !important;
        color: black !important;
        box-shadow: 0px 0px 15px #00bfff;
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
        sender_name = st.text_input("Sender Name", placeholder="अपना नाम लिखें")
        gmail_id = st.text_input("Gmail ID", placeholder="your-email@gmail.com")
        app_password = st.text_input("App Password", type="password", placeholder="16 अंकों का पासवर्ड")

# दूसरा बॉक्स - ईमेल मैसेज और डेटा
with col2:
    with st.container(border=True):  
        st.subheader("2. संदेश और डेटा")
        subject_line = st.text_input("Subject Line", placeholder="ईमेल का विषय")
        email_template = st.text_area("Email Template", height=110, placeholder="अपना मैसेज यहाँ लिखें...")
        data = st.text_area("Data (Email IDs - हर लाइन में एक)", height=110, placeholder="example1@gmail.com\nexample2@gmail.com")

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
