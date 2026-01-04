import streamlit as st
import requests
import time

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="root@archlinux:~",
    page_icon="🐧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS ARCH LINUX THEME ---
st.markdown("""
<style>
    /* Import Font Terminal */
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&display=swap');

    :root {
        --arch-blue: #1793d1;
        --arch-bg: #0f0f0f;
        --arch-fg: #d3dae3;
        --term-green: #23d18b;
        --term-red: #fa5c5c;
        --term-yellow: #f2d648;
    }

    /* Reset Streamlit */
    .stApp {
        background-color: var(--arch-bg);
        color: var(--arch-fg);
        font-family: 'Fira Code', monospace;
    }

    /* Hide UI Elements */
    #MainMenu, footer, header {visibility: hidden;}

    /* INPUT FIELD - Terminal Style */
    .stTextInput > div > div > input {
        background-color: #1a1a1a !important;
        color: var(--arch-fg) !important;
        border: 1px solid #333 !important;
        font-family: 'Fira Code', monospace;
        border-radius: 0;
        padding-left: 10px;
    }
    .stTextInput > div > div > input:focus {
        border-color: var(--arch-blue) !important;
        box-shadow: none !important;
    }

    /* BUTTON STYLE */
    .stButton > button {
        background: transparent;
        border: 1px solid #444;
        color: var(--arch-fg);
        font-family: 'Fira Code', monospace;
        border-radius: 0;
        width: 100%;
        transition: 0.2s;
    }
    .stButton > button:hover {
        border-color: var(--arch-blue);
        color: var(--arch-blue);
    }

    /* NEOFETCH CONTAINER STYLE */
    .neofetch-table {
        width: 100%;
        max-width: 800px;
        margin-bottom: 30px;
        border-collapse: collapse;
    }
    .neofetch-logo {
        color: var(--arch-blue);
        font-weight: bold;
        padding-right: 30px;
        vertical-align: top;
        white-space: pre; /* Wajib biar ASCII gak hancur */
        font-family: 'Fira Code', monospace;
        line-height: 1.2;
    }
    .neofetch-info {
        vertical-align: top;
        font-family: 'Fira Code', monospace;
        line-height: 1.4;
        color: var(--arch-fg);
    }
    .info-key { color: var(--arch-blue); font-weight: bold; }
    .info-val { color: var(--arch-fg); }

    /* HASIL SCAN STYLE */
    .terminal-line {
        font-family: 'Fira Code', monospace;
        margin-bottom: 5px;
        border-bottom: 1px solid #222;
        padding-bottom: 2px;
    }
    .bracket { color: #555; font-weight: bold; }
    .plus { color: var(--term-green); font-weight: bold; }
    .minus { color: var(--term-red); font-weight: bold; }
    .warn { color: var(--term-yellow); font-weight: bold; }
    
    a { color: var(--arch-blue) !important; text-decoration: none; }
    a:hover { text-decoration: underline; }
</style>
""", unsafe_allow_html=True)

# --- FUNGSI PROGRESS BAR TEXT-BASED ---
def render_terminal_progress(placeholder, percent, current_node):
    bar_length = 30
    filled_length = int(bar_length * percent // 100)
    pacman_char = "C" if percent % 2 == 0 else "c"
    if percent == 100: pacman_char = "o"
    
    bar = " " * filled_length + pacman_char + "•" * (bar_length - filled_length - 1)
    
    text_bar = f"""
    <div style="font-family: 'Fira Code', monospace; color: #d3dae3; margin-top: 10px;">
        <span style="color:#555">::</span> Processing node: <span style="color:#1793d1">{current_node}</span><br>
        <span style="color:#d3dae3">[{bar}]</span> {percent}%
    </div>
    """
    placeholder.markdown(text_bar, unsafe_allow_html=True)

# --- LOGIKA PROGRAM ---
def check_username(username, anim_placeholder):
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    sites_auto = {
        "aur.archlinux.org": "https://aur.archlinux.org/account/{}",
        "github.com": "https://github.com/{}",
        "gitlab.com": "https://gitlab.com/{}",
        "spotify.com": "https://open.spotify.com/user/{}",
        "steamcommunity.com": "https://steamcommunity.com/id/{}",
        "roblox.com": "https://www.roblox.com/user.aspx?username={}",
        "wattpad.com": "https://www.wattpad.com/user/{}",
        "medium.com": "https://medium.com/@{}",
    }

    sites_manual = {
        "instagram.com": "https://www.instagram.com/{}",
        "twitter.com": "https://twitter.com/{}",
        "tiktok.com": "https://www.tiktok.com/@{}",
        "facebook.com": "https://www.facebook.com/{}",
    }

    found_list = []
    total = len(sites_auto)
    count = 0
    
    for site, url_pattern in sites_auto.items():
        count += 1
        url = url_pattern.format(username)
        percent = int((count / total) * 100)
        
        render_terminal_progress(anim_placeholder, percent, site)
        
        try:
            response = requests.get(url, headers=headers, timeout=1)
            if response.status_code == 200 and "not found" not in response.text.lower():
                found_list.append((site, url))
        except:
            pass
        time.sleep(0.1)

    render_terminal_progress(anim_placeholder, 100, "done")
    time.sleep(0.5)
    anim_placeholder.empty()
    
    return found_list, sites_manual

# --- BAGIAN UTAMA (HEADER NEOFETCH YANG DIPERBAIKI) ---

# Perhatikan double backslash (\\) agar logo tidak hancur
logo_ascii = """       /\\
      /  \\
     /    \\
    /      \\
   /   ,,   \\
  /   |  |   \\
 /_-''    ''-_\\"""

# Layout menggunakan HTML Table agar RAPI dan PRESISI
st.markdown(f"""
<table class="neofetch-table">
    <tr>
        <td class="neofetch-logo">{logo_ascii}</td>
        <td class="neofetch-info">
            <span class="info-key">taksvj</span>@<span class="info-key">archlinux</span><br>
            ------------------<br>
            <span class="info-key">OS</span>: Arch Linux x86_64<br>
            <span class="info-key">Host</span>: Streamlit Cloud<br>
            <span class="info-key">Kernel</span>: 6.6.7-arch1-1<br>
            <span class="info-key">Shell</span>: zsh 5.9<br>
            <span class="info-key">Tool</span>: OSINT Scanner v5.0 (Pacman Edition)<br>
            <span class="info-key">Theme</span>: Dark / Arch Blue
        </td>
    </tr>
</table>
""", unsafe_allow_html=True)

# --- INPUT SECTION ---
st.markdown("""
<div style="font-family: 'Fira Code'; color: #23d18b; margin-bottom: -15px;">
    [taksvj@archlinux ~]$ <span style="color: #d3dae3;">sudo osint -Syu target_username</span>
</div>
""", unsafe_allow_html=True)

# Container untuk Input dan Tombol
input_col, btn_col = st.columns([4, 1])

with input_col:
    target = st.text_input("", placeholder="enter username...", label_visibility="collapsed")

with btn_col:
    run_btn = st.button("EXECUTE")

# Area Animasi
loading_area = st.empty()

if run_btn:
    if target:
        st.markdown(f"<div style='font-family:Fira Code; color:#d3dae3; margin-top: 10px;'>:: Synchronizing package databases for <b>{target}</b>...</div>", unsafe_allow_html=True)
        time.sleep(0.5)
        
        hits, manuals = check_username(target, loading_area)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # HASIL AUTO
        if hits:
            for site, url in hits:
                st.markdown(f"""
                <div class='terminal-line'>
                    <span class='bracket'>[</span><span class='plus'> OK </span><span class='bracket'>]</span> 
                    Found target on <a href='{url}' target='_blank'>{site}</a>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("<div class='terminal-line'><span class='minus'>error:</span> target not found in public repositories.</div>", unsafe_allow_html=True)

        # HASIL MANUAL
        st.markdown("<div style='font-family:Fira Code; color:#777; margin-top:20px;'>:: Warning: Some repositories require manual verification:</div>", unsafe_allow_html=True)
        
        for site, url_pattern in manuals.items():
            url = url_pattern.format(target)
            st.markdown(f"""
            <div class='terminal-line'>
                <span class='bracket'>[</span><span class='warn'> ?? </span><span class='bracket'>]</span> 
                {site} -> <a href='{url}' target='_blank'>manual_check</a>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br><div style='color:#1793d1'>:: Transaction successfully finished.</div>", unsafe_allow_html=True)

    else:
        st.markdown("<br><span class='minus'>error:</span> no target specified.", unsafe_allow_html=True)
