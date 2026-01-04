import streamlit as st
import requests
import time
import random

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="NEON OSINT // TAKSVJ",
    page_icon="👾",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS: CYBERPUNK + PACMAN LOADING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

    :root {
        --neon-pink: #ff2a6d;
        --neon-blue: #05d9e8;
        --pacman-yellow: #f2d648;
        --dark-bg: #01012b;
    }

    * { cursor: crosshair !important; }

    .stApp {
        background-color: var(--dark-bg);
        color: var(--neon-blue);
        font-family: 'Orbitron', sans-serif;
    }

    /* --- PAC-MAN LOADING ANIMATION (PURE CSS) --- */
    .pacman-holder {
        width: 100%;
        height: 100px;
        position: relative;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
        overflow: hidden;
    }

    /* Tubuh Pacman (Terdiri dari 2 bagian mulut) */
    .pacman {
        width: 0px;
        height: 0px;
        position: relative;
        animation: movePacman 2s linear infinite; 
    }
    
    .pacman > div {
        background-color: var(--pacman-yellow);
        width: 40px;
        height: 20px;
        position: absolute;
        left: -20px; /* Center adjustment */
    }
    
    /* Mulut Atas */
    .pacman > div:nth-child(1) {
        top: -20px;
        border-radius: 40px 40px 0 0;
        animation: chompTop 0.3s ease-in-out infinite alternate;
        transform-origin: bottom center;
    }
    
    /* Mulut Bawah */
    .pacman > div:nth-child(2) {
        top: 0;
        border-radius: 0 0 40px 40px;
        animation: chompBottom 0.3s ease-in-out infinite alternate;
        transform-origin: top center;
    }

    /* Titik-titik Makanan (Data Dots) */
    .dot {
        position: absolute;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background-color: var(--neon-pink);
        right: 0;
        top: 45px; /* Center vertical */
        animation: moveDot 2s linear infinite;
        box-shadow: 0 0 5px var(--neon-pink);
    }
    
    /* Delay untuk setiap dot biar ngantri */
    .dot:nth-child(3) { animation-delay: 0s; }
    .dot:nth-child(4) { animation-delay: 0.5s; }
    .dot:nth-child(5) { animation-delay: 1.0s; }
    .dot:nth-child(6) { animation-delay: 1.5s; }

    /* ANIMASI KEYFRAMES */
    @keyframes chompTop {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(-45deg); }
    }
    @keyframes chompBottom {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(45deg); }
    }
    @keyframes moveDot {
        0% { transform: translateX(200px); opacity: 1; }
        80% { opacity: 1; }
        100% { transform: translateX(-200px); opacity: 0; }
    }
    
    /* --- END PACMAN CSS --- */

    /* HEADER STYLE */
    .cyber-header {
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        color: white;
        text-shadow: 2px 2px 0px var(--neon-pink), -2px -2px 0px var(--neon-blue);
        letter-spacing: 4px;
        text-transform: uppercase;
    }

    /* INPUT STYLE */
    .stTextInput > div > div > input {
        background-color: rgba(5, 217, 232, 0.1) !important;
        color: var(--neon-blue) !important;
        border: 2px solid var(--neon-blue) !important;
        font-family: 'Orbitron', sans-serif;
        text-align: center;
        font-size: 1.2rem;
        box-shadow: 0 0 10px var(--neon-blue);
        border-radius: 0;
        z-index: 100;
    }

    /* BUTTON STYLE */
    .stButton > button {
        background: transparent;
        border: 2px solid var(--neon-pink);
        color: var(--neon-pink);
        font-family: 'Orbitron', sans-serif;
        font-size: 1.2rem;
        font-weight: bold;
        text-transform: uppercase;
        padding: 15px;
        width: 100%;
        transition: 0.3s;
        box-shadow: 0 0 5px var(--neon-pink);
        z-index: 100;
    }
    .stButton > button:hover {
        background: var(--neon-pink);
        color: #fff;
        box-shadow: 0 0 25px var(--neon-pink);
        transform: scale(1.02);
    }

    /* RESULT STYLES */
    .result-box {
        border-left: 5px solid var(--neon-blue);
        background: linear-gradient(90deg, rgba(5, 217, 232, 0.1) 0%, rgba(0,0,0,0) 100%);
        padding: 15px; margin-bottom: 10px;
    }
    .manual-box {
        border-left: 5px solid var(--neon-pink);
        background: linear-gradient(90deg, rgba(255, 42, 109, 0.1) 0%, rgba(0,0,0,0) 100%);
        padding: 15px; margin-bottom: 10px;
    }
    a { text-decoration: none; font-weight: bold; }
    
    .link-blue { color: var(--neon-blue) !important; }
    .link-pink { color: var(--neon-pink) !important; }

    /* HIDE UI & CANVAS BG */
    #cyber-canvas { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -1; opacity: 0.3; pointer-events: none; }
    #MainMenu, footer, header {visibility: hidden;}
    .footer-sig { text-align: center; color: rgba(255,255,255,0.5); font-size: 0.8rem; margin-top: 50px; letter-spacing: 2px; }
</style>

<canvas id="cyber-canvas"></canvas>
<script>
    const canvas = document.getElementById('cyber-canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    const chars = '01';
    const letters = chars.split('');
    const fontSize = 14;
    const columns = canvas.width / fontSize;
    const drops = [];
    for(let x = 0; x < columns; x++) { drops[x] = 1; }
    function draw() {
        ctx.fillStyle = 'rgba(1, 1, 43, 0.1)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.font = fontSize + 'px monospace';
        for(let i = 0; i < drops.length; i++) {
            const text = letters[Math.floor(Math.random() * letters.length)];
            ctx.fillStyle = (Math.random() > 0.5) ? '#ff2a6d' : '#05d9e8';
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);
            if(drops[i] * fontSize > canvas.height && Math.random() > 0.975) { drops[i] = 0; }
            drops[i]++;
        }
    }
    setInterval(draw, 40);
    window.addEventListener('resize', () => { canvas.width = window.innerWidth; canvas.height = window.innerHeight; });
</script>
""", unsafe_allow_html=True)

# --- LOGIKA PROGRAM ---
def check_username(username, loading_placeholder):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    sites_auto = {
        "GITHUB": "https://github.com/{}",
        "SPOTIFY": "https://open.spotify.com/user/{}",
        "WATTPAD": "https://www.wattpad.com/user/{}",
        "ROBLOX": "https://www.roblox.com/user.aspx?username={}",
        "STEAM": "https://steamcommunity.com/id/{}",
        "PINTEREST": "https://www.pinterest.com/{}",
        "MEDIUM": "https://medium.com/@{}",
    }

    sites_manual = {
        "INSTAGRAM": "https://www.instagram.com/{}",
        "TIKTOK": "https://www.tiktok.com/@{}",
        "TWITTER / X": "https://twitter.com/{}",
        "FACEBOOK": "https://www.facebook.com/{}",
        "YOUTUBE": "https://www.youtube.com/@{}"
    }

    found_list = []
    
    # HTML UNTUK ANIMASI PACMAN
    pacman_html = """
    <div class="pacman-holder">
        <div class="pacman">
            <div></div>
            <div></div>
        </div>
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
    </div>
    <div style="text-align:center; color: #f2d648; font-weight:bold; letter-spacing: 2px;">
        EATING DATA PACKETS...
    </div>
    """
    
    # TAMPILKAN PACMAN DI PLACEHOLDER
    loading_placeholder.markdown(pacman_html, unsafe_allow_html=True)
    
    total = len(sites_auto)
    
    # LOOP SCANNING (Tanpa bar, tapi Pacman tetap jalan)
    for site, url_pattern in sites_auto.items():
        url = url_pattern.format(username)
        try:
            response = requests.get(url, headers=headers, timeout=1.5)
            if response.status_code == 200:
                page_text = response.text.lower()
                if "not found" not in page_text and "404" not in page_text:
                    found_list.append((site, url))
        except:
            pass
        # Delay sedikit biar animasi Pacman sempat terlihat
        time.sleep(0.2)

    # HAPUS PACMAN SETELAH SELESAI
    loading_placeholder.empty()
    
    return found_list, sites_manual

# --- UI TAMPILAN UTAMA ---
st.markdown("<div class='cyber-header'>NEON OSINT</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #05d9e8; letter-spacing: 2px;'>// PAC-MAN PROTOCOL ACTIVATED //</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

target = st.text_input("", placeholder="INSERT COIN (USERNAME)")
st.markdown("<br>", unsafe_allow_html=True)

# Placeholder untuk animasi (Wadah Kosong)
loading_area = st.empty()

if st.button("EXECUTE TRACE"):
    if target:
        # Panggil fungsi dengan placeholder animasi
        hits, manuals = check_username(target, loading_area)
        
        st.markdown("---")
        
        # HASIL AUTO
        st.markdown(f"<h3 style='color: #05d9e8;'>// DATA CONSUMED</h3>", unsafe_allow_html=True)
        if hits:
            for site, url in hits:
                st.markdown(f"""
                <div class='result-box'>
                    <span style='color: #fff; font-size: 1.1rem;'>{site}</span><br>
                    <a href='{url}' target='_blank' class='link-blue'>[ ACCESS DATA ]</a>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("GAME OVER: NO DATA FOUND.")

        st.markdown("<br>", unsafe_allow_html=True)

        # HASIL MANUAL
        st.markdown(f"<h3 style='color: #ff2a6d;'>// BOSS LEVEL (MANUAL CHECK)</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        idx = 0
        for site, url_pattern in manuals.items():
            url = url_pattern.format(target)
            with (col1 if idx % 2 == 0 else col2):
                st.markdown(f"""
                <div class='manual-box'>
                    <span style='color: #fff; font-weight: bold;'>{site}</span><br>
                    <a href='{url}' target='_blank' class='link-pink'>[ CHALLENGE ]</a>
                </div>
                """, unsafe_allow_html=True)
            idx += 1

    else:
        st.warning("PLEASE INSERT USERNAME TO PLAY.")

# --- FOOTER ---
st.markdown(f"<div class='footer-sig'>HIGH SCORE BY <b>TAKSVJ</b> // GAME ON</div>", unsafe_allow_html=True)
