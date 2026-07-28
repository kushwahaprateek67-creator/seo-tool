import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 1. पेज की सेटिंग (यह लाइन सबसे ऊपर होनी चाहिए)
st.set_page_config(page_title="Bulk Email Pro", page_icon="🚀", layout="wide")

# 2. ब्लैक बैकग्राउंड और स्टाइलिश डिज़ाइन के लिए कस्टम CSS
custom_css = """
<style>
/* पूरा बैकग्राउंड ब्लैक करने के लिए */
[data-testid="stAppViewContainer"] {
    background-color: #050505;
    color: #ffffff;
}
[data-testid="stHeader"] {
    background-color: rgba(0,0,0,0);
}

/* इनपुट बॉक्स का डिज़ाइन */
div.stTextInput > div > div > input, div.stTextArea > div > div > textarea {
    background-color: #1A1A1A !important;
    color: #00FF41 !important; /* टाइप करते समय मैट्रिक्स जैसा हरा टेक्स्ट */
    border: 1px solid #333333 !important;
    border-radius: 8px;
}

/* बटन का डिज़ाइन */
div.stButton > button {
    background-color: #00FF41 !important;
    color: #000000 !important;
    border-radius: 8px;
    border: none;
    font-size: 18px;
    font-weight: bold;
    transition: 0.3s;
}
div.stButton > button:hover {
    background-color: #00cc33 !important;
    box-shadow: 0px 0px 20px #00FF41; /* बटन पर चमक (Glow) */
    color: white !important;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 3. मेन हेडिंग
st.markdown("<h1 style='text-align: center; color: #00FF41;'>🚀 Bulk Email Pro (Dark Edition)</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #AAAAAA;'>आसानी से एक साथ कई लोगों को प्रोफेशनल ईमेल भेजें</p>", unsafe_allow_html=True)
st.markdown("<hr style='border-top: 1px solid #333;'>", unsafe_allow_html=True)

# 4. फॉर्म को दो हिस्सों (Columns) में बांटना
col1, col2 = st.columns(2)

with col1:
    st.markdown("<h4 style='color: #ffffff;'>👤 प्रेषक की जानकारी (Sender Info)</h4>", unsafe_allow_html=True)
    name = st.text_input("Name (आपका नाम)", placeholder="उदा. Prateek Kushwaha")
    gmail_id = st.text_input("Gmail ID (आपकी ईमेल)", placeholder="example@gmail.com")
    app_password = st.text_input("App Password", type="password", help="जीमेल का 16 अक्षरों का ऐप पासवर्ड यहाँ डालें")

with col2:
    st.markdown("<h4 style='color: #ffffff;'>📝 ईमेल सामग्री (Email Content)</h4>", unsafe_allow_html=True)
    subject_line = st.text_input("Subject Line (विषय)", placeholder="ईमेल का विषय लिखें")
    email_template = st.text_area("Email Template (आपका मैसेज)", height=183, placeholder="नमस्ते, अपना मैसेज यहाँ लिखें...")

st.markdown("<hr style='border-top: 1px solid #333;'>", unsafe_allow_html=True)

# 5. ईमेल लिस्ट का बड़ा बॉक्स
st.markdown("<h4 style='color: #ffffff;'>👥 प्राप्तकर्ताओं की सूची (Receiver List)</h4>", unsafe_allow_html=True)
email_list = st.text_area(
    "Email List (ईमेल आईडी लिखें)", 
    height=120, 
    placeholder="client1@gmail.com, client2@gmail.com\nया एक के नीचे एक लिखें"
)

st.markdown("<br>", unsafe_allow_html=True)

# 6. बटन को बीच में रखना और चौड़ा करना
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])

with col_btn2:
    send_button = st.button("🚀 SEND EMAILS", use_container_width=True)

# 7. ईमेल भेजने का लॉजिक
if send_button:
    if name and gmail_id and app_password and subject_line and email_template and email_list:
        
        # ईमेल को सही फॉर्मेट में लाना
        cleaned_email_list = email_list.replace('\n', ',').replace('\r', ',')
        receiver_list = [email.strip() for email in cleaned_email_list.split(",") if email.strip()]
        
        # ⏳ लोडिंग एनीमेशन
        with st.spinner(f"⏳ {len(receiver_list)} लोगों को ईमेल भेजी जा रही है..."):
            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(gmail_id, app_password)
                
                success_count = 0
                
                for receiver_email in receiver_list:
                    msg = MIMEMultipart()
                    msg['From'] = f"{name} <{gmail_id}>"
                    msg['To'] = receiver_email
                    msg['Subject'] = subject_line
                    
                    msg.attach(MIMEText(email_template, 'plain'))
                    
                    server.sendmail(gmail_id, receiver_email, msg.as_string())
                    success_count += 1
                
                server.quit()
                
                st.success(f"✅ मिशन पूरा हुआ! कुल {success_count} ईमेल सफलतापूर्वक भेज दिए गए हैं।")
                st.balloons() 
                
            except Exception as e:
                st.error(f"❌ एरर आ गया: {e}")
    else:
        st.warning("⚠️ कृपया सभी बॉक्स ठीक से भरें!")
