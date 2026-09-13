import streamlit as st
import smtplib
import time
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# डार्क थीम और नियॉन-ब्लू बॉर्डर के लिए कस्टम CSS
st.set_page_config(page_title="Bulk Email Tool", layout="centered")
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: white;
    }
    .main-container {
        border: 2px solid #00d2ff;
        border-radius: 10px;
        padding: 25px;
        background-color: #1a1c24;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("✉️ Email Outreach Tool (Manual)")

with st.form("email_form"):
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # सेंडर की डिटेल्स
    st.subheader("Sender Details")
    sender_email = st.text_input("Your Gmail Address (e.g., you@gmail.com)")
    app_password = st.text_input("App Password", type="password", help="16-character Google App Password")
    
    st.markdown("---")
    
    # ईमेल का कंटेंट
    st.subheader("Email Content")
    subject = st.text_input("Email Subject")
    body = st.text_area("Email Message", height=150)
    
    st.markdown("---")
    
    # ईमेल टाइप करने का बॉक्स
    st.subheader("Add Contacts")
    manual_emails = st.text_area(
        "Enter Email IDs (separated by comma)", 
        placeholder="test1@gmail.com, test2@yahoo.com",
        help="आप यहाँ एक या कई ईमेल आईडी कॉमा लगाकर टाइप कर सकते हैं।"
    )
    
    submit_button = st.form_submit_button("Start Sending Campaign")
    st.markdown('</div>', unsafe_allow_html=True)

# सेंडिंग लॉजिक
if submit_button:
    if not sender_email or not app_password or not subject or not body or not manual_emails.strip():
        st.error("⚠️ Please fill in all details and enter at least one email address.")
    else:
        # कॉमा (,) से अलग करके लिस्ट बनाना
        raw_emails = manual_emails.split(",")
        email_list = [email.strip() for email in raw_emails if email.strip()]
        email_list = list(set(email_list)) # डुप्लीकेट हटाना
        
        if not email_list:
            st.error("⚠️ No valid email addresses found.")
        else:
            total_emails = len(email_list)
            st.info(f"🚀 Starting campaign for {total_emails} contacts...")
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # SMTP कनेक्शन
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, app_password)
                
                for i, receiver_email in enumerate(email_list):
                    try:
                        # ईमेल तैयार करना
                        msg = MIMEMultipart()
                        msg['From'] = sender_email
                        msg['To'] = receiver_email
                        msg['Subject'] = subject
                        msg.attach(MIMEText(body, 'plain'))
                        
                        # ईमेल भेजना
                        server.send_message(msg)
                        
                        # प्रोग्रेस अपडेट
                        progress_bar.progress((i + 1) / total_emails)
                        status_text.success(f"✅ Sent to: {receiver_email} ({i+1}/{total_emails})")
                        
                        # स्पैम से बचने के लिए डिले (12-16 या 6-8 सेकंड)
                        if i < total_emails - 1:
                            delay = random.choice([random.randint(6, 8), random.randint(12, 16)]) 
                            status_text.info(f"⏳ Waiting {delay} seconds before next email...")
                            time.sleep(delay)
                            
                    except Exception as e:
                        st.error(f"❌ Failed to send to {receiver_email}: {e}")
                        continue
                
                server.quit()
                status_text.success("🎉 Campaign Completed Successfully!")
                st.balloons()
                
            except smtplib.SMTPAuthenticationError:
                st.error("❌ SMTP Login Failed. Check your App Password.")
            except Exception as e:
                st.error(f"❌ Error: {e}")
