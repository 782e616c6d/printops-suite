<div align="center">
  <img src="https://img.icons8.com/color/120/000000/print.png" alt="Printer App Logo">
  <h1>🖨️ Printer App</h1>
  <p><em>Python solution for centralized management of local and network printers in Windows environments.</em></p>
  
  [![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
  [![PyQt6](https://img.shields.io/badge/GUI-PyQt6-brightgreen.svg?style=flat-square&logo=qt)](https://riverbankcomputing.com/software/pyqt/)
  [![Windows API](https://img.shields.io/badge/OS-Windows-0078D6.svg?style=flat-square&logo=windows&logoColor=white)](https://microsoft.com/)
  [![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](#)
</div>

---

## 📖 Table of Contents

1. [Overview](#-overview)
2. [Key Features](#-key-features)
3. [User Interface (UI)](#-user-interface-ui)
4. [Architecture and Modules](#-architecture-and-modules)
5. [Data Structure and Logs](#-data-structure-and-logs)
6. [Requirements and Installation](#-requirements-and-installation)

---

## 🚀 Overview

The **Printer App** is an advanced utility designed for system administrators and IT professionals who need to manage, monitor, and perform maintenance on physical and virtual printers. 

Leveraging the `win32print` library alongside a fluid `PyQt6`-based interface, the application offers native integration with the Windows _Spooler_, supporting everything from batch driver installation to forcibly clearing corrupted print queues.

> **💡 Note:** The application features a built-in internationalization (i18n) system, natively supporting English, Portuguese, Spanish, French, and Arabic.

---

## ✨ Key Features

*   🌐 **Network Device Management:** Smart mapping of corporate printers via IP or print server.
*   🔌 **Local Device Control:** Management of printers physically connected to the machine (USB/LPT).
*   📦 **Driver Visualization:** Listing of installed operating system driver packages and their respective paths.
*   🛠️ **Batch Actions:** 
    *   *Install/Remove* printers per machine or per user.
    *   *Purge Queues* for multiple printers simultaneously.
    *   *Print Test Pages* massively.
*   🔧 **Spooler Repair:** Automatic restart of the Windows spooler service and forced cleanup of corrupted temporary files (requires Administrator privileges).
*   📊 **Export and Logs:** Real-time auditing of performed actions and data export to `CSV` files.
*   📚 **Guides and Manuals:** Integrated PDF manual reader to streamline field support.

---

## 🖥️ User Interface (UI)

The interface utilizes modern `PyQt6` components inspired by Windows 11 **Fluent Design**, offering support for both Light and Dark themes. The layout is logically divided into navigation tabs:

### 📌 Main Navigation
| Icon | Section | Description |
|:---:|---|---|
| 📡 | **Network Devices** | Displays devices grouped by server, status, or manufacturer. |
| 🖨️ | **Installed Devices** | Shows devices currently mapped to the local host machine. |
| 📁 | **System Drivers** | Lists installed drivers and their architectural environments (e.g., x64). |
| 📋 | **Logs & Tasks** | History of all successful or failed actions performed in the app. |
| 💻 | **System Info** | Displays crucial data such as IP, RAM, User, and Local Hostname. |
| 📖 | **Guides & Manuals** | Management and viewing of PDF documentation files. |
| ⚙️ | **Settings** | Adjust theme, font, colors, auto-refresh intervals, and languages. |

> *The interface responds dynamically to printer selection, displaying a floating right panel with contextual quick actions.*

---

## 🏗️ Architecture and Modules

The code is structured in a modular and asynchronous manner, ensuring the interface remains responsive during network scans or communication with the Windows API.

### 🧵 Thread Management (`QThreadPool` and `QRunnable`)
Status retrieval and Spooler communication operations utilize `QRunnable`-based classes:
- `PrinterStatusWorker`: Fetches real-time printer status (Online, Jam, Offline).
- `ServerWorker`: Scans servers for shared printers.
- `DriverWorker`: Maps all drivers installed in the Registry/Spooler.

### 📦 Core Dependencies
- **`PyQt6`**: Graphical User Interface rendering.
- **`pywin32` (`win32print`, `pythoncom`)**: Low-level interaction with the Windows print subsystem.
- **`qtawesome`**: Provides the rich SVG icon library (FontAwesome/Material Design) for the UI.
- **`ctypes` / `subprocess`**: Execution of CMD commands (e.g., `net stop spooler` or `rundll32 printui.dll`) and privilege elevation.

---

## 📂 Data Structure and Logs

The application saves settings and history logs in the user's native Windows directory (`%APPDATA%`), keeping the executable's installation directory clean.

```text
📁 C:\Users\Username\AppData\Roaming\PrinterApp
 ├── 📄 printer_app.log              # Rotating log file (max 5MB)
 ├── 📄 user_preferences_config.json # Themes, fonts, and user preferences
 └── 📁 icons                        # Imported custom icons

📁 Executable Directory (Base)
 ├── 📄 servers.json                 # Tracked IP Servers list
 ├── 📄 ui_tabs_config.json          # Tab visibility settings (Admin)
 └── 📁 Documents                    # PDF Guides and Manuals
