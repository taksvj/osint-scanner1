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

# --- CSS: CYBERPUNK + SUDO PACMAN ANIMATION ---
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

    /* --- SUDO PACMAN PROGRESS BAR CSS --- */
    .pacman-container {
        width: 100%;
        max-width: 600px;
        margin: 20px auto;
        font-family: 'Courier New', monospace; /* Font Terminal */
    }

    /* Jalur Titik-titik (Makanan) */
    .pacman-track {
        position: relative;
        height: 30px;
        background: transparent;
        display: flex;
        align-items: center;
        overflow: hidden;
    }
    
    .dots-layer {
        position: absolute;
        width: 100%;
        top: 50%;
        transform: translateY(-50%);
        color: rgba(255, 255, 255, 0.3);
        font-size: 20px;
        letter-spacing: 5px;
        white-space: nowrap;
        z-index: 1;
    }

    /* Layer Penutup (Masking) - Mengikuti Pacman untuk menutupi titik */
    .eaten-path {
        position: absolute;
        height: 100%;
        background-color: var(--dark-bg); /* Warna sama dgn background biar titik ilang */
        left: 0;
        top: 0;
        z-index: 2;
        transition: width 0.2s linear; /* Animasi halus */
        border-right: none;
    }

    /* Si Pacman */
    .pacman-head {
        position: absolute;
        right: -15px; /* Biar mulutnya pas di ujung bar */
        top: 50%;
        transform: translateY(-50%);
        width: 20px;
        height: 20px;
        z-index: 3;
    }

    /* Mulut Pacman Animasi CSS */
    .pacman-mouth {
        width: 0; 
        height: 0; 
        border-right: 10px solid transparent; 
        border-top: 10px solid var(--pacman-yellow); 
        border-left: 10px solid var(--pacman-yellow); 
        border-bottom: 10px solid var(--pacman-yellow); 
        border-top-left-radius: 10px; 
        border-top-right-radius: 10px; 
        border-bottom-left-radius: 10px; 
        border-bottom-right-radius: 10px; 
        animation: bite 0.2s infinite linear;
    }

    @keyframes bite {
        0% { transform: rotate(0deg); }
        50% { transform: rotate(45deg); } # Buka mulut (Kurang pas, kita ganti logic border)
    }
    
    /* Animasi Mulut Buka Tutup yang lebih bener */
    .pacman-shape {
        width: 20px;
        height: 20px;
        background: var(--pacman-yellow);
        border-radius: 50%;
        position: relative;
        clip-path: polygon(100% 74%, 44% 48%, 100% 21%, 100% 0, 0 0, 0 100%, 100% 100%);
        animation: chomp 0.2s infinite linear alternate;
    }

    @keyframes chomp {
        0% { clip-path: polygon(100% 74%, 44% 48%, 100% 21%, 100% 0, 0 0, 0 100%, 100% 100%); }
        100% { clip-path: polygon(100% 60%, 44% 48%, 100% 40%, 100% 0, 0 0, 0 100%, 100% 100%); }
    }

    /* Teks Persentase */
    .progress-text {
        text-align: right;
        color: var(--pacman-yellow);
        font-weight: bold;
        font-size: 1.2rem;
        margin-top: 5px;
        text-shadow: 0 0 10px var(--pacman-yellow);
    }
    
    /* Status Text */
    .status-log {
        color: var(--neon-blue);
        font-size: 0.9rem;
        font-family: 'Courier New', monospace;
    }

    /* --- END ANIMATION CSS --- */

    /* HEADER & INPUT styles (Sama kaya sebelumnya) */
    .cyber-header {
        font-size: 3.5rem; font-weight: 900; text-align: center; color: white;
        text-shadow: 2px 2px 0px var(--neon-pink), -2px -2px 0px var(--neon-blue);
        letter-spacing: 4px; text-transform: uppercase;
    }
    .stTextInput > div > div > input {
        background-color: rgba(5, 217, 232, 0.1) !important; color: var(--neon-blue) !important;
        border: 2px solid var(--neon-blue) !important; font-family: 'Orbitron', sans-serif;
        text-align: center; font-size: 1.2rem; box-shadow: 0 0 10px var(--neon-blue); border-radius: 0; z-index: 100;
    }
    .stButton > button {
        background: transparent; border: 2px solid var(--neon-pink); color: var(--neon-pink);
        font-family: 'Orbitron', sans-serif; font-size: 1.2rem; font-weight: bold; text-transform: uppercase;
        padding: 15px; width: 100%; transition: 0.3s; box-shadow: 0 0 5px var(--neon-pink); z-index: 100;
    }
    .stButton > button:hover {
        background: var(--neon-pink); color: #fff; box-shadow: 0 0 25px var(--neon-pink); transform: scale(1.02);
    }
    .result-box { border-left: 5px solid var(--neon-blue); background: linear-gradient(90deg, rgba(5, 217, 232, 0.1) 0%, rgba(0,0,0,0) 100%); padding: 15px; margin-bottom: 10px; }
    .manual-box { border-left: 5px solid var(--neon-pink); background: linear-gradient(90deg, rgba(255, 42, 109, 0.1) 0%, rgba(0,0,0,0) 100%); padding: 15px; margin-bottom: 10px; }
    a { text-decoration: none; font-weight: bold; }
    .link-blue { color: var(--neon-blue) !important; } .link-pink { color: var(--neon-pink) !important; }
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
        ctx.fillStyle = 'rgba(1, 1, 43, 0.1)'; ctx.fillRect(0, 0, canvas.width, canvas.height);
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

# --- FUNGSI UPDATE BAR PACMAN ---
def render_pacman_bar(placeholder, percent, current_node):
    # Membuat string titik-titik panjang (makanan)
    dots = "• " * 30 
    
    # HTML Dinamis
    # logic: width dari 'eaten-path' akan bertambah sesuai persen, menutupi dots layer di bawahnya
    html_code = f"""
    <div class="pacman-container">
        <div class="status-log">>> PROCESSING NODE: {current_node}...</div>
        <div class="pacman-track">
            <div class="dots-layer">{dots}</div>
            
            <div class="eaten-path" style="width: {percent}%;">
                <div class="pacman-head">
                    <div class="pacman-shape"></div>
                </div>
            </div>
        </div>
        <div class="progress-text">{percent}%</div>
    </div>
    """
    placeholder.markdown(html_code, unsafe_allow_html=True)

# --- LOGIKA PROGRAM UTAMA ---
def check_username(username, anim_placeholder):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    sites_auto = {
        "GITHUB": "https://github.com/{}",
        "SPOTIFY": "https://open.spotify.com/user/{}",
        "WATTPAD": "https://www.wattpad.com/user/{}",
        "ROBLOX": "https://www.roblox.com/user.aspx?username={}",
        "STEAM": "https://steamcommunity.com/id/{}",
        "PINTEREST": "https://www.pinterest.com/{}",
        "MEDIUM": "https://medium.com/@{}",
        "VIMEO": "https://vimeo.com/{}",
        "SOUNDCLOUD": "https://soundcloud.com/{}"
    }

    sites_manual = {
        "INSTAGRAM": "https://www.instagram.com/{}",
        "TIKTOK": "https://www.tiktok.com/@{}",
        "TWITTER / X": "https://twitter.com/{}",
        "FACEBOOK": "https://www.facebook.com/{}",
        "YOUTUBE": "https://www.youtube.com/@{}"
    }

    found_list = []
    
    total = len(sites_auto)
    count = 0
    
    # LOOP SCANNING DENGAN PROGRESS PACMAN
    for site, url_pattern in sites_auto.items():
        count += 1
        url = url_pattern.format(username)
        
        # Hitung Persentase (0 - 100)
        percent = int((count / total) * 100)
        
        # Update Animasi Pacman
        render_pacman_bar(anim_placeholder, percent, site)
        
        try:
            response = requests.get(url, headers=headers, timeout=1.5)
            if response.status_code == 200:
                page_text = response.text.lower()
                if "not found" not in page_text and "404" not in page_text:
                    found_list.append((site, url))
        except:
            pass
        
        # Delay biar animasinya kelihatan jalan (kalau terlalu cepat gak enak dilihat)
        time.sleep(0.3)

    # Hapus bar setelah selesai (opsional, atau biarkan 100%)
    render_pacman_bar(anim_placeholder, 100, "COMPLETE")
    time.sleep(0.8)
    anim_placeholder.empty()
    
    return found_list, sites_manual

# --- UI TAMPILAN UTAMA ---
st.markdown("<div class='cyber-header'>NEON OSINT</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #05d9e8; letter-spacing: 2px;'>// SUDO PACMAN -Syu TARGET //</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

target = st.text_input("", placeholder="INSERT USERNAME")
st.markdown("<br>", unsafe_allow_html=True)

# Area untuk animasi
loading_area = st.empty()

if st.button("EXECUTE TRACE"):
    if target:
        # Jalankan Scan
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
