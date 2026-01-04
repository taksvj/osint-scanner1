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
        background-color: #020202; /* Hitam lebih pekat */
        color: #00ff41;
        font-family: 'Share Tech Mono', monospace;
        cursor: crosshair !important;
        overflow-x: hidden; /* Mencegah scrollbar samping saat animasi keluar layar */
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
        letter-spacing: 5px;
    }

    /* --- INPUT FIELDS --- */
    .stTextInput > div > div > input {
        background-color: #0a0a0a !important;
        color: #00ff41 !important;
        border: 1px solid #00ff41 !important;
        font-family: 'Share Tech Mono', monospace;
        box-shadow: inset 0 0 10px rgba(0, 255, 65, 0.1);
    }
    .stTextInput > div > div > input:focus {
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.6);
        border-color: #fff !important;
        background-color: #000 !important;
    }

    /* --- BUTTONS --- */
    .stButton > button {
        width: 100%;
        background: rgba(0, 255, 65, 0.1);
        border: 1px solid #00ff41;
        color: #00ff41;
        font-family: 'Share Tech Mono', monospace;
        font-size: 1.2em;
        transition: 0.3s;
        text-transform: uppercase;
        letter-spacing: 3px;
    }
    .stButton > button:hover {
        background: #00ff41;
        color: #000;
        box-shadow: 0 0 30px #00ff41;
        cursor: crosshair;
        font-weight: bold;
    }

    /* --- RESULT BOXES --- */
    div[data-baseweb="notification"] {
        background-color: rgba(0, 10, 0, 0.9) !important;
        border: 1px solid #00ff41 !important;
        border-left: 5px solid #00ff41 !important;
        box-shadow: 0 0 10px rgba(0, 255, 65, 0.2);
    }
    a {
        color: #fff !important;
        text-decoration: none;
        border-bottom: 1px dotted #00ff41;
    }
    a:hover {
        text-shadow: 0 0 10px #ffffff;
        border-bottom: 1px solid #ffffff;
    }
    
    /* --- SIGNATURE FOOTER --- */
    .signature-container {
        position: fixed;
        left: 0;
        bottom: 20px;
        width: 100%;
        text-align: center;
        pointer-events: none; /* Agar tidak mengganggu klik */
        z-index: 99;
    }
    .signature-text {
        font-family: 'Share Tech Mono', monospace;
        color: #00ff41;
        font-size: 1.2em;
        letter-spacing: 4px;
        text-transform: uppercase;
        text-shadow: 0 0 10px #00ff41, 0 0 20px #00ff41, 0 0 40px #00ff41;
        opacity: 0.7;
    }

    /* --- HIDE DEFAULT STREAMLIT UI --- */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

</style>

<script>
document.addEventListener('mousemove', function(e) {
    // Karakter biner acak
    const binaryChars = ['0', '1'];
    const char = binaryChars[Math.floor(Math.random() * binaryChars.length)];

    // Membuat elemen span untuk karakter biner
    let binaryDrop = document.createElement('span');
    binaryDrop.innerText = char;
    binaryDrop.className = 'binary-trail';
    document.body.appendChild(binaryDrop);

    // Posisi mengikuti mouse dengan sedikit variasi acak
    let x = e.pageX + (Math.random() * 20 - 10);
    let y = e.pageY;
    
    binaryDrop.style.left = x + 'px';
    binaryDrop.style.top = y + 'px';

    // Styling CSS langsung di JS
    binaryDrop.style.position = 'absolute';
    binaryDrop.style.color = '#00ff41';
    binaryDrop.style.fontSize = (Math.random() * 10 + 12) + 'px'; // Ukuran acak
    binaryDrop.style.fontFamily = 'Share Tech Mono, monospace';
    binaryDrop.style.pointerEvents = 'none';
    binaryDrop.style.zIndex = '9998';
    binaryDrop.style.textShadow = '0 0 5px #00ff41';
    binaryDrop.style.opacity = '1';
    binaryDrop.style.transition = 'all 1s ease-out'; // Animasi jatuh dan pudar

    // Animasi jatuh ke bawah dan menghilang
    setTimeout(function() {
        binaryDrop.style.top = (y + 100) + 'px'; // Jatuh 100px ke bawah
        binaryDrop.style.opacity = '0';
    }, 50);

    // Hapus elemen setelah animasi selesai
    setTimeout(function() {
        binaryDrop.remove();
    }, 1000);
});
</script>
""", unsafe_allow_html=True)

# --- LOGIKA PROGRAM ---
def check_username(username):
    headers = {'User-Agent': 'Mozilla/5.0'}
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
    
    # Progress Bar (Teks lebih bersih tanpa panah)
    progress_text = "INITIALIZING BRUTEFORCE PROTOCOL..."
    my_bar = st.progress(0, text=progress_text)
    
    total = len(sites)
    count = 0

    for site, url_pattern in sites.items():
        url = url_pattern.format(username)
        count += 1
        
        status_msg = f"SCANNING NODE [{site}]... {random.randint(10,99)}%"
        my_bar.progress(count / total, text=status_msg)
        
        try:
            response = requests.get(url, headers=headers, timeout=3)
            if response.status_code == 200:
                page_text = response.text.lower()
                if "not found" not in page_text and "404" not in page_text:
                    found_list.append((site, url))
        except:
            pass
        
        time.sleep(0.05)

    my_bar.progress(1.0, text="ACCESS GRANTED. DATA RETRIEVED.")
    time.sleep(0.5)
    my_bar.empty()
    return found_list

# --- TAMPILAN UTAMA ---
st.markdown("<div class='glitch-text'>SYSTEM OVERRIDE</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #fff; letter-spacing: 3px; opacity: 0.7;'>[ TARGET IDENTIFICATION PROTOCOL ]</p>", unsafe_allow_html=True)

st.markdown("---")

col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    target = st.text_input("", placeholder="ENTER USERNAME")

    # Tombol bersih tanpa panah
    if st.button("[ INITIATE SEARCH ]"):
        if target:
            st.write(f"CONNECTING TO SERVER... [TARGET: {target}]")
            time.sleep(1)
            results = check_username(target)
            
            # Judul hasil bersih tanpa panah
            st.markdown("### DATABASE MATCHES:")
            if results:
                for site, url in results:
                    st.success(f"HIT FOUND: {site}")
                    st.markdown(f"└─ [ACCESS DATA]({url})")
            else:
                st.error("NEGATIVE RESULT. TARGET IS GHOSTING.")
        else:
            st.warning("ERROR: INPUT PARAMETER MISSING.")

# --- SIGNATURE FOOTER (Bagian Bawah) ---
st.markdown("""
<div class='signature-container'>
    <div class='signature-text'>// DEVELOPED BY TAKSVJ //</div>
</div>
""", unsafe_allow_html=True)
