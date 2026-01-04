import streamlit as st
import requests
import time
import random

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="NEON OSINT // TAKSVJ",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS CYBERPUNK STYLE & JAVASCRIPT ---
st.markdown("""
<style>
    /* Import Font Futuristik: Orbitron */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

    :root {
        --neon-pink: #ff2a6d;
        --neon-blue: #05d9e8;
        --dark-bg: #01012b;
        --matrix-green: #00ff41;
    }

    * { cursor: crosshair !important; }

    .stApp {
        background-color: var(--dark-bg);
        color: var(--neon-blue);
        font-family: 'Orbitron', sans-serif;
    }

    /* HEADER GLITCH EFFECT (PINK & BLUE) */
    .cyber-header {
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        color: white;
        text-shadow: 2px 2px 0px var(--neon-pink), -2px -2px 0px var(--neon-blue);
        letter-spacing: 4px;
        margin-bottom: 10px;
        text-transform: uppercase;
    }

    /* INPUT FIELD */
    .stTextInput > div > div > input {
        background-color: rgba(5, 217, 232, 0.1) !important;
        color: var(--neon-blue) !important;
        border: 2px solid var(--neon-blue) !important;
        font-family: 'Orbitron', sans-serif;
        text-align: center;
        font-size: 1.2rem;
        box-shadow: 0 0 10px var(--neon-blue);
        border-radius: 0px; /* Kotak tajam */
        z-index: 100;
    }
    .stTextInput > div > div > input:focus {
        background-color: rgba(0,0,0,0.8) !important;
        border-color: var(--neon-pink) !important;
        box-shadow: 0 0 20px var(--neon-pink);
        color: var(--neon-pink) !important;
    }

    /* TOMBOL UTAMA */
    .stButton > button {
        background: transparent;
        border: 2px solid var(--neon-pink);
        color: var(--neon-pink);
        font-family: 'Orbitron', sans-serif;
        font-size: 1.2rem;
        font-weight: bold;
        text-transform: uppercase;
        padding: 15px;
        transition: 0.3s;
        width: 100%;
        letter-spacing: 2px;
        box-shadow: 0 0 5px var(--neon-pink);
        z-index: 100;
    }
    .stButton > button:hover {
        background: var(--neon-pink);
        color: #fff;
        box-shadow: 0 0 25px var(--neon-pink), 0 0 50px var(--neon-pink);
        border-color: #fff;
        transform: scale(1.02);
    }

    /* RESULT BOXES (CYBER CARDS) */
    .result-box {
        border-left: 5px solid var(--neon-blue);
        background: linear-gradient(90deg, rgba(5, 217, 232, 0.1) 0%, rgba(0,0,0,0) 100%);
        padding: 15px;
        margin-bottom: 15px;
        border-top: 1px solid var(--neon-blue);
    }
    .manual-box {
        border-left: 5px solid var(--neon-pink);
        background: linear-gradient(90deg, rgba(255, 42, 109, 0.1) 0%, rgba(0,0,0,0) 100%);
        padding: 15px;
        margin-bottom: 15px;
        border-top: 1px solid var(--neon-pink);
    }
    
    a { text-decoration: none; font-weight: bold; transition: 0.3s; }
    
    /* LINK AUTO (BLUE) */
    .link-blue { color: var(--neon-blue) !important; border-bottom: 1px dotted var(--neon-blue); }
    .link-blue:hover { color: white !important; text-shadow: 0 0 10px var(--neon-blue); }

    /* LINK MANUAL (PINK) */
    .link-pink { color: var(--neon-pink) !important; border-bottom: 1px dotted var(--neon-pink); }
    .link-pink:hover { color: white !important; text-shadow: 0 0 10px var(--neon-pink); }

    /* CANVAS BACKGROUND */
    #cyber-canvas {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -1;
        opacity: 0.3;
        pointer-events: none;
    }

    /* HIDE UI */
    #MainMenu, footer, header {visibility: hidden;}

    /* SIGNATURE */
    .footer-sig {
        text-align: center;
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.8rem;
        margin-top: 50px;
        letter-spacing: 2px;
    }
</style>

<canvas id="cyber-canvas"></canvas>
<script>
    const canvas = document.getElementById('cyber-canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    // Karakter Cyberpunk (Katakana + Angka)
    const chars = 'アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポ0123456789';
    const letters = chars.split('');
    const fontSize = 14;
    const columns = canvas.width / fontSize;
    const drops = [];
    for(let x = 0; x < columns; x++) { drops[x] = 1; }

    function draw() {
        ctx.fillStyle = 'rgba(1, 1, 43, 0.1)'; // Background trail gelap
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.font = fontSize + 'px monospace';

        for(let i = 0; i < drops.length; i++) {
            const text = letters[Math.floor(Math.random() * letters.length)];
            
            // Random Color: Pink or Cyan
            if (Math.random() > 0.5) {
                ctx.fillStyle = '#ff2a6d'; // Neon Pink
            } else {
                ctx.fillStyle = '#05d9e8'; // Neon Blue
            }

            ctx.fillText(text, i * fontSize, drops[i] * fontSize);

            if(drops[i] * fontSize > canvas.height && Math.random() > 0.975) { drops[i] = 0; }
            drops[i]++;
        }
    }
    setInterval(draw, 40);
    window.addEventListener('resize', () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });
</script>
""", unsafe_allow_html=True)

# --- LOGIKA PROGRAM (SAMA SEPERTI SEBELUMNYA) ---
def check_username(username):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
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

    sites_manual = {
        "INSTAGRAM": "https://www.instagram.com/{}",
        "TIKTOK": "https://www.tiktok.com/@{}",
        "TWITTER / X": "https://twitter.com/{}",
        "FACEBOOK": "https://www.facebook.com/{}",
        "TELEGRAM": "https://t.me/{}",
        "YOUTUBE": "https://www.youtube.com/@{}"
    }

    found_list = []
    
    # Progress Bar UI hack
    progress_text = "INITIALIZING NEURAL LINK..."
    my_bar = st.progress(0, text=progress_text)
    
    total = len(sites_auto) + len(sites_manual)
    count = 0

    for site, url_pattern in sites_auto.items():
        url = url_pattern.format(username)
        count += 1
        my_bar.progress(count / total, text=f"SCANNING SECTOR: {site}...")
        try:
            response = requests.get(url, headers=headers, timeout=2)
            if response.status_code == 200:
                page_text = response.text.lower()
                if "not found" not in page_text and "404" not in page_text:
                    found_list.append((site, url))
        except:
            pass
        time.sleep(0.05)

    my_bar.progress(1.0, text="SYNC COMPLETE.")
    time.sleep(0.5)
    my_bar.empty()
    
    return found_list, sites_manual

# --- UI TAMPILAN UTAMA ---
st.markdown("<div class='cyber-header'>CYBER OSINT</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #05d9e8; letter-spacing: 2px;'>// TARGET RECOGNITION SYSTEM //</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

target = st.text_input("", placeholder="ENTER USERNAME_")
st.markdown("<br>", unsafe_allow_html=True)

if st.button("EXECUTE TRACE"):
    if target:
        st.write(f">> ESTABLISHING CONNECTION TO: {target}")
        time.sleep(1)
        
        hits, manuals = check_username(target)
        
        st.markdown("---")
        
        # HASIL AUTO (BLUE THEME)
        st.markdown(f"<h3 style='color: #05d9e8;'>// CONFIRMED DATA FRAGMENTS</h3>", unsafe_allow_html=True)
        if hits:
            for site, url in hits:
                st.markdown(f"""
                <div class='result-box'>
                    <span style='color: #fff; font-size: 1.1rem;'>{site}</span><br>
                    <a href='{url}' target='_blank' class='link-blue'>[ ACCESS DATA NODE ]</a>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("NO DATA FRAGMENTS FOUND.")

        st.markdown("<br>", unsafe_allow_html=True)

        # HASIL MANUAL (PINK THEME - WARNING)
        st.markdown(f"<h3 style='color: #ff2a6d;'>// RESTRICTED ACCESS (MANUAL OVERRIDE)</h3>", unsafe_allow_html=True)
        st.caption("Secure nodes detected. Click to override manually.")
        
        col1, col2 = st.columns(2)
        idx = 0
        for site, url_pattern in manuals.items():
            url = url_pattern.format(target)
            with (col1 if idx % 2 == 0 else col2):
                st.markdown(f"""
                <div class='manual-box'>
                    <span style='color: #fff; font-weight: bold;'>{site}</span><br>
                    <a href='{url}' target='_blank' class='link-pink'>[ BREACH FIREWALL ]</a>
                </div>
                """, unsafe_allow_html=True)
            idx += 1

    else:
        st.warning("INPUT ERROR: TARGET ID REQUIRED")

# --- FOOTER ---
st.markdown(f"<div class='footer-sig'>DEVELOPED BY <b>TAKSVJ</b> // NETRUNNER V.2077</div>", unsafe_allow_html=True)
