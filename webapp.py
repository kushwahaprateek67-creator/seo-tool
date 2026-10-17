import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
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
st.set_page_config(page_title="Outlook 2021 Advanced Dashboard", layout="wide")

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
    "<h1 style='text-align: center; font-size: 28px; color: #0078d4;'>📧 Outlook 2021 Dashboard (Today's Replies Filter)</h1>",
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


# ================= TAB 2: OUTLOOK 2021 MAILBOX (TODAY'S REPLIES SEPARATION) =================
with tab2:
  st.markdown("<br>", unsafe_allow_html=True)

  top_c1, top_c2, top_c3 = st.columns([1, 1, 1], gap="medium")
  with top_c1:
    inbox_email_id = st.text_input(
        "Mailbox Gmail ID", placeholder="your-email@gmail.com", key="today_email"
    )
  with top_c2:
    inbox_app_password = st.text_input(
        "App Password",
        type="password",
        placeholder="16 अंकों का पासवर्ड",
        key="today_pass",
    )
  with top_c3:
    st.markdown("<br>", unsafe_allow_html=True)
    fetch_today_btn = st.button("🔄 Sync & Check Today's Replies", use_container_width=True)

  if fetch_today_btn:
    if not inbox_email_id or not inbox_app_password:
      st.error("⚠️ कृपया अपनी Gmail आईडी और ऐप पासवर्ड दर्ज करें!")
    else:
      with st.spinner("मेल्स सिंक हो रहे हैं..."):
        try:
          mail = imaplib.IMAP4_SSL("imap.gmail.com")
          mail.login(inbox_email_id, inbox_app_password)
          mail.select("inbox")

          status, messages = mail.search(None, "ALL")

          if status != "OK":
            st.error("❌ मेलबॉक्स फेच करने में असफल।")
          else:
            email_ids = messages[0].split()
            latest_email_ids = email_ids[-40:]  # आखिरी 40 मेल्स
            latest_email_ids.reverse()

            all_mailbox_data = []
            today_date_str = datetime.now().strftime("%d %b %Y") # आज की तारीख फॉर्मेट (जैसे 17 Oct 2026)

            for i, num in enumerate(latest_email_ids):
              status, data = mail.fetch(num, "(RFC822)")
              for response_part in data:
                if isinstance(response_part, tuple):
                  msg = email.message_from_bytes(response_part[1])
                  subject = msg["subject"] or "No Subject"
                  sender = msg["from"] or "Unknown Sender"
                  date_header = msg["date"] or ""

                  body = ""
                  if msg.is_multipart():
                    for part in msg.walk():
                      content_type = part.get_content_type()
                      content_disposition = str(part.get("Content-Disposition"))
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

                  if not body.strip():
                    body = f"[System Notification / Status Mail]\nSubject: {subject}\nSender: {sender}"

                  body = re.sub('<.*?>', '', body)
                  is_reply = "re:" in subject.lower() or "original message" in body.lower()

                  # यह जाँचने के लिए कि क्या यह मेल आज ही आया है
                  is_today = False
                  try:
                    parsed_date = email.utils.parsedate_to_datetime(date_header)
                    if parsed_date.date() == datetime.now().date():
                      is_today = True
                  except:
                    pass

                  category = "🔥 Today's Reply" if (is_today and is_reply) else ("📅 Today's Mail" if is_today else ("💬 Older Reply" if is_reply else "📥 Older Mail"))

                  all_mailbox_data.append({
                      "Index": i + 1,
                      "Sender": sender,
                      "Subject": subject,
                      "Full_Body": body,
                      "Category": category,
                      "Date": date_header[:16]
                  })

            if all_mailbox_data:
              st.session_state["today_mailbox_df"] = all_mailbox_data
              st.success(f"✅ कुल {len(all_mailbox_data)} मेल्स लोड हो गए हैं!")

          mail.logout()

        except Exception as e:
          st.error(f"❌ मेलबॉक्स लोड करने में एरर आया: {e}")

  # अगर डेटा मौजूद है, तो लेआउट दिखाएं
  if "today_mailbox_df" in st.session_state and st.session_state["today_mailbox_df"]:
    st.markdown("<hr style='border: 1px solid #2d2d2d; margin: 15px 0;'>", unsafe_allow_html=True)

    # मेल्स को अलग-अलग फिल्टर करना (आज के रिप्लाई अलग, बाकी सब अलग)
    df_data = st.session_state["today_mailbox_df"]
    today_replies = [m for m in df_data if "Today's Reply" in m["Category"]]
    other_mails = [m for m in df_data if "Today's Reply" not in m["Category"]]

    # 3-पैनल लेआउट
    panel1, panel2, panel3 = st.columns([0.8, 1.2, 1.5], gap="medium")

    with panel1:
      st.markdown("##### 📁 Outlook Folders")
      st.markdown("🔥 **Today's Replies**")
      st.markdown("📂 **All Other Mailbox**")
      st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;📥 **Inbox Mails**")
      st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;📤 **Sent Items**")
      st.markdown("---")
      st.info("💡 आज के नए रिप्लाई सबसे ऊपर अलग बॉक्स में दिखेंगे।")

    with panel2:
      st.markdown("##### 📋 Select Message Category")
      
      view_mode = st.radio(
          "बॉक्स चुनें:",
          ["🔥 Today's Replies (आज के नए रिप्लाई)", "📂 All Other Mails (बाकी सभी मेल्स)"],
          label_visibility="collapsed"
      )

      active_list = today_replies if "Today's Replies" in view_mode else other_mails

      if not active_list:
        st.warning("इस फोल्डर में कोई मेल नहीं है।")
        selected_mail = None
      else:
        mail_options = {
            f"{item['Index']}. [{item['Category']}] {item['Subject'][:18]}...": item
            for item in active_list
        }

        selected_label = st.selectbox(
            "मेल्स सूची:",
            options=list(mail_options.keys()),
            label_visibility="collapsed",
        )
        selected_mail = mail_options[selected_label]

    with panel3:
      st.markdown("##### 📖 Reading & Forward Pane")
      
      if 'selected_mail' in locals() and selected_mail:
        st.markdown(f"**Category:** `{selected_mail['Category']}`")
        st.markdown(f"**From:** `{selected_mail['Sender']}`")
        st.markdown(f"**Subject:** {selected_mail['Subject']}")
        st.markdown(f"**Date:** {selected_mail['Date']}")
        st.markdown("---")

        # रीडिंग एरिया (बिना की के ताकि तुरंत अपडेट हो)
        st.text_area(
            "Reading Area",
            value=selected_mail["Full_Body"],
            height=160,
            label_visibility="collapsed",
        )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("##### 🔄 Forward Mail to Someone")

        forward_target = st.text_input(
            "Forward To (Receiver Gmail ID)", 
            placeholder="recipient@gmail.com",
            key="today_forward_input"
        )

        custom_note = st.text_area(
            "Note / Message (Optional)",
            placeholder="यदि कुछ लिखना चाहें...",
            height=50,
            key="today_note_box",
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
                  f"✅ ईमेल सफलतापूर्वक **{forward_target}** को फॉरवर्ड कर दिया गया है!"
              )

            except Exception as e:
              st.error(f"❌ भेजने में एरर आया: {e}")
      else:
        st.info("कृपया बाईं तरफ से कोई मेल चुनें।")
