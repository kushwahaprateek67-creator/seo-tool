import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ऐप का शीर्षक
st.title("📧 मेरा ईमेल ऑटोमेशन टूल")

st.markdown("यहाँ अपनी जानकारी भरें और डिफ़ॉल्ट मैसेज को अपने हिसाब से इस्तेमाल करें:")

# यूज़र इनपुट फ़ील्ड्स
sender_email = st.text_input("आपका ईमेल (Sender Email)")
sender_password = st.text_input("ऐप पासवर्ड (App Password)", type="password")
receiver_email = st.text_input("प्राप्तकर्ता का ईमेल (Receiver Email)")
email_subject = st.text_input("विषय (Subject)", value="महत्वपूर्ण अपडेट या सूचना")

# डिफ़ॉल्ट टेक्स्ट / मैसेज बॉक्स (जिसे आप बदलना चाहते थे)
default_message = """नमस्ते,

यह एक डिफ़ॉल्ट मैसेज है जो ऐप खुलते ही दिखाई देगा। 
आप इस टेक्स्ट को मिटाकर अपना नया मैसेज यहाँ लिख सकते हैं।

धन्यवाद!"""

email_body = st.text_area("संदेश (Message Body)", value=default_message, height=150)

# ईमेल भेजने का बटन
if st.button("ईमेल भेजें"):
    if not sender_email or not sender_password or not receiver_email:
        st.warning("कृपया अपनी ईमेल आईडी, पासवर्ड और प्राप्तकर्ता का ईमेल भरें!")
    else:
        try:
            # ईमेल तैयार करना
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = email_subject
            
            msg.attach(MIMEText(email_body, 'plain'))
            
            # आउटलुक / ऑफिस 365 का SMTP सर्वर (आप चाहें तो जीमेल का भी इस्तेमाल कर सकते हैं)
            server = smtplib.SMTP('smtp-mail.outlook.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
            
            st.success("सफलतापूर्वक ईमेल भेज दिया गया है!")
        except Exception as e:
            st.error(f"ईमेल भेजने में विफल: {e}")
