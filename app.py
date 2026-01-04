import streamlit as st
import requests
import time

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="CYBER OSINT // SCANNER",
    page_icon="💀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS HACKER STYLE V2 (ULTIMATE EDITION) ---
st.markdown("""
<style>
    /* Import Font Keren ala Kodingan */
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&display=swap');

    /* --- MAIN CONTAINER --- */
    .stApp {
        background-color: #020202; /* Hitam pekat */
        color: #0f0; /* Hijau Neon terminal */
        font-family: 'Fira Code', 'Courier New', monospace;
        /* Efek garis scan halus di background */
        background-image: linear-gradient(rgba(0, 255, 0, 0.03) 1px, transparent 1px);
        background-size: 100% 4px;
    }

    /* --- TYPOGRAPHY & GLOW --- */
    /* Semua teks dikasih efek cahaya pendar */
    h1, h2, h3, p, span, div, label {
        text-shadow: 0 0 4px rgba(0, 255, 0, 0.6);
    }

    /* Judul Utama dibikin warna Cyan biar kontras */
    h1 {
        color: #0ff !important; /* Cyan Neon */
        text-shadow: 0 0 10px rgba(0, 255, 255, 0.8), 0 0 20px rgba(0, 255, 255, 0.4) !important;
        text-transform: uppercase;
        letter-spacing: 3px;
        font-weight: 800;
        border-bottom: 2px solid #0ff;
        padding-bottom: 10px;
    }

    /* --- INPUT FIELD (KOTAK ISIAN) --- */
    /* Mengubah kotak input biar kayak command prompt */
    .stTextInput > div > div > input {
        color: #0f0 !important;
        background-color: #000 !important;
        border: 2px solid #0f0 !important;
        box-shadow: inset 0 0 10px rgba(0, 255, 0, 0.2);
        font-family: 'Fira Code', monospace;
        border-radius: 0px; /* Biar kotak tajem */
    }
    /* Saat diklik (fokus) warnanya berubah jadi Cyan */
    .stTextInput > div > div > input:focus {
        border-color: #0ff !important;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.5) !important;
        color: #0ff !important;
    }
    /* Warna placeholder (teks bayangan) */
    ::placeholder {
        color: rgba(0, 255, 0, 0.4) !important;
    }

    /* --- TOMBOL (BUTTON) --- */
    .stButton > button {
        width: 100%;
        background-color: #000;
        color: #0f0;
        border: 2px solid #0f0;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: all 0.3s ease;
        box-shadow: 0 0 5px rgba(0, 255, 0, 0.5);
        border-radius: 0px; /* Kotak tajem */
        padding: 15px 0;
    }
    /* Efek hover (saat mouse di atas tombol) */
    .stButton > button:hover {
        background-color: #0f0;
        color: #000;
        box-shadow: 0 0 25px rgba(0, 255, 0, 1);
        border-color: #0f0;
        cursor: pointer;
        font-weight: 900;
    }

    /* --- HASIL SCAN (ALERT BOXES) --- */
    /* Mengubah kotak 'success' default Streamlit jadi gelap */
    div[data-baseweb="notification"] {
        background-color: rgba(0, 20, 0, 0.9) !important;
        border-left: 5px solid #0f0 !important;
        border-top: 1px solid #0f0 !important;
        border-right: 1px solid #0f0 !important;
        border-bottom: 1px solid #0f0 !important;
        color: #0f0 !important;
        border-radius: 0px;
    }
    /* Ikon centang di hasil */
    div[data-baseweb="notification"] svg {
        fill: #0f0 !important;
        filter: drop-shadow(0 0 5px #0f0);
    }
    /* Link di dalam hasil */
    div[data-baseweb="notification"] a {
        color: #0ff !important;
        text-decoration: none;
        font-weight: bold;
        border-bottom: 1px dotted #0ff;
        margin-left: 10px;
    }
    div[data-baseweb="notification"] a:hover {
        text-shadow: 0 0 10px #0ff;
        border-bottom: 1px solid #0ff;
    }

    /* --- PROGRESS BAR --- */
    .stProgress > div > div > div {
        background-color: #0f0;
        box-shadow: 0 0 10px #0f0, 0 0 20px #0f0;
    }
    
    /* --- HIDE JUNK --- */
    /* Menyembunyikan menu bawaan Streamlit biar bersih */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# --- FUNGSI SCAN (Sama seperti sebelumnya) ---
def check_username(username):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    sites = {
        "Instagram": "https://www.instagram.com/{}",
        "Facebook": "https://www.facebook.com/{}",
        "Twitter/X": "https://twitter.com/{}",
        "TikTok": "https://www.tiktok.com/@{}",
        "Telegram": "https://t.me/{}",
        "Pinterest": "https://www.pinterest.com/{}",
        "GitHub": "https://github.com/{}",
        "GitLab": "https://gitlab.com/{}",
        "Spotify": "https://open.spotify.com/user/{}",
        "SoundCloud": "https://soundcloud.com/{}",
        "YouTube": "https://www.youtube.com/@{}",
        "Wattpad": "https://www.wattpad.com/user/{}",
        "Steam": "https://steamcommunity.com/id/{}",
        "Roblox": "https://www.roblox.com/user.aspx?username={}",
        "Linktree": "https://linktr.ee/{}",
        "Freelancer": "https://www.freelancer.com/u/{}",
        "Fiverr": "https://www.fiverr.com/{}",
    }

    found_list = []
    
    # Progress Bar Style Hacker
    progress_text = "INITIALIZING SCAN PROTOCOL..."
    my_bar = st.progress(0, text=progress_text)
    status_text = st.empty()
    
    total = len(sites)
    count = 0

    for site, url_pattern in sites.items():
        url = url_pattern.format(username)
        count += 1
        
        # Update progress
        prog_percent = count / total
        my_bar.progress(prog_percent, text=f"SCANNING MODULE [{count}/{total}]: {site.upper()}...")
        
        try:
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                page_text = response.text.lower()
                not_found_indicators = ["page not found", "user not found", "not found", "404", "doesn't exist", "halaman tidak ditemukan"]
                is_false_positive = any(indicator in page_text for indicator in not_found_indicators)
                
                if not is_false_positive:
                    found_list.append((site, url))
            
        except Exception:
            pass
            
        # Sedikit delay biar keliatan prosesnya (opsional)
        # time.sleep(0.1)

    my_bar.progress(1.0, text="SCAN COMPLETE. DATA RETRIEVED.")
    time.sleep(1)
    my_bar.empty()
    return found_list

# --- TAMPILAN UTAMA ---
st.title("SYSTEM // OVERRIDE")
st.markdown("### >> OSINT TARGET SCANNER V.2.0")
st.write("UNIT: taksvj | STATUS: CONNECTED_")

st.markdown("<br>", unsafe_allow_html=True) # Spasi

target = st.text_input("ENTER TARGET ID_ >", placeholder="username_here...")

st.markdown("<br>", unsafe_allow_html=True) # Spasi

if st.button(">> EXECUTE SCAN <<"):
    if target:
        st.markdown("---")
        results = check_username(target)
        
        st.markdown("### >> SCAN REPORT // RESULTS")
        if results:
            for site, url in results:
                # Menggunakan layout kolom untuk hasil biar rapi
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.success(f"HIT CONFIRMED: [{site}]")
                with col2:
                     st.markdown(f"[>> ACCESS LINK <<]({url})")
            st.markdown("---")
            st.write(f">> TOTAL HITS: {len(results)}")
        else:
            st.error("NEGATIVE RESULT. NO TRACE FOUND IN DATABASE.")
    else:
        st.warning("[!] ERROR: INPUT INVALID. TARGET ID REQUIRED.")

# Footer ala hacker
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: #0f0; opacity: 0.5;'>--- END OF LINE ---</div>", unsafe_allow_html=True)
