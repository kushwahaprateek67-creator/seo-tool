import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# पेज की सेटिंग
st.set_page_config(page_title="Bulk Email Automation Tool", page_icon="⚡", layout="centered")

# शानदार बैकग्राउंड, शैडो और कार्ड स्टाइल के लिए Custom CSS
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .custom-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        border: 1px solid #e2e8f0;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #0072ff 0%, #00c6ff 100%);
        color: white;
        font-weight: bold;
        border-radius: 10px;
        height: 55px;
        font-size: 18px;
        border: none;
        box-shadow: 0 5px 15px rgba(0, 114, 255, 0.4);
        transition: 0.3s;
        margin-top: 10px;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
        box-shadow: 0 8px 20px rgba(0, 198, 255, 0.6);
        color: #ffffff;
    }
    .main-title {
        background: linear-gradient(90deg, #1e3a8a, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# मुख्य शीर्षक
st.markdown("<h1 class='main-title'>⚡ स्मार्ट बल्क ईमेल टूल</h1>", unsafe_allow_html=True)
st.markdown("---")

# -------------------------------------------------------------------------
# आपके बताए गए क्रम के अनुसार फॉर्म
# -------------------------------------------------------------------------
st.markdown("<div class='custom-card'>", unsafe_allow_html=True)

# 1, 2, 3: Sender Name, Gmail ID, App Password (एक ही लाइन में ताकि जगह बचे और सुंदर लगे)
col1, col2, col3 = st.columns(3)
with col1:
    sender_name = st.text_input("1. 👤 Sender Name", placeholder="आपका नाम")
with col2:
    gmail_id = st.text_input("2. 📧 Gmail ID", placeholder="your-email@gmail.com")
with col3:
    app_password = st.text_input("3. 🔑 App Password", type="password", placeholder="16 अंकों का पासवर्ड")

st.markdown("<hr style='margin: 15px 0px; border-color: #f1f5f9;'>", unsafe_allow_html=True)

# 4. Subject Line
subject_line = st.text_input("4. 📌 Subject Line", value="✨ आपके लिए महत्वपूर्ण अपडेट")

# 5. Email Template
default_template = """नमस्ते,

यह आपके लिए एक स्वचालित (Automated) ईमेल है। 
आप यहाँ अपना मैसेज कस्टमाइज़ कर सकते हैं।

शुभकामनाएं,
{sender}"""
email_template = st.text_area("5. ✍️ Email Template", value=default_template, height=180)

# 6. Data (ईमेल लिस्ट)
data = st.text_area("6. 📋 Data (यहाँ सभी Email IDs पेस्ट करें, हर लाइन में एक)", 
                    placeholder="example1@gmail.com\nexample2@gmail.com\nexample3@gmail.com", height=150)

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------------------------
# सेंड बटन और एनिमेशन लॉजिक
# -------------------------------------------------------------------------
send_mail = st.button("🚀 ईमेल भेजें (Send Mail)")

if send_mail:
    if not sender_name or not gmail_id or not app_password:
        st.warning("⚠️ कृपया Sender Name, Gmail ID और App Password भरें!")
    elif not data.strip():
        st.warning("⚠️ कृपया Data बॉक्स में कम से कम एक ईमेल आईडी डालें!")
    else:
        # Data बॉक्स से ईमेल को अलग-अलग करना
        emails_list = [email.strip() for email in data.split('\n') if email.strip()]
        
        with st.spinner(f"रॉकेट की गति से कुल {len(emails_list)} ईमेल भेजे जा रहे हैं... 🚀"):
            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(gmail_id, app_password)
                
                success_count = 0
                for rcv_email in emails_list:
                    # टेम्पलेट में सेंडर का नाम अपने आप सेट करना
                    personalized_body = email_template.replace("{sender}", sender_name)
                    
                    msg = MIMEMultipart()
                    msg['From'] = f"{sender_name} <{gmail_id}>"
                    msg['To'] = rcv_email
                    msg['Subject'] = subject_line
                    msg.attach(MIMEText(personalized_body, 'plain'))
                    
                    server.sendmail(gmail_id, rcv_email, msg.as_string())
                    success_count += 1
                    
                server.quit()
                st.balloons() # शानदार एनिमेशन
                st.success(f"🎉 कमाल हो गया! कुल **{success_count}** लोगों को सफलतापूर्वक ईमेल भेज दिए गए हैं!")
            except Exception as e:
                st.error(f"❌ ईमेल भेजने में समस्या आई: {e}")
