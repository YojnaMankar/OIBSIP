# OASIS INFOBYTE — Python Programming Internship
## Task 3: Random Password Generator (Advanced)

[![Python Version](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Security Standard](https://img.shields.io/badge/Security-CSPRNG%20(secrets)-brightgreen.svg)](https://docs.python.org/3/library/secrets.html)
[![GUI Framework](https://img.shields.io/badge/GUI-Tkinter%20%26%20TTK-teal.svg)](https://docs.python.org/3/library/tkinter.html)
[![Clipboard Support](https://img.shields.io/badge/Clipboard-pyperclip-orange.svg)](https://pypi.org/project/pyperclip/)

---

## 📌 Project Overview & Objective
This project is developed for the **OASIS INFOBYTE SIP Internship (Python Programming Domain)** under **Task 3: Random Password Generator (Advanced)**.

The primary objective is to engineer a desktop application that generates high-entropy, cryptographically secure passwords. Unlike basic demos that use Python's pseudo-random `random` module, this system strictly utilizes the standard library `secrets` module (CSPRNG), guarantees representation across all selected character sets, enforces a minimum security policy ($\ge 2$ character categories), calculates real-time cryptographic Shannon entropy, and maintains a strict ephemeral session-only history.

---

## 🛡 Security Architecture & Cryptographic Approach

### 1. CSPRNG via Python's `secrets` Module
- **Zero Use of `random`**: Python's `random` module relies on the Mersenne Twister PRNG, which is completely deterministic and cryptographically broken. This project exclusively employs `secrets.choice()` and `secrets.SystemRandom().shuffle()` sourced directly from the operating system's kernel entropy pool (`CryptGenRandom` / `BCryptGenRandom` on Windows).

### 2. Guaranteed Character Inclusion
- When a user selects a combination of character pools (e.g., Uppercase + Lowercase + Numbers), standard random generators may coincidentally omit one category.
- Our implementation guarantees that **every selected category has at least one character explicitly included**, followed by a cryptographically secure Fisher-Yates shuffle to ensure character positions remain non-deterministic.

### 3. Ambiguous Character Filtration
- Option to exclude look-alike characters (`0, O, o, 1, l, I, |`, etc.) to eliminate transcription errors when copying passwords between devices or reading printed credentials.

### 4. Ephemeral In-Memory History
- In compliance with cybersecurity best practices, generated passwords are **NEVER saved to any database, text file, or persistent disk storage**.
- The session history maintains only the last 5 passwords in volatile RAM, which is automatically purged when the application window closes.

---

## ✨ Application Features

- **Modern Clean GUI**: Professional split-card layout with dark slate header banner and responsive controls.
- **Dual Length Control**: Synchronized slider and numeric spinbox supporting lengths from 8 to 64 characters (default: 16).
- **Enforced Security Policy**: Requires at least **2 character types** to be selected. Prevents weak single-pool password generation with user-friendly validation.
- **Dynamic Security Meter**:
  - 🔴 **Weak**: Score $< 40$ (Short lengths, low character pool diversity).
  - 🟡 **Medium**: Score $40 - 69$ (Standard combinations, moderate length).
  - 🔵 **Strong**: Score $70 - 87$ (Multi-pool combinations with 14+ characters).
  - 🟢 **Very Strong**: Score $\ge 88$ (Full diversity, 16+ characters, high entropy).
- **Shannon Entropy Calculation**: Live display of theoretical password entropy in bits ($E = L \times \log_2(R)$).
- **One-Click Clipboard Copying**: Copies to Windows clipboard with visual confirmation using `pyperclip` (with a built-in Tkinter fallback).
- **Session History Panel**: Shows up to 5 recently generated passwords with individual quick-copy buttons and timestamps.
- **Seamless Regeneration**: Click "⚡ Generate Password" repeatedly without closing or resetting the application.

---

## 🛠 Technologies & Libraries Used

| Component | Library / Module | Purpose |
|---|---|---|
| **Programming Language** | Python 3.11+ | Core engine |
| **CSPRNG** | `secrets` (Standard Library) | Cryptographically secure random selection & shuffling |
| **Character Sets** | `string` (Standard Library) | Standard ASCII alphanumeric and punctuation sets |
| **Desktop GUI** | `tkinter` & `ttk` | Modern graphical desktop window and controls |
| **Clipboard** | `pyperclip` | Windows system clipboard integration |
| **Testing** | `unittest` | Automated verification test suite |

---

## 📂 Project Directory Structure

```
Random_Password_Generator_Advanced/
│
├── main.py                  # Tkinter GUI application, events, layout, history UI
├── password_generator.py    # Pure CSPRNG generation logic, strength scoring, entropy
├── test_pwd.py              # Automated test suite (8 test cases)
├── requirements.txt         # External dependencies (pyperclip)
├── README.md                # Comprehensive documentation & setup instructions
└── screenshots/             # Visual previews of the application
```

---

## 🚀 Installation & Setup Instructions

### 1. Verify Python Installation
```powershell
python --version
```

### 2. Navigate to Project Directory
```powershell
cd c:\Users\hp\Desktop\oasis\Random_Password_Generator_Advanced
```

### 3. Create & Activate Virtual Environment (Optional)
```powershell
python -m venv venv
venv\Scripts\activate
```

### 4. Install Dependencies
```powershell
pip install -r requirements.txt
```

---

## 🖥 How to Run the Application

```powershell
python main.py
```

### Run Automated Unit Tests
```powershell
python test_pwd.py
```

---

## 🎯 OASIS INFOBYTE Task Mapping

| Requirement Specified by OASIS | Implementation Status | Implementation Details |
|---|:---:|---|
| Modern Clean Interface | ✅ Completed | Built with custom TTK styles, responsive card containers, and color badges. |
| Title "Secure Password Generator" | ✅ Completed | Prominently displayed in the top application banner and window title. |
| Length Control (Slider / Spinbox) | ✅ Completed | Dual synchronized slider and numeric spinbox (range: 8–64, default: 16). |
| 4 Character Types (Upper, Lower, Num, Sym) | ✅ Completed | Checkboxes for each, with validation requiring $\ge 2$ selected. |
| Exclude Ambiguous Characters | ✅ Completed | Checkbox filters out `0, O, o, 1, l, I, \|, \`, ~, ;, :, ., ,` completely. |
| Cryptographically Secure (`secrets`) | ✅ Completed | Uses `secrets.choice()` and `secrets.SystemRandom().shuffle()`; no `random` module. |
| Guaranteed Character Inclusion | ✅ Completed | Guarantees representation from every active character pool. |
| Visual Strength Indicator | ✅ Completed | Dynamic colored progress bar + badge (Weak, Medium, Strong, Very Strong). |
| Copy to Clipboard | ✅ Completed | Powered by `pyperclip` with confirmation tooltip and messagebox. |
| Session Generation History | ✅ Completed | Displays last 5 passwords; in-memory only; wiped cleanly on exit. |
| Robust Error Handling | ✅ Completed | Comprehensive validation dialogs; prevents invalid inputs and zero crashes. |

---

## 🔮 Future Enhancements
- Passphrase generation mode using Diceware / EFF wordlists.
- Export batch passwords to encrypted `.zip` or password-protected PDF.
- HaveIBeenPwned API hash check (k-anonymity model) to flag previously breached passwords.
