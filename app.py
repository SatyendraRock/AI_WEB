import streamlit as st
import pandas as pd
import qrcode
from PIL import Image
from io import BytesIO
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="NEON PULSE // CA 2026", page_icon="⚡", layout="wide")

# --- CUSTOM THEME (Dark Glassmorphism) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@700&family=Inter:wght@300;400;600&display=swap');
    
    .stApp {
        background-color: #050505;
        color: white;
        font-family: 'Inter', sans-serif;
    }
    
    .font-heading { font-family: 'Syncopate', sans-serif; }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 1rem;
    }
    
    .neon-text {
        text-shadow: 0 0 10px #00f2ff, 0 0 20px #00f2ff;
        color: #00f2ff;
        font-family: 'Syncopate', sans-serif;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #bf00ff, #00f2ff);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = "Home"

# --- HELPER FUNCTIONS ---
def generate_qr(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf

# --- NAVIGATION ---
with st.sidebar:
    st.markdown("<h1 class='neon-text'>NEON PULSE</h1>", unsafe_allow_html=True)
    if not st.session_state.logged_in:
        choice = st.radio("Navigation", ["Home", "Lineup", "Tickets", "Login / Sign Up"])
    else:
        choice = st.radio("User Portal", ["Dashboard", "Book Tickets", "Admin Panel", "Logout"])

    if choice == "Logout":
        st.session_state.logged_in = False
        st.rerun()
    
    st.session_state.page = choice

# --- PAGE: HOME ---
if st.session_state.page == "Home":
    st.markdown("<h1 class='font-heading' style='font-size: 70px; line-height: 1;'>THE FUTURE<br><span style='color:#bf00ff'>OF SOUND</span></h1>", unsafe_allow_html=True)
    st.write("### August 14-16 // Joshua Tree, California")
    
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=800")
    with col2:
        st.markdown("""
        <div class='glass-card'>
            <h4>EXPERIENCE IMMERSION</h4>
            <p style='color: #888;'>Join us for a 3-day odyssey through electronic soundscapes and desert art installations.</p>
            <hr style='border-color: rgba(255,255,255,0.1)'>
            <p><b>EARLY BIRD ENDS IN:</b> 01:54:22</p>
        </div>
        """, unsafe_allow_html=True)

# --- PAGE: LOGIN / SIGN UP ---
elif st.session_state.page == "Login / Sign Up":
    st.markdown("<h2 class='font-heading'>SECURE ACCESS</h2>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        if st.button("LOGIN"):
            with st.spinner("Authenticating..."):
                time.sleep(1.5)
                st.session_state.logged_in = True
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE: BOOK TICKETS (The Form) ---
elif st.session_state.page == "Book Tickets":
    st.markdown("<h2 class='font-heading'>RESERVE YOUR PASS</h2>", unsafe_allow_html=True)
    
    with st.form("booking_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name (as per ID)")
            phone = st.text_input("Phone Number")
            tier = st.selectbox("Ticket Tier", ["General Admission ($299)", "VIP Infinity ($599)"])
        with col2:
            addr = st.text_area("Home Address")
            # NOTE: In a real app, this file would be uploaded to a secure, encrypted S3 bucket.
            id_file = st.file_uploader("Upload Government ID (JPG/PNG)", type=['png', 'jpg', 'jpeg'])
            
        st.info("🔒 Your data is protected using simulation-level security.")
        
        submitted = st.form_submit_state = st.form_submit_button("PROCEED TO SECURE PAYMENT")
        
        if submitted:
            if name and id_file:
                st.success("Redirecting to Secure Payment Gateway...")
                time.sleep(2)
                st.balloons()
                st.session_state.booking_success = True
                st.session_state.page = "Dashboard"
                st.rerun()
            else:
                st.error("Please complete all fields and upload your ID.")

# --- PAGE: DASHBOARD ---
elif st.session_state.page == "Dashboard":
    st.markdown("<h2 class='font-heading'>YOUR DASHBOARD</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.write("### ACTIVE TICKETS")
        st.write("**Event:** Neon Pulse // California 2026")
        st.write("**Tier:** VIP Infinity")
        st.write("**Status:** ✅ Verified")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='glass-card' style='text-align: center;'>", unsafe_allow_html=True)
        st.write("YOUR ENTRY QR")
        qr_img = generate_qr("TICKET-VP-99283-CONFIRMED")
        st.image(qr_img, width=200)
        st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE: ADMIN PANEL ---
elif st.session_state.page == "Admin Panel":
    st.markdown("<h2 class='font-heading'>ADMIN COMMAND CENTER</h2>", unsafe_allow_html=True)
    
    # Mock Analytics
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Revenue", "$142,500", "+12%")
    m2.metric("Tickets Sold", "482 / 1000", "48%")
    m3.metric("Pending Verifications", "14", "-2")
    
    st.write("### RECENT BOOKINGS")
    mock_data = {
        "Customer": ["Alex Rivers", "Sarah Chen", "Jordan Smith"],
        "Tier": ["VIP", "GA", "VIP"],
        "Payment": ["Paid", "Paid", "Pending"],
        "ID Status": ["Verified", "Pending Review", "Verified"]
    }
    st.table(pd.DataFrame(mock_data))
    
    st.write("### ID VERIFICATION QUEUE")
    st.info("Reviewing 1 pending ID for: **Sarah Chen**")
    st.image("https://images.unsplash.com/photo-1557683311-eac922347aa1?q=80&w=400", caption="Mock ID Document Preview")
    if st.button("APPROVE DOCUMENT"):
        st.success("Ticket activated for Sarah Chen.")

# --- FOOTER ---
st.markdown("<br><hr><center style='color: #444; font-size: 10px; letter-spacing: 2px;'>© 2026 NEON PULSE FESTIVAL PROTOTYPE</center>", unsafe_allow_html=True)
