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

# --- CSS & ANIMASI MATRIX ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

    * { cursor: crosshair !important; }

    .stApp {
        background-color: #000;
        color: #00ff41;
        font-family: 'Share Tech Mono', monospace;
    }

    /* GLITCH HEADER */
    .glitch-header {
        color: #00ff41;
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        text-shadow: 2px 2px #003300;
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
        z-index: 100;
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
        width: 100%;
        z-index: 100;
    }
    .stButton > button:hover {
        background: #00ff41;
        color: black;
        box-shadow: 0 0 30px #00ff41;
        font-weight: bold;
    }

    /* RESULT BOXES */
    .result-box {
        border: 1px solid #00ff41;
        padding: 10px;
        margin-bottom: 10px;
        background: rgba(0, 20, 0, 0.8);
    }
    .manual-box {
        border: 1px solid #ffcc00;
        padding: 10px;
        margin-bottom: 10px;
        background: rgba(20, 20, 0, 0.8);
        color: #ffcc00;
    }
    a { text-decoration: none; font-weight: bold; }
    
    /* MATRIX CANVAS */
    #matrix-canvas {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -1;
        opacity: 0.15;
        pointer-events: none;
    }

    /* HIDE UI */
    #MainMenu, footer, header {visibility: hidden;}
    
</style>

<canvas id="matrix-canvas"></canvas>
<script>
    const canvas = document.getElementById('matrix-canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    const katakana = '01';
    const letters = katakana.split('');
    const fontSize = 16;
    const columns = canvas.width / fontSize;
    const drops = [];
    for(let x = 0; x < columns; x++) { drops[x] = 1; }
    function draw() {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#0F0';
        ctx.font = fontSize + 'px monospace';
        for(let i = 0; i < drops.length; i++) {
            const text = letters[Math.floor(Math.random() * letters.length)];
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);
            if(drops[i] * fontSize > canvas.height && Math.random() > 0.975) { drops[i] = 0; }
            drops[i]++;
        }
    }
    setInterval(draw, 33);
    window.addEventListener('resize', () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });
</script>
""", unsafe_allow_html=True)

# --- LOGIKA PROGRAM ---
def check_username(username):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    # KATEGORI 1: SITUS YANG BISA DISCAN OTOMATIS
    sites_auto = {
        "GITHUB": "https://github.com/{}",
        "SPOTIFY": "https://open.spotify.com/user/{}",
        "WATTPAD": "https://www.wattpad.com/user/{}",
        "ROBLOX": "https://www.roblox.com/user.aspx?username={}",
        "STEAM": "https://steamcommunity.com/id/{}",
        "PINTEREST": "https://www.pinterest.com/{}",
        "VIMEO": "https://vimeo.com/{}",
        "MEDIUM": "https://medium.com/@{}",
    }

    # KATEGORI 2: SITUS HIGH SECURITY (ANTI-BOT) - WAJIB CEK MANUAL
    sites_manual = {
        "INSTAGRAM": "https://www.instagram.com/{}",
        "TIKTOK": "https://www.tiktok.com/@{}",
        "TWITTER / X": "https://twitter.com/{}",
        "FACEBOOK": "https://www.facebook.com/{}",
        "TELEGRAM": "https://t.me/{}",
        "YOUTUBE": "https://www.youtube.com/@{}"
    }

    found_list = []
    
    # Progress Bar
    progress_text = "INITIALIZING BRUTEFORCE..."
    my_bar = st.progress(0, text=progress_text)
    
    total = len(sites_auto) + len(sites_manual)
    count = 0

    # 1. SCANNING AUTO SITES
    for site, url_pattern in sites_auto.items():
        url = url_pattern.format(username)
        count += 1
        my_bar.progress(count / total, text=f"HACKING NODE: {site}...")
        
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
    
    return found_list, sites_manual

# --- TAMPILAN UTAMA ---
st.markdown("<div class='glitch-header'>SYSTEM OVERRIDE</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #fff; background: rgba(0,0,0,0.5);'>[ TARGET IDENTIFICATION PROTOCOL ]</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

target = st.text_input("", placeholder="ENTER USERNAME HERE")
st.markdown("<br>", unsafe_allow_html=True)

if st.button("INITIATE SEARCH"):
    if target:
        st.write(f"CONNECTING TO SERVER... [TARGET: {target}]")
        time.sleep(1)
        
        # Jalankan Scan
        hits, manuals = check_username(target)
        
        st.markdown("---")
        
        # HASIL 1: YANG BERHASIL DITEMUKAN (HIJAU)
        st.markdown("### ✅ CONFIRMED HITS (SCANNED):")
        if hits:
            for site, url in hits:
                st.markdown(f"""
                <div class='result-box'>
                    <span style='color: #00ff41; font-weight: bold;'>[FOUND] {site}</span><br>
                    <a href='{url}' target='_blank' style='color: #fff;'>└─ ACCESS DATA >></a>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("NO OPEN DATA FOUND IN PUBLIC NODES.")

        st.markdown("---")

        # HASIL 2: YANG WAJIB CEK MANUAL (KUNING)
        st.markdown("### ⚠️ HIGH SECURITY NODES (MANUAL CHECK REQUIRED):")
        st.info("Situs di bawah ini memblokir scanner otomatis. Klik link secara manual untuk memastikan.")
        
        col1, col2 = st.columns(2)
        idx = 0
        for site, url_pattern in manuals.items():
            url = url_pattern.format(target)
            
            # Membagi tampilan jadi 2 kolom
            with (col1 if idx % 2 == 0 else col2):
                st.markdown(f"""
                <div class='manual-box'>
                    <span style='color: #ffcc00; font-weight: bold;'>[SECURE] {site}</span><br>
                    <a href='{url}' target='_blank' style='color: #fff;'>└─ CLICK TO CHECK >></a>
                </div>
                """, unsafe_allow_html=True)
            idx += 1

    else:
        st.warning("ERROR: INPUT PARAMETER MISSING.")

# --- SIGNATURE ---
st.markdown("<br><br><div style='text-align: center; color: #00ff41; opacity: 0.7;'>// DEVELOPED BY TAKSVJ // V.4.0 //</div>", unsafe_allow_html=True)
