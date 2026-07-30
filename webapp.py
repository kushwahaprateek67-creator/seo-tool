import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# पेज की सेटिंग (Wide Mode)
st.set_page_config(page_title="Professional Email Automation Tool", page_icon="📧", layout="centered")

# मॉडर्न और खूबसूरत लुक के लिए Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        background-color: #0066cc;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        height: 45px;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #004c99;
        color: #ffffff;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 8px;
        border: 1px solid #ced4da;
    }
    .card {
        padding: 20px;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# साइडबार में सेटिंग्स और जानकारी
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/281/281769.png", width=70)
    st.markdown("### ⚙️ सेटिंग्स & गाइड")
    st.info("यह टूल आपके आउटलुक (Outlook) या माइक्रोसॉफ्ट अकाउंट के माध्यम से सुरक्षित रूप से ईमेल भेजता है।")
    st.markdown("---")
    st.markdown("**डेवलपर:** Prateek")
    st.markdown("**स्टेटस:** `Live & Active`")

# मुख्य हेडर
st.markdown("<h2 style='text-align: center; color: #1f2937;'>📧 स्मार्ट ईमेल ऑटोमेशन टूल</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6b7280;'>अपने ग्राहकों या दोस्तों को आसानी से प्रोफेशनल ईमेल भेजें।</p>", unsafe_allow_html=True)
st.markdown("---")

# फॉर्म लेआउट
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        sender_email = st.text_input("📤 आपका ईमेल (Sender Email)", placeholder="example@outlook.com")
    
    with col2:
        sender_password = st.text_input("🔑 ऐप पासवर्ड (App Password)", type="password", placeholder="पासवर्ड दर्ज करें")

receiver_email = st.text_input("📥 प्राप्तकर्ता का ईमेल (Receiver Email)", placeholder="receiver@example.com")
email_subject = st.text_input("📌 विषय (Subject)", value="महत्वपूर्ण अपडेट या सूचना")

# डिफ़ॉल्ट टेक्स्ट / मैसेज बॉक्स
default_message = """नमस्ते,

यह एक डिफ़ॉल्ट मैसेज है जो ऐप खुलते ही दिखाई देगा। 
आप इस टेक्स्ट को मिटाकर अपना नया मैसेज यहाँ लिख सकते हैं।

धन्यवाद!"""

email_body = st.text_area("📝 संदेश (Message Body)", value=default_message, height=160)

st.markdown("<br>", unsafe_allow_html=True)

# ईमेल भेजने का बटन
if st.button("🚀 अब ईमेल भेजें"):
    if not sender_email or not sender_password or not receiver_email:
        st.warning("⚠️ कृपया अपनी ईमेल आईडी, पासवर्ड और प्राप्तकर्ता का ईमेल भरें!")
    else:
        with st.spinner("ईमेल भेजा जा रहा है, कृपया प्रतीक्षा करें..."):
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
                
                st.success("🎉 सफलतापूर्वक ईमेल भेज दिया गया है!")
            except Exception as e:
                st.error(f"❌ ईमेल भेजने में विफल: {e}")
