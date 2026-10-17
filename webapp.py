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

# पेज सेटिंग (वाइड लेआउट)
st.set_page_config(page_title="Outlook 2021 Fixed Dashboard", layout="wide")

# आउटलुक 2021 मॉडर्न CSS डिज़ाइन
st.markdown(
    """
    <style>
    .stApp, .stApp > header {
        background-color: #121212 !important; 
    }
    .block-container {
        background-color: #1e1e1e !important;
        border: 1px solid #2d2d2d !important;
        border-radius: 14px !important;
        box-shadow: 0px 8px 24px rgba(0, 0, 0, 0.5) !important;
        padding: 25px 30px !important;
        max-width: 1350px !important;
    }
    h1, h2, h3, label p, .stMarkdown p {
        font-weight: 600 !important;
        color: #0078d4 !important; 
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #2d2d2d !important; 
        color: #ffffff !important; 
        border: 1px solid #3f3f3f !important; 
        border-radius: 8px !important;
    }
    .stButton>button {
        background-color: #0078d4 !important;
        color: white !important;
        border: none !important;
        font-weight: 600;
        border-radius: 8px;
        transition: 0.2s;
        height: 42px;
    }
    .stButton>button:hover {
        background-color: #106ebe !important;
        box-shadow: 0px 0px 8px rgba(0, 120, 212, 0.6);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ऐप हेडर
st.markdown(
    "<h1 style='text-align: center; font-size: 28px; color: #0078d4;'>📧 Outlook 2021 Dashboard (Fixed Body Viewer)</h1>",
    unsafe_allow_html=True,
)
st.markdown("<hr style='border: 1px solid #2d2d2d; margin: 15px 0;'>", unsafe_allow_html=True)

# मुख्य टैब्स
tab1, tab2 = st.tabs(["📤 Bulk Email Campaign", "📥 Outlook Mailbox & Forward"])

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
        key="send_pass_mod",
    )

  with col2:
    st.markdown("### 2. Campaign Template & List")
    subject_line = st.text_input("Subject Line", placeholder="ईमेल का विषय")
    email_template = st.text_area(
        "Email Template", height=100, placeholder="अपना मैसेज यहाँ लिखें..."
    )
    data = st.text_area(
        "Data (Email IDs - हर लाइन में एक)",
        height=100,
        placeholder="example1@gmail.com\nexample2@gmail.com",
    )

  st.markdown("<br>", unsafe_allow_html=True)
  col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
  with col_b2:
    send_button = st.button("🚀 Start Bulk Campaign", use_container_width=True)

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


# ================= TAB 2: OUTLOOK 2021 MAILBOX (FIXED BODY EXTRACTION) =================
with tab2:
  st.markdown("<br>", unsafe_allow_html=True)

  top_c1, top_c2, top_c3 = st.columns([1, 1, 1], gap="medium")
  with top_c1:
    inbox_email_id = st.text_input(
        "Mailbox Gmail ID", placeholder="your-email@gmail.com", key="fix_email"
    )
  with top_c2:
    inbox_app_password = st.text_input(
        "App Password",
        type="password",
        placeholder="16 अंकों का पासवर्ड",
        key="fix_pass",
    )
  with top_c3:
    st.markdown("<br>", unsafe_allow_html=True)
    fetch_fix_btn = st.button("🔄 Sync Mailbox & Messages", use_container_width=True)

  if fetch_fix_btn:
    if not inbox_email_id or not inbox_app_password:
      st.error("⚠️ कृपया अपनी Gmail ID और App Password दर्ज करें!")
    else:
      with st.spinner("मेल्स और उनके कंटेंट लोड हो रहे हैं..."):
        try:
          mail = imaplib.IMAP4_SSL("imap.gmail.com")
          mail.login(inbox_email_id, inbox_app_password)
          mail.select("inbox")

          status, messages = mail.search(None, "ALL")

          if status != "OK":
            st.error("❌ मेलबॉक्स फेच करने में असफल।")
          else:
            email_ids = messages[0].split()
            latest_email_ids = email_ids[-30:]  # आखिरी 30 मेल्स
            latest_email_ids.reverse()

            fixed_mailbox_data = []

            for i, num in enumerate(latest_email_ids):
              status, data = mail.fetch(num, "(RFC822)")
              for response_part in data:
                if isinstance(response_part, tuple):
                  msg = email.message_from_bytes(response_part[1])
                  subject = msg["subject"] or "No Subject"
                  sender = msg["from"] or "Unknown Sender"

                  # --- मजबूत बॉडी एक्सट्रैक्शन लॉजिक (ताकि कोई मेल खाली न रहे) ---
                  body = ""
                  if msg.is_multipart():
                    for part in msg.walk():
                      content_type = part.get_content_type()
                      content_disposition = str(part.get("Content-Disposition"))
                      # अटैचमेंट छोड़कर टेक्स्ट या html ढूंढें
                      if content_type in ["text/plain", "text/html"] and "attachment" not in content_disposition:
                        payload = part.get_payload(decode=True)
                        if payload:
                          for enc in ["utf-8", "latin-1", "iso-8859-1"]:
                            try:
                              body = payload.decode(enc)
                              break
                            except:
                              continue
                        if body:
                          break
                  else:
                    payload = msg.get_payload(decode=True)
                    if payload:
                      for enc in ["utf-8", "latin-1", "iso-8859-1"]:
                        try:
                          body = payload.decode(enc)
                          break
                        except:
                          continue

                  # अगर फिर भी बॉडी खाली है, तो सब्जेक्ट या हेडर दिखा दें ताकि डिब्बा खाली न लगे
                  if not body.strip():
                    body = f"[System Notification / Status Mail]\nSubject: {subject}\nSender: {sender}"

                  # HTML टैग्स हटाने के लिए साधारण क्लीनिंग (optional)
                  body = re.sub('<.*?>', '', body)

                  is_reply = "re:" in subject.lower() or "original message" in body.lower()

                  fixed_mailbox_data.append({
                      "Index": i + 1,
                      "Sender": sender,
                      "Subject": subject,
                      "Full_Body": body,
                      "Type": "💬 Reply" if is_reply else "📥 Mail"
                  })

            if fixed_mailbox_data:
              st.session_state["fixed_mailbox_df"] = fixed_mailbox_data
              st.success(f"✅ कुल {len(fixed_mailbox_data)} मेल्स सफलतापूर्वक लोड हो गए हैं!")

          mail.logout()

        except Exception as e:
          st.error(f"❌ मेलबॉक्स लोड करने में एरर आया: {e}")

  # अगर डेटा मौजूद है, तो 3-पैनल लेआउट दिखाएं
  if "fixed_mailbox_df" in st.session_state and st.session_state["fixed_mailbox_df"]:
    st.markdown("<hr style='border: 1px solid #2d2d2d; margin: 15px 0;'>", unsafe_allow_html=True)

    panel1, panel2, panel3 = st.columns([0.8, 1.2, 1.5], gap="medium")

    with panel1:
      st.markdown("##### 📁 Folders")
      st.markdown("🔹 **Inbox**")
      st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;📥 **All Messages**")
      st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;📤 **Sent Items**")
      st.markdown("---")
      st.info("💡 किसी भी मेल पर क्लिक करते ही उसका कंटेंट दाईं तरफ दिखेगा।")

    with panel2:
      st.markdown("##### 📋 Messages List")
      mail_options = {
          f"{item['Index']}. [{item['Type']}] {item['Subject'][:20]}...": item["Index"]
          for item in st.session_state["fixed_mailbox_df"]
      }

      selected_mail_label = st.radio(
          "मेल्स:",
          options=list(mail_options.keys()),
          label_visibility="collapsed",
      )

      selected_index = mail_options[selected_mail_label]

    with panel3:
      st.markdown("##### 📖 Reading & Forward Pane")
      selected_mail = next(
          item
          for item in st.session_state["fixed_mailbox_df"]
          if item["Index"] == selected_index
      )

      st.markdown(f"**Type:** `{selected_mail['Type']}`")
      st.markdown(f"**From:** `{selected_mail['Sender']}`")
      st.markdown(f"**Subject:** {selected_mail['Subject']}")
      st.markdown("---")

      # अब यहाँ हर मेल का असली कंटेंट साफ़-साफ़ दिखाई देगा
      st.text_area(
          "Reading Area",
          value=selected_mail["Full_Body"],
          height=180,
          key="fix_reading_box",
          label_visibility="collapsed",
      )

      st.markdown("<br>", unsafe_allow_html=True)
      st.markdown("##### 🔄 Forward to Someone")

      forward_target = st.text_input(
          "Forward To (Receiver Gmail ID)", 
          placeholder="recipient@gmail.com",
          key="fix_forward_input"
      )

      custom_note = st.text_area(
          "Note / Message",
          placeholder="साथ में कोई नोट जोड़ना चाहें...",
          height=60,
          key="fix_note_box",
      )

      if st.button("🚀 Forward Mail Now", use_container_width=True):
        if not inbox_email_id or not inbox_app_password:
          st.error("⚠️ कृपया ऊपर अपनी Gmail ID और App Password दर्ज करें!")
        elif not forward_target:
          st.error("⚠️ कृपया पाने वाले की Gmail ID दर्ज करें!")
        else:
          try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(inbox_email_id, inbox_app_password)

            msg = MIMEMultipart()
            msg["From"] = inbox_email_id
            msg["To"] = forward_target
            msg["Subject"] = f"Fwd: {selected_mail['Subject']}"

            forward_body = (
                f"{custom_note}\n\n---------- Forwarded Message ----------\n"
                f"From: {selected_mail['Sender']}\n"
                f"Subject: {selected_mail['Subject']}\n\n"
                f"{selected_mail['Full_Body']}"
            )

            msg.attach(MIMEText(forward_body, "plain"))
            server.sendmail(inbox_email_id, forward_target, msg.as_string())
            server.quit()

            st.success(
                f"✅ ईमेल सफलतापूर्वक **{forward_target}** को भेज दिया गया है!"
            )

          except Exception as e:
            st.error(f"❌ भेजने में एरर आया: {e}")
