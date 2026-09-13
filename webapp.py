import streamlit as st
import pandas as pd
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

st.title("✉️ Bulk Email Outreach Tool")

# सिंगल-फ्रेम UI कंटेनर
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
    
    # CSV अपलोड
    st.subheader("Upload Contacts")
    uploaded_file = st.file_uploader("Upload CSV (Max 100 Contacts)", type=["csv"])
    
    submit_button = st.form_submit_button("Start Sending Campaign")
    st.markdown('</div>', unsafe_allow_html=True)

# सेंडिंग लॉजिक
if submit_button:
    if not sender_email or not app_password or not subject or not body or not uploaded_file:
        st.error("⚠️ Please fill in all the details and upload your CSV file.")
    else:
        try:
            # CSV रीड करना
            df = pd.read_csv(uploaded_file)
            
            if 'Email' not in df.columns:
                st.error("⚠️ CSV file must contain a column named 'Email'.")
            else:
                email_list = df['Email'].dropna().tolist()[:100]
                total_emails = len(email_list)
                
                if total_emails == 0:
                    st.warning("No valid emails found in the CSV.")
                else:
                    st.info(f"🚀 Starting campaign for {total_emails} contacts...")
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # SMTP सर्वर से कनेक्ट करना
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
                            
                            # स्पैम से बचने के लिए 6 से 16 सेकंड का रैंडम डिले
                            if i < total_emails - 1:
                                delay = random.randint(6, 16)
                                status_text.info(f"⏳ Waiting {delay} seconds before next email...")
                                time.sleep(delay)
                                
                        except Exception as e:
                            st.error(f"❌ Failed to send to {receiver_email}: {e}")
                            continue # एरर आने पर न रुके, अगले ईमेल पर जाए
                    
                    server.quit()
                    status_text.success("🎉 Campaign Completed Successfully!")
                    st.balloons()
                    
        except smtplib.SMTPAuthenticationError:
            st.error("❌ SMTP Login Failed. Please double-check your Email and App Password.")
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {e}")
