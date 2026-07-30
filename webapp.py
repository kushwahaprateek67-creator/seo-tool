import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd

# पेज की सेटिंग
st.set_page_config(page_title="Pro Email Automation Suite", page_icon="⚡", layout="wide")

# शानदार बैकग्राउंड और स्टाइल के लिए CSS
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .custom-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
        margin-bottom: 20px;
        border: 1px solid #e1e4e8;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #0072ff 0%, #00c6ff 100%);
        color: white;
        font-weight: bold;
        border-radius: 12px;
        height: 52px;
        font-size: 17px;
        border: none;
        box-shadow: 0 5px 15px rgba(0, 114, 255, 0.4);
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
        box-shadow: 0 8px 20px rgba(0, 198, 255, 0.6);
        color: #ffffff;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 10px;
        border: 2px solid #cbd5e1;
        background-color: #f8fafc;
    }
    .main-title {
        background: linear-gradient(90deg, #1e3a8a, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# साइडबार नेविगेशन
st.sidebar.markdown("### 🧭 नेविगेशन मेनू")
app_mode = st.sidebar.radio("मोड चुनें:", ["📤 सिंगल ईमेल (Single Email)", "📂 बल्क डेटा लिस्ट (CSV Bulk Mail)"])

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔐 अकाउंट क्रेडेंशियल्स")
sender_name = st.sidebar.text_input("👤 Sender Name", placeholder="प्रतीक कुशवाहा")
gmail_id = st.sidebar.text_input("📧 Gmail ID", placeholder="your-email@gmail.com")
app_password = st.sidebar.text_input("🔑 App Password", type="password", placeholder="16 अंकों का पासवर्ड")

# -------------------------------------------------------------------------
# मोड 1: सिंगल ईमेल भेजने का पेज
# -------------------------------------------------------------------------
if app_mode == "📤 सिंगल ईमेल (Single Email)":
    st.markdown("<h1 class='main-title'>⚡ सिंगल ईमेल ऑटोमेशन</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #475569; font-size: 16px;'>किसी एक व्यक्ति को प्रोफेशनल अंदाज़ में ईमेल भेजें।</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.markdown("### 📥 प्राप्तकर्ता विवरण")
        receiver_email = st.text_input("Receiver Email (प्राप्तकर्ता की मेल)", placeholder="client@example.com")
        receiver_name = st.text_input("Receiver Name (प्राप्तकर्ता का नाम)", placeholder="राहुल कुमार")
        subject_line = st.text_input("📌 Subject Line (विषय)", value="✨ आपके लिए महत्वपूर्ण अपडेट")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.markdown("### ✍️ ईमेल टेम्पलेट (Message)")
        default_template = """नमस्ते {name},

यह आपके लिए एक स्वचालित (Automated) प्रोफेशनल ईमेल है। 
आप यहाँ अपना पूरा ईमेल टेम्पलेट लिख सकते हैं।

शुभकामनाएं,
{sender}"""
        email_body = st.text_area("संदेश लिखें", value=default_template, height=185)
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
    with col_b2:
        send_single = st.button("🚀 सिंगल ईमेल भेजें")
        
    if send_single:
        if not gmail_id or not app_password or not sender_name or not receiver_email:
            st.warning("⚠️ कृपया अपने क्रेडेंशियल्स (Sidebar) और प्राप्तकर्ता का ईमेल भरें!")
        else:
            with st.spinner("ईमेल भेजा जा रहा है..."):
                try:
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(gmail_id, app_password)
                    
                    personalized_body = email_body.replace("{name}", receiver_name if receiver_name else "Client").replace("{sender}", sender_name)
                    
                    msg = MIMEMultipart()
                    msg['From'] = f"{sender_name} <{gmail_id}>"
                    msg['To'] = receiver_email
                    msg['Subject'] = subject_line
                    msg.attach(MIMEText(personalized_body, 'plain'))
                    
                    server.sendmail(gmail_id, receiver_email, msg.as_string())
                    server.quit()
                    
                    st.balloons()
                    st.success(f"🎉 शानदार! ईमेल सफलताપूर्वक **{receiver_email}** पर भेज दिया गया है!")
                except Exception as e:
                    st.error(f"❌ त्रुटि: {e}")

# -------------------------------------------------------------------------
# मोड 2: CSV फाइल / डेटा लिस्ट वाला पेज
# -------------------------------------------------------------------------
elif app_mode == "📂 बल्क डेटा लिस्ट (CSV Bulk Mail)":
    st.markdown("<h1 class='main-title'>📂 बल्क ईमेल ऑटोमेशन (CSV List)</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #475569; font-size: 16px;'>CSV फाइल अपलोड करें और एक साथ सैकड़ों लोगों को मेल भेजें।</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.markdown("### 📁 CSV फाइल अपलोड करें")
        st.info("आपकी CSV फाइल में कम से कम **'Email'** नाम का कॉलम होना ज़रूरी है। (वैकल्पिक: 'Name' कॉलम)")
        uploaded_file = st.file_uploader("अपनी CSV फाइल चुनें", type=["csv"])
        
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.success(f"फ़ाइल लोड हो गई! कुल रिकॉर्ड: {len(df)}")
            st.dataframe(df.head(3))
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.markdown("### ✍️ बल्क ईमेल टेम्पलेट और सब्जेक्ट")
        bulk_subject = st.text_input("📌 Subject Line (विषय)", value="✨ आपके लिए विशेष व्यावसायिक अपडेट")
        
        bulk_template = """नमस्ते {name},

यह आपके लिए एक स्वचालित (Automated) बल्क ईमेल है। 
आप यहाँ अपना मैसेज कस्टमाइज़ कर सकते हैं।

शुभकामनाएं,
{sender}"""
        bulk_body = st.text_area("संदेश टेम्पलेट", value=bulk_template, height=140)
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
    with col_b2:
        send_bulk = st.button("🚀 सभी को बल्क ईमेल भेजें")
        
    if send_bulk:
        if not gmail_id or not app_password or not sender_name:
            st.warning("⚠️ कृपया साइडबार में अपनी Gmail ID और App Password भरें!")
        elif uploaded_file is None:
            st.warning("⚠️ कृपया पहले अपनी CSV फाइल अपलोड करें!")
        else:
            if 'Email' not in df.columns:
                st.error("❌ आपकी CSV फाइल में 'Email' नाम का कॉलम नहीं मिला!")
            else:
                with st.spinner("रॉकेट की गति से बल्क ईमेल भेजे जा रहे हैं... 🚀"):
                    try:
                        server = smtplib.SMTP('smtp.gmail.com', 587)
                        server.starttls()
                        server.login(gmail_id, app_password)
                        
                        success_count = 0
                        for index, row in df.iterrows():
                            rcv_email = row['Email']
                            rcv_name = row.get('Name', 'Valued Customer')
                            
                            personalized_body = bulk_body.replace("{name}", str(rcv_name)).replace("{sender}", sender_name)
                            
                            msg = MIMEMultipart()
                            msg['From'] = f"{sender_name} <{gmail_id}>"
                            msg['To'] = rcv_email
                            msg['Subject'] = bulk_subject
                            msg.attach(MIMEText(personalized_body, 'plain'))
                            
                            server.sendmail(gmail_id, rcv_email, msg.as_string())
                            success_count += 1
                            
                        server.quit()
                        st.balloons()
                        st.success(f"🎉 कमाल हो गया! डेटा लिस्ट से कुल {success_count} ईमेल सफलताપूर्वक भेज दिए गए हैं!")
                    except Exception as e:
                        st.error(f"❌ त्रुटि: {e}")

# नीचे मददगार गाइड
st.markdown("---")
with st.expander("📌 **गाइड और जानकारी (App Password & CSV Format)**"):
    st.markdown("""
    - **App Password:** जीमेल का सामान्य पासवर्ड काम नहीं करता। Google Account सुरक्षा सेटिंग्स से 'App Passwords' जनरेट करके 16 अंकों का कोड साइडबार में डालें।
    - **CSV Format:** एक्सेल या नोटपैड में फाइल बनाएं जिसमें पहली लाइन में **`Email`** और **`Name`** लिखा हो, फिर उसे `.csv` के रूप में सेव करें।
    """)
