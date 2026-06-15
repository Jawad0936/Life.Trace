import streamlit as st
import time
import threading

def show_scanning_animation(username: str, done_flag: threading.Event = None):
    """Shows a hacking-style terminal animation until done_flag is set"""

    boot_lines = [
        f"[*] Initializing OSINT engine...",
        f"[*] Loading platform database — 400+ targets",
        f"[*] Spoofing user-agent headers...",
        f"[*] Establishing anonymous connections...",
        f"[~] Target acquired: {username.upper()}",
        f"[*] Injecting username into query matrix...",
    ]

    loop_lines = [
        "[~] Probing GitHub... Reddit... Twitter...",
        "[~] Probing Steam... Twitch... TikTok...",
        "[~] Probing Pastebin... HackerNews... Gitlab...",
        "[~] Probing Instagram... Snapchat... Pinterest...",
        "[*] Cross-referencing digital footprints...",
        "[~] Bypassing rate limiters...",
        "[~] Probing SoundCloud... Spotify... Medium...",
        "[~] Probing Keybase... Replit... Kaggle...",
        "[*] Scanning social graph layer 2...",
        "[~] Probing DeviantArt... Flickr... Vimeo...",
        "[*] Aggregating partial results...",
        "[~] Probing WordPress... Blogger... About.me...",
        "[*] Scanning social graph layer 3...",
        "[~] Probing TryHackMe... HackTheBox...",
        "[*] Verifying connections...",
    ]

    placeholder = st.empty()
    displayed = []

    def render(extra_line=None):
        html_lines = ""
        lines = displayed + ([extra_line] if extra_line else [])
        for l in lines:
            if l.startswith("[✓]"):
                css = "terminal-line success"
            elif l.startswith("[~]"):
                css = "terminal-line dim"
            elif l.startswith("[!]"):
                css = "terminal-line warn"
            else:
                css = "terminal-line"
            html_lines += f'<div class="{css}">{l}</div>'

        placeholder.markdown(f"""
        <div class="terminal-box">
            <div class="terminal-line dim">// LIFE.TRACE SCANNER — ACTIVE SESSION //</div>
            <br>
            {html_lines}
            <span class="blink">█</span>
        </div>
        """, unsafe_allow_html=True)

    # Show boot lines first
    for line in boot_lines:
        displayed.append(line)
        render()
        time.sleep(0.2)

    # Keep looping until scan is done
    i = 0
    while done_flag and not done_flag.is_set():
        line = loop_lines[i % len(loop_lines)]
        # Keep last 10 lines visible so terminal scrolls
        if len(displayed) > 10:
            displayed.pop(6)  # remove oldest loop line, keep boot lines
        displayed.append(line)
        render()
        time.sleep(0.4)
        i += 1

    # Done
    displayed.append("[✓] Scan complete. Compiling report...")
    render()
    time.sleep(0.6)
    placeholder.empty()