from datetime import datetime
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
    "<h1 style='text-align: center;'>✉️ Bulk Email Tool (Multi-ID Pool)</h1>",
    unsafe_allow_html=True,
)
st.markdown("<hr style='border: 1px solid #0066ff;'>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# लेआउट को दो भागों में बाँटना
col1, col2 = st.columns(2, gap="large")

# पहला हिस्सा - अकाउंट पूल की जानकारी
with col1:
    st.markdown("### 1. अकाउंट्स पूल डिटेल्स")
    sender_name = st.text_input(
        "Sender Name", value="Prateek Kushwaha", placeholder="अपना नाम लिखें"
    )
    accounts_data = st.text_area(
        "Gmail Accounts Pool (email:password - हर लाइन में एक)",
        height=210,
        placeholder="id1@gmail.com:app_password_1\nid2@gmail.com:app_password_2",
    )

# दूसरा हिस्सा - ईमेल मैसेज और डेटा
with col2:
    st.markdown("### 2. संदेश और टारगेट डेटा")
    subject_line = st.text_input(
        "Subject Line",
        value="Quick question about your content performance",
        placeholder="ईमेल का विषय",
    )

    default_template = """Hi,

Searchers asking complex, intent-driven questions are usually closer to buying than those searching broad keywords.

I help companies structure their FAQs, guides, and core pages for Answer Engine Optimization (AEO) to capture those high-intent users.

Would you be interested in reviewing how your current content performs for conversational answer queries?

Regards,
{sender}"""

    email_template = st.text_area(
        "Email Template",
        value=default_template,
        height=180,
        placeholder="अपना मैसेज यहाँ लिखें...",
    )
    data = st.text_area(
        "Target Recipients (Email IDs - हर लाइन में एक)",
        height=110,
        placeholder="recipient1@gmail.com\nrecipient2@gmail.com",
    )

st.markdown("<br>", unsafe_allow_html=True)

# सेंड बटन को बीच में करने के लिए
col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
with col_b2:
    send_button = st.button(
        "🚀 Start Rotational Campaign", use_container_width=True
    )

# ईमेल भेजने का लॉजिक (Rotation & Limits के साथ)
if send_button:
    if not sender_name or not accounts_data or not data:
        st.error(
            "⚠️ कृपया Sender Name, Accounts Pool और Target Recipients सभी जानकारी"
            " भरें!"
        )
    else:
        # Accounts parse karein (email:password format)
        raw_accounts = [acc.strip() for acc in accounts_data.split("\n") if acc.strip()]
        account_pool = []
        for acc in raw_accounts:
            if ":" in acc:
                email, pwd = acc.split(":", 1)
                account_pool.append(
                    {"email": email.strip(), "password": pwd.strip()}
                )

        recipients_list = [
            email.strip() for email in data.split("\n") if email.strip()
        ]

        if not account_pool:
            st.error(
                "❌ कोई वैध अकाउंट नहीं मिला! कृपया 'email:app_password' फॉर्मेट"
                " में डालें।"
            )
        elif not recipients_list:
            st.error("❌ कोई टारगेट रिसीपिएंट ईमेल नहीं मिला!")
        else:
            # 130 IDs max randomly pick karein pool me se roz ke liye
            active_accounts = random.sample(
                account_pool, min(130, len(account_pool))
            )

            total_recipients = len(recipients_list)
            recipient_index = 0
            success_count = 0

            progress_bar = st.progress(0)
            status_text = st.empty()

            for account in active_accounts:
                if recipient_index >= total_recipients:
                    break

                sender_email = account["email"]
                app_password = account["password"]
                sent_with_this_id = 0
                max_per_id = 10  # Har ID se max 10 emails

                try:
                    server = smtplib.SMTP("smtp.gmail.com", 587)
                    server.starttls()
                    server.login(sender_email, app_password)

                    while (
                        sent_with_this_id < max_per_id
                        and recipient_index < total_recipients
                    ):
                        rcv_email = recipients_list[recipient_index]

                        unsubscribe_html = f"""
                        <br><br>
                        <p style='font-size: 12px; color: #888;'>
                        <a href="mailto:{sender_email}?subject=Unsubscribe" style='color: #00bfff;'>Unsubscribe</a>
                        </p>
                        """

                        personalized_body = (
                            email_template.replace("{sender}", sender_name).replace(
                                "\n", "<br>"
                            )
                            + unsubscribe_html
                        )

                        msg = MIMEMultipart()
                        msg["From"] = f"{sender_name} <{sender_email}>"
                        msg["To"] = rcv_email
                        msg["Subject"] = subject_line
                        msg.attach(MIMEText(personalized_body, "html"))

                        server.sendmail(sender_email, rcv_email, msg.as_string())
                        success_count += 1
                        sent_with_this_id += 1
                        recipient_index += 1

                        progress = recipient_index / total_recipients
                        progress_bar.progress(min(progress, 1.0))

                        # Human-like delay (60 se 120 seconds taaki spam flag na ho)
                        if recipient_index < total_recipients:
                            delay_seconds = random.randint(60, 120)
                            for remaining in range(delay_seconds, 0, -1):
                                status_text.info(
                                    f"📨 ID: {sender_email} | Sent: {sent_with_this_id}/10"
                                    f" | Next email in {remaining}s..."
                                )
                                time.sleep(1)

                    server.quit()

                except Exception as e:
                    status_text.warning(
                        f"⚠️ ID {sender_email} error: {e}. Moving to next ID..."
                    )
                    time.sleep(2)
                    continue

            status_text.empty()
            progress_bar.empty()

            st.balloons()
            st.success(
                f"✅ शानदार! कुल {success_count} ईमेल सफलतापूर्वक 130 IDs के रोटेशन"
                " और एंटी-स्पैम डिले के साथ भेज दिए गए!"
            )
