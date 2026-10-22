import streamlit as st
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64
from email.message import EmailMessage

# Gmail API scopes (Read aur Send dono ke liye)
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    if 'credentials' not in st.session_state:
        # Aapko Google Cloud Console se credentials.json file download karni hogi
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        st.session_state['credentials'] = flow.run_local_server(port=0)
    
    creds = st.session_state['credentials']
    service = build('gmail', 'v1', credentials=creds)
    return service

st.title("⚡ Wild Rank Outlook Dashboard - Live Gmail")

# Login Button agar authenticate nahi hai
if 'credentials' not in st.session_state:
    if st.button("🔐 Login with Google (Gmail API)"):
        try:
            service = get_gmail_service()
            st.success("Successfully Connected to Gmail!")
            st.rerun()
        except Exception as e:
            st.error(f"Login Failed: {e}")
else:
    service = get_gmail_service()
    
    # 1. RECEIVING / FETCHING EMAILS (Inbox)
    st.subheader("📥 Inbox")
    try:
        results = service.users().messages().list(userId='me', maxResults=10, q="in:inbox").execute()
        messages = results.get('messages', [])
        
        if messages:
            for msg in messages:
                txt = service.users().messages().get(userId='me', id=msg['id'], format='metadata', metadataHeaders=['Subject', 'From', 'Date']).execute()
                headers = txt['payload']['headers']
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
                
                with st.expander(f"✉️ {subject} (From: {sender})"):
                    st.write(f"Snippet: {txt.get('snippet', '')}")
        else:
            st.info("No messages found in Inbox.")
    except Exception as e:
        st.error(f"Error fetching inbox: {e}")
        
    # 2. SENDING EMAIL
    st.subheader("📤 Compose & Send New Email")
    with st.form("send_form"):
        to_email = st.text_input("To (Recipient Email)")
        subject = st.text_input("Subject")
        body = st.text_area("Message Body")
        submit_btn = st.form_submit_button("Send Email")
        
        if submit_btn:
            try:
                message = EmailMessage()
                message.set_content(body)
                message['To'] = to_email
                message['Subject'] = subject
                
                # Encode message for Gmail API
                encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
                create_message = {'raw': encoded_message}
                
                sent_message = service.users().messages().send(userId="me", body=create_message).execute()
                st.success(f"Email sent successfully! (ID: {sent_message['id']})")
            except Exception as e:
                st.error(f"Failed to send email: {e}")
