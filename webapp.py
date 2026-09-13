import streamlit as st
import pandas as pd
import smtplib
import time
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

with st.form("email_form"):
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.subheader("Sender Details")
    sender_email = st.text_input("Your Gmail Address (e.g., you@gmail.com)")
    app_password = st.text_input("App Password", type="password", help="16-character Google App Password")
    
    st.markdown("---")
    
    st.subheader("Email Content")
    subject = st.text_input("Email Subject")
    body = st.text_area("Email Message", height=150)
    
    st.markdown("---")
    
    st.subheader("Add Contacts")
    manual_emails = st.text_area("Enter Email IDs (separated by comma)", placeholder="test1@gmail.com, test2@yahoo.com")
    
    st.markdown("**AND / OR**")
    
    uploaded_file = st.file_uploader("Upload CSV Sheet (Max 100 Contacts)", type=["csv"])
    
    submit_button = st.form_submit_button("Start Sending Campaign")
    st.markdown('</div>', unsafe_allow_html=True)

if submit_button:
    if not sender_email or not app_password or not subject or not body:
        st.error("⚠️ Please fill in all Sender and Content details.")
    else:
        email_list = []
        
        if manual_emails.strip():
            raw_emails = manual_emails.split(",")
            email_list.extend([email.strip() for email in raw_emails if email.strip()])
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                if 'Email' in df.columns:
                    email_list.extend(df['Email'].dropna().tolist())
                else:
                    st.error("⚠️ CSV file must contain a column named 'Email'.")
            except Exception as e:
                st.error(f"Error reading CSV: {e}")
        
        email_list = list(set(email_list))
        
        if not email_list:
             st.error("⚠️ Please enter emails manually or upload a CSV file.")
        else:
            email_list = email_list[:100]
            total_emails = len(email_list)
            
            st.info(f"🚀 Starting campaign for {total_emails} contacts...")
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, app_password)
                
                for i, receiver_email in enumerate(email_list):
                    try:
                        msg = MIMEMultipart()
                        msg['From'] = sender_email
                        msg['To'] = receiver_email
                        msg['Subject'] = subject
                        msg.attach(MIMEText(body, 'plain'))
                        
                        server.send_message(msg)
                        
                        progress_bar.progress((i + 1) / total_emails)
                        status_text.success(f"✅ Sent to: {receiver_email} ({i+1}/{total_emails})")
                        
                        if i < total_emails - 1:
                            delay = random.choice([random.randint(6, 8), random.randint(12, 16)]) 
                            status_text.info(f"⏳ Waiting {delay} seconds...")
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
