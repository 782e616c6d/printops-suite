# 🖥️ Application Directory and Configuration Guide

---

## 📁 Directory Structure

### 🎨 The `.\Icons` Folder


*Figure 1: Visual representation of the application's icon asset storage.*

The `Icons` directory is responsible for storing application iconography and exists in two distinct locations:

* **Application Directory:** Located in the same directory as the application’s executable file.
* **APPDATA Directory:** Located within `%APPDATA%` acting as a backup copy of the original directory.

---

### 📄 The `.\Documents` Folder


*Figure 2: Storage path for user guides and administrative resources.*

Used to store user guides and other application-relevant materials.

> **Administrative Notice:** Items added to this folder can only be modified, removed, or added by OS administrators.

---

## ⚙️ Configuration Files

### 🖥️ `servers.json`

Defines the server endpoints and status settings for the application infrastructure.

```json
[
    {
        "name": "Local",
        "enabled": true,
        "ip": "127.0.0.1",
        "status": "Online",
        "qty": 1
    },
    {
        "name": "print-server.domain.com",
        "enabled": "enabled",
        "status": "status",
        "qty": "xx",
        "ip": "xxx.xxx.xxx.xxx"
    }
]

```

*Figure 3: Sample schema for server definitions.*

---

### 🎛️ `ui_tabs_config.json`

Controls the visibility and interactivity of the application's navigation tabs.

```json
{
    "nav_devices": "visible",
    "nav_local": "visible",
    "nav_drivers": "visible",
    "nav_tasks": "visible",
    "nav_sysinfo": "visible",
    "nav_guides": "visible",
    "nav_settings": "visible",
    "nav_about": "visible"
}

```

*Figure 4: User interface tab configuration settings.*

#### **Valid Options for Key Values**

| Option | Description |
| --- | --- |
| `"visible"` | Tab is visible and fully clickable. |
| `"disabled"` | Tab is visible but disabled. |
| `"hidden"` | Tab is completely hidden from the user interface. |
