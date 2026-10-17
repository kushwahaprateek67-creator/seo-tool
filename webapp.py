# ================= TAB 2: EMAIL RECEIVING (INBOX) LOGIC =================
with tab2:
  st.markdown("<br>", unsafe_allow_html=True)
  st.markdown("### 📥 इनबॉक्स चेक करें (Inbox)")

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

  fetch_button = st.button("🔄 Fetch Latest Emails", use_container_width=True)

  if fetch_button:
    if not inbox_email_id or not inbox_app_password:
      st.error("⚠️ कृपया अपनी Gmail ID और App Password दर्ज करें!")
    else:
      with st.spinner("इनबॉक्स से मेल्स लोड हो रहे हैं..."):
        try:
          mail = imaplib.IMAP4_SSL("imap.gmail.com")
          mail.login(inbox_email_id, inbox_app_password)
          mail.select("inbox")

          status, messages = mail.search(None, "ALL")

          if status != "OK":
            st.error("❌ इनबॉक्स फेच करने में असफल।")
          else:
            email_ids = messages[0].split()
            latest_email_ids = email_ids[-5:]
            latest_email_ids.reverse()

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### 📬 आपके हालिया 5 ईमेल:")

            for num in latest_email_ids:
              status, data = mail.fetch(num, "(RFC822)")
              for response_part in data:
                if isinstance(response_part, tuple):
                  msg = email.message_from_bytes(response_part[1])
                  subject = msg["subject"]
                  sender = msg["from"]

                  body = ""
                  if msg.is_multipart():
                    for part in msg.walk():
                      content_type = part.get_content_type()
                      content_disposition = str(part.get("Content-Disposition"))
                      if (
                          content_type == "text/plain"
                          and "attachment" not in content_disposition
                      ):
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

                  with st.expander(f"📩 From: {sender} | Sub: {subject}"):
                    st.write(f"**Subject:** {subject}")
                    st.write(f"**From:** {sender}")
                    st.markdown("---")
                    st.write(
                        body[:500] + "..."
                        if len(body) > 500
                        else body if body else "[No text body found]"
                    )

          mail.logout()

        except Exception as e:
          st.error(f"❌ इनबॉक्स लोड करने में एरर आया: {e}")
