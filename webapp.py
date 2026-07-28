import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.subheader("ईमेल सेटिंग्स")

# स्क्रीन पर इनपुट बॉक्स बनाने का कोड
sender_name = st.text_input("भेजने वाले का नाम (Sender Name)", placeholder="जैसे: Prateek Kushwaha")
sender_email = st.text_input("आपकी जीमेल आईडी (Your Gmail)", placeholder="example@gmail.com")
sender_password = st.text_input("आपका ऐप पासवर्ड", type="password") # पासवर्ड टाइप करते समय छिपेगा
receiver_email = st.text_input("पाने वाले का ईमेल (Client/Receiver Email)")
message_body = st.text_area("अपना मैसेज यहाँ लिखें")

# जब यूजर 'ईमेल भेजें' बटन दबाएगा
if st.button("ईमेल भेजें"):
    if sender_name and sender_email and sender_password and receiver_email:
        try:
            # ईमेल तैयार करना
            msg = MIMEMultipart()
            # यहाँ आपका डाला हुआ नाम और ईमेल अपने आप सेट हो जाएगा
            msg['From'] = f"{sender_name} <{sender_email}>"
            msg['To'] = receiver_email
            msg['Subject'] = "SEO Tool से नया मैसेज"
            
            msg.attach(MIMEText(message_body, 'plain'))
            
            # ईमेल भेजने का प्रोसेस
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            server.quit()
            
            st.success("✅ ईमेल सफलतापूर्वक भेज दी गई है!")
        except Exception as e:
            st.error(f"❌ ईमेल भेजने में दिक्कत आई: {e}")
    else:
        st.warning("⚠️ कृपया ऊपर दिए गए सभी बॉक्स भरें!")
