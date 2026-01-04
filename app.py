import streamlit as st
import requests
import time
import random

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="CYBER OSINT // TAKSVJ",
    page_icon="💀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- MATRIKS RAIN ANIMATION & GLOBAL CSS ---
st.markdown("""
<style>
    /* Import Font Hacker */
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

    /* PAKSA CURSOR JADI CROSSHAIR UNTUK SEMUA ELEMEN */
    * {
        cursor: crosshair !important;
    }

    /* BACKGROUND UTAMA */
    .stApp {
        background-color: #000;
        color: #00ff41;
        font-family: 'Share Tech Mono', monospace;
    }

    /* TITLE GLITCH */
    @keyframes glitch {
        0% { transform: translate(0) }
        20% { transform: translate(-2px, 2px) }
        40% { transform: translate(-2px, -2px) }
        60% { transform: translate(2px, 2px) }
        80% { transform: translate(2px, -2px) }
        100% { transform: translate(0) }
    }
    .glitch-header {
        color: #00ff41;
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        text-shadow: 2px 2px #003300;
        animation: glitch 1.5s infinite;
        letter-spacing: 5px;
        margin-bottom: 20px;
    }

    /* INPUT FIELD */
    .stTextInput > div > div > input {
        background-color: rgba(0, 20, 0, 0.8) !important;
        color: #00ff41 !important;
        border: 2px solid #00ff41 !important;
        font-family: 'Share Tech Mono', monospace;
        text-align: center;
        font-size: 1.2rem;
        z-index: 100; /* Biar di atas matrix rain */
    }
    .stTextInput > div > div > input:focus {
        box-shadow: 0 0 20px #00ff41;
        background-color: #000 !important;
    }

    /* TOMBOL */
    .stButton > button {
        background: black;
        border: 2px solid #00ff41;
        color: #00ff41;
        font-family: 'Share Tech Mono', monospace;
        font-size: 1.5rem;
        text-transform: uppercase;
        padding: 10px;
        transition: 0.3s;
        z-index: 100;
    }
    .stButton > button:hover {
        background: #00ff41;
        color: black;
        box-shadow: 0 0 30px #00ff41;
        font-weight: bold;
    }

    /* HASIL SCAN */
    div[data-baseweb="notification"] {
        background-color: rgba(0, 0, 0, 0.9) !important;
        border: 1px solid #00ff41 !important;
        color: #00ff41 !important;
        z-index: 100;
    }
    a { color: #fff !important; text-decoration: none; border-bottom: 1px dotted #fff; }
    a:hover { text-shadow: 0 0 10px #fff; }

    /* CANVAS MATRIX RAIN (Ditaruh di belakang) */
    #matrix-canvas {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -1; /* Di belakang konten */
        opacity: 0.2; /* Transparan biar tulisan tetap terbaca */
        pointer-events: none;
    }

    /* SIGNATURE */
    .footer-sig {
        position: fixed;
        bottom: 10px;
        width: 100%;
        text-align: center;
        color: #00ff41;
        font-family: 'Share Tech Mono', monospace;
        opacity: 0.8;
        font-size: 1rem;
        pointer-events: none;
        text-shadow: 0 0 10px #00ff41;
        z-index: 99;
    }

    /* SEMBUNYIKAN UI BAWAAN */
    #MainMenu, footer, header {visibility: hidden;}
    
</style>

<canvas id="matrix-canvas"></canvas>
<script>
    const canvas = document.getElementById('matrix-canvas');
    const ctx = canvas.getContext('2d');

    // Set canvas full screen
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const katakana = '01'; // Bisa diganti '01' atau huruf jepang
    const letters = katakana.split('');

    const fontSize = 16;
    const columns = canvas.width / fontSize;

    const drops = [];
    for(let x = 0; x < columns; x++) {
        drops[x] = 1;
    }

    function draw() {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.05)'; // Efek trail pudar
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = '#0F0'; // Warna teks hijau
        ctx.font = fontSize + 'px monospace';

        for(let i = 0; i < drops.length; i++) {
            const text = letters[Math.floor(Math.random() * letters.length)];
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);

            if(drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
            }
            drops[i]++;
        }
    }
    setInterval(draw, 33); // Kecepatan animasi

    // Resize handling
    window.addEventListener('resize', () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
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
    
    # Progress Bar Custom
    progress_text = "INITIALIZING BRUTEFORCE..."
    my_bar = st.progress(0, text=progress_text)
    
    total = len(sites)
    count = 0

    for site, url_pattern in sites.items():
        url = url_pattern.format(username)
        count += 1
        
        status_msg = f"SCANNING NODE: {site}... {random.randint(10,99)}%"
        my_bar.progress(count / total, text=status_msg)
        
        try:
            response = requests.get(url, headers=headers, timeout=2)
            if response.status_code == 200:
                page_text = response.text.lower()
                if "not found" not in page_text and "404" not in page_text:
                    found_list.append((site, url))
        except:
            pass
        
        time.sleep(0.05)

    my_bar.progress(1.0, text="SCAN COMPLETE.")
    time.sleep(0.5)
    my_bar.empty()
    return found_list

# --- TAMPILAN UTAMA ---
st.markdown("<div class='glitch-header'>SYSTEM OVERRIDE</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #fff; letter-spacing: 3px; background: rgba(0,0,0,0.5); padding: 5px;'>[ TARGET IDENTIFICATION PROTOCOL ]</p>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Layout Input
target = st.text_input("", placeholder="ENTER USERNAME HERE")

st.markdown("<br>", unsafe_allow_html=True)

if st.button("INITIATE SEARCH"):
    if target:
        st.write(f"CONNECTING TO SERVER... [TARGET: {target}]")
        time.sleep(1)
        results = check_username(target)
        
        st.markdown("---")
        st.markdown("### DATABASE MATCHES:")
        if results:
            for site, url in results:
                st.success(f"HIT FOUND: {site}")
                st.markdown(f"└─ [ACCESS DATA]({url})")
        else:
            st.error("NEGATIVE RESULT. TARGET IS GHOSTING.")
    else:
        st.warning("ERROR: INPUT PARAMETER MISSING.")

# --- SIGNATURE FOOTER ---
st.markdown("<div class='footer-sig'>// DEVELOPED BY TAKSVJ // V.3.0 //</div>", unsafe_allow_html=True)
