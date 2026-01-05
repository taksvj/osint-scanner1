import streamlit as st
import requests
import time
import socket
import whois
import dns.resolver
import instaloader
import re
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from faker import Faker
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from geopy.geocoders import Nominatim

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
        --term-gray: #928374;
        --term-white: #ebdbb2;
        --term-pink: #d3869b;
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

    .stTextInput > div > div > input, .stSelectbox > div > div > div, .stTextArea > div > div > textarea {
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
    .geo { color: var(--term-gray); font-weight: bold; }
    .net { color: var(--term-white); font-weight: bold; }
    .num { color: var(--term-pink); font-weight: bold; }
    
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

# --- FUNGSI HELPER ---
def get_decimal_from_dms(dms, ref):
    degrees = dms[0]
    minutes = dms[1]
    seconds = dms[2]
    decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
    if ref in ['S', 'W']: decimal = -decimal
    return decimal

def render_terminal_progress(placeholder, percent, task_name):
    bar_len = 20
    filled = int(bar_len * percent // 100)
    bar = "█" * filled + "░" * (bar_len - filled)
    text = f"""<div style="font-family:'Fira Code'; color:#aaa; margin-top:10px;">[{bar}] {percent}% :: {task_name}</div>"""
    placeholder.markdown(text, unsafe_allow_html=True)

# --- MODULES SEBELUMNYA (DISINGKAT) ---
def run_username_recon():
    st.markdown("""<div style="font-family: 'Fira Code'; color: #23d18b; margin-bottom: 10px;">[taksvj@archlinux ~]$ <span style="color: #d3dae3;">./sherlock --timeout 1 target_user</span></div>""", unsafe_allow_html=True)
    c1, c2 = st.columns([5, 1])
    target = c1.text_input("", placeholder="username...", label_visibility="collapsed")
    run = c2.button("SCAN USER")
    loading = st.empty()
    if run and target:
        st.markdown(f"<div style='color:#777;'>:: Initializing scan for user: <b>{target}</b>...</div><br>", unsafe_allow_html=True)
        sites = {"GitHub": f"https://github.com/{target}", "Instagram": f"https://www.instagram.com/{target}", "Twitter": f"https://twitter.com/{target}"}
        found = []
        for site, url in sites.items():
            try:
                r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=1.5)
                if r.status_code == 200: found.append((site, url))
            except: pass
        if found:
            for s, u in found: st.markdown(f"<div class='terminal-line'><span class='bracket'>[</span><span class='plus'> FOUND </span><span class='bracket'>]</span> <a href='{u}' target='_blank'>{s} account found</a></div>", unsafe_allow_html=True)
        else: st.markdown("<div class='terminal-line'><span class='minus'>error:</span> No accounts found.</div>", unsafe_allow_html=True)

def run_domain_recon():
    st.markdown("""<div style="font-family: 'Fira Code'; color: #23d18b; margin-bottom: 10px;">[taksvj@archlinux ~]$ <span style="color: #d3dae3;">sudo nmap -sn target_domain</span></div>""", unsafe_allow_html=True)
    c1, c2 = st.columns([5, 1])
    domain = c1.text_input("", placeholder="domain.com...", label_visibility="collapsed")
    run = c2.button("SCAN DOMAIN")
    if run and domain:
        domain = domain.replace("https://", "").replace("http://", "").replace("www.", "").split('/')[0]
        try:
            ip = socket.gethostbyname(domain)
            st.markdown(f"<div class='terminal-line'><span class='bracket'>[</span><span class='info'> NET </span><span class='bracket'>]</span> IPv4: <span style='color:#d3dae3'>{ip}</span></div>", unsafe_allow_html=True)
            r = requests.get(f"http://ip-api.com/json/{ip}").json()
            if r['status'] == 'success':
                st.markdown(f"<div class='terminal-line'><span class='bracket'>[</span><span class='info'> GEO </span><span class='bracket'>]</span> Loc: <span style='color:#d3dae3'>{r['city']}, {r['country']}</span></div>", unsafe_allow_html=True)
        except: pass

def run_instagram_recon():
    st.markdown("""<div style="font-family: 'Fira Code'; color: #b16286; margin-bottom: 10px;">[taksvj@archlinux ~]$ <span style="color: #d3dae3;">instaloader --profile target_ig</span></div>""", unsafe_allow_html=True)
    c1, c2 = st.columns([5, 1])
    username = c1.text_input("", placeholder="instagram username...", label_visibility="collapsed")
    run = c2.button("SCAN IG")
    if run and username:
        L = instaloader.Instaloader()
        try:
            profile = instaloader.Profile.from_username(L.context, username)
            html_content = f"""<div style="border: 1px solid #b16286; padding: 20px; margin-top: 10px;"><h3 style="color: #b16286; margin:0;">@{profile.username}</h3><div style="color: #777;">ID: {profile.userid} | Followers: {profile.followers}</div></div>"""
            st.markdown(html_content, unsafe_allow_html=True)
        except Exception as e: st.error(f"Error: {e}")

def run_persona_forge():
    st.markdown("""<div style="font-family: 'Fira Code'; color: #8ec07c; margin-bottom: 10px;">[taksvj@archlinux ~]$ <span style="color: #d3dae3;">python forge_identity.py --locale en_US</span></div>""", unsafe_allow_html=True)
    c1, c2 = st.columns([3, 1])
    locale = c1.selectbox("Select Region", ["en_US", "id_ID"], label_visibility="collapsed")
    run = c2.button("GENERATE ID")
    if run:
        fake = Faker(locale)
        st.markdown(f"""<div style="border: 1px solid #8ec07c; padding: 20px; margin-top: 10px;"><div style="color: #8ec07c;">IDENTITY FORGED</div><div style="color: #d3dae3;">{fake.name()}</div><div style="color: #666;">{fake.address()}</div></div>""", unsafe_allow_html=True)

def run_exif_probe():
    st.markdown("""<div style="font-family: 'Fira Code'; color: #fe8019; margin-bottom: 10px;">[taksvj@archlinux ~]$ <span style="color: #d3dae3;">exiftool -all target_image.jpg</span></div>""", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=['jpg', 'jpeg', 'png'], label_visibility="collapsed")
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            st.markdown(f"<div class='terminal-line'><span class='bracket'>[</span><span class='plus'> OK </span><span class='bracket'>]</span> Image Loaded</div>", unsafe_allow_html=True)
            exifdata = image._getexif()
            if exifdata:
                st.markdown("<div class='terminal-line'><span class='exif'> DAT </span> Metadata Extracted (Check Console)</div>", unsafe_allow_html=True)
        except: pass

def run_geo_spy():
    st.markdown("""<div style="font-family: 'Fira Code'; color: #928374; margin-bottom: 10px;">[taksvj@archlinux ~]$ <span style="color: #d3dae3;">./geospy --triangulate target</span></div>""", unsafe_allow_html=True)
    mode = st.radio("Select Mode:", ["IP Tracker", "Address Hunter"], horizontal=True)
    if mode == "IP Tracker":
        c1, c2 = st.columns([5, 1])
        ip_addr = c1.text_input("", placeholder="Enter IP...", label_visibility="collapsed")
        run = c2.button("TRACE IP")
        if run and ip_addr:
            try:
                r = requests.get(f"http://ip-api.com/json/{ip_addr}").json()
                if r['status'] == 'success':
                    st.markdown(f"<div style='border:1px solid #928374; padding:15px; margin-top:10px;'>LOCATION: {r['city']}, {r['country']} <br> ISP: {r['isp']}</div>", unsafe_allow_html=True)
                    st.map(data={'lat': [r['lat']], 'lon': [r['lon']]})
            except: pass
    elif mode == "Address Hunter":
        c1, c2 = st.columns([5, 1])
        address = c1.text_input("", placeholder="Enter Address...", label_visibility="collapsed")
        run = c2.button("LOCATE")
        if run and address:
            geolocator = Nominatim(user_agent="osint_scanner_v1")
            try:
                location = geolocator.geocode(address)
                if location:
                    st.markdown(f"<div style='margin-top:10px;'>COORDINATES: {location.latitude}, {location.longitude}</div>", unsafe_allow_html=True)
                    st.map(data={'lat': [location.latitude], 'lon': [location.longitude]})
            except: pass

def run_net_stalker():
    st.markdown("""<div style="font-family: 'Fira Code'; color: #ebdbb2; margin-bottom: 10px;">[taksvj@archlinux ~]$ <span style="color: #d3dae3;">grep -E "([0-9]{1,3}\.){3}[0-9]{1,3}" email_header.txt</span></div>""", unsafe_allow_html=True)
    header_text = st.text_area("", placeholder="Paste Raw Email Header here...", height=200)
    run = st.button("ANALYZE HEADER")
    if run and header_text:
        ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', header_text)
        public_ips = []
        for ip in ips:
            if not (ip.startswith('127.') or ip.startswith('192.168.') or ip.startswith('10.')):
                if ip not in public_ips: public_ips.append(ip)
        if public_ips:
            st.markdown(f"<br><div class='terminal-line'><span class='plus'> SUCCESS </span> Found {len(public_ips)} Potential Public IPs</div>", unsafe_allow_html=True)
            for ip in public_ips:
                try:
                    r = requests.get(f"http://ip-api.com/json/{ip}").json()
                    st.markdown(f"<div style='border:1px solid #ebdbb2; padding:10px; margin-top:10px;'>IP: {ip} | LOC: {r['city']}, {r['country']} ({r['isp']})</div>", unsafe_allow_html=True)
                except: pass

# --- MODULE 8: NUM SEEKER (NEW) ---
def run_num_seeker():
    st.markdown("""
    <div style="font-family: 'Fira Code'; color: #d3869b; margin-bottom: 10px;">
        [taksvj@archlinux ~]$ <span style="color: #d3dae3;">./num_seeker -v target_phone</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='color:#777; margin-bottom:5px;'>:: Analyze Phone Number (Carrier, Location, WA). Use Int'l Format (e.g. +6281...)</div>", unsafe_allow_html=True)
    
    c1, c2 = st.columns([5, 1])
    phone_input = c1.text_input("", placeholder="+628123456789...", label_visibility="collapsed")
    run = c2.button("TRACK NUM")
    
    if run and phone_input:
        try:
            # Parse Number
            parsed_num = phonenumbers.parse(phone_input, None)
            
            # Cek Validitas
            is_valid = phonenumbers.is_valid_number(parsed_num)
            is_possible = phonenumbers.is_possible_number(parsed_num)
            
            if is_valid:
                # Ambil Data
                country = geocoder.description_for_number(parsed_num, "en")
                provider = carrier.name_for_number(parsed_num, "en")
                time_zones = timezone.time_zones_for_number(parsed_num)
                formatted_intl = phonenumbers.format_number(parsed_num, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
                
                # Buat Link WhatsApp (Tanpa Save Nomor)
                # Kita hapus tanda '+' dan spasi buat link WA
                wa_clean = str(parsed_num.country_code) + str(parsed_num.national_number)
                wa_link = f"https://wa.me/{wa_clean}"
                
                st.markdown(f"""
                <div style="border: 1px solid #d3869b; padding: 15px; background: rgba(211, 134, 155, 0.1); margin-top: 15px;">
                    <div style="display:flex; justify-content:space-between;">
                        <span style="color:#d3dae3; font-size: 1.2em; font-weight:bold;">{formatted_intl}</span>
                        <span style="color:#23d18b; font-weight:bold;">[ VALID ]</span>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 15px;">
                        <div>
                            <div style="color:#777; font-size:0.8em;">COUNTRY / REGION</div>
                            <div style="color:#d3869b;">{country}</div>
                        </div>
                        <div>
                            <div style="color:#777; font-size:0.8em;">CARRIER (PROVIDER)</div>
                            <div style="color:#d3dae3;">{provider}</div>
                        </div>
                    </div>
                    
                    <div style="margin-top: 10px;">
                        <div style="color:#777; font-size:0.8em;">TIMEZONE</div>
                        <div style="color:#d3dae3;">{', '.join(time_zones)}</div>
                    </div>
                    
                    <div style="margin-top: 20px; border-top: 1px dashed #555; padding-top: 10px;">
                        <span style="color:#23d18b;">WHATSAPP RECON:</span> 
                        <a href="{wa_link}" target="_blank" style="color:#d3869b; border-bottom:1px dotted #d3869b;">[ OPEN DIRECT CHAT ]</a>
                        <br><span style="color:#777; font-size:0.8em;">*Click to view Profile Picture without saving contact.</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("Invalid Phone Number. Make sure to use Country Code (e.g., +62).")
                
        except Exception as e:
            st.error(f"Error Parsing: {e}. Please use format +628...")

# --- MAIN LAYOUT & SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:#1793d1; text-align:center;'>// TOOLKIT</h2>", unsafe_allow_html=True)
    selected_tool = st.radio(
        "Select Operation:",
        ["User Recon", "Domain Recon", "Instagram Recon", "Persona Forge", "Exif Probe", "Geo Spy", "Net Stalker", "Num Seeker"],
        label_visibility="collapsed"
    )
    st.markdown("<br><div style='text-align:center; color:#555; font-size:0.8em;'>v8.0-unlimited</div>", unsafe_allow_html=True)

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
if selected_tool == "User Recon": run_username_recon()
elif selected_tool == "Domain Recon": run_domain_recon()
elif selected_tool == "Instagram Recon": run_instagram_recon()
elif selected_tool == "Persona Forge": run_persona_forge()
elif selected_tool == "Exif Probe": run_exif_probe()
elif selected_tool == "Geo Spy": run_geo_spy()
elif selected_tool == "Net Stalker": run_net_stalker()
elif selected_tool == "Num Seeker": run_num_seeker()

st.markdown("""<br><div style="border-top: 1px dashed #333; padding-top: 10px; color: #555; font-size: 0.8em; text-align: right;">[ system ready ] :: execute with caution</div>""", unsafe_allow_html=True)
