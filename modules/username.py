import subprocess
import sys
import requests
from config import TRUSTED_PLATFORMS

def run_sherlock(username: str) -> dict:
    """Run Sherlock and return dict of {platform: url}"""
    result = subprocess.run(
        [sys.executable, "-m", "sherlock_project", username, "--print-found", "--timeout", "10"],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    found = {}
    for line in result.stdout.splitlines():
        if "[+]" in line and "http" in line:
            parts = line.split(": ", 1)
            if len(parts) == 2:
                platform = parts[0].replace("[+]", "").strip()
                url = parts[1].strip()
                found[platform] = url
    return found

def verify_profile(url: str) -> bool | None:
    """Returns True if confirmed, False if fake, None if unverifiable"""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        r = requests.get(url, headers=headers, timeout=8)
        not_found_phrases = [
            "page not found", "user not found", "doesn't exist",
            "no user", "account not found", "this account doesn't exist",
            "sorry, this page isn't available", "404", "not available"
        ]
        for phrase in not_found_phrases:
            if phrase in r.text.lower():
                return False
        return True
    except:
        return None

def categorize_results(found: dict, deep: bool = False, progress_callback=None):
    """Sort results into confirmed / unverified / false positives"""
    confirmed, unverified, false_positives = {}, {}, {}

    if not deep:
        confirmed = {p: u for p, u in found.items() if p in TRUSTED_PLATFORMS}
        return confirmed, unverified, false_positives

    total = len(found)
    for i, (platform, url) in enumerate(found.items()):
        if progress_callback:
            progress_callback(i, total, platform)
        if platform in TRUSTED_PLATFORMS:
            confirmed[platform] = url
        else:
            status = verify_profile(url)
            if status is True:
                confirmed[platform] = url
            elif status is None:
                unverified[platform] = url
            else:
                false_positives[platform] = url

    return confirmed, unverified, false_positives