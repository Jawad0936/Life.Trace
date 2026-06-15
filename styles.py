def load_styles():
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@700&display=swap');

html, body, [class*="css"] {
    background-color: #0a0a0a !important;
    color: #00ff41 !important;
    font-family: 'Share Tech Mono', monospace !important;
}

.lt-header { text-align: center; padding: 2rem 0 1rem 0; }
.lt-title {
    font-family: 'Orbitron', monospace;
    font-size: 3rem;
    color: #00ff41;
    text-shadow: 0 0 20px #00ff41, 0 0 40px #00ff41;
    letter-spacing: 0.3em;
}
.lt-subtitle {
    color: #005f1a;
    font-size: 0.85rem;
    letter-spacing: 0.2em;
    margin-top: 0.3rem;
}
.lt-divider {
    border: none;
    border-top: 1px solid #003a0f;
    margin: 1rem 0 2rem 0;
    box-shadow: 0 0 8px #00ff41;
}

/* Input */
.stTextInput > div > div > input {
    background-color: #0d0d0d !important;
    border: 1px solid #00ff41 !important;
    color: #00ff41 !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 1rem !important;
    border-radius: 0 !important;
    box-shadow: 0 0 8px #00ff4133 !important;
}
.stTextInput > div > div > input:focus {
    box-shadow: 0 0 16px #00ff41 !important;
}
.stTextInput label { color: #00ff41 !important; font-family: 'Share Tech Mono', monospace !important; }

/* Button */
.stButton > button {
    background-color: #000 !important;
    color: #00ff41 !important;
    border: 1px solid #00ff41 !important;
    border-radius: 0 !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.15em !important;
    padding: 0.6rem 2rem !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background-color: #00ff41 !important;
    color: #000 !important;
    box-shadow: 0 0 20px #00ff41 !important;
}

/* Radio */
.stRadio label { color: #00ff41 !important; font-family: 'Share Tech Mono', monospace !important; }
.stRadio > div { gap: 1.5rem !important; }

/* Cards */
.card-confirmed {
    background: #050f05;
    border: 1px solid #00ff41;
    border-left: 4px solid #00ff41;
    padding: 0.75rem 1rem;
    margin-bottom: 0.5rem;
    box-shadow: 0 0 10px #00ff4122;
    font-family: 'Share Tech Mono', monospace;
}
.card-unverified {
    background: #0f0e00;
    border: 1px solid #ffcc00;
    border-left: 4px solid #ffcc00;
    padding: 0.75rem 1rem;
    margin-bottom: 0.5rem;
    font-family: 'Share Tech Mono', monospace;
}
.card-false {
    background: #0f0000;
    border: 1px solid #ff003c;
    border-left: 4px solid #ff003c;
    padding: 0.75rem 1rem;
    margin-bottom: 0.5rem;
    font-family: 'Share Tech Mono', monospace;
    opacity: 0.6;
}
.card-platform { font-size: 1rem; font-weight: bold; color: #00ff41; }
.card-url { font-size: 0.78rem; color: #007a1f; word-break: break-all; }
.card-url a { color: #00cc34 !important; text-decoration: none !important; }
.card-url a:hover { text-shadow: 0 0 8px #00ff41; }

/* Stats */
.stats-bar {
    display: flex;
    gap: 2rem;
    padding: 1rem;
    background: #050f05;
    border: 1px solid #003a0f;
    margin-bottom: 1.5rem;
    font-family: 'Share Tech Mono', monospace;
}
.stat-item { text-align: center; }
.stat-number { font-size: 1.8rem; color: #00ff41; text-shadow: 0 0 10px #00ff41; }
.stat-label { font-size: 0.7rem; color: #005f1a; letter-spacing: 0.1em; }

/* Hacking terminal animation */
.terminal-box {
    background: #020f02;
    border: 1px solid #00ff41;
    padding: 1.2rem 1.5rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.85rem;
    color: #00ff41;
    min-height: 220px;
    box-shadow: 0 0 20px #00ff4133;
    margin-bottom: 1.5rem;
    overflow: hidden;
}
.terminal-line { margin: 0.15rem 0; }
.terminal-line.dim { color: #005f1a; }
.terminal-line.warn { color: #ffcc00; }
.terminal-line.success { color: #00ff41; text-shadow: 0 0 6px #00ff41; }
.blink { animation: blink 1s step-end infinite; }
@keyframes blink { 50% { opacity: 0; } }

.section-label {
    color: #005f1a;
    font-size: 0.75rem;
    letter-spacing: 0.2em;
    margin-bottom: 0.5rem;
    border-bottom: 1px solid #003a0f;
    padding-bottom: 0.3rem;
}

.stProgress > div > div > div { background-color: #00ff41 !important; }
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""