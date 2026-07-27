import streamlit as st
import smtplib
from email.mime.text import MIMEText
import time
 
# वेबसाइट का डिज़ाइन
st.title("Prateek's SEO Email Tool 🚀")
st.write("एक नाम से कई ईमेल पर बल्क मेल भेजने का डैशबोर्ड")
 
# 1. जीमेल और पासवर्ड के लिए बॉक्स
st.subheader("1. अपनी जीमेल डिटेल्स डालें")
sender_email = st.text_input("अपनी Gmail ID डालें:")
app_password = st.text_input("अपना 16-डिजिट का पासवर्ड डालें:", type="password")
 
st.markdown("---") 
 
# 2. सब्जेक्ट और ईमेल टेम्पलेट के लिए अलग बॉक्स
st.subheader("2. ईमेल कंटेंट (सब्जेक्ट और मैसेज)")
 
default_subject = "Quick question regarding your website's SEO"
email_subject = st.text_input("यहाँ सब्जेक्ट लाइन (Subject Line) लिखें:", value=default_subject)
 
default_body = """Hi {name},
 
I was doing some research in your industry and came across your website. Great work on the design! 
 
However, while browsing, I noticed a few technical SEO issues that might be stopping your website from ranking higher on Google and getting more organic traffic. 
 
I would love to share a few quick fixes that can help improve your search ranking. Would you be open to a quick 5-minute chat this week?
 
Best regards,
Prateek Kushwaha
SEO Specialist"""
 
email_template = st.text_area("यहाँ अपना ईमेल मैसेज (Template) लिखें:", value=default_body, height=200)
 
st.markdown("---")
 
# 3. एक नाम और बहुत सारी ईमेल के लिए बॉक्सेस
st.subheader("3. क्लाइंट का डेटा")
common_name = st.text_input("वह नाम जो सभी मेल्स में जाएगा (जैसे: Sir/Madam या Website Owner):", value="Sir/Madam")
 
st.write("नीचे एक-एक लाइन में अपनी सारी ईमेल आईडी पेस्ट कर दें (जितनी चाहें उतनी):")
emails_list_text = st.text_area("यहाँ ईमेल लिस्ट डालें (हर लाइन में एक ईमेल):", height=150, placeholder="email1@gmail.com\nemail2@gmail.com\nemail3@gmail.com")
 
st.markdown("---")
 
# 4. ईमेल भेजने का बटन
if st.button("Send Bulk Emails Now 🚀", type="primary"):
    if not sender_email or not app_password:
        st.warning("⚠️ कृपया अपनी जीमेल आईडी और पासवर्ड ज़रूर डालें।")
    elif not emails_list_text.strip():
        st.warning("⚠️ कृपया कम से कम एक ईमेल आईडी ज़रूर डालें।")
    else:
        try:
            st.info("सर्वर से कनेक्ट हो रहा है...")
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, app_password)
            st.success("✅ Login Successful!")
 
            # ईमेल लिस्ट को अलग-अलग लाइनों में बांटना
            emails = [e.strip() for e in emails_list_text.strip().split('\n') if e.strip()]
            name_to_use = common_name.strip() if common_name.strip() else "Sir/Madam"
 
            success_count = 0
            for receiver_email in emails:
                # मैसेज तैयार करना
                body = email_template.format(name=name_to_use)
                
                msg = MIMEText(body)
                msg['Subject'] = email_subject
                msg['From'] = sender_email
                msg['To'] = receiver_email
 
                # मेल भेजना
                server.send_message(msg)
                st.write(f"✅ ({receiver_email}) को ईमेल भेज दिया गया!")
                success_count += 1
                
                # स्पैम से बचने के लिए 8 सेकंड का गैप
                time.sleep(8) 
 
            server.quit()
            st.balloons()
            st.success(f"🎉 कुल {success_count} लोगों को सफलतापूर्वक ईमेल भेज दिए गए हैं!")
 
        except Exception as e:
            st.error(f"❌ कोई एरर आ गई: {e}")
st.info
 