import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd

# पेज की सेटिंग
st.set_page_config(page_title="Pro Email Automation Suite", page_icon="⚡", layout="wide")

# शानदार बैकग्राउंड, बॉक्स लेआउट और कलरफुल स्टाइल के लिए CSS
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

# हेडर सेक्शन
st.markdown("<h1 class='main-title'>⚡ स्मार्ट ईमेल ऑटोमेशन सूट</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #475569; font-size: 16px; font-weight: 500;'>एक ही क्लिक में सिंगल या बल्क ईमेल भेजें, बेहद शानदार और आसान तरीके से!</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# लेआउट को दो कॉलम में बांटना (पहला: क्रेडेंशियल्स, दूसरा: मैसेज और डेटा)
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("### 🔐 1. अकाउंट और सेंडर डिटेल्स")
    
    sender_name = st.text_input("👤 Sender Name (भेजने वाले का नाम)", placeholder="प्रतीक कुशवाहा")
    gmail_id = st.text_input("📧 Gmail ID (आपकी जीमेल)", placeholder="your-email@gmail.com")
    app_password = st.text_input("🔑 App Password (जीमेल ऐप पासवर्ड)", type="password", placeholder="16 अंकों का ऐप पासवर्ड यहाँ डालें")
    
    st.markdown("---")
    st.markdown("### 📂 2. Data List (बल्क ईमेल के लिए)")
    st.info("यदि आप सूची (List) के माध्यम से कई लोगों को भेजना चाहते हैं, तो 'Email' कॉलम वाली CSV फाइल यहाँ अपलोड करें:")
    uploaded_file = st.file_uploader("अपनी CSV फाइल चुनें", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success(f"फ़ाइल लोड हो गई! कुल ईमेल मिले: {len(df)}")
        st.dataframe(df.head(3))
    
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("### ✍️ 3. ईमेल टेम्पलेट और सब्जेक्ट")
    
    # अगर सिंगल भेजना हो तो उसके लिए रिसीवर ईमेल
    single_receiver = st.text_input("📥 Single Receiver Email (अगर अकेले को भेजना हो)", placeholder="receiver@example.com")
    
    subject_line = st.text_input("📌 Subject Line (विषय)", value="✨ आपके लिए महत्वपूर्ण अपडेट और जानकारी")
    
    # डिफ़ॉल्ट ईमेल टेम्पलेट
    default_template = """नमस्ते {name},

यह आपके लिए एक स्वचालित (Automated) प्रोफेशनल ईमेल है। 
आप यहाँ अपना पूरा ईमेल टेम्पलेट लिख सकते हैं।

शुभकामनाएं,
{sender}"""

    email_template = st.markdown("📝 **Email Template (यहाँ अपना फॉर्मेट लिखें)**")
    email_body = st.text_area("", value=default_template, height=220)
    
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# सेंड बटन सेंटर में
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    send_button = st.button("🚀 अब ईमेल भेजें (Send Mail)")

# ईमेल भेजने का लॉजिक
if send_button:
    if not gmail_id or not app_password or not sender_name:
        st.warning("⚠️ कृपया Sender Name, Gmail ID और App Password सही-सही भरें!")
    else:
        with st.spinner("रॉकेट की गति से ईमेल भेजे जा रहे हैं... कृपया प्रतीक्षा करें 🚀"):
            try:
                # जीमेल के लिए SMTP सर्वर (पोर्ट 587)
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(gmail_id, app_password)
                
                success_count = 0
                
                # केस 1: अगर CSV फाइल अपलोड की गई है (Data List से भेजना)
                if uploaded_file is not None and 'Email' in df.columns:
                    for index, row in df.iterrows():
                        rcv_email = row['Email']
                        rcv_name = row.get('Name', 'Valued Customer')
                        
                        # टेम्पलेट में नाम बदलना
                        personalized_body = email_body.replace("{name}", str(rcv_name)).replace("{sender}", sender_name)
                        
                        msg = MIMEMultipart()
                        msg['From'] = f"{sender_name} <{gmail_id}>"
                        msg['To'] = rcv_email
                        msg['Subject'] = subject_line
                        msg.attach(MIMEText(personalized_body, 'plain'))
                        
                        server.sendmail(gmail_id, rcv_email, msg.as_string())
                        success_count += 1
                        
                    st.balloons()
                    st.success(f"🎉 कमाल हो गया! डेटा लिस्ट से कुल {success_count} ईमेल सफलताપूर्वक भेज दिए गए हैं!")
                
                # केस 2: अगर सिंगल ईमेल भेजना है
                elif single_receiver:
                    personalized_body = email_body.replace("{name}", "Client").replace("{sender}", sender_name)
                    
                    msg = MIMEMultipart()
                    msg['From'] = f"{sender_name} <{gmail_id}>"
                    msg['To'] = single_receiver
                    msg['Subject'] = subject_line
                    msg.attach(MIMEText(personalized_body, 'plain'))
                    
                    server.sendmail(gmail_id, single_receiver, msg.as_string())
                    server.quit()
                    
                    st.balloons()
                    st.success(f"🎉 शानदार! ईमेल सफलतापूर्वक **{single_receiver}** पर भेज दिया गया है!")
                else:
                    st.warning("⚠️ कृपया या तो कोई सिंगल रिसीवर ईमेल डालें या डेटा लिस्ट (CSV) अपलोड करें!")
                    
            except Exception as e:
                st.error(f"❌ ईमेल भेजने में विफल रहा। एरर: {e}")

# नीचे मददगार गाइड (Fields Info)
st.markdown("---")
with st.expander("📌 **टूल को इस्तेमाल करने की गाइड (Fields & App Password जानकारी)**"):
    st.markdown("""
    1. **Sender Name:** यहाँ अपना या अपनी कंपनी का नाम लिखें जो प्राप्तकर्ता को दिखेगा।
    2. **Gmail ID:** अपनी असली जीमेल आईडी दर्ज करें।
    3. **App Password:** जीमेल का सामान्य पासवर्ड यहाँ **काम नहीं करेगा**। इसके लिए आपको अपने Google Account में जाकर **'App Passwords'** जनरेट करना होगा और उस 16 अंकों के कोड को यहाँ डालना होगा।
    4. **Data List (CSV):** यदि आप बल्क में मेल भेजना चाहते हैं, तो एक्सेल/नोटपैड में एक फाइल बनाएं जिसमें एक कॉलम का नाम **`Email`** और दूसरे का नाम **`Name`** हो, फिर उसे `.csv` फॉर्मेट में सेव करके यहाँ अपलोड करें।
    5. **Email Template:** आप मैसेज बॉक्स के अंदर `{name}` का उपयोग कर सकते हैं जो हर ग्राहक के नाम से बदल जाएगा।
    """)
