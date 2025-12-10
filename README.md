# 🧰 Personal Productivity Suite (Python GUI)

A complete productivity application built using **Python (Tkinter)** with a clean modular architecture and persistent data storage.  
This suite includes a **Calculator**, **Notes Manager**, **Timer & Stopwatch**, **File Organizer**, **Unit Converter**, and **Backup & Restore System**—all integrated into a modern GUI dashboard.

---

# ✨ Features Overview

### 🖩 Calculator
- Perform basic arithmetic operations  
- Live expression evaluation  
- Error-safe operations  

### 📝 Notes Manager
- Create, edit, delete, and search notes  
- Notes saved in JSON format  
- Export notes to CSV or TXT  
- Auto-generated Note IDs and timestamps  

### ⏱ Timer & Stopwatch
- Countdown timer  
- Stopwatch with start/stop/reset  
- Tkinter-based popup windows  

### 📁 File Organizer
- Automatically organize files by extension  
- Creates folders like: *Images, Documents, Audio, Video, Others*  
- Safe file movement with error handling  

### 🔄 Backup & Restore System
- One-click backup  
- Backup folders include timestamps  
- Restore earlier data safely  
- Prevents accidental data loss  

### 🔧 Utility Module
- Reusable functions  
- Path validation  
- File system helpers  

---

# 🗂 Project Structure

```
project-folder/
│
├── main.py                # Main GUI launcher
├── calculator.py
├── notes_manager.py
├── timer.py
├── file_organizer.py
├── unit_converter.py
├── backup_manager.py
├── utils.py
│
├── data/
│   ├── notes.json
│   ├── calculator_log.csv
│   └── backups/
│
├── screenshots/
│
├── README.md
└── requirements.txt
```

---

# 🧱 Technical Requirements Fulfilled

| Requirement | Status |
|------------|--------|
| GUI Application | ✔ Tkinter modern UI |
| Modular Architecture | ✔ Separate Python modules |
| File Operations | ✔ JSON, CSV, TXT |
| Error Handling | ✔ Input validation everywhere |
| Data Persistence | ✔ Stored in `/data` folder |
| Backup & Restore | ✔ Timestamped folder backups |
| OOP Concepts | ✔ Classes used for tools |
| Utility Functions | ✔ In `utils.py` |
| User-friendly UI | ✔ Card-style dashboard |

---

# ▶️ Installation & Setup

### 1️⃣ Install Python  
Ensure **Python 3.8 or above** is installed.

### 2️⃣ Install Requirements
```
pip install -r requirements.txt
```

*(Most imports are built-in, so installation is nearly instant.)*

### 3️⃣ Run the Application
```
python main.py
```

---

# 📸 Screenshots  
Place your screenshots inside:

```
screenshots/
```

Then embed them in README like:

```
![App Dashboard](screenshots/dashboard.png)
![Notes Manager](screenshots/notes.png)
```

---

# 🛠 Troubleshooting Guide

### ❗ The app does not launch  
Run:
```
python main.py
```

### ❗ notes.json corrupted  
Delete `notes.json` — the app will recreate it.

### ❗ Backup not restoring  
Make sure your backup folder contains:
- `notes.json`  
- `calculator_log.csv` (if available)

### ❗ Tkinter not found (rare)  
Install Tkinter manually:
```
sudo apt-get install python3-tk
```

---

# 👨‍💻 Author  
Your Name  
B.Tech CSE – Cyber Security  
Year: 2025  

---

# 📜 License  
Free to use for academic and learning purposes.