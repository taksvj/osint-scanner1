import streamlit as st
import requests
import time
import socket
import whois
import dns.resolver
import instaloader # Library baru buat IG

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="root@archlinux:~",
    page_icon="🐧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS ARCH LINUX THEME ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&display=swap');

    :root {
        --arch-blue: #1793d1;
        --arch-bg: #0f0f0f;
        --arch-fg: #d3dae3;
        --term-green: #23d18b;
        --term-red: #fa5c5c;
        --term-yellow: #f2d648;
        --term-purple: #b16286;
    }

    .stApp {
        background-color: var(--arch-bg);
        color: var(--arch-fg);
        font-family: 'Fira Code', monospace;
    }

    #MainMenu, footer, header {visibility: hidden;}
    
    [data-testid="stSidebar"] {
        background-color: #0a0a0a;
        border-right: 1px solid #333;
    }
    [data-testid="stSidebar"] * {
        font-family: 'Fira Code', monospace !important;
    }

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
    }

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

    .terminal-line { margin-bottom: 5px; border-bottom: 1px solid #1a1a1a; padding-bottom: 2px; }
    .bracket { color: #555; font-weight: bold; }
    .plus { color: var(--term-green); font-weight: bold; }
    .minus { color: var(--term-red); font-weight: bold; }
    .warn { color: var(--term-yellow); font-weight: bold; }
    .info { color: var(--arch-blue); font-weight: bold; }
    .ig { color: var(--term-purple); font-weight: bold; }
    
    a { color: var(--arch-blue) !important; text-decoration: none; border-bottom: 1px dotted #333; }
    
    .neofetch-container {
        display: flex; gap: 40px; margin-bottom: 30px; padding-top: 10px;
        font-family: 'Fira Code', monospace;
    }
    .ascii-logo { color: var(--arch-blue); font-weight: bold; white-space: pre; line-height: 1.2; }
    .system-info { line-height: 1.4; color: var(--arch-fg); }
    .info-key { color: var(--arch-blue); font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- FUNGSI PROGRESS BAR ---
def render_terminal_progress(placeholder, percent, task_name):
    bar_len = 20
    filled = int(bar_len * percent // 100)
    bar = "█" * filled + "░" * (bar_len - filled)
    text = f"""<div style="font-family:'Fira Code'; color:#aaa; margin-top:10px;">[{bar}] {percent}% :: {task_name}</div>"""
    placeholder.markdown(text, unsafe_allow_html=True)

# --- MODULE 1: USERNAME RECON ---
def run_username_recon():
    st.markdown("""<div style="font-family: 'Fira Code'; color: #23d18b; margin-bottom: 10px;">[taksvj@archlinux ~]$ <span style="color: #d3dae3;">./sherlock --timeout 1 target_user</span></div>""", unsafe_allow_html=True)
    c1, c2 = st.columns([5, 1])
    target = c1.text_input("", placeholder="username...", label_visibility="collapsed")
    run = c2.button("SCAN USER")
    loading = st.empty()

    if run and target:
        st.markdown(f"<div style='color:#777;'>:: Initializing scan for user: <b>{target}</b>...</div><br>", unsafe_allow_html=True)
        sites = {
            "GitHub": f"https://github.com/{target}",
            "Instagram": f"https://www.instagram.com/{target}",
            "Twitter/X": f"https://twitter.com/{target}",
            "Facebook": f"https://www.facebook.com/{target}",
            "Steam": f"https://steamcommunity.com/id/{target}"
        }
        found = []
        count = 0
        for site, url in sites.items():
            count += 1
            render_terminal_progress(loading, int((count/len(sites))*100), f"Checking {site}...")
            try:
                r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=1.5)
                if r.status_code == 200: found.append((site, url))
            except: pass
        loading.empty()
        if found:
            for s, u in found:
                st.markdown(f"<div class='terminal-line'><span class='bracket'>[</span><span class='plus'> FOUND </span><span class='bracket'>]</span> <a href='{u}' target='_blank'>{s} account found</a></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='terminal-line'><span class='minus'>error:</span> No accounts found.</div>", unsafe_allow_html=True)

# --- MODULE 2: DOMAIN RECON ---
def run_domain_recon():
    st.markdown("""<div style="font-family: 'Fira Code'; color: #23d18b; margin-bottom: 10px;">[taksvj@archlinux ~]$ <span style="color: #d3dae3;">sudo nmap -sn target_domain</span></div>""", unsafe_allow_html=True)
    c1, c2 = st.columns([5, 1])
    domain = c1.text_input("", placeholder="domain.com...", label_visibility="collapsed")
    run = c2.button("SCAN DOMAIN")

    if run and domain:
        domain = domain.replace("https://", "").replace("http://", "").replace("www.", "").split('/')[0]
        st.markdown(f"<div style='color:#777; margin-bottom:10px;'>:: Resolving info for <b>{domain}</b>...</div>", unsafe_allow_html=True)
        
        try:
            ip = socket.gethostbyname(domain)
            st.markdown(f"<div class='terminal-line'><span class='bracket'>[</span><span class='info'> NET </span><span class='bracket'>]</span> IPv4: <span style='color:#d3dae3'>{ip}</span></div>", unsafe_allow_html=True)
        except: pass

        try:
            r = requests.get(f"http://ip-api.com/json/{domain}").json()
            if r['status'] == 'success':
                st.markdown(f"<div class='terminal-line'><span class='bracket'>[</span><span class='info'> GEO </span><span class='bracket'>]</span> Loc: <span style='color:#d3dae3'>{r['city']}, {r['country']}</span></div>", unsafe_allow_html=True)
        except: pass
        
        try:
            w = whois.whois(domain)
            st.markdown(f"<div class='terminal-line'><span class='bracket'>[</span><span class='warn'> WHOIS </span><span class='bracket'>]</span> Registrar: <span style='color:#d3dae3'>{w.registrar}</span></div>", unsafe_allow_html=True)
        except: pass

# --- MODULE 3: INSTAGRAM RECON (BARU) ---
def run_instagram_recon():
    st.markdown("""
    <div style="font-family: 'Fira Code'; color: #b16286; margin-bottom: 10px;">
        [taksvj@archlinux ~]$ <span style="color: #d3dae3;">instaloader --profile target_ig</span>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([5, 1])
    username = c1.text_input("", placeholder="instagram username (no @)...", label_visibility="collapsed")
    run = c2.button("SCAN IG")

    if run and username:
        st.markdown(f"<div style='color:#777; margin-bottom:10px;'>:: Connecting to Instagram Gateway for <b>{username}</b>...</div>", unsafe_allow_html=True)
        
        # Bikin Instance Instaloader
        L = instaloader.Instaloader()
        
        try:
            # Tarik Data Profil
            profile = instaloader.Profile.from_username(L.context, username)
            
            # Tampilkan Data
            st.markdown(f"""
            <div style="border: 1px solid #b16286; padding: 20px; margin-top: 10px;">
                <h3 style="color: #b16286; margin:0;">@{profile.username}</h3>
                <div style="color: #777; font-size: 0.9em; margin-bottom: 15px;">User ID: {profile.userid}</div>
                
                <div style="display: flex; gap: 30px;">
                    <div>
                        <div style="color: #d3dae3; font-size: 1.5em; font-weight: bold;">{profile.mediacount}</div>
                        <div style="color: #b16286;">Posts</div>
                    </div>
                    <div>
                        <div style="color: #d3dae3; font-size: 1.5em; font-weight: bold;">{profile.followers}</div>
                        <div style="color: #b16286;">Followers</div>
                    </div>
                    <div>
                        <div style="color: #d3dae3; font-size: 1.5em; font-weight: bold;">{profile.followees}</div>
                        <div style="color: #b16286;">Following</div>
                    </div>
                </div>
                
                <div style="margin-top: 15px; border-top: 1px dashed #333; padding-top: 10px;">
                    <span style="color: #b16286;">Bio:</span> <span style="color: #aaa;">{profile.biography}</span>
                </div>
                <div style="margin-top: 5px;">
                     <span style="color: #b16286;">Verified:</span> <span style="color: { '#23d18b' if profile.is_verified else '#fa5c5c' }">{str(profile.is_verified)}</span> | 
                     <span style="color: #b16286;">Private:</span> <span style="color: { '#fa5c5c' if profile.is_private else '#23d18b' }">{str(profile.is_private)}</span>
                </div>
                <div style="margin-top: 5px;">
                     <span style="color: #b16286;">External URL:</span> <a href="{profile.external_url}" target="_blank">{profile.external_url}</a>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Download Profile Pic (Opsional, kadang bikin lemot)
            st.markdown(f"<br><div class='terminal-line'><span class='bracket'>[</span><span class='ig'> IMG </span><span class='bracket'>]</span> Profile Picture URL: <a href='{profile.profile_pic_url}' target='_blank'>Click to view</a></div>", unsafe_allow_html=True)

        except Exception as e:
            error_msg = str(e)
            if "LoginRequired" in error_msg:
                st.error("FATAL ERROR: Instagram memblokir akses publik (Login Required). Coba lagi nanti atau gunakan IP lokal.")
            elif "ConnectionRefused" in error_msg or "429" in error_msg:
                st.error("FATAL ERROR: Terlalu banyak request (IP Blocked). Instagram mendeteksi bot.")
            elif "ProfileNotExists" in error_msg:
                st.warning(f"User '{username}' tidak ditemukan.")
            else:
                st.error(f"Error tidak dikenal: {error_msg}")

# --- MAIN LAYOUT & SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:#1793d1; text-align:center;'>// TOOLKIT</h2>", unsafe_allow_html=True)
    selected_tool = st.radio(
        "Select Operation:",
        ["User Recon", "Domain Recon", "Instagram Recon"],
        label_visibility="collapsed"
    )
    st.markdown("<br><div style='text-align:center; color:#555; font-size:0.8em;'>v3.0-nightly</div>", unsafe_allow_html=True)

# HEADER NEOFETCH
st.markdown(r"""
<div class="neofetch-container">
    <div class="ascii-logo">
       /\
      /  \
     /    \
    /      \
   /   ,,   \
  /   |  |   \
 /_-''    ''-_\
    </div>
    <div class="system-info">
        <span class="info-key">taksvj</span>@<span class="info-key">archlinux</span><br>
        ------------------<br>
        <span class="info-key">OS</span>: Arch Linux x86_64<br>
        <span class="info-key">Kernel</span>: 6.6.7-arch1-1<br>
        <span class="info-key">Tool</span>: """ + selected_tool + r"""<br>
        <span class="info-key">Theme</span>: Dark / Arch Blue
    </div>
</div>
""", unsafe_allow_html=True)

# LOGIC SWITCHER
if selected_tool == "User Recon":
    run_username_recon()
elif selected_tool == "Domain Recon":
    run_domain_recon()
elif selected_tool == "Instagram Recon":
    run_instagram_recon()

# --- FOOTER ---
st.markdown("""<br><div style="border-top: 1px dashed #333; padding-top: 10px; color: #555; font-size: 0.8em; text-align: right;">[ system ready ] :: execute with caution</div>""", unsafe_allow_html=True)
