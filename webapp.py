import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Outlook Style Cold Email Dashboard",
    page_icon="📧",
    layout="wide"
)

# Custom CSS for Outlook-like Dark Theme (Black BG, Neon Blue Borders, Gold Accents)
st.markdown("""
    <style>
    /* Main Background & Theme */
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #00f0ff;
    }
    
    /* Card / Container Styling */
    .email-card {
        background-color: #1f2937;
        border: 1px solid #1e3a8a;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 8px;
        transition: 0.3s;
    }
    .email-card:hover {
        border-color: #00f0ff;
        box-shadow: 0 0 10px rgba(0, 240, 255, 0.2);
    }
    
    /* Gold Accents for Branding & Headers */
    h1, h2, h3, .gold-text {
        color: #fbbf24 !important;
    }
    
    /* Neon Blue Buttons */
    .stButton>button {
        background-color: #1e3a8a;
        color: #ffffff;
        border: 1px solid #00f0ff;
        border-radius: 6px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #00f0ff;
        color: #0b0f19;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar - Accounts & Folders (Outlook Style)
with st.sidebar:
    st.markdown("### ⚡ Wild Rank Outlook")
    st.markdown("---")
    
    # Account Selector
    selected_account = st.selectbox(
        "Connected Accounts",
        ["outreach1@wildrank.com", "outreach2@wildrank.com", "support@wildrank.com"]
    )
    
    st.markdown("---")
    
    # Navigation Folders
    folder = st.radio(
        "Folders",
        ["📥 Inbox", "📤 Sent", "📝 Drafts", "⏳ Scheduled", "🗑️ Trash"]
    )
    
    st.markdown("---")
    if st.button("➕ New Email / Compose", use_container_width=True):
        st.session_state['compose_open'] = True

# Main Layout: Split Pane (Left: Email List, Right: Reading/Compose Pane)
col1, col2 = st.columns([1, 2], gap="medium")

with col1:
    st.markdown(f"### {folder}")
    search_query = st.text_input("🔍 Search emails...", placeholder="Search leads, subject...")
    
    st.markdown("---")
    
    # Dummy Email List (Outlook style item)
    emails = [
        {"sender": "John Doe", "subject": "SEO Backlink Proposal", "time": "10:45 AM", "snippet": "Hey Prateek, interested in your services..."},
        {"sender": "Sarah Smith", "subject": "Cold Outreach Strategy", "time": "Yesterday", "snippet": "Can we schedule a quick call tomorrow?"},
        {"sender": "Alex Mercer", "subject": "Collaboration Inquiry", "time": "Oct 20", "snippet": "Loved your 3D animation shorts!"}
    ]
    
    selected_email_idx = 0
    for idx, em in enumerate(emails):
        if st.button(f"**{em['sender']}**\n\n_{em['subject']}_\n\n{em['snippet']}", key=f"email_{idx}", use_container_width=True):
            selected_email_idx = idx

with col2:
    if st.session_state.get('compose_open', False):
        st.markdown("### ✉️ New Message")
        to_email = st.text_input("To:")
        subject = st.text_input("Subject:")
        body = st.text_area("Message Body", height=200)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🚀 Send Now", use_container_width=True):
                st.success("Email sent successfully!")
                st.session_state['compose_open'] = False
        with c2:
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state['compose_open'] = False
    else:
        st.markdown("### 📖 Reading Pane")
        st.markdown("---")
        active_email = emails[selected_email_idx]
        st.markdown(f"### **{active_email['subject']}**")
        st.markdown(f"**From:** {active_email['sender']} | **Time:** {active_email['time']}")
        st.markdown("---")
        st.write(f"Hello Prateek,\n\n{active_email['snippet']}\n\nLooking forward to your response.\n\nBest regards,\n{active_email['sender']}")
        
        st.markdown("---")
        col_reply, col_forward = st.columns(2)
        with col_reply:
            st.button("↩️ Reply", use_container_width=True)
        with col_forward:
            st.button("➡️ Forward", use_container_width=True)
