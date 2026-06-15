import streamlit as st
import threading
from styles import load_styles
from config import PLATFORM_ICONS, APP_NAME, APP_VERSION
from modules.username import run_sherlock, categorize_results
from components.scanner_ui import show_scanning_animation

st.set_page_config(page_title="Life.Trace", page_icon="🔍", layout="wide")
st.markdown(load_styles(), unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="lt-header">
    <div class="lt-title">⟨ {APP_NAME} ⟩</div>
    <div class="lt-subtitle">// PERSONAL OSINT AGGREGATOR v{APP_VERSION} — PRIVATE USE ONLY //</div>
</div>
<hr class="lt-divider">
""", unsafe_allow_html=True)

# ── Input ──────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">&gt; TARGET_USERNAME</div>', unsafe_allow_html=True)
username = st.text_input("TARGET", placeholder="enter username or handle...", label_visibility="hidden")

mode = st.radio(
    "SCAN_MODE:",
    ["[ TRUSTED ] Accurate platforms only", "[ DEEP ] All platforms + live verify"],
    horizontal=True
)

st.markdown("<br>", unsafe_allow_html=True)
search = st.button("▶  EXECUTE SCAN — " + ("TRUSTED MODE" if "TRUSTED" in (mode or "") else "DEEP SCAN MODE"))
st.markdown("<br>", unsafe_allow_html=True)

# ── Scan ───────────────────────────────────────────────────────────────────
if search:
    if not username.strip():
        st.warning("⚠ NO TARGET SPECIFIED — ENTER A USERNAME")
    else:
        found_results = {}
        done_flag = threading.Event()

        def run_scan():
            found_results.update(run_sherlock(username))
            done_flag.set()  # signal animation to stop

        # Start Sherlock in background thread
        thread = threading.Thread(target=run_scan)
        thread.start()

        # Show hacking animation while scan runs in background
        show_scanning_animation(username, done_flag=done_flag)

        # Wait for scan to finish if animation ends first
        thread.join()

        found = found_results

        if not found:
            st.error("[ NO RESULTS FOUND FOR TARGET ]")
        else:
            deep = "DEEP" in mode

            if deep:
                bar = st.progress(0)
                status_text = st.empty()

                def update_progress(i, total, platform):
                    bar.progress((i + 1) / total)
                    status_text.markdown(
                        f'<div class="section-label">&gt; VERIFYING: {platform.upper()}</div>',
                        unsafe_allow_html=True
                    )

                confirmed, unverified, false_positives = categorize_results(
                    found, deep=True, progress_callback=update_progress
                )
                bar.empty()
                status_text.empty()
            else:
                confirmed, unverified, false_positives = categorize_results(found, deep=False)

            # Stats bar
            st.markdown(f"""
            <div class="stats-bar">
                <div class="stat-item">
                    <div class="stat-number">{len(found)}</div>
                    <div class="stat-label">TOTAL HITS</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number" style="color:#00ff41">{len(confirmed)}</div>
                    <div class="stat-label">CONFIRMED</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number" style="color:#ffcc00">{len(unverified)}</div>
                    <div class="stat-label">UNVERIFIED</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number" style="color:#ff003c">{len(false_positives)}</div>
                    <div class="stat-label">FALSE POS.</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Confirmed results
            if confirmed:
                st.markdown('<div class="section-label">&gt; CONFIRMED PROFILES</div>', unsafe_allow_html=True)
                cols = st.columns(2)
                for i, (platform, url) in enumerate(confirmed.items()):
                    icon = PLATFORM_ICONS.get(platform, "🔍")
                    with cols[i % 2]:
                        st.markdown(f"""
                        <div class="card-confirmed">
                            <div class="card-platform">{icon} {platform}</div>
                            <div class="card-url"><a href="{url}" target="_blank">{url}</a></div>
                        </div>
                        """, unsafe_allow_html=True)

            # Unverified results
            if unverified:
                st.markdown('<br><div class="section-label">&gt; UNVERIFIED — MANUAL CHECK REQUIRED</div>', unsafe_allow_html=True)
                cols = st.columns(2)
                for i, (platform, url) in enumerate(unverified.items()):
                    icon = PLATFORM_ICONS.get(platform, "🔍")
                    with cols[i % 2]:
                        st.markdown(f"""
                        <div class="card-unverified">
                            <div class="card-platform" style="color:#ffcc00">{icon} {platform}</div>
                            <div class="card-url"><a href="{url}" target="_blank" style="color:#ccaa00">{url}</a></div>
                        </div>
                        """, unsafe_allow_html=True)

            # False positives
            if false_positives:
                with st.expander(f"[ {len(false_positives)} FALSE POSITIVES — CLICK TO EXPAND ]"):
                    cols = st.columns(2)
                    for i, (platform, url) in enumerate(false_positives.items()):
                        icon = PLATFORM_ICONS.get(platform, "🔍")
                        with cols[i % 2]:
                            st.markdown(f"""
                            <div class="card-false">
                                <div class="card-platform" style="color:#ff003c">{icon} {platform}</div>
                                <div class="card-url"><a href="{url}" target="_blank" style="color:#cc0030">{url}</a></div>
                            </div>
                            """, unsafe_allow_html=True)