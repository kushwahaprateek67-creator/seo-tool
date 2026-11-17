
import csv
import io
import re
import ssl
import time
import smtplib
import html
from datetime import datetime
from email.message import EmailMessage
from email.utils import formataddr
from urllib.parse import quote

import pandas as pd
import streamlit as st


# ==================================================
# PAGE SETTINGS
# ==================================================
st.set_page_config(
    page_title="AI SEO Email Outreach",
    page_icon="✉️",
    layout="wide"
)


# ==================================================
# DARK BLUE PROFESSIONAL DESIGN
# ==================================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #06152e 0%, #0b2345 55%, #102d50 100%);
    color: #f4f7fb;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3, h4, p, label, span {
    color: #f4f7fb;
}

div[data-testid="stSidebar"] {
    background: #071a35;
    border-right: 1px solid #1d3d63;
}

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    background-color: #102b4d;
    color: #ffffff;
    border: 1px solid #315477;
    border-radius: 8px;
}

div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    border-color: #38a7ff;
    box-shadow: 0 0 0 1px #38a7ff;
}

.stButton button {
    background: linear-gradient(90deg, #0878d1, #1595f5);
    color: white;
    border: none;
    border-radius: 9px;
    font-weight: 700;
    min-height: 43px;
    padding: 0.4rem 1.2rem;
}

.stButton button:hover {
    background: linear-gradient(90deg, #1595f5, #38a7ff);
    color: white;
    border: none;
}

div[data-testid="stMetric"] {
    background: #102b4d;
    border: 1px solid #24496f;
    padding: 15px;
    border-radius: 12px;
}

div[data-testid="stAlert"] {
    border-radius: 10px;
}

hr {
    border-color: #29496b;
}
