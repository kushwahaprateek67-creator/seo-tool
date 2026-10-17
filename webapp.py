import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import imaplib
import random
import re
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

# पेज सेटिंग (डैशबोर्ड के लिए वाइड लेआउट)
st.set_page_config(page_title="Outlook Email Dashboard", layout="wide")

# पूरे ऐप का शानदार CSS डिज़ाइन
st.markdown(
    """
    <style>
    .stApp, .stApp > header {
        background-color: #0b0f19 !important; 
    }
    .block-container {
        background-color: #111827 !important;
        border: 2px solid #00bfff !important;
        border-radius: 16px !important;
        box-shadow: 0px 0px 25px rgba(0, 191, 255, 0.3) !important;
        padding: 30px 30px !important;
        max-width: 1200px !important;
    }
    h1, h2, h3, label p, .stMarkdown p {
        font-weight: 700 !important;
        color: #00bfff !important; 
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #030712 !important; 
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
        height: 45px;
    }
    .stButton>button:hover {
        background-color: #00bfff !important;
        color: black !important;
        box-shadow: 0px 0px 12px #00bfff;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# शीर्षक
st.markdown(
    "<h1 style='text-align: center;'>🌐 Professional Outlook Email Dashboard</h1>",
    unsafe_allow_html=True,
)
st.markdown("<hr style='border: 1px solid #0066ff;'>", unsafe_allow_html=True)

# मुख्य टैब्स
tab1, tab2 = st.tabs(["📤 Send Bulk Campaign", "📥 Outlook Split-View Dashboard"])

# ================= TAB 1: BULK EMAIL SENDING =================
with tab1:
  st.markdown("<br>", unsafe_allow_html=True)
  col1, col2 = st.columns(2, gap="large")

  with col1:
    st.markdown("### 1. Sender Details")
    sender_name = st.text_input("Sender Name", placeholder="अपना नाम लिखें")
    gmail_id = st.text_input("Gmail ID", placeholder="your-email@gmail.com")
    app_password = st.text_input(
        "App Password",
        type="password",
        placeholder="16 अंकों का पासवर्ड",
        key="send_pass_main",
    )

  with col2:
    st.markdown("### 2. Campaign Template & List")
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
    send_button = st.button("🚀 Start Bulk Email Campaign", use_container_width=True)

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
              f"✅ शानदार! कुल {success_count} ईमेल सफलतापूर्वक भेज दिए गए!"
          )

        except Exception as e:
          st.error(f"❌ ईमेल भेजने में समस्या आई। एरर: {e}")


# ================= TAB 2: OUTLOOK SPLIT-VIEW DASHBOARD =================
with tab2:
  st.markdown("<br>", unsafe_allow_html=True)

  # क्रेडेंशियल्स बार
  cred_col1, cred_col2, cred_col3 = st.columns([1, 1, 1], gap="medium")
  with cred_col1:
    inbox_email_id = st.text_input(
        "Dashboard Gmail ID", placeholder="your-email@gmail.com", key="dash_email"
    )
  with cred_col2:
    inbox_app_password = st.text_input(
        "App Password",
        type="password",
        placeholder="16 अंकों का पासवर्ड",
        key="dash_pass",
    )
  with cred_col3:
    st.markdown("<br>", unsafe_allow_html=True)
    fetch_button = st.button("🔄 Sync & Load Inbox", use_container_width=True)

  if fetch_button:
    if not inbox_email_id or not inbox_app_password:
      st.error("⚠️ कृपया अपनी Gmail ID और App Password दर्ज करें!")
    else:
      with st.spinner("आउटलुक इनबॉक्स सिंक हो रहा है..."):
        try:
          mail = imaplib.IMAP4_SSL("imap.gmail.com")
          mail.login(inbox_email_id, inbox_app_password)
          mail.select("inbox")

          status, messages = mail.search(None, "ALL")

          if status != "OK":
            st.error("❌ इनबॉक्स फेच करने में असफल।")
          else:
            email_ids = messages[0].split()
            latest_email_ids = email_ids[-15:]  # आखिरी 15 मेल्स
            latest_email_ids.reverse()

            dashboard_data = []

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

                  is_reply = "re:" in subject.lower() or "original message" in body.lower()

                  dashboard_data.append({
                      "Index": i + 1,
                      "Sender": sender,
                      "Subject": subject,
                      "Full_Body": body if body else "[No text body]",
                      "Status": "💬 Reply Received" if is_reply else "📬 Normal Mail"
                  })

            if dashboard_data:
              st.session_state["outlook_dash_df"] = dashboard_data

          mail.logout()

        except Exception as e:
          st.error(f"❌ इनबॉक्स लोड करने में एरर आया: {e}")

  # अगर डैशबोर्ड डेटा मौजूद है, तो स्प्लिट-व्यू लेआउट दिखाएं
  if "outlook_dash_df" in st.session_state and st.session_state["outlook_dash_df"]:
    st.markdown("<hr style='border: 1px solid #003366;'>", unsafe_allow_html=True)
    
    # स्प्लिट स्क्रीन: बायां हिस्सा (List), दायां हिस्सा (Reading Pane & Forward Panel)
    list_col, read_col = st.columns([1, 1.2], gap="large")

    with list_col:
      st.markdown("#### 📂 Inbox Messages")
      mail_options = {
          f"{item['Index']} | {item['Status']} | {item['Subject'][:22]}...": item["Index"]
          for item in st.session_state["outlook_dash_df"]
      }

      selected_mail_label = st.radio(
          "मेल्स सूची:",
          options=list(mail_options.keys()),
          label_visibility="collapsed",
      )

      selected_index = mail_options[selected_mail_label]

    with read_col:
      st.markdown("#### 📖 Reading & Forward Pane")
      selected_mail = next(
          item
          for item in st.session_state["outlook_dash_df"]
          if item["Index"] == selected_index
      )

      st.markdown(f"**Type:** `{selected_mail['Status']}`")
      st.markdown(f"**From:** `{selected_mail['Sender']}`")
      st.markdown(f"**Subject:** {selected_mail['Subject']}")
      st.markdown("---")
      
      st.text_area(
          "Email Content",
          value=selected_mail["Full_Body"],
          height=180,
          key="dash_reading_pane",
          label_visibility="collapsed",
      )

      st.markdown("<br>", unsafe_allow_html=True)
      st.markdown("#### 🔄 Forward / Reply Options")

      # एक्शन और फॉरवर्डिंग फील्ड्स
      forward_target = st.text_input(
          "Send/Forward To (Other Person's Gmail)", 
          placeholder="target-email@gmail.com",
          key="dash_forward_target"
      )

      custom_note = st.text_area(
          "Add Custom Note / Message",
          placeholder="इसके साथ कोई नोट जोड़ना चाहें...",
          height=60,
          key="dash_custom_note",
      )

      if st.button("🚀 Send / Forward Now", use_container_width=True):
        if not inbox_email_id or not inbox_app_password:
          st.error("⚠️ कृपया ऊपर अपनी Gmail ID और App Password दर्ज करें!")
        elif not forward_target:
          st.error("⚠️ कृपया उस व्यक्ति की Gmail ID दर्ज करें जिसे भेजना है!")
        else:
          try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(inbox_email_id, inbox_app_password)

            msg = MIMEMultipart()
            msg["From"] = inbox_email_id
            msg["To"] = forward_target
            msg["Subject"] = f"Fwd / Reply: {selected_mail['Subject']}"

            forward_body = (
                f
