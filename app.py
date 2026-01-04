import streamlit as st
import requests
import time
import random

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="CYBER OSINT // TARGET LOCKED",
    page_icon="👁️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- INJECT CSS & JAVASCRIPT ANIMATION ---
st.markdown("""
<style>
    /* Import Font Hacker */
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

    /* --- BASIC SETUP --- */
    .stApp {
        background-color: #050505;
        color: #00ff41;
        font-family: 'Share Tech Mono', monospace;
        cursor: crosshair !important; /* Mouse jadi bidikan */
        overflow-x: hidden;
    }

    /* --- GLITCH TITLE EFFECT --- */
    @keyframes glitch {
        0% { transform: translate(0) }
        20% { transform: translate(-2px, 2px) }
        40% { transform: translate(-2px, -2px) }
        60% { transform: translate(2px, 2px) }
        80% { transform: translate(2px, -2px) }
        100% { transform: translate(0) }
    }
    .glitch-text {
        color: #00ff41;
        font-size: 3em;
        font-weight: bold;
        text-align: center;
        text-shadow: 2px 2px #ff00ff;
        animation: glitch 1s infinite;
    }

    /* --- INPUT FIELDS --- */
    .stTextInput > div > div > input {
        background-color: #000 !important;
        color: #00ff41 !important;
        border: 1px solid #00ff41 !important;
        font-family: 'Share Tech Mono', monospace;
        box-shadow: 0 0 10px rgba(0, 255, 65, 0.2);
    }
    .stTextInput > div > div > input:focus {
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.6);
        border-color: #fff !important;
    }

    /* --- BUTTONS --- */
    .stButton > button {
        width: 100%;
        background: transparent;
        border: 2px solid #00ff41;
        color: #00ff41;
        font-family: 'Share Tech Mono', monospace;
        font-size: 1.2em;
        transition: 0.3s;
        text-transform: uppercase;
    }
    .stButton > button:hover {
        background: #00ff41;
        color: #000;
        box-shadow: 0 0 20px #00ff41;
        cursor: crosshair;
    }

    /* --- RESULT BOXES --- */
    div[data-baseweb="notification"] {
        background-color: rgba(0, 20, 0, 0.95) !important;
        border: 1px solid #00ff41 !important;
        border-left: 10px solid #00ff41 !important;
    }
    a {
        color: #fff !important;
        text-decoration: underline;
    }
    
    /* --- HIDE DEFAULT STREAMLIT UI --- */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

</style>

<script>
document.addEventListener('mousemove', function(e) {
    // Membuat elemen jejak
    let trail = document.createElement('div');
    trail.className = 'trail';
    document.body.appendChild(trail);

    // Posisi mengikuti mouse
    trail.style.left = e.pageX + 'px';
    trail.style.top = e.pageY + 'px';

    // Random ukuran biar variatif
    let size = Math.random() * 10 + 5; 
    trail.style.width = size + 'px';
    trail.style.height = size + 'px';

    // Styling CSS langsung di JS biar nempel
    trail.style.position = 'absolute';
    trail.style.background = '#00ff41';
    trail.style.borderRadius = '50%';
    trail.style.pointerEvents = 'none';
    trail.style.opacity = '0.8';
    trail.style.zIndex = '9999';
    trail.style.boxShadow = '0 0 10px #00ff41';
    trail.style.transition = 'all 0.5s linear';

    // Hilangkan elemen setelah 0.5 detik
    setTimeout(function() {
        trail.style.opacity = '0';
        trail.style.transform = 'scale(0)';
    }, 50);

    setTimeout(function() {
        trail.remove();
    }, 500);
});
</script>
""", unsafe_allow_html=True)

# --- LOGIKA PROGRAM ---
def check_username(username):
    # Simulasi headers
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    # Database situs
    sites = {
        "INSTAGRAM": "https://www.instagram.com/{}",
        "TIKTOK": "https://www.tiktok.com/@{}",
        "TWITTER/X": "https://twitter.com/{}",
        "FACEBOOK": "https://www.facebook.com/{}",
        "TELEGRAM": "https://t.me/{}",
        "GITHUB": "https://github.com/{}",
        "SPOTIFY": "https://open.spotify.com/user/{}",
        "YOUTUBE": "https://www.youtube.com/@{}",
        "WATTPAD": "https://www.wattpad.com/user/{}",
        "ROBLOX": "https://www.roblox.com/user.aspx?username={}",
        "STEAM": "https://steamcommunity.com/id/{}",
    }

    found_list = []
    
    # Progress Bar Hacker Style
    progress_text = "INITIALIZING BRUTEFORCE PROTOCOL..."
    my_bar = st.progress(0, text=progress_text)
    
    total = len(sites)
    count = 0

    for site, url_pattern in sites.items():
        url = url_pattern.format(username)
        count += 1
        
        # Animasi text berubah-ubah saat loading
        status_msg = f"SCANNING NODE [{site}]... {random.randint(10,99)}%"
        my_bar.progress(count / total, text=status_msg)
        
        try:
            response = requests.get(url, headers=headers, timeout=3)
            if response.status_code == 200:
                # Filter sederhana
                page_text = response.text.lower()
                if "not found" not in page_text and "404" not in page_text:
                    found_list.append((site, url))
        except:
            pass
        
        # Delay super cepat biar ada efek 'computing'
        time.sleep(0.05)

    my_bar.progress(1.0, text="ACCESS GRANTED. DATA RETRIEVED.")
    time.sleep(0.5)
    my_bar.empty()
    return found_list

# --- TAMPILAN UTAMA ---
st.markdown("<div class='glitch-text'>SYSTEM // OVERRIDE</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #fff; letter-spacing: 2px;'>[ TARGET IDENTIFICATION PROTOCOL ]</p>", unsafe_allow_html=True)

st.markdown("---")

col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    target = st.text_input("", placeholder="ENTER USERNAME_")

    if st.button(">> INITIATE SEARCH <<"):
        if target:
            st.write(f">> CONNECTING TO SERVER... [TARGET: {target}]")
            time.sleep(1) # Efek dramatis
            results = check_username(target)
            
            st.markdown("### >> DATABASE MATCHES:")
            if results:
                for site, url in results:
                    st.success(f"HIT FOUND: {site}")
                    st.markdown(f"└─ [ACCESS DATA]({url})")
            else:
                st.error("NEGATIVE RESULT. TARGET IS GHOSTING.")
        else:
            st.warning("ERROR: INPUT PARAMETER MISSING.")

# Footer
st.markdown("<br><br><br><center style='color: #004400;'>SECURE CONNECTION ESTABLISHED<br>SESSION ID: X99-21</center>", unsafe_allow_html=True)
