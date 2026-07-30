import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# पेज की सेटिंग
st.set_page_config(page_title="Bulk Email Automation Tool", page_icon="⚡", layout="wide")

# शानदार बैकग्राउंड और स्टाइल के लिए CSS
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .custom-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
        margin-bottom: 20px;
        border: 1px solid #e1e4e8;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #0072ff 0%, #00c6ff 100%);
        color: white;
        font-weight: bold;
        border-radius: 12px;
        height: 52px;
        font-size: 17px;
        border: none;
        box-shadow: 0 5px 15px rgba(0, 114, 255, 0.4);
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
        box-shadow: 0 8px 20px rgba(0, 198, 255, 0.6);
        color: #ffffff;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 10px;
        border: 2px solid #cbd5e1;
        background-color: #f8fafc;
    }
    .main-title {
        background: linear-gradient(90deg, #1e3a8a, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# साइडबार में क्रेडेंशियल्स
st.sidebar.markdown("### 🔐 अकाउंट क्रेडेंशियल्स")
sender_name = st.sidebar.text_input("👤 Sender Name", placeholder="प्रतीक कुशवाहा")
gmail_id = st.sidebar.text_input("📧 Gmail ID", placeholder="your-email@gmail.com")
app_password = st.sidebar.text_input("🔑 App Password", type="password", placeholder="16 अंकों का पासवर्ड")

st.sidebar.markdown("---")
st.sidebar.info("💡 यह टूल केवल बल्क डायरेक्ट मेल भेजने के लिए डिज़ाइन किया गया है।")

# मुख्य पृष्ठ - बल्क डायरेक्ट मेल
st.markdown("<h1 class='main-title'>🚀 बल्क डायरेक्ट ईमेल ऑटोमेशन</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #475569; font-size: 16px;'>नीचे दिए गए बॉक्स में एक के नीचे एक कई ईमेल आईडी पेस्ट करें और एक साथ सभी को मेल भेजें।</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("### 📋 ईमेल आईडी लिस्ट (एक लाइन में एक)")
    bulk_emails_input = st.text_area(
        "यहाँ ईमेल आईडी लिखें या पेस्ट करें:",
        placeholder="example1@gmail.com\nexample2@gmail.com\nexample3@gmail.com",
        height=180
    )
    bulk_subject = st.text_input("📌 Subject Line (विषय)", value="✨ आपके लिए विशेष व्यावसायिक अपडेट")
    st.markdown("</div>", unsafe_allow_html=True)
    
with col2:
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("### ✍️ ईमेल टेम्पलेट और संदेश")
    bulk_template = """नमस्ते,

यह आपके लिए एक स्वचालित (Automated) बल्क ईमेल है। 
आप यहाँ अपना मैसेज कस्टमाइज़ कर सकते हैं।

शुभकामनाएं,
{sender}"""
    bulk_body = st.text_area("संदेश टेम्पलेट", value=bulk_template, height=185)
    st.markdown("</div>", unsafe_allow_html=True)
    
st.markdown("<br>", unsafe_allow_html=True)
col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
with col_b2:
    send_bulk = st.button("🚀 सभी को एक साथ मेल भेजें")
    
if send_bulk:
    if not gmail_id or not app_password or not sender_name:
        st.warning("⚠️ कृपया साइडबार में अपनी Gmail ID, App Password और Sender Name भरें!")
    elif not bulk_emails_input.strip():
        st.warning("⚠️ कृपया कम से कम एक ईमेल आईडी बॉक्स में दर्ज करें!")
    else:
        # ईमेल को लाइनों के हिसाब से अलग करना
        emails_list = [email.strip() for email in bulk_emails_input.split('\n') if email.strip()]
        
        with st.spinner(f"रॉकेट की गति से कुल {len(emails_list)} ईमेल भेजे जा रहे हैं... 🚀"):
            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(gmail_id, app_password)
                
                success_count = 0
                for rcv_email in emails_list:
                    personalized_body = bulk_body.replace("{sender}", sender_name)
                    
                    msg = MIMEMultipart()
                    msg['From'] = f"{sender_name} <{gmail_id}>"
                    msg['To'] = rcv_email
                    msg['Subject'] = bulk_subject
                    msg.attach(MIMEText(personalized_body, 'plain'))
                    
                    server.sendmail(gmail_id, rcv_email, msg.as_string())
                    success_count += 1
                    
                server.quit()
                st.balloons()
                st.success(f"🎉 कमाल हो गया! कुल **{success_count}** लोगों को सफलतापूर्वक ईमेल भेज दिए गए हैं!")
            except Exception as e:
                st.error(f"❌ त्रुटि: {e}")

# नीचे मददगार गाइड
st.markdown("---")
with st.expander("📌 **टूल इस्तेमाल करने की गाइड**"):
    st.markdown("""
    - **डायरेक्ट मेल मोड:** इसमें आपको किसी भी फाइल की ज़रूरत नहीं है। बस बाईं तरफ के बड़े बॉक्स में अपनी ईमेल लिस्ट (हर लाइन में एक ईमेल) कॉपी-पेस्ट कर दें।
    - **App Password:** जीमेल का सामान्य पासवर्ड काम नहीं करता। Google Account सुरक्षा सेटिंग्स से 'App Passwords' जनरेट करके 16 अंकों का कोड साइडबार में डालें।
    """)
