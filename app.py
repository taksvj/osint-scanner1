import streamlit as st
import requests
import time

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="OSINT Scanner - taksvj",
    page_icon="🕵️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS BIAR TAMPILAN KEREN (HACKER STYLE) ---
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #00ff41;
        font-family: 'Courier New', Courier, monospace;
    }
    .stTextInput > div > div > input {
        color: #00ff41;
        background-color: #262730;
    }
    .stButton > button {
        width: 100%;
        background-color: #00ff41;
        color: black;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- FUNGSI SCAN ---
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
    
    # Progress Bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total = len(sites)
    count = 0

    for site, url_pattern in sites.items():
        url = url_pattern.format(username)
        count += 1
        
        # Update progress
        progress_bar.progress(count / total)
        status_text.text(f"Scanning module: {site}...")
        
        try:
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                page_text = response.text.lower()
                not_found_indicators = ["page not found", "user not found", "not found", "404", "doesn't exist"]
                is_false_positive = any(indicator in page_text for indicator in not_found_indicators)
                
                if not is_false_positive:
                    found_list.append((site, url))
            
        except Exception:
            pass

    status_text.text("Scan Complete.")
    progress_bar.empty()
    return found_list

# --- TAMPILAN UTAMA ---
st.title("🕵️ OSINT USERNAME SCANNER")
st.text("BY: taksvj | SYSTEM STATUS: ONLINE")
st.markdown("---")

target = st.text_input("ENTER TARGET USERNAME:", placeholder="e.g. johndoe")

if st.button("INITIATE SCAN"):
    if target:
        results = check_username(target)
        
        st.markdown("### 📝 SCAN REPORT")
        if results:
            for site, url in results:
                st.success(f"[{site}] FOUND: {url}")
                st.markdown(f"[Buka Link]({url})") # Link bisa diklik
        else:
            st.error("NO TRACE FOUND IN DATABASE.")
    else:
        st.warning("PLEASE ENTER A USERNAME.")
