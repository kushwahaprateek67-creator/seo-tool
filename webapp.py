import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# पेज की सेटिंग (इसे हमेशा सबसे ऊपर रखना होता है)
st.set_page_config(page_title="Bulk Email Pro", page_icon="🚀", layout="centered")

# टूल को सुंदर बनाने के लिए थोड़ी सी CSS (कस्टम डिज़ाइन)
st.markdown("""
    <style>
    .stButton>button {
        background-color: #2e86de;
        color: white;
        border-radius: 8px;
        width: 100%;
        padding: 12px;
        font-size: 18px;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1e62a8;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# आकर्षक मेन हेडिंग
st.markdown("<h1 style='text-align: center; color: #2e86de;'>🚀 Bulk Email Sender Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray; font-size: 16px;'>आसानी से एक साथ कई लोगों को ईमेल भेजें</p>", unsafe_allow_html=True)
st.divider()

# सेक्शन 1: भेजने वाले की जानकारी (2 कॉलम में बाँटा गया है)
st.subheader("👤 Sender Details (आपकी जानकारी)")
col1, col2 = st.columns(2)

with col1:
    name = st.text_input("📝 Name (आपका नाम)", placeholder="उदा: Prateek Kushwaha")
    gmail_id = st.text_input("📧 Gmail ID (आपकी ईमेल)", placeholder="example@gmail.com")

with col2:
    app_password = st.text_input("🔑 App Password", type="password", placeholder="16 अंकों का ऐप पासवर्ड")

st.divider()

# सेक्शन 2: ईमेल का विषय और संदेश
st.subheader("✉️ Email Content (संदेश)")
subject_line = st.text_input("📌 Subject Line (विषय)", placeholder="ईमेल का विषय यहाँ लिखें...")
email_template = st.text_area("✍️ Email Template (मैसेज)", placeholder="अपना पूरा मैसेज यहाँ टाइप करें...", height=150)

st.divider()

# सेक्शन 3: ईमेल लिस्ट
st.subheader("👥 Recipients (पाने वालों की लिस्ट)")
email_list = st.text_area("📋 Email List", placeholder="client1@gmail.com\nclient2@gmail.com", height=150)
st.info("💡 टिप: आप ईमेल आईडी लाइन बदलकर (Enter दबाकर) या कॉमा (,) लगाकर डाल सकते हैं।")

st.write("") # थोड़ी सी खाली जगह बनाने के लिए

# ईमेल भेजने वाला बटन
if st.button("🚀 Send Emails Now"):
    if name and gmail_id and app_password and subject_line and email_template and email_list:
        
        # जब ईमेल जा रहा हो तो लोडिंग इफ़ेक्ट दिखाना
        with st.spinner('⏳ ईमेल भेजे जा रहे हैं, कृपया प्रतीक्षा करें...'):
            
            # लाइन ब्रेक को कॉमा में बदलना और खाली जगह हटाना
            cleaned_email_list = email_list.replace('\n', ',').replace('\r', ',')
            receiver_list = [email.strip() for email in cleaned_email_list.split(",") if email.strip()]
            
            try:
                # जीमेल सर्वर से कनेक्ट करना
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(gmail_id, app_password)
                
                success_count = 0
                
                # एक-एक करके ईमेल भेजना
                for receiver_email in receiver_list:
                    msg = MIMEMultipart()
                    msg['From'] = f"{name} <{gmail_id}>"
                    msg['To'] = receiver_email
                    msg['Subject'] = subject_line
                    
                    msg.attach(MIMEText(email_template, 'plain'))
                    
                    server.sendmail(gmail_id, receiver_email, msg.as_string())
                    success_count += 1
                
                server.quit()
                
                # सफलतापूर्वक भेजे जाने पर मैसेज और गुब्बारे 🎈
                st.success(f"✅ शानदार! कुल {success_count} ईमेल सफलतापूर्वक भेज दिए गए हैं।")
                st.balloons() 
                
            except Exception as e:
                st.error(f"❌ एरर: {e}")
    else:
        st.warning("⚠️ कृपया ईमेल भेजने से पहले सभी बॉक्स सही से भरें!")
