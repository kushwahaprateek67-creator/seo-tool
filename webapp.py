import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# पेज की सेटिंग
st.set_page_config(page_title="Colorful Email Automation Tool", page_icon="🎨", layout="centered")

# कलरफुल और आकर्षक Custom CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #ff416c 0%, #ff4b2b 100%);
        color: white;
        font-weight: bold;
        border-radius: 12px;
        height: 50px;
        font-size: 16px;
        border: none;
        box-shadow: 0 4px 15px rgba(255, 65, 108, 0.4);
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #ff4b2b 0%, #ff416c 100%);
        box-shadow: 0 6px 20px rgba(255, 75, 43, 0.6);
        color: #ffffff;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 10px;
        border: 2px solid #ff758c;
        background-color: #fff0f3;
    }
    .header-title {
        background: linear-gradient(90deg, #ff758c, #ff7eb3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# साइडबार को कलरफुल और स्टाइलिश बनाना
with st.sidebar:
    st.markdown("### 🎨 कलरफुल सेटिंग्स")
    st.success("आपका टूल पूरी तरह से एक्टिव है!")
    st.markdown("---")
    st.markdown("✨ **थीम:** मॉडर्न वाइब्रेंट")
    st.markdown("💻 **डेवलपर:** Prateek")

# मुख्य हेडर (कलरफुल)
st.markdown("<h1 class='header-title'>🎨 स्मार्ट ईमेल ऑटोमेशन टूल</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555; font-weight: 500;'>अब अपने ईमेल भेजें एक नए और रंगीन अंदाज़ में!</p>", unsafe_allow_html=True)
st.markdown("---")

# फॉर्म लेआउट
col1, col2 = st.columns(2)

with col1:
    sender_email = st.text_input("📤 आपका ईमेल (Sender Email)", placeholder="example@outlook.com")

with col2:
    sender_password = st.text_input("🔑 ऐप पासवर्ड (App Password)", type="password", placeholder="पासवर्ड दर्ज करें")

receiver_email = st.text_input("📥 प्राप्तकर्ता का ईमेल (Receiver Email)", placeholder="receiver@example.com")
email_subject = st.text_input("📌 विषय (Subject)", value="✨ विशेष अपडेट और सूचना")

# डिफ़ॉल्ट टेक्स्ट / मैसेज बॉक्स
default_message = """नमस्ते!

यह एक डिफ़ॉल्ट कलरफुल मैसेज है जो ऐप खुलते ही दिखाई देगा। 
आप इस टेक्स्ट को बदलकर अपना नया मैसेज लिख सकते हैं।

शुभकामनाएं! 🌟"""

email_body = st.text_area("📝 संदेश (Message Body)", value=default_message, height=160)

st.markdown("<br>", unsafe_allow_html=True)

# ईमेल भेजने का कलरफुल बटन
if st.button("🚀 रंगीन अंदाज़ में ईमेल भेजें"):
    if not sender_email or not sender_password or not receiver_email:
        st.warning("⚠️ कृपया अपनी ईमेल आईडी, पासवर्ड और प्राप्तकर्ता का ईमेल भरें!")
    else:
        with st.spinner("रॉकेट की गति से ईमेल भेजा जा रहा है... 🚀"):
            try:
                # ईमेल तैयार करना
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = receiver_email
                msg['Subject'] = email_subject
                
                msg.attach(MIMEText(email_body, 'plain'))
                
                # आउटलुक / ऑफिस 365 का SMTP सर्वर
                server = smtplib.SMTP('smtp-mail.outlook.com', 587)
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)
                server.quit()
                
                st.balloons()
                st.success("🎉 सफलतापूर्वक और शानदार तरीके से ईमेल भेज दिया गया है!")
            except Exception as e:
                st.error(f"❌ ईमेल भेजने में विफल: {e}")
