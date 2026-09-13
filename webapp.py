import streamlit as st
import smtplib
import time
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# डार्क थीम और नियॉन-ब्लू बॉर्डर
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: white;
    }
    .main-container {
        border: 2px solid #00d2ff;
        border-radius: 10px;
        padding: 20px;
        background-color: #1a1c24;
    }
    </style>
""", unsafe_allow_html=True)

st.title("✉️ Bulk Email Outreach Tool")

# एक ही फॉर्म / कंटेनर
with st.form("email_form"):
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    sender_email = st.text_input("Your Gmail Address")
    app_password = st.text_input("App Password", type="password")
    
    subject = st.text_input("Subject")
    body = st.text_area("Email Message", height=150)
    
    # ईमेल डालने का बॉक्स
    receiver_emails = st.text_area("Receiver Emails (Comma separated)")
    
    submit_button = st.form_submit_button("Start Sending")
    st.markdown('</div>', unsafe_allow_html=True)

if submit_button:
    if not sender_email or not app_password or not subject or not body or not receiver_emails:
        st.error("Please fill all fields.")
    else:
        # ईमेल लिस्ट बनाना
        email_list = [email.strip() for email in receiver_emails.split(",") if email.strip()]
        total_emails = len(email_list)
        
        st.info("Starting campaign...")
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # SMTP कनेक्शन
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, app_password)
            
            for i, email_id in enumerate(email_list):
                try:
                    # मैसेज तैयार करना
                    msg = MIMEMultipart()
                    msg['From'] = sender_email
                    msg['To'] = email_id
                    msg['Subject'] = subject
                    msg.attach(MIMEText(body, 'plain'))
                    
                    # मैसेज भेजना
                    server.send_message(msg)
                    
                    # प्रोग्रेस अपडेट
                    progress_bar.progress((i + 1) / total_emails)
                    status_text.text(f"Sent to: {email_id} ({i+1}/{total_emails})")
                    
                    # डिले (12-16 सेकंड और 6-16 का मिक्स)
                    if i < total_emails - 1:
                        time.sleep(random.randint(6, 16))
                        
                except Exception as e:
                    st.error(f"Failed to send to {email_id}: {e}")
                    continue
            
            server.quit()
            st.success("✅ All emails sent successfully!")
            
        except Exception as e:
            st.error(f"SMTP Login Failed: {e}. Check Email and App Password.")
