import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# पेज की सेटिंग (Wide Mode)
st.set_page_config(page_title="Professional Bulk Email Tool", page_icon="⚡", layout="wide")

# शानदार बैकग्राउंड, शैडो और मॉडर्न कार्ड स्टाइल के लिए Custom CSS
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
        height: 55px;
        font-size: 18px;
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

# मुख्य शीर्षक
st.markdown("<h1 class='main-title'>⚡ स्मार्ट बल्क ईमेल ऑटोमेशन सूट</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #475569; font-size: 16px;'>सारी जानकारी एक ही पेज पर भरें और एक क्लिक में सबको मेल भेजें!</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------------------------------------------------
# सेक्शन 1: अकाउंट और सेंडर जानकारी (सबसे ऊपर एक ही लाइन में 3 बॉक्स)
# -------------------------------------------------------------------------
st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
st.markdown("### 🔐 1. अकाउंट और सेंडर जानकारी")
c1, c2, c3 = st.columns(3, gap="medium")

with c1:
    sender_name = st.text_input("👤 Sender Name (आपका नाम)", placeholder="प्रतीक कुशवाहा")
with c2:
    gmail_id = st.text_input("📧 Gmail ID (आपकी जीमेल)", placeholder="your-email@gmail.com")
with c3:
    app_password = st.text_input("🔑 App Password (16 अंकों का पासवर्ड)", type="password", placeholder="पासवर्ड यहाँ डालें")
st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------------------------
# सेक्शन 2: ईमेल लिस्ट और मैसेज टेम्पलेट (आमने-सामने दो बड़े बॉक्स)
# -------------------------------------------------------------------------
col_left, col_right = st.columns(2, gap="large")

with col_left:
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("### 📋 2. ईमेल आईडी लिस्ट (एक लाइन में एक)")
    bulk_emails_input = st.text_area(
        "यहाँ अपनी सभी ईमेल आईडी पेस्ट करें:",
        placeholder="example1@gmail.com\nexample2@gmail.com\nexample3@gmail.com",
        height=180
    )
    bulk_subject = st.text_input("📌 Subject Line (विषय)", value="✨ आपके लिए विशेष व्यावसायिक अपडेट")
    st.markdown("</div>", unsafe_allow_html=True)
    
with col_right:
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("### ✍️ 3. ईमेल टेम्पलेट और संदेश")
    bulk_template = """नमस्ते,

यह आपके लिए एक स्वचालित (Automated) बल्क ईमेल है। 
आप यहाँ अपना मैसेज कस्टमाइज़ कर सकते हैं।

शुभकामनाएं,
{sender}"""
    bulk_body = st.text_area("संदेश टेम्पलेट (Message Body)", value=bulk_template, height=215)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------------------------------------------------
# सेक्शन 3: सेंड बटन और एनिमेशन लॉजिक
# -------------------------------------------------------------------------
col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
with col_b2:
    send_bulk = st.button("🚀 सभी को एक साथ मेल भेजें")

if send_bulk:
    if not gmail_id or not app_password or not sender_name:
        st.warning("⚠️ कृपया ऊपर दिए गए बॉक्स में Sender Name, Gmail ID और App Password भरें!")
    elif not bulk_emails_input.strip():
        st.warning("⚠️ कृपया कम से कम एक ईमेल आईडी 'ईमेल आईडी लिस्ट' वाले बॉक्स में दर्ज करें!")
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
    1. **अकाउंट जानकारी:** सबसे ऊपर अपने नाम, जीमेल और ऐप पासवर्ड को भरें।
    2. **ईमेल लिस्ट:** बाईं तरफ के बॉक्स में अपनी ईमेल आईडी एक के नीचे एक (Line by Line) पेस्ट करें।
    3. **संदेश:** दाईं तरफ के बॉक्स में अपना मैसेज लिखें और नीचे दिए गए बड़े बटन से एक साथ सभी को भेज दें।
    4. **App Password:** जीमेल का सामान्य पासवर्ड काम नहीं करता। Google Account सेटिंग्स से 'App Passwords' जनरेट करके 16 अंकों का कोड इस्तेमाल करें।
    """)
