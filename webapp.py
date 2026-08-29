import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time      
import random    

# --- PAGE SETTING ---
st.set_page_config(page_title="Bulk Email Tool", layout="centered")

# --- PASSWORD SYSTEM ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    user_password = st.text_input("Tool open karne ke liye password dalein:", type="password")
    
    if user_password:
        try:
            if user_password == st.secrets["my_password"]:
                st.session_state["logged_in"] = True
                st.rerun() 
            else:
                st.warning("Kripya sahi password enter karein.")
        except Exception:
            st.error("⚠️ Secrets file configure nahi hai. Kripya .streamlit/secrets.toml check karein.")
    st.stop() 

# --- CSS DESIGN ---
st.markdown("""
    <style>
    .stApp, .stApp > header { background-color: #000000 !important; }
    .block-container {
        background-color: #001122 !important; 
        border: 3px solid #00bfff !important; 
        border-radius: 20px !important; 
        box-shadow: 0px 0px 30px rgba(0, 191, 255, 0.5) !important; 
        padding: 40px 30px !important; 
        margin-top: 40px !important; 
        margin-bottom: 40px !important; 
        max-width: 900px !important; 
    }
    h1, h2, h3, label p, .stMarkdown p { font-weight: 800 !important; color: #00bfff !important; font-size: 16px !important; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { background-color: #000000 !important; color: #00bfff !important; border: 1px solid #0066ff !important; border-radius: 8px !important; }
    .stButton>button { background-color: #0044cc !important; color: white !important; border: 2px solid #00bfff !important; font-weight: bold; border-radius: 8px; transition: 0.3s; height: 50px; }
    .stButton>button:hover { background-color: #00bfff !important; color: black !important; box-shadow: 0px 0px 15px #00bfff; }
    </style>
""", unsafe_allow_html=True)

# --- MAIN FRAME CONTENT ---
st.markdown("<h1 style='text-align: center;'>✉️ Bulk Email Tool</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #0066ff;'>", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### 1. अकाउंट डिटेल्स")
    sender_name = st.text_input("Sender Name", placeholder="अपना नाम लिखें")
    gmail_id = st.text_input("Gmail ID", placeholder="your-email@gmail.com")
    app_password = st.text_input("App Password", type="password", placeholder="16 अंकों का पासवर्ड")

with col2:
    st.markdown("### 2. संदेश और डेटा")
    subject_line = st.text_input("Subject Line", placeholder="ईमेल का विषय")
    email_template = st.text_area("Email Template", height=110, placeholder="अपना मैसेज यहाँ लिखें...")
    data = st.text_area("Data (Email IDs - हर लाइन में एक)", height=110, placeholder="example1@gmail.com\nexample2@gmail.com")

st.markdown("<br>", unsafe_allow_html=True)

col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
with col_b2:
    send_button = st.button("🚀 Send Mail", use_container_width=True)

# --- EMAIL SENDING LOGIC ---
if send_button:
    if not sender_name or not gmail_id or not app_password or not data:
        st.error("⚠️ कृपया सभी ज़रूरी जानकारी (Sender Name, Gmail ID, Password और Data) भरें!")
    else:
        emails_list = [email.strip() for email in data.split('\n') if email.strip()]
        total_emails = len(emails_list)
        
        with st.spinner("ईमेल सर्वर से कनेक्ट हो रहा है..."):
            try:
                # सर्वर से कनेक्शन बनाना
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(gmail_id, app_password)
                
                success_count = 0
                failed_count = 0
                error_logs = []
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for index, rcv_email in enumerate(emails_list):
                    try:
                        # ईमेल कंटेंट तैयार करना
                        personalized_body = email_template.replace("{sender}", sender_name)
                        
                        msg = MIMEMultipart()
                        msg['From'] = f"{sender_name} <{gmail_id}>"
                        msg['To'] = rcv_email
                        msg['Subject'] = subject_line
                        msg.attach(MIMEText(personalized_body, 'plain'))
                        
                        # ईमेल सेंड करना
                        server.sendmail(gmail_id, rcv_email, msg.as_string())
                        success_count += 1
                        
                        progress_bar.progress((index + 1) / total_emails)
                        
                        # डिले लॉजिक (सर्वर कनेक्शन एक्टिव रखने के लिए)
                        if index < total_emails - 1:
                            delay_seconds = random.randint(6, 8)
                            for remaining in range(delay_seconds, 0, -1):
                                status_text.info(f"✅ {rcv_email} को भेज दिया। स्पैम से बचने के लिए अगले में {remaining} सेकंड का इंतज़ार...")
                                time.sleep(1)
                        else:
                            status_text.success(f"✅ {rcv_email} को भेज दिया। सभी ईमेल पूरे हुए!")
                            
                    except Exception as email_err:
                        # अगर किसी एक ईमेल में दिक्कत हो, तो यहाँ पकड़ी जाएगी
                        failed_count += 1
                        error_logs.append(f"{rcv_email}: {email_err}")
                        st.warning(f"⚠️ {rcv_email} पर ईमेल नहीं गया, अगले पर जा रहे हैं...")
                        time.sleep(2) # एरर के बाद 2 सेकंड रुक कर आगे बढ़े
                        progress_bar.progress((index + 1) / total_emails)
                        
                server.quit()
                
                # स्क्रीन क्लीनअप
                time.sleep(1)
                status_text.empty()
                progress_bar.empty()
                
                # फाइनल रिपोर्ट
                if success_count > 0:
                    st.balloons()
                    st.success(f"🎉 शानदार! {total_emails} में से {success_count} ईमेल सफलतापूर्वक भेज दिए गए!")
                
                if failed_count > 0:
                    st.error(f"❌ {failed_count} ईमेल फेल हो गए।")
                    with st.expander("Failed Emails की लिस्ट देखें"):
                        for log in error_logs:
                            st.write(log)
                            
            except Exception as e:
                # अगर लॉगिन या सर्वर कनेक्शन में कोई दिक्कत हो
                st.error(f"❌ सर्वर से कनेक्ट करने में समस्या आई (शायद पासवर्ड या ID गलत है)। एरर: {e}")
