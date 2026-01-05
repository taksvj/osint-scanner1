import streamlit as st
import requests
import time
import socket
import whois
import dns.resolver
import instaloader
from faker import Faker
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

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
        --term-cyan: #8ec07c;
        --term-orange: #fe8019;
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

    .stTextInput > div > div > input, .stSelectbox > div > div > div {
        background-color: #1a1a1a !important;
        color: var(--arch-fg) !important;
        border: 1px solid #333 !important;
        font-family: 'Fira Code', monospace;
        border-radius: 0;
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
    
    /* File Uploader Style */
    [data-testid="stFileUploader"] {
        border: 1px dashed #444;
        padding: 20px;
        border-radius: 5px;
    }

    .terminal-line { margin-bottom: 5px; border-bottom: 1px solid #1a1a1a; padding-bottom: 2px; }
    .bracket { color: #555; font-weight: bold; }
    .plus { color: var(--term-green); font-weight: bold; }
    .minus { color: var(--term-red); font-weight: bold; }
    .warn { color: var(--term-yellow); font-weight: bold; }
    .info { color: var(--arch-blue); font-weight: bold; }
    .ig { color: var(--term-purple); font-weight: bold; }
    .id { color: var(--term-cyan); font-weight: bold; }
    .exif { color: var(--term-orange); font-weight: bold; }
    
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

# --- FUNGSI HELPER GPS ---
def get_decimal_from_dms(dms, ref):
    degrees = dms[0]
    minutes = dms[1]
    seconds = dms[2]
    decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
    if ref in ['S', 'W']:
        decimal = -decimal
    return decimal

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

# --- MODULE 3: INSTAGRAM RECON ---
def run_instagram_recon():
    st.markdown("""<div style="font-family: 'Fira Code'; color: #b16286; margin-bottom: 10px;">[taksvj@archlinux ~]$ <span style="color: #d3dae3;">instaloader --profile target_ig</span></div>""", unsafe_allow_html=True)
    c1, c2 = st.columns([5, 1])
    username = c1.text_input("", placeholder="instagram username...", label_visibility="collapsed")
    run = c2.button("SCAN IG")

    if run and username:
        st.markdown(f"<div style='color:#777; margin-bottom:10px;'>:: Connecting to Gateway for <b>{username}</b>...</div>", unsafe_allow_html=True)
        L = instaloader.Instaloader()
        try:
            profile = instaloader.Profile.from_username(L.context, username)
            html_content = f"""
<div style="border: 1px solid #b16286; padding: 20px; margin-top: 10px;">
<h3 style="color: #b16286; margin:0;">@{profile.username}</h3>
<div style="color: #777; font-size: 0.9em; margin-bottom: 15px;">ID: {profile.userid}</div>
<div style="display: flex; gap: 30px;">
<div><div style="color: #d3dae3; font-size: 1.5em; font-weight: bold;">{profile.mediacount}</div><div style="color: #b16286;">Posts</div></div>
<div><div style="color: #d3dae3; font-size: 1.5em; font-weight: bold;">{profile.followers}</div><div style="color: #b16286;">Followers</div></div>
<div><div style="color: #d3dae3; font-size: 1.5em; font-weight: bold;">{profile.followees}</div><div style="color: #b16286;">Following</div></div>
</div>
<div style="margin-top: 15px; border-top: 1px dashed #333; padding-top: 10px;">
<span style="color: #b16286;">Bio:</span> <span style="color: #aaa;">{profile.biography}</span>
</div>
</div>
"""
            st.markdown(html_content, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {e}")

# --- MODULE 4: PERSONA FORGE ---
def run_persona_forge():
    st.markdown("""<div style="font-family: 'Fira Code'; color: #8ec07c; margin-bottom: 10px;">[taksvj@archlinux ~]$ <span style="color: #d3dae3;">python forge_identity.py --locale en_US</span></div>""", unsafe_allow_html=True)
    c1, c2 = st.columns([3, 1])
    locale = c1.selectbox("Select Region", ["en_US", "id_ID", "ja_JP", "ru_RU", "de_DE"], label_visibility="collapsed")
    run = c2.button("GENERATE ID")

    if run:
        fake = Faker(locale)
        name = fake.name()
        addr = fake.address().replace('\n', ', ')
        job = fake.job()
        email = fake.email()
        ua = fake.user_agent()
        ipv4 = fake.ipv4()
        credit_card = fake.credit_card_number()
        
        html_code = f"""
<div style="border: 1px solid #8ec07c; padding: 20px; margin-top: 10px; background: rgba(0,20,0,0.2);">
<div style="display:flex; justify-content:space-between; align-items:center; border-bottom: 1px dashed #444; padding-bottom: 10px;">
<h3 style="color: #8ec07c; margin:0;">IDENTITY FORGED</h3>
<span style="color: #555; font-size: 0.8em;">[ VERIFIED ]</span>
</div>
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 15px;">
<div><div style="color: #666; font-size: 0.8em;">FULL NAME</div><div style="color: #d3dae3; font-size: 1.2em; font-weight: bold;">{name}</div></div>
<div><div style="color: #666; font-size: 0.8em;">OCCUPATION</div><div style="color: #d3dae3;">{job}</div></div>
</div>
<div style="margin-top: 15px;"><div style="color: #666; font-size: 0.8em;">ADDRESS</div><div style="color: #d3dae3;">{addr}</div></div>
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 15px;">
<div><div style="color: #666; font-size: 0.8em;">EMAIL</div><div style="color: #8ec07c;">{email}</div></div>
<div><div style="color: #666; font-size: 0.8em;">IP SPOOF</div><div style="color: #fa5c5c;">{ipv4}</div></div>
</div>
<div style="margin-top: 15px; border-top: 1px dashed #333; padding-top: 10px;">
<div style="color: #666; font-size: 0.8em;">USER AGENT</div><div style="color: #aaa; font-size: 0.8em; font-family: monospace;">{ua}</div>
</div>
<div style="margin-top: 10px;">
<div style="color: #666; font-size: 0.8em;">CREDIT CARD (FAKE)</div><div style="color: #d3dae3; font-family: monospace;">{credit_card}</div>
</div>
</div>
"""
        st.markdown(html_code, unsafe_allow_html=True)

# --- MODULE 5: EXIF PROBE (NEW) ---
def run_exif_probe():
    st.markdown("""
    <div style="font-family: 'Fira Code'; color: #fe8019; margin-bottom: 10px;">
        [taksvj@archlinux ~]$ <span style="color: #d3dae3;">exiftool -all target_image.jpg</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='color:#777; font-size:0.9em; margin-bottom:15px;'>:: Upload image to extract metadata, camera info, and GPS coordinates.</div>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("", type=['jpg', 'jpeg', 'png', 'tiff'], label_visibility="collapsed")

    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            exifdata = image._getexif()
            
            st.markdown(f"<br><div class='terminal-line'><span class='bracket'>[</span><span class='plus'> OK </span><span class='bracket'>]</span> Image Loaded: <span style='color:#d3dae3'>{uploaded_file.name}</span> ({image.format}, {image.size})</div>", unsafe_allow_html=True)

            if not exifdata:
                st.markdown("<div class='terminal-line'><span class='minus'>ERR</span> No EXIF metadata found in this image.</div>", unsafe_allow_html=True)
            else:
                st.markdown("<br><div style='color:#fe8019; border-bottom:1px dashed #444;'>// METADATA EXTRACTED</div>", unsafe_allow_html=True)
                
                # Parsing EXIF
                metadata = {}
                for tag_id in exifdata:
                    tag = TAGS.get(tag_id, tag_id)
                    data = exifdata.get(tag_id)
                    if isinstance(data, bytes):
                        try: data = data.decode()
                        except: data = "[Binary Data]"
                    metadata[tag] = data
                
                # Tampilkan Data Penting
                important_tags = ['Make', 'Model', 'DateTime', 'Software', 'LensModel']
                for key in important_tags:
                    if key in metadata:
                        st.markdown(f"<div class='terminal-line'><span class='bracket'>[</span><span class='exif'> DAT </span><span class='bracket'>]</span> {key}: <span style='color:#d3dae3'>{metadata[key]}</span></div>", unsafe_allow_html=True)

                # Parsing GPS
                if 'GPSInfo' in metadata:
                    gps_info = metadata['GPSInfo']
                    geo_data = {}
                    for key in gps_info.keys():
                        decode = GPSTAGS.get(key, key)
                        geo_data[decode] = gps_info[key]
                    
                    if 'GPSLatitude' in geo_data and 'GPSLongitude' in geo_data:
                        lat = get_decimal_from_dms(geo_data['GPSLatitude'], geo_data['GPSLatitudeRef'])
                        lon = get_decimal_from_dms(geo_data['GPSLongitude'], geo_data['GPSLongitudeRef'])
                        
                        st.markdown(f"""
                        <div style="margin-top:20px; border: 1px solid #fe8019; padding: 15px; background: rgba(254, 128, 25, 0.1);">
                            <h4 style="color:#fe8019; margin:0;">🎯 GPS COORDINATES FOUND</h4>
                            <div style="color:#d3dae3; margin-top:5px;">Latitude: {lat}</div>
                            <div style="color:#d3dae3;">Longitude: {lon}</div>
                            <div style="margin-top:10px;">
                                <a href="https://www.google.com/maps?q={lat},{lon}" target="_blank" style="color:#fe8019; border-bottom:1px dotted #fe8019;">[ OPEN IN GOOGLE MAPS ]</a>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("<div class='terminal-line'><span class='warn'>WARN</span> GPS Tags found but incomplete.</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='terminal-line'><span class='warn'>WARN</span> No GPS data in this image.</div>", unsafe_allow_html=True)
                    
        except Exception as e:
            st.error(f"Error reading image: {e}")

# --- MAIN LAYOUT & SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:#1793d1; text-align:center;'>// TOOLKIT</h2>", unsafe_allow_html=True)
    selected_tool = st.radio(
        "Select Operation:",
        ["User Recon", "Domain Recon", "Instagram Recon", "Persona Forge", "Exif Probe"],
        label_visibility="collapsed"
    )
    st.markdown("<br><div style='text-align:center; color:#555; font-size:0.8em;'>v5.0-fullstack</div>", unsafe_allow_html=True)

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
elif selected_tool == "Persona Forge":
    run_persona_forge()
elif selected_tool == "Exif Probe":
    run_exif_probe()

# --- FOOTER ---
st.markdown("""<br><div style="border-top: 1px dashed #333; padding-top: 10px; color: #555; font-size: 0.8em; text-align: right;">[ system ready ] :: execute with caution</div>""", unsafe_allow_html=True)
