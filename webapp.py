import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import imaplib
import random
import smtplib
import time
import pandas as pd
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
""",
    unsafe_allow_html=True,
)

# ----------------- फ्रेम के अंदर का कंटेंट -----------------

st.markdown(
    "<h1 style='text-align: center;'>✉️ Bulk Email Tool & Outlook Inbox</h1>",
    unsafe_allow_html=True,
)
st.markdown("<hr style='border: 1px solid #0066ff;'>", unsafe_allow_html=True)

# टैब्स डिफाइन करना
tab1, tab2 = st.tabs(["📤 Send Bulk Emails", "📥 Outlook Split-View Inbox"])

# ================= TAB 1: EMAIL SENDING LOGIC =================
with tab1:
  st.markdown("<br>", unsafe_allow_html=True)
  col1, col2 = st.columns(2, gap="large")

  with col1:
    st.markdown("### 1. अकाउंट डिटेल्स")
    sender_name = st.text_input("Sender Name", placeholder="अपना नाम लिखें")
    gmail_id = st.text_input("Gmail ID", placeholder="your-email@gmail.com")
    app_password = st.text_input(
        "App Password",
        type="password",
        placeholder="16 अंकों का पासवर्ड",
        key="send_pass",
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
    send_button = st.button("🚀 Send Mail Now", use_container_width=True)

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
              f"✅ शानदार! कुल {success_count} ईमेल सफलतापूर्वक (एंटी-स्पैम डिले"
              " के साथ) भेज दिए गए!"
          )

        except Exception as e:
          st.error(f"❌ ईमेल भेजने में समस्या आई। एरर: {e}")


# ================= TAB 2: OUTLOOK SPLIT-VIEW INBOX =================
with tab2:
  st.markdown("<br>", unsafe_allow_html=True)
  st.markdown("### 📥 Outlook Split-View Inbox")

  inbox_col1, inbox_col2 = st.columns(2, gap="large")
  with inbox_col1:
    inbox_email_id = st.text_input(
        "Gmail ID", placeholder="your-email@gmail.com", key="inbox_email"
    )
  with inbox_col2:
    inbox_app_password = st.text_input(
        "App Password",
        type="password",
        placeholder="16 अंकों का पासवर्ड",
        key="inbox_pass",
    )

  fetch_button = st.button("🔄 Load Outlook Inbox", use_container_width=True)

  if fetch_button:
    if not inbox_email_id or not inbox_app_password:
      st.error("⚠️ कृपया अपनी Gmail ID और App Password दर्ज करें!")
    else:
      with st.spinner("इनबॉक्स लोड हो रहा है..."):
        try:
          mail = imaplib.IMAP4_SSL("imap.gmail.com")
          mail.login(inbox_email_id, inbox_app_password)
          mail.select("inbox")

          status, messages = mail.search(None, "ALL")

          if status != "OK":
            st.error("❌ इनबॉक्स फेच करने में असफल।")
          else:
            email_ids = messages[0].split()
            latest_email_ids = email_ids[-10:]
            latest_email_ids.reverse()

            emails_list_data = []

            for i, num in enumerate(latest_email_ids):
              status, data = mail.fetch(num, "(RFC822)")
              for response_part in data:
                if isinstance(response_part, tuple):
                  msg = email.message_from_bytes(response_part[1])
                  subject = msg["subject"] or "No Subject"
                  sender = msg["from"] or "Unknown Sender"

                  body = ""
                  if msg.is_multipart():
                    for part in msg.walk():
                      if part.get_content_type() == "text/plain":
                        payload = part.get_payload(decode=True)
                        if payload:
                          try:
                            body = payload.decode("utf-8", errors="ignore")
                          except:
                            body = payload.decode("latin-1", errors="ignore")
                        break
                  else:
                    payload = msg.get_payload(decode=True)
                    if payload:
                      try:
                        body = payload.decode("utf-8", errors="ignore")
                      except:
                        body = payload.decode("latin-1", errors="ignore")

                  emails_list_data.append({
                      "Index": i + 1,
                      "Sender": sender,
                      "Subject": subject,
                      "Full_Body": body if body else "[No text body]",
                  })

            if emails_list_data:
              st.session_state["outlook_df"] = emails_list_data

          mail.logout()

        except Exception as e:
          st.error(f"❌ इनबॉक्स लोड करने में एरर आया: {e}")

  if "outlook_df" in st.session_state and st.session_state["outlook_df"]:
    st.markdown("<br>", unsafe_allow_html=True)
    list_col, read_col = st.columns([1, 1], gap="medium")

    with list_col:
      st.markdown("#### 📋 Inbox List")
      mail_options = {
          f"{item['Index']}. {item['Subject'][:25]}...": item["Index"]
          for item in st.session_state["outlook_df"]
      }

      selected_mail_label = st.radio(
          "मेल्स चुनें:",
          options=list(mail_options.keys()),
          label_visibility="collapsed",
      )

      selected_index = mail_options[selected_mail_label]

    with read_col:
      st.markdown("#### 📖 Reading Pane")
      selected_mail = next(
          item
          for item in st.session_state["outlook_df"]
          if item["Index"] == selected_index
      )

      st.markdown(f"**From:** `{selected_mail['Sender']}`")
      st.markdown(f"**Subject:** {selected_mail['Subject']}")
      st.markdown("---")
      st.text_area(
          "Message Content",
          value=selected_mail["Full_Body"],
          height=300,
          key="outlook_body_box",
          label_visibility="collapsed",
      )
