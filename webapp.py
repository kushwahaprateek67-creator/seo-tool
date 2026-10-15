from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import smtplib
import time
import streamlit as st

# Apna fixed password yahan set karein
MY_FIXED_PASSWORD = "Prateek@2026"

# Password System
login_box = st.empty()
user_password = login_box.text_input(
    "Tool open karne ke liye password dalein:", type="password"
)

if user_password != MY_FIXED_PASSWORD:
  st.warning("Kripya sahi password enter karein.")
  st.stop()
else:
  login_box.empty()

# पेज सेटिंग
st.set_page_config(page_title="Bulk Email Tool", layout="centered")

# पूरे ऐप का CSS डिज़ाइन और JavaScript Live Clock
st.markdown(
    """
    <style>
    .stApp, .stApp > header {
        background-color: #000000 !important; 
    }
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
    h1, h2, h3, label p, .stMarkdown p {
        font-weight: 800 !important;
        color: #00bfff !important; 
        font-size: 16px !important;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #000000 !important; 
        color: #00bfff !important; 
        border: 1px solid #0066ff !important; 
        border-radius: 8px !important;
    }
    .stButton>button {
        background-color: #0044cc !important;
        color: white !important;
        border: 2px solid #00bfff !important;
        font-weight: bold;
        border-radius: 8px;
        transition: 0.3s;
        height: 50px;
    }
    .stButton>button:hover {
        background-color: #00bfff !important;
        color: black !important;
        box-shadow: 0px 0px 15px #00bfff;
    }
    </style>

    <script>
    function updateClock() {
        const tzSelect = document.getElementById('city-selector-hidden');
        if (!tzSelect) return;
        const tz = tzSelect.value;
        const options = { timeZone: tz, hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true, month: 'short', day: 'numeric', year: 'numeric' };
        const now = new Date();
        const clockElem = document.getElementById('live-running-clock');
        if (clockElem) {
            clockElem.innerText = now.toLocaleString('en-US', options);
        }
    }
    setInterval(updateClock, 1000);
    window.onload = updateClock;
    </script>
""",
    unsafe_allow_html=True,
)

# ----------------- फ्रेम के अंदर का कंटेंट -----------------

st.markdown(
    "<h1 style='text-align: center;'>✉️ Bulk Email Tool (USA Live Time"
    " Target)</h1>",
    unsafe_allow_html=True,
)
st.markdown("<hr style='border: 1px solid #0066ff;'>", unsafe_allow_html=True)

# 🇺🇸 City Target Selector
st.markdown(
    "<h3 style='text-align: center;'>🎯 Target USA City & Live Clock</h3>",
    unsafe_allow_html=True,
)

target_city = st.selectbox(
    "Jis city ke time zone ko dekhna/target karna hai, use chunein:",
    [
        "New York (Eastern Time - EST/EDT)",
        "Los Angeles (Pacific Time - PST/PDT)",
        "Chicago (Central Time - CST/CDT)",
        "Denver (Mountain Time - MST/MDT)",
    ],
)

tz_mapping = {
    "New York (Eastern Time - EST/EDT)": "America/New_York",
    "Los Angeles (Pacific Time - PST/PDT)": "America/Los_Angeles",
    "Chicago (Central Time - CST/CDT)": "America/Chicago",
    "Denver (Mountain Time - MST/MDT)": "America/Denver",
}
selected_tz_code = tz_mapping[target_city]

# Hidden input to pass selected timezone to Javascript
st.markdown(
    f'<input type="hidden" id="city-selector-hidden" value="{selected_tz_code}">',
    unsafe_allow_html=True,
)

# Live Running Clock Display Box
st.markdown(
    f"""
    <div style="background-color: #000000; border: 2px solid #00bfff; border-radius: 10px; padding: 20px; text-align: center; margin-bottom: 20px; box-shadow: 0px 0px 15px rgba(0, 191, 255, 0.3);">
        <p style="color: #00bfff; margin: 0; font-size: 15px;">Live Running Time in {target_city}</p>
        <h2 id="live-running-clock" style="color: white; margin: 10px 0 0 0; font-size: 26px;">Loading...</h2>
    </div>
""",
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

# लेआउट को दो भागों में बाँटना
col1, col2 = st.columns(2, gap="large")

# पहला हिस्सा - अकाउंट की जानकारी
with col1:
  st.markdown("### 1. अकाउंट डिटेल्स")
  sender_name = st.text_input("Sender Name", placeholder="अपना नाम लिखें")
  gmail_id = st.text_input("Gmail ID", placeholder="your-email@gmail.com")
  app_password = st.text_input(
      "App Password", type="password", placeholder="16 अंकों का पासवर्ड"
  )

# दूसरा हिस्सा - ईमेल मैसेज और डेटा
with col2:
  st.markdown(f"### 2. संदेश और डेटा ({target_city.split(' ')[0]})")
  subject_line = st.text_input("Subject Line", placeholder="ईमेल का विषय")
  email_template = st.text_area(
      "Email Template", height=110, placeholder="अपना मैसेज यहाँ लिखें..."
  )
  data = st.text_area(
      "Data (Email IDs - हर लाइन में एक)",
      height=110,
      placeholder="example1@gmail.com\nexample2@gmail.com",
  )

st.markdown("<br>", unsafe_allow_html=True)

# सेंड बटन को बीच में करने के लिए
col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
with col_b2:
  send_button = st.button("🚀 Send Mail Now", use_container_width=True)

# ईमेल भेजने का लॉजिक
if send_button:
  if not sender_name or not gmail_id or not app_password or not data:
    st.error(
        "⚠️ कृपया सभी ज़रूरी जानकारी (Sender Name, Gmail ID, Password और Data)"
        " भरें!"
    )
  else:
    emails_list = [
        email.strip() for email in data.split("\n") if email.strip()
    ]
    total_emails = len(emails_list)

    with st.spinner("ईमेल सर्वर से कनेक्ट हो रहा है..."):
      try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(gmail_id, app_password)

        success_count = 0
        progress_bar = st.progress(0)
        status_text = st.empty()

        for index, rcv_email in enumerate(emails_list):
          personalized_body = email_template.replace("{sender}", sender_name)

          msg = MIMEMultipart()
          msg["From"] = f"{sender_name} <{gmail_id}>"
          msg["To"] = rcv_email
          msg["Subject"] = subject_line
          msg.attach(MIMEText(personalized_body, "plain"))

          server.sendmail(gmail_id, rcv_email, msg.as_string())
          success_count += 1

          progress = (index + 1) / total_emails
          progress_bar.progress(progress)

          if index < total_emails - 1:
            delay_seconds = random.randint(6, 8)
            for remaining in range(delay_seconds, 0, -1):
              status_text.info(
                  f"✅ {rcv_email} को भेज दिया। स्पैम से बचने के लिए अगले ईमेल"
                  f" में {remaining} सेकंड का इंतज़ार..."
              )
              time.sleep(1)
          else:
            status_text.success(
                f"✅ {rcv_email} को भेज दिया। सभी ईमेल सफलतापूर्वक भेजे गए!"
            )

        server.quit()
        time.sleep(1)
        status_text.empty()
        progress_bar.empty()

        st.balloons()
        st.success(
            f"✅ शानदार! कुल {success_count} ईमेल सफलतापूर्वक (एंटी-स्पैम डिले के"
            " साथ) भेज दिए गए!"
        )

      except Exception as e:
        st.error(f"❌ ईमेल भेजने में समस्या आई। एरर: {e}")
