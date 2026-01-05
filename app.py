import streamlit as st
import requests
import time
import socket
import whois
import dns.resolver

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
    }

    .stApp {
        background-color: var(--arch-bg);
        color: var(--arch-fg);
        font-family: 'Fira Code', monospace;
    }

    #MainMenu, footer, header {visibility: hidden;}
    
    /* SIDEBAR STYLE */
    [data-testid="stSidebar"] {
        background-color: #0a0a0a;
        border-right: 1px solid #333;
    }
    [data-testid="stSidebar"] * {
        font-family: 'Fira Code', monospace !important;
    }

    /* INPUT FIELD */
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

    /* TERMINAL OUTPUT STYLES */
    .terminal-line { margin-bottom: 5px; border-bottom: 1px solid #1a1a1a; padding-bottom: 2px; }
    .bracket { color: #555; font-weight: bold; }
    .plus { color: var(--term-green); font-weight: bold; }
    .minus { color: var(--term-red); font-weight: bold; }
    .warn { color: var(--term-yellow); font-weight: bold; }
    .info { color: var(--arch-blue); font-weight: bold; }
    
    a { color: var(--arch-blue) !important; text-decoration: none; border-bottom: 1px dotted #333; }

    /* NEOFETCH CONTAINER */
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
    
    text = f"""
    <div style="font-family:'Fira Code'; color:#aaa; margin-top:10px;">
        [{bar}] {percent}% :: {task_name}
    </div>
    """
    placeholder.markdown(text, unsafe_allow_html=True)

# --- MODULE 1: USERNAME RECON ---
def run_username_recon():
    st.markdown("""
    <div style="font-family: 'Fira Code'; color: #23d18b; margin-bottom: 10px;">
        [taksvj@archlinux ~]$ <span style="color: #d3dae3;">./sherlock --timeout 1 target_user</span>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([5, 1])
    target = c1.text_input("", placeholder="username...", label_visibility="collapsed")
    run = c2.button("SCAN USER")
    
    loading = st.empty()

    if run and target:
        st.markdown(f"<div style='color:#777;'>:: Initializing scan for user: <b>{target}</b>...</div><br>", unsafe_allow_html=True)
        
        # List Website
        sites = {
            "GitHub": f"https://github.com/{target}",
            "Instagram": f"https://www.instagram.com/{target}",
            "Twitter/X": f"https://twitter.com/{target}",
            "Facebook": f"https://www.facebook.com/{target}",
            "Steam": f"https://steamcommunity.com/id/{target}",
            "GitLab": f"https://gitlab.com/{target}",
            "Reddit": f"https://www.reddit.com/user/{target}",
            "Medium": f"https://medium.com/@{target}",
            "TikTok": f"https://www.tiktok.com/@{target}"
        }

        found = []
        count = 0
        
        for site, url in sites.items():
            count += 1
            render_terminal_progress(loading, int((count/len(sites))*100), f"Checking {site}...")
            
            try:
                # Request sederhana
                r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=1.5)
                # Filter respons 200 OK
                if r.status_code == 200:
                    found.append((site, url))
            except:
                pass
        
        loading.empty()
        
        # Hasil Output
        if found:
            for s, u in found:
                st.markdown(f"<div class='terminal-line'><span class='bracket'>[</span><span class='plus'> FOUND </span><span class='bracket'>]</span> <a href='{u}' target='_blank'>{s} account found</a></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='terminal-line'><span class='minus'>error:</span> No accounts found with standard scan.</div>", unsafe_allow_html=True)

# --- MODULE 2: DOMAIN RECON ---
def run_domain_recon():
    st.markdown("""
    <div style="font-family: 'Fira Code'; color: #23d18b; margin-bottom: 10px;">
        [taksvj@archlinux ~]$ <span style="color: #d3dae3;">sudo nmap -sn --dns-servers target_domain</span>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([5, 1])
    domain = c1.text_input("", placeholder="domain.com...", label_visibility="collapsed")
    run = c2.button("SCAN DOMAIN")

    if run and domain:
        # Cleaning input
        domain = domain.replace("https://", "").replace("http://", "").replace("www.", "").split('/')[0]
        
        st.markdown(f"<div style='color:#777; margin-bottom:10px;'>:: Resolving DNS and Whois for <b>{domain}</b>...</div>", unsafe_allow_html=True)
        
        # 1. IP ADDRESS
        try:
            ip = socket.gethostbyname(domain)
            st.markdown(f"""
            <div class='terminal-line'>
                <span class='bracket'>[</span><span class='info'> NET </span><span class='bracket'>]</span> 
                IPv4 Address: <span style='color:#d3dae3'>{ip}</span>
            </div>""", unsafe_allow_html=True)
        except:
            st.markdown("<div class='terminal-line'><span class='minus'>ERR</span> Could not resolve IP</div>", unsafe_allow_html=True)

        # 2. GEO IP (API Gratis)
        try:
            r = requests.get(f"http://ip-api.com/json/{domain}").json()
            if r['status'] == 'success':
                st.markdown(f"""
                <div class='terminal-line'>
                    <span class='bracket'>[</span><span class='info'> GEO </span><span class='bracket'>]</span> 
                    Server Location: <span style='color:#d3dae3'>{r['city']}, {r['country']} ({r['isp']})</span>
                </div>""", unsafe_allow_html=True)
        except:
            pass

        # 3. DNS RECORDS (MX & NS)
        st.markdown("<br><span style='color:#555'>:: DNS Records</span>", unsafe_allow_html=True)
        record_types = ['NS', 'MX', 'TXT']
        for rt in record_types:
            try:
                answers = dns.resolver.resolve(domain, rt)
                for rdata in answers:
                    st.markdown(f"""
                    <div class='terminal-line'>
                        <span class='bracket'>[</span><span class='warn'> DNS </span><span class='bracket'>]</span> 
                        {rt}: <span style='color:#d3dae3'>{rdata.to_text()}</span>
                    </div>""", unsafe_allow_html=True)
            except:
                pass
        
        # 4. WHOIS
        st.markdown("<br><span style='color:#555'>:: Registrar Info</span>", unsafe_allow_html=True)
        try:
            w = whois.whois(domain)
            st.markdown(f"""
            <div style='font-size:0.9em; color:#888; border-left: 2px solid #333; padding-left:10px;'>
                Registrar: {w.registrar}<br>
                Creation Date: {w.creation_date}<br>
                Expiration: {w.expiration_date}<br>
                Emails: {w.emails}
            </div>
            """, unsafe_allow_html=True)
        except:
            st.markdown("<div class='terminal-line'><span class='minus'>ERR</span> Whois data protected/unavailable</div>", unsafe_allow_html=True)

# --- MAIN LAYOUT & SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:#1793d1; text-align:center;'>// TOOLKIT</h2>", unsafe_allow_html=True)
    selected_tool = st.radio(
        "Select Operation:",
        ["User Recon", "Domain Recon"],
        label_visibility="collapsed"
    )
    st.markdown("<br><div style='text-align:center; color:#555; font-size:0.8em;'>v2.0-stable</div>", unsafe_allow_html=True)

# HEADER NEOFETCH (Static for aesthetics)
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
        <span class="info-key">Uptime</span>: 12 mins<br>
        <span class="info-key">Active Tool</span>: """ + selected_tool + r"""<br>
        <span class="info-key">Theme</span>: Dark / Arch Blue
    </div>
</div>
""", unsafe_allow_html=True)

# LOGIC SWITCHER
if selected_tool == "User Recon":
    run_username_recon()
elif selected_tool == "Domain Recon":
    run_domain_recon()

# --- FOOTER ---
st.markdown("""
<br>
<div style="border-top: 1px dashed #333; padding-top: 10px; color: #555; font-size: 0.8em; text-align: right;">
    [ system ready ] :: execute with caution
</div>
""", unsafe_allow_html=True)
