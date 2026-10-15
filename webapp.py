from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import smtplib
import time
from zoneinfo import ZoneInfo
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

# पूरे ऐप का CSS डिज़ाइन
st.markdown(
    """
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
        const selectedZone = document.getElementById('target-city-tz').value;
        if (!selectedZone) return;
        const options = { timeZone: selectedZone, hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true, month: 'short', day: 'numeric' };
        const now = new Date();
        const elem = document.getElementById('single-clock');
        if (elem) elem.innerText = now.toLocaleString('en-US', options);
    }
    setInterval(updateClock, 1000);
    </script>
""",
    unsafe_allow_html=True,
)

st.markdown(
    "<h1 style='text-align: center;'>✉️ Bulk Email Tool (USA Time Zone"
    " Targeted)</h1>",
    unsafe_allow_html=True,
)
st.markdown("<hr style='border: 1px solid #0066ff;'>", unsafe_allow_html=True)

# 🇺🇸 Target City & Time Selector
st.markdown(
    "<h3 style='text-align: center;'>🎯 USA Target Time Zone Selection</h3>",
    unsafe_allow_html=True,
)

target_city = st.selectbox(
    "Kis USA Time Zone ke hisab se mail bhejna hai?",
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

st.markdown(
    f'<input type="hidden" id="target-city-tz" value="{selected_tz_code}">',
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div style="background-color: #000000; border: 2px solid #00bfff; border-radius: 10px; padding: 20px; text-align: center; margin-bottom: 20px; box-shadow: 0px 0px 15px rgba(0, 191, 255, 0.3);">
        <p style="color: #00bfff; margin: 0; font-size: 15px;">Live Clock ({target_city}):</p>
        <h2 id="single-clock" style="color: white; margin: 10px 0 0 0; font-size: 26px;">Loading...</h2>
    </div>
""",
    unsafe_allow_html=True,
)

# Target USA Time input for scheduling
st.markdown("### ⏰ USA Local Time par Mail Land Karane ke liye Schedule Set karein")
col_t1, col_t2 = st.columns(2)
with col_t1:
  target_date = st.date_input(
      "Target Date (USA Time)", datetime.now(ZoneInfo(selected_tz_code)).date()
  )
with col_t2:
  target_time = st.time_input(
      "Target Time (USA Local Time)",
      datetime.now(ZoneInfo(selected_tz_code)).time(),
  )

st.markdown("<br>", unsafe_allow_html=True)

# Form Layout
col1, col2 = st.columns(2, gap="large")

with col1:
  st.markdown("### 1. अकाउंट डिटेल्स")
  sender_name = st.text_input("Sender Name", placeholder="अपना नाम लिखें")
  gmail_id = st.text_input("Gmail ID", placeholder="your-email@gmail.com")
  app_password = st.text_input(
      "App Password", type="password", placeholder="16 अंकों का पासवर्ड"
  )

with col2:
  st.markdown("### 2. संदेश और डेटा")
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

col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
with col_b2:
  send_button = st.button("🚀 Schedule & Send Mail", use_container_width=True)

# Email Sending & Time Zone Delay Logic
if send_button:
  if not sender_name or not gmail_id or not app_password or not data:
    st.error(
        "⚠️ कृपया सभी ज़रूरी जानकारी (Sender Name, Gmail ID, Password और Data)"
        " भरें!"
    )
  else:
    # Calculate target time in USA timezone and convert difference to seconds
    us_tz = ZoneInfo(selected_tz_code)
    target_dt_us = datetime.combine(target_date, target_time, tzinfo=us_tz)
    now_us = datetime.now(us_tz)

    delay_seconds = (target_dt_us - now_us).total_seconds()

    if delay_seconds < 0:
      st.error(
          "❌ Aapne jo time chuna hai woh beeta hua waqt (past) hai! Kripya"
          " aane wala time chunein."
      )
    else:
      st.info(
          f"⏳ Target set ho gaya hai! {target_city} ke mutabiq sahi waqt aane"
          f" par mail dispatch hoga (Lagbhag {int(delay_seconds)} seconds baad)."
      )

      # Countdown / Wait execution
      wait_placeholder = st.empty()
      while delay_seconds > 0:
        hrs = int(delay_seconds // 3600)
        mins = int((delay_seconds % 3600) // 60)
        secs = int(delay_seconds % 60)
        wait_placeholder.warning(
            f"🕒 USA Time ({target_city}) ka intezaar ho raha hai... Baaki"
            f" samay: {hrs}h {mins}m {secs}s"
        )
        time.sleep(1)
        delay_seconds -= 1

      wait_placeholder.empty()

      emails_list = [
          email.strip() for email in data.split("\n") if email.strip()
      ]
      total_emails = len(emails_list)

      with st.spinner("USA Time match hone par email bheja ja raha hai..."):
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
              anti_spam_delay = random.randint(6, 8)
              for remaining in range(anti_spam_delay, 0, -1):
                status_text.info(
                    f"✅ {rcv_email} ko bhej diya. Spam se bachne ke liye agle"
                    f" email mein {remaining} second ka delay..."
                )
                time.sleep(1)
            else:
              status_text.success(
                  f"✅ {rcv_email} ko bhej diya. Sabhi emails safal rahe!"
              )

          server.quit()
          time.sleep(1)
          status_text.empty()
          progress_bar.empty()

          st.balloons()
          st.success(
              f"✅ Shandar! Kul {success_count} emails USA ke targeted time zone"
              " ke mutabiq successfully bhej diye gaye!"
          )

        except Exception as e:
          st.error(f"❌ Email bhejne mein samasya aayi. Error: {e}")
