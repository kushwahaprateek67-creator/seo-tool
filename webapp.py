import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 1. पेज की सेटिंग (यह लाइन सबसे ऊपर होनी चाहिए)
st.set_page_config(page_title="Bulk Email Pro", page_icon="📧", layout="wide")

# 2. मेन हेडिंग
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>📧 Bulk Email Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>आसानी से एक साथ कई लोगों को प्रोफेशनल ईमेल भेजें</p>", unsafe_allow_html=True)
st.divider() # एक लाइन खींचने के लिए

# 3. फॉर्म को दो हिस्सों (Columns) में बांटना
col1, col2 = st.columns(2)

with col1:
    st.subheader("👤 प्रेषक की जानकारी (Sender Info)")
    name = st.text_input("Name (आपका नाम)", placeholder="उदा. Prateek Kushwaha")
    gmail_id = st.text_input("Gmail ID (आपकी ईमेल)", placeholder="example@gmail.com")
    app_password = st.text_input("App Password", type="password", help="जीमेल का 16 अक्षरों का ऐप पासवर्ड यहाँ डालें")

with col2:
    st.subheader("📝 ईमेल सामग्री (Email Content)")
    subject_line = st.text_input("Subject Line (विषय)", placeholder="ईमेल का विषय लिखें")
    email_template = st.text_area("Email Template (आपका मैसेज)", height=150, placeholder="नमस्ते, अपना मैसेज यहाँ लिखें...")

st.divider()

# 4. ईमेल लिस्ट का बड़ा बॉक्स
st.subheader("👥 प्राप्तकर्ताओं की सूची (Receiver List)")
email_list = st.text_area(
    "Email List (ईमेल आईडी लिखें)", 
    height=100, 
    placeholder="client1@gmail.com, client2@gmail.com\nया एक के नीचे एक लिखें"
)

st.markdown("<br>", unsafe_allow_html=True)

# 5. बटन को बीच में रखना और चौड़ा करना
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])

with col_btn2:
    send_button = st.button("🚀 Send Emails (ईमेल भेजें)", use_container_width=True)

# 6. ईमेल भेजने का लॉजिक
if send_button:
    if name and gmail_id and app_password and subject_line and email_template and email_list:
        
        # ईमेल को सही फॉर्मेट में लाना
        cleaned_email_list = email_list.replace('\n', ',').replace('\r', ',')
        receiver_list = [email.strip() for email in cleaned_email_list.split(",") if email.strip()]
        
        # ⏳ लोडिंग एनीमेशन दिखाना
        with st.spinner(f"⏳ {len(receiver_list)} लोगों को ईमेल भेजी जा रही है, कृपया प्रतीक्षा करें..."):
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
                
                # ✅ सफलता का मैसेज और गुब्बारे उड़ाना
                st.success(f"✅ बधाई हो! कुल {success_count} ईमेल सफलतापूर्वक भेज दिए गए हैं!")
                st.balloons() 
                
            except Exception as e:
                st.error(f"❌ एरर: {e}")
    else:
        st.warning("⚠️ कृपया सभी 6 बॉक्स सही से भरें!")
