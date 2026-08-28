About the .\Icons folder:

The Icons folder exists in two locations: in the same directory as the application’s executable file, and within %APPDATA%. It is responsible for storing the icon(s) for the main application.
The folder located in %APPDATA% is a backup copy of the original directory.

About the .\Documents folder:

The Documents folder is used to store user guides and other materials relevant to the application; items added to it can only be modified, removed, or added by OS administrators.

Regarding the “servers.json” configuration file:

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

Regarding the “ui_tabs_config.json” configuration file:

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

Valid options for each key: “visible” (Visible and clickable), ‘disabled’ (Visible but disabled), or “hidden” (Completely hidden).
