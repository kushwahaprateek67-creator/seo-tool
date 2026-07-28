import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.subheader("Bulk Email Tool")

# केवल आपकी माँगी गई 6 चीजें
name = st.text_input("Name (आपका नाम)")
gmail_id = st.text_input("Gmail ID (आपकी ईमेल)")
app_password = st.text_input("App Password", type="password")
subject_line = st.text_input("Subject Line (विषय)")
email_template = st.text_area("Email Template (आपका मैसेज)")
email_list = st.text_area("Email List (ईमेल आईडी, कॉमा ',' लगाकर लिखें)")

# बटन
if st.button("Send Emails"):
    # चेक करना कि सभी बॉक्स भरे हैं या नहीं
    if name and gmail_id and app_password and subject_line and email_template and email_list:
        
        # कॉमा (,) से ईमेल अलग करना
        receiver_list = [email.strip() for email in email_list.split(",")]
        
        try:
            # जीमेल सर्वर से कनेक्ट करना
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(gmail_id, app_password)
            
            success_count = 0
            
            # एक-एक करके ईमेल भेजना
            for receiver_email in receiver_list:
                if receiver_email:
                    msg = MIMEMultipart()
                    msg['From'] = f"{name} <{gmail_id}>"
                    msg['To'] = receiver_email
                    msg['Subject'] = subject_line
                    
                    msg.attach(MIMEText(email_template, 'plain'))
                    
                    server.sendmail(gmail_id, receiver_email, msg.as_string())
                    success_count += 1
            
            server.quit()
            st.success(f"✅ कुल {success_count} ईमेल सफलतापूर्वक भेज दिए गए हैं!")
            
        except Exception as e:
            st.error(f"❌ एरर: {e}")
    else:
        st.warning("⚠️ कृपया ऊपर दिए गए सभी 6 बॉक्स भरें!")
