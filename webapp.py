import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# Password System
user_password = st.text_input("Tool open karne ke liye password dalein:", type="password")

if user_password != st.secrets["prateek"]:
    st.warning("prateek")
    st.stop() # Jab tak password sahi nahi hoga, niche ka tool load nahi hoga

# पेज सेटिंग
st.set_page_config(page_title="Bulk Email Tool", layout="centered")

# पूरे ऐप को एक "मेन फ्रेम" में फिक्स करने के लिए CSS
st.markdown("""
    <style>
    /* 1. स्क्रीन का बाहरी हिस्सा (पूरा ब्लैक) */
    .stApp, .stApp > header {
        background-color: #000000 !important; 
    }
    
    /* 2. आपका मेन फ्रेम (जिसके अंदर सब कुछ रहेगा) */
    .block-container {
        background-color: #001122 !important; /* फ्रेम के अंदर डार्क ब्लू */
        border: 3px solid #00bfff !important; /* चारो तरफ से नियॉन ब्लू बॉर्डर */
        border-radius: 20px !important; /* गोल किनारे */
        box-shadow: 0px 0px 30px rgba(0, 191, 255, 0.5) !important; /* चमकती हुई शैडो */
        padding: 40px 30px !important; /* फ्रेम के अंदर की जगह */
        margin-top: 40px !important; /* ऊपर से गैप */
        margin-bottom: 40px !important; /* नीचे से गैप */
        max-width: 900px !important; /* फ्रेम की चौड़ाई फिक्स कर दी */
    }
    
    /* 3. टेक्स्ट और हेडर्स का रंग */
    h1, h2, h3, label p, .stMarkdown p {
        font-weight: 800 !important;
        color: #00bfff !important; 
        font-size: 16px !important;
    }

    /* 4. इनपुट बॉक्स का डिज़ाइन */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #000000 !important; 
        color: #00bfff !important; 
        border: 1px solid #0066ff !important; 
        border-radius: 8px !important;
    }

    /* 5. सेंड बटन का डिज़ाइन */
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

# ----------------- फ्रेम के अंदर का कंटेंट -----------------

st.markdown("<h1 style='text-align: center;'>✉️ Bulk Email Tool</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #0066ff;'>", unsafe_allow_html=True)

# लेआउट को दो भागों में बाँटना (ताकि फॉर्म आमने-सामने रहे)
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
    email_template = st.text_area("Email Template", height=110, placeholder="अपना मैसेज यहाँ लिखें...")
    data = st.text_area("Data (Email IDs - हर लाइन में एक)", height=110, placeholder="example1@gmail.com\nexample2@gmail.com")

st.markdown("<br>", unsafe_allow_html=True)

# सेंड बटन को बीच में करने के लिए
col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
with col_b2:
    send_button = st.button("🚀 Send Mail", use_container_width=True)

# ईमेल भेजने का लॉजिक
if send_button:
    if not sender_name or not gmail_id or not app_password or not data:
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
                
                st.balloons() 
                st.success(f"✅ शानदार! कुल {success_count} ईमेल सफलतापूर्वक भेज दिए गए!")
            except Exception as e:
                st.error(f"❌ ईमेल भेजने में समस्या आई। एरर: {e}")
