import streamlit as st
import threading
import tempfile
import os
from pathlib import Path
from styles import load_styles
from config import PLATFORM_ICONS, APP_NAME, APP_VERSION
from modules.username import run_sherlock, categorize_results
from modules.image_search import run_image_search
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

tab1, tab2 = st.tabs(["👤 USERNAME SEARCH", "🖼️ IMAGE SEARCH"])

# ── Tab 1: Username ─────────────────────────────────────────────────────────
with tab1:
    search = st.button("▶  EXECUTE SCAN — " + ("TRUSTED MODE" if "TRUSTED" in (mode or "") else "DEEP SCAN MODE"))
    st.markdown("<br>", unsafe_allow_html=True)

    if search:
        if not username.strip():
            st.warning("⚠ NO TARGET SPECIFIED — ENTER A USERNAME")
        else:
            found_results = {}
            done_flag = threading.Event()

            def run_scan():
                found_results.update(run_sherlock(username))
                done_flag.set()

            thread = threading.Thread(target=run_scan)
            thread.start()
            show_scanning_animation(username, done_flag=done_flag)
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

                st.markdown(f"""
                <div class="stats-bar">
                    <div class="stat-item"><div class="stat-number">{len(found)}</div><div class="stat-label">TOTAL HITS</div></div>
                    <div class="stat-item"><div class="stat-number" style="color:#00ff41">{len(confirmed)}</div><div class="stat-label">CONFIRMED</div></div>
                    <div class="stat-item"><div class="stat-number" style="color:#ffcc00">{len(unverified)}</div><div class="stat-label">UNVERIFIED</div></div>
                    <div class="stat-item"><div class="stat-number" style="color:#ff003c">{len(false_positives)}</div><div class="stat-label">FALSE POS.</div></div>
                </div>
                """, unsafe_allow_html=True)

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

# ── Tab 2: Image Search ──────────────────────────────────────────────────────
with tab2:
    st.markdown('<div class="section-label">&gt; UPLOAD_TARGET_IMAGE</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], label_visibility="hidden")

    if uploaded_file:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(uploaded_file, caption="TARGET IMAGE", width=200)
        with col2:
            st.markdown(f"""
            <div class="card-confirmed" style="margin-top:0">
                <div class="card-platform">📁 {uploaded_file.name}</div>
                <div class="card-url">Size: {round(uploaded_file.size / 1024, 1)} KB &nbsp;|&nbsp; Type: {uploaded_file.type}</div>
            </div>
            """, unsafe_allow_html=True)

    img_search = st.button("▶  EXECUTE IMAGE SCAN")

    if img_search:
        if not uploaded_file:
            st.warning("⚠ NO IMAGE UPLOADED — SELECT A FILE FIRST")
        else:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name

            img_results = {}
            done_flag2 = threading.Event()

            def run_img_scan():
                img_results.update(run_image_search(tmp_path))
                done_flag2.set()

            thread2 = threading.Thread(target=run_img_scan)
            thread2.start()
            show_scanning_animation("IMAGE TARGET", done_flag=done_flag2)
            thread2.join()

            # Cleanup temp file
            os.unlink(tmp_path)

            yandex = img_results.get("yandex", [])
            tineye = img_results.get("tineye", [])
            errors = img_results.get("errors", [])

            total = len(yandex) + len(tineye)
            st.markdown(f"""
            <div class="stats-bar">
                <div class="stat-item"><div class="stat-number">{total}</div><div class="stat-label">TOTAL MATCHES</div></div>
                <div class="stat-item"><div class="stat-number" style="color:#00ff41">{len(yandex)}</div><div class="stat-label">YANDEX</div></div>
                <div class="stat-item"><div class="stat-number" style="color:#ffcc00">{len(tineye)}</div><div class="stat-label">TINEYE</div></div>
                <div class="stat-item"><div class="stat-number" style="color:#ff003c">{len(errors)}</div><div class="stat-label">ERRORS</div></div>
            </div>
            """, unsafe_allow_html=True)

            if yandex:
                st.markdown('<div class="section-label">&gt; YANDEX MATCHES</div>', unsafe_allow_html=True)
                cols = st.columns(2)
                for i, result in enumerate(yandex[:20]):
                    with cols[i % 2]:
                        st.markdown(f"""
                        <div class="card-confirmed">
                            <div class="card-platform">🔍 {result.get('title', 'Unknown')[:50]}</div>
                            <div class="card-url"><a href="{result['url']}" target="_blank">{result['url'][:80]}</a></div>
                        </div>
                        """, unsafe_allow_html=True)

            if tineye:
                st.markdown('<br><div class="section-label">&gt; TINEYE MATCHES</div>', unsafe_allow_html=True)
                cols = st.columns(2)
                for i, result in enumerate(tineye[:20]):
                    with cols[i % 2]:
                        st.markdown(f"""
                        <div class="card-unverified">
                            <div class="card-platform" style="color:#ffcc00">👁️ {result.get('title', 'Unknown')[:50]}</div>
                            <div class="card-url"><a href="{result['url']}" target="_blank" style="color:#ccaa00">{result['url'][:80]}</a></div>
                        </div>
                        """, unsafe_allow_html=True)

            if not yandex and not tineye:
                st.error("[ NO MATCHES FOUND — TRY A DIFFERENT IMAGE ]")

            if errors:
                with st.expander("[ ERRORS — CLICK TO EXPAND ]"):
                    for err in errors:
                        st.code(f"{err['source']}: {err['error']}")