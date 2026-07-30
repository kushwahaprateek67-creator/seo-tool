import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.title("Bulk Email Tool")

# एकदम सीधे और साधारण इनपुट फील्ड्स
sender_name = st.text_input("Sender Name")
gmail_id = st.text_input("Gmail ID")
app_password = st.text_input("App Password", type="password")
subject_line = st.text_input("Subject Line")
email_template = st.text_area("Email Template")
data = st.text_area("Data (Email IDs - हर लाइन में एक)")

if st.button("Send Mail"):
    if not sender_name or not gmail_id or not app_password or not data:
        st.warning("कृपया सभी ज़रूरी जानकारी भरें!")
    else:
        emails_list = [email.strip() for email in data.split('\n') if email.strip()]
        
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(gmail_id, app_password)
            
            for rcv_email in emails_list:
                personalized_body = email_template.replace("{sender}", sender_name)
                
                msg = MIMEMultipart()
                msg['From'] = f"{sender_name} <{gmail_id}>"
                msg['To'] = rcv_email
                msg['Subject'] = subject_line
                msg.attach(MIMEText(personalized_body, 'plain'))
                
                server.sendmail(gmail_id, rcv_email, msg.as_string())
                
            server.quit()
            st.success(f"सफलतापूर्वक {len(emails_list)} ईमेल भेज दिए गए!")
        except Exception as e:
            st.error(f"ईमेल भेजने में एरर: {e}")
