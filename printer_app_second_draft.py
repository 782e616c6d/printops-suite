import sys
import os
import json
import subprocess
import winreg
import csv
import socket
import platform
import ctypes
import shutil
from datetime import datetime

# Verificação e importação de dependências
try:
    from PyQt6.QtWidgets import (
        QApplication,
        QMainWindow,
        QWidget,
        QVBoxLayout,
        QHBoxLayout,
        QLabel,
        QPushButton,
        QTableWidget,
        QTableWidgetItem,
        QHeaderView,
        QLineEdit,
        QMenu,
        QMessageBox,
        QAbstractItemView,
        QFrame,
        QInputDialog,
        QComboBox,
        QStackedWidget,
        QFormLayout,
        QScrollArea,
        QFileDialog,
        QStyledItemDelegate,
        QProgressBar,
        QListView,
        QCheckBox,
        QListWidget,
        QListWidgetItem,
        QTreeWidget,
        QTreeWidgetItem,
        QTreeWidgetItemIterator,
        QDialog,
        QSpinBox,
    )
    from PyQt6.QtCore import (
        Qt,
        QObject,
        pyqtSignal,
        QSize,
        QTimer,
        QLocale,
        QRunnable,
        QThreadPool,
        QUrl,
    )
    from PyQt6.QtGui import QFont, QAction, QIcon, QColor, QBrush, QFontDatabase, QDesktopServices
    import win32print
    import pythoncom
    import qtawesome as qta
except ImportError:
    import tkinter as tk
    from tkinter import messagebox

    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Dependências", "Instale: pip install PyQt6 pywin32 qtawesome")
    sys.exit()

# ================= SISTEMA DE IDIOMAS (i18n) =================
TRANSLATIONS = {
    "pt": {
        "app_title": "Printer App",
        "nav_devices": "Dispositivos de Rede",
        "nav_local": "Dispositivos Instalados",
        "nav_drivers": "Drivers do Sistema",
        "nav_tasks": "Logs e Tarefas",
        "nav_sysinfo": "Info. do Sistema",
        "nav_guides": "Guias e Manuais",
        "nav_settings": "Configurações",
        "nav_about": "Sobre",
        "search_ph": "Buscar dispositivos, drivers, ips...",
        "title_devices": "Dispositivos de Rede",
        "sub_devices": "Gestão de impressoras mapeadas e conexões corporativas",
        "title_local": "Dispositivos Instalados",
        "sub_local": "Dispositivos conectados fisicamente ou mapeados neste computador",
        "title_drivers": "Drivers do Sistema",
        "sub_drivers": "Pacotes de drivers de impressão instalados na máquina local",
        "title_tasks": "Logs e Tarefas",
        "sub_tasks": "Monitorização de ações em tempo real e status do aplicativo",
        "title_sysinfo": "Informações do Sistema",
        "sub_sysinfo": "Detalhes de hardware, rede e sistema operacional local",
        "title_guides": "Guias e Manuais",
        "sub_guides": "Documentação, manuais de impressoras e orientações de uso",
        "title_settings": "Configurações",
        "sub_settings": "Personalize a experiência e gerencie os servidores de impressão",
        "title_about": "Sobre o App",
        "sub_about": "Informações de desenvolvimento, links e atualizações",
        "card_sync": "Sincronizar",
        "card_sync_sub": "Atualizar lista da rede e local.",
        "card_map": "Mapear",
        "card_map_sub": "Adicionar dispositivo (IP/Caminho).",
        "card_repair": "Reparar Spooler",
        "card_repair_sub": "Reiniciar serviço e limpar a fila.",
        "card_export": "Exportar Dados",
        "card_export_sub": "Exportar lista de dispositivos.",
        "tree_all": "Todos os dispositivos",
        "tree_smart": "Filtros inteligentes",
        "tree_groups": "Servidores e Grupos",
        "tree_manufacturers": "Fabricantes",
        "tree_conn_types": "Tipos de Conexão",
        "status_all": "Todos os Status",
        "status_ok": "Prontas / OK",
        "status_warn": "Atenção / Erros",
        "status_off": "Offline",
        "server_all": "Todos os Servidores",
        "col_name": "Nome do nó / Modelo",
        "col_manufacturer": "Fabricante",
        "col_type": "Tipo",
        "col_driver": "Driver",
        "col_port": "Porta / IP",
        "col_server": "Servidor",
        "col_status": "Status",
        "col_installed": "Instalada",
        "col_env": "Ambiente",
        "col_path": "Caminho",
        "col_date": "Data / Hora",
        "col_action": "Ação",
        "col_details": "Detalhes",
        "col_active": "Ativo",
        "col_ip": "Endereço IP",
        "col_qty": "Qtd",
        "col_test": "Ação",
        "col_task_type": "Tipo de tarefa",
        "col_started": "Iniciado",
        "col_finished": "Concluído",
        "col_target": "Alvo",
        "ctx_copy": "Copiar",
        "ctx_test": "Imprimir Teste",
        "ctx_default": "Definir Padrão",
        "ctx_purge": "Limpar Fila",
        "ctx_props": "Propriedades",
        "ctx_reinstall": "Reinstalar",
        "ctx_remove": "Remover",
        "cfg_appearance": "Aparência e Idioma",
        "cfg_theme": "Tema Visual:",
        "cfg_color": "Cor de Destaque:",
        "cfg_lang": "Idioma do App:",
        "cfg_font": "Fonte do App:",
        "cfg_size": "Tamanho da Fonte:",
        "cfg_behavior": "Comportamento",
        "cfg_refresh": "Atualização Automática:",
        "cfg_servers": "Servidores de Impressão",
        "cfg_btn_add": "Adicionar",
        "cfg_btn_rem": "Remover Selecionado",
        "cfg_save": "Salvar Alterações",
        "msg_success": "Sucesso",
        "msg_error": "Erro",
        "msg_warning": "Aviso",
        "msg_info": "Info",
        "msg_ready": "Pronto.",
        "msg_syncing": "A varrer dispositivos...",
        "msg_sync_done": "Sincronização concluída.",
        "msg_install_batch_success": "As impressoras foram instaladas com sucesso.",
        "msg_test_batch_success": "Teste enviado para {count} dispositivos.",
        "msg_purge_batch_success": "Filas limpas para {count} dispositivos.",
        "msg_remove_batch_confirm": "Deseja remover as {count} conexões selecionadas?",
        "msg_remove_batch_success": "Conexões removidas com sucesso.",
        "msg_admin_req": "Executar como Administrador para esta ação.",
        "msg_spooler_warn": "O serviço de impressão será reiniciado e a fila limpa. Continuar?",
        "msg_install_mode": "Modo de instalação",
        "msg_install_machine": "Instalação por Máquina",
        "msg_install_user": "Instalação por Usuário",
        "msg_install_confirm": "Deseja prosseguir com a instalação de {count} dispositivo(s)?",
        "btn_clear_logs": "Limpar Histórico",
        "btn_export_logs": "Exportar Logs",
        "btn_test": "Testar",
        "btn_install": "Instalar",
        "btn_batch_test": "Imprimir Teste",
        "btn_batch_purge": "Limpar Filas",
        "btn_batch_remove": "Desinstalar",
        "btn_web_interface": "Interface Web",
        "btn_properties": "Detalhes e Propriedades",
        "btn_export_csv": "Exportar para CSV",
        "btn_add_pdf": "Anexar PDF",
        "btn_open_pdf": "Abrir Selecionado",
        "btn_rem_pdf": "Remover PDF",
        "chk_per_machine": "Instalar por Máquina",
        "cfg_icon_sidebar": "Ícone Principal:",
        "cfg_icon_custom": "Procurar Ficheiro...",
        "theme_system": "Sistema",
        "theme_light": "Claro",
        "theme_dark": "Escuro",
        "lang_sys": "Sistema",
        "color_blue": "Azul Win11",
        "color_green": "Verde Esmeralda",
        "color_purple": "Roxo Profundo",
        "color_gray": "Cinza Grafite",
        "ref_off": "Desligado",
        "ref_30s": "A cada 30 seg",
        "ref_60s": "A cada 1 min",
        "ref_300s": "A cada 5 min",
        "default_guide_name": "⭐ Manual de Utilização da Aplicação",
        "default_guide_desc": "Orientações padrão de uso do Printer App (Não removível)",
        "batch_actions": "Ações em lote",
        "filter_online": "Online",
        "filter_offline": "Offline",
        "filter_warn": "Atenção",
        "conn_network": "Rede",
        "conn_local": "Local",
        "msg_verifying": "A verificar...",
        "guide_welcome_title": "Guia de Abas do Printer App",
        "guide_welcome_text": "<b>1. Dispositivos de Rede:</b> Gerencie impressoras corporativas e mapeadas.<br><b>2. Dispositivos Instalados:</b> Impressoras conectadas diretamente na sua máquina.<br><b>3. Drivers do Sistema:</b> Visualize os pacotes de drivers instalados.<br><b>4. Logs e Tarefas:</b> Acompanhe o histórico de ações e erros.<br><b>5. Info. do Sistema:</b> Verifique dados de rede, IP e hardware.<br><b>6. Guias e Manuais:</b> Central de documentações e manuais.",
        "sysinfo_os": "Sistema Operacional:",
        "sysinfo_pc_name": "Nome do Computador:",
        "sysinfo_user": "Usuário Atual:",
        "sysinfo_ip": "Endereço IP (Local):",
        "sysinfo_ram": "Memória RAM:",
        "ram_free": "livre",
        "sys_unknown": "Desconhecido",
        "about_version": "Versão:",
        "about_desc": "Aplicativo profissional para gestão centralizada de impressoras locais e de rede. Construído com PyQt6 e win32print para oferecer máximo desempenho e integração nativa.",
        "about_modules": "Módulos utilizados:",
        "about_repo": "Repositório GitHub",
        "about_docs": "Documentação",
        "about_web": "Website Oficial",
        "about_check_updates": "Verificar Atualizações",
        "about_up_to_date": "Você já possui a versão mais recente.",
        "task_sync": "Sincronização",
        "task_settings": "Configurações",
        "task_conn_test": "Teste de Conexão",
        "task_install": "Instalação",
        "task_print_test": "Teste de Impressão",
        "task_purge_queues": "Limpar Filas",
        "task_purge_queue": "Limpar Fila",
        "task_remove": "Remoção",
        "task_remove_single": "Remover",
        "task_repair_spooler": "Reparar Spooler",
        "task_export_csv": "Exportar CSV",
        "task_test": "Teste",
        "target_all": "Todos",
        "target_sys": "Sistema",
        "target_dev_data": "Dados de Dispositivos",
        "target_devices": "Dispositivos",
        "msg_testing": "Testando...",
        "msg_loading_drivers": "A carregar drivers...",
        "msg_conn_failed": "{host} inacessível",
        "msg_conn_success": "{host} conectado ({count} dispositivos)",
        "msg_guide_no_rem": "O manual padrão não pode ser removido.",
        "msg_pdf_not_found": "O arquivo PDF não foi encontrado.",
        "msg_icon_copied": "Ícone personalizado copiado e aplicado com sucesso.",
        "msg_install_partial": "Instalação concluída com ressalvas.\n\nSucesso:\n{successes}\n\nFalhas:\n{errors}",
        "msg_install_fail": "Falha ao instalar as impressoras:\n\n{errors}",
        "msg_processing": "Processando {completed}/{total}",
        "msg_no_data_export": "Sem dados para exportar.",
        "msg_queue_purged_single": "Fila de '{printer}' limpa.",
        "msg_reinstall_success": "{printer} reinstalada com sucesso!",
        "msg_remove_single_confirm": "Deseja remover a conexão selecionada?",
    },
    "en": {
        "app_title": "Printer App",
        "nav_devices": "Network Devices",
        "nav_local": "Installed Devices",
        "nav_drivers": "System Drivers",
        "nav_tasks": "Logs & Tasks",
        "nav_sysinfo": "System Info",
        "nav_guides": "Guides & Manuals",
        "nav_settings": "Settings",
        "nav_about": "About",
        "search_ph": "Search devices, drivers, ips...",
        "title_devices": "Network Devices",
        "sub_devices": "Manage mapped printers and corporate connections",
        "title_local": "Installed Devices",
        "sub_local": "Locally connected or mapped devices on your machine",
        "title_drivers": "System Drivers",
        "sub_drivers": "Installed printer driver packages on this machine",
        "title_tasks": "Logs & Tasks",
        "sub_tasks": "Monitor real-time application actions and statuses",
        "title_sysinfo": "System Information",
        "sub_sysinfo": "Hardware, network, and local OS details",
        "title_guides": "Guides & Manuals",
        "sub_guides": "Documentation, printer manuals and usage guidelines",
        "title_settings": "Settings",
        "sub_settings": "Customize experience and manage print servers",
        "title_about": "About App",
        "sub_about": "Development info, links, and updates",
        "card_sync": "Sync Network",
        "card_sync_sub": "Scan network and local machine.",
        "card_map": "Map Printer",
        "card_map_sub": "Add a new device (IP/Path).",
        "card_repair": "Repair Spooler",
        "card_repair_sub": "Restart service and clear queue.",
        "card_export": "Export Data",
        "card_export_sub": "Export device list to CSV.",
        "tree_all": "All devices",
        "tree_smart": "Smart filters",
        "tree_groups": "Servers & Groups",
        "tree_manufacturers": "Manufacturers",
        "tree_conn_types": "Connection Types",
        "status_all": "All Statuses",
        "status_ok": "Ready / OK",
        "status_warn": "Warning / Errors",
        "status_off": "Offline",
        "server_all": "All Servers",
        "col_name": "Node / Model Name",
        "col_manufacturer": "Manufacturer",
        "col_type": "Connection Type",
        "col_driver": "Driver",
        "col_port": "Port / IP",
        "col_server": "Server",
        "col_status": "Status",
        "col_installed": "Installed",
        "col_env": "Environment",
        "col_path": "Path",
        "col_date": "Date / Time",
        "col_action": "Action",
        "col_details": "Details",
        "col_active": "Active",
        "col_ip": "IP Address",
        "col_qty": "Qty",
        "col_test": "Action",
        "col_task_type": "Task Type",
        "col_started": "Started",
        "col_finished": "Finished",
        "col_target": "Target",
        "ctx_copy": "Copy Value",
        "ctx_test": "Print Test Page",
        "ctx_default": "Set as Default",
        "ctx_purge": "Purge Queue",
        "ctx_props": "Properties",
        "ctx_reinstall": "Reinstall",
        "ctx_remove": "Remove",
        "cfg_appearance": "Appearance & Language",
        "cfg_theme": "Visual Theme:",
        "cfg_color": "Accent Color:",
        "cfg_lang": "App Language:",
        "cfg_font": "App Font:",
        "cfg_size": "Font Size:",
        "cfg_behavior": "Behavior",
        "cfg_refresh": "Auto-Refresh:",
        "cfg_servers": "Print Servers",
        "cfg_btn_add": "Add",
        "cfg_btn_rem": "Remove Selected",
        "cfg_save": "Save Changes",
        "msg_success": "Success",
        "msg_error": "Error",
        "msg_warning": "Warning",
        "msg_info": "Info",
        "msg_ready": "Ready.",
        "msg_syncing": "Scanning devices...",
        "msg_sync_done": "Sync successfully completed.",
        "msg_install_batch_success": "Printers installed successfully.",
        "msg_test_batch_success": "Test page sent to {count} devices.",
        "msg_purge_batch_success": "Queue purged for {count} devices.",
        "msg_remove_batch_confirm": "Do you really want to uninstall the {count} selected connections?",
        "msg_remove_batch_success": "Connections removed successfully.",
        "msg_admin_req": "Run as Administrator is required for this action.",
        "msg_spooler_warn": "The print spooler will be restarted and queues cleared. Continue?",
        "msg_install_mode": "Installation mode",
        "msg_install_machine": "Per Machine Installation",
        "msg_install_user": "Per User Installation",
        "msg_install_confirm": "Do you want to proceed with installing {count} device(s)?",
        "btn_clear_logs": "Clear History",
        "btn_export_logs": "Export Logs",
        "btn_test": "Test",
        "btn_install": "Install",
        "btn_batch_test": "Print Test",
        "btn_batch_purge": "Purge Queues",
        "btn_batch_remove": "Uninstall",
        "btn_web_interface": "Web Interface",
        "btn_properties": "Details & Properties",
        "btn_export_csv": "Export to CSV",
        "btn_add_pdf": "Attach PDF",
        "btn_open_pdf": "Open Selected",
        "btn_rem_pdf": "Remove PDF",
        "chk_per_machine": "Install Per Machine",
        "cfg_icon_sidebar": "Sidebar Icon Logo:",
        "cfg_icon_custom": "Custom (Image File)...",
        "theme_system": "System",
        "theme_light": "Light",
        "theme_dark": "Dark",
        "lang_sys": "System",
        "color_blue": "Win11 Blue",
        "color_green": "Emerald Green",
        "color_purple": "Deep Purple",
        "color_gray": "Graphite Gray",
        "ref_off": "Off",
        "ref_30s": "Every 30 sec",
        "ref_60s": "Every 1 min",
        "ref_300s": "Every 5 min",
        "default_guide_name": "⭐ Application User Manual",
        "default_guide_desc": "Standard usage guidelines for Printer App (Non-removable)",
        "batch_actions": "Batch Actions",
        "filter_online": "Online",
        "filter_offline": "Offline",
        "filter_warn": "Warning",
        "conn_network": "Network",
        "conn_local": "Local",
        "msg_verifying": "Verifying...",
        "guide_welcome_title": "Printer App Tabs Guide",
        "guide_welcome_text": "<b>1. Network Devices:</b> Manage mapped and corporate printers.<br><b>2. Installed Devices:</b> Printers physically connected to your machine.<br><b>3. System Drivers:</b> View installed driver packages.<br><b>4. Logs & Tasks:</b> Track the history of actions and errors.<br><b>5. System Info:</b> Check network, IP, and hardware data.<br><b>6. Guides & Manuals:</b> Documentation and manual center.",
        "sysinfo_os": "Operating System:",
        "sysinfo_pc_name": "Computer Name:",
        "sysinfo_user": "Current User:",
        "sysinfo_ip": "IP Address (Local):",
        "sysinfo_ram": "RAM Memory:",
        "ram_free": "free",
        "sys_unknown": "Unknown",
        "about_version": "Version:",
        "about_desc": "Professional application for centralized management of local and network printers. Built with PyQt6 and win32print to offer maximum performance and native integration.",
        "about_modules": "Modules used:",
        "about_repo": "GitHub Repository",
        "about_docs": "Documentation",
        "about_web": "Official Website",
        "about_check_updates": "Check for Updates",
        "about_up_to_date": "You already have the latest version.",
        "task_sync": "Synchronization",
        "task_settings": "Settings",
        "task_conn_test": "Connection Test",
        "task_install": "Installation",
        "task_print_test": "Print Test",
        "task_purge_queues": "Purge Queues",
        "task_purge_queue": "Purge Queue",
        "task_remove": "Removal",
        "task_remove_single": "Remove",
        "task_repair_spooler": "Repair Spooler",
        "task_export_csv": "Export CSV",
        "task_test": "Test",
        "target_all": "All",
        "target_sys": "System",
        "target_dev_data": "Device Data",
        "target_devices": "Devices",
        "msg_testing": "Testing...",
        "msg_loading_drivers": "Loading drivers...",
        "msg_conn_failed": "{host} unreachable",
        "msg_conn_success": "{host} connected ({count} devices)",
        "msg_guide_no_rem": "The default manual cannot be removed.",
        "msg_pdf_not_found": "The PDF file was not found.",
        "msg_icon_copied": "Custom icon copied and applied successfully.",
        "msg_install_partial": "Installation completed with warnings.\n\nSuccess:\n{successes}\n\nFailures:\n{errors}",
        "msg_install_fail": "Failed to install printers:\n\n{errors}",
        "msg_processing": "Processing {completed}/{total}",
        "msg_no_data_export": "No data to export.",
        "msg_queue_purged_single": "Queue for '{printer}' purged.",
        "msg_reinstall_success": "{printer} reinstalled successfully!",
        "msg_remove_single_confirm": "Do you want to remove the selected connection?",
    },
    "es": {
        "app_title": "Printer App",
        "nav_devices": "Dispositivos de Red",
        "nav_local": "Dispositivos Instalados",
        "nav_drivers": "Controladores",
        "nav_tasks": "Registros y Tareas",
        "nav_sysinfo": "Info. del Sistema",
        "nav_guides": "Guías y Manuales",
        "nav_settings": "Configuración",
        "nav_about": "Acerca de",
        "search_ph": "Buscar dispositivos, controladores...",
        "title_devices": "Dispositivos de Red",
        "sub_devices": "Gestión de impresoras mapeadas y conexiones",
        "title_local": "Dispositivos Instalados",
        "sub_local": "Dispositivos conectados físicamente o IP directo",
        "title_drivers": "Controladores del Sistema",
        "sub_drivers": "Paquetes de controladores instalados",
        "title_tasks": "Registros y Tareas",
        "sub_tasks": "Monitoriza acciones y estados de la aplicación",
        "title_sysinfo": "Información del Sistema",
        "sub_sysinfo": "Detalles del hardware, red y sistema",
        "title_guides": "Guías y Manuales",
        "sub_guides": "Documentación, manuales de impresoras y guías de uso",
        "title_settings": "Configuración",
        "sub_settings": "Personaliza la experiencia y servidores",
        "title_about": "Acerca de la App",
        "sub_about": "Información, enlaces y actualizaciones",
        "card_sync": "Sincronizar",
        "card_sync_sub": "Escanear red y máquina local.",
        "card_map": "Mapear",
        "card_map_sub": "Añadir dispositivo (IP/Ruta).",
        "card_repair": "Reparar Spooler",
        "card_repair_sub": "Reinicia el servicio y limpia la cola.",
        "card_export": "Exportar Datos",
        "card_export_sub": "Exporta la lista a un archivo CSV.",
        "tree_all": "Todos los dispositivos",
        "tree_smart": "Filtros inteligentes",
        "tree_groups": "Servidores y Grupos",
        "tree_manufacturers": "Fabricantes",
        "tree_conn_types": "Tipos de Conexión",
        "status_all": "Todos los Estados",
        "status_ok": "Listas / OK",
        "status_warn": "Atención / Errores",
        "status_off": "Desconectado",
        "server_all": "Todos los Servidores",
        "col_name": "Nombre de nodo / Modelo",
        "col_manufacturer": "Fabricante",
        "col_type": "Tipo de conexión",
        "col_driver": "Controlador",
        "col_port": "Puerto / IP",
        "col_server": "Servidor",
        "col_status": "Estado",
        "col_installed": "Instalada",
        "col_env": "Entorno",
        "col_path": "Ruta",
        "col_date": "Fecha / Hora",
        "col_action": "Acción",
        "col_details": "Detalles",
        "col_active": "Activo",
        "col_ip": "Dirección IP",
        "col_qty": "Cant",
        "col_test": "Acción",
        "col_task_type": "Tipo de tarea",
        "col_started": "Iniciado",
        "col_finished": "Concluido",
        "col_target": "Objetivo",
        "ctx_copy": "Copiar Valor",
        "ctx_test": "Imprimir Prueba",
        "ctx_default": "Predeterminada",
        "ctx_purge": "Limpiar Cola",
        "ctx_props": "Propiedades",
        "ctx_reinstall": "Reinstalar",
        "ctx_remove": "Quitar",
        "cfg_appearance": "Apariencia e Idioma",
        "cfg_theme": "Tema Visual:",
        "cfg_color": "Color de Acento:",
        "cfg_lang": "Idioma de la App:",
        "cfg_font": "Fuente de la App:",
        "cfg_size": "Tamaño de Fuente:",
        "cfg_behavior": "Comportamiento",
        "cfg_refresh": "Actualización Automática:",
        "cfg_servers": "Servidores de Impresión",
        "cfg_btn_add": "Añadir",
        "cfg_btn_rem": "Quitar Seleccionado",
        "cfg_save": "Guardar Cambios",
        "msg_success": "Éxito",
        "msg_error": "Error",
        "msg_warning": "Advertencia",
        "msg_info": "Info",
        "msg_ready": "Listo.",
        "msg_syncing": "Iniciando escaneo...",
        "msg_sync_done": "Sincronización completada.",
        "msg_install_batch_success": "Impresoras instaladas con éxito.",
        "msg_test_batch_success": "Prueba enviada a {count} dispositivos.",
        "msg_purge_batch_success": "Cola de impresión limpia para {count} dispositivos.",
        "msg_remove_batch_confirm": "¿Deseja desinstalar las {count} conexiones seleccionadas?",
        "msg_remove_batch_success": "Conexiones quitadas con éxito.",
        "msg_admin_req": "Ejecutar como Administrador es necesario para esta acción.",
        "msg_spooler_warn": "El servicio de impresión se reiniciará y se limpiará la cola. ¿Continuar?",
        "msg_install_mode": "Modo de instalación",
        "msg_install_machine": "Instalación por Máquina",
        "msg_install_user": "Instalación por Usuario",
        "msg_install_confirm": "¿Desea proceder con la instalación de {count} dispositivo(s)?",
        "btn_clear_logs": "Limpiar Historial",
        "btn_export_logs": "Exportar Registros",
        "btn_test": "Probar",
        "btn_install": "Instalar",
        "btn_batch_test": "Imprimir Prueba",
        "btn_batch_purge": "Limpiar Colas",
        "btn_batch_remove": "Desinstalar",
        "btn_web_interface": "Interfaz Web",
        "btn_properties": "Detalles y Propiedades",
        "btn_export_csv": "Exportar a CSV",
        "btn_add_pdf": "Adjuntar PDF",
        "btn_open_pdf": "Abrir Seleccionado",
        "btn_rem_pdf": "Quitar PDF",
        "chk_per_machine": "Instalación por Máquina",
        "cfg_icon_sidebar": "Icono Principal:",
        "cfg_icon_custom": "Buscar Archivo...",
        "theme_system": "Sistema",
        "theme_light": "Claro",
        "theme_dark": "Oscuro",
        "lang_sys": "Sistema",
        "color_blue": "Azul Win11",
        "color_green": "Verde Esmeralda",
        "color_purple": "Púrpura Profundo",
        "color_gray": "Gris Grafito",
        "ref_off": "Apagado",
        "ref_30s": "Cada 30 seg",
        "ref_60s": "Cada 1 min",
        "ref_300s": "Cada 5 min",
        "default_guide_name": "⭐ Manual de Usuario de la App",
        "default_guide_desc": "Guías de uso estándar para Printer App (No removible)",
        "batch_actions": "Acciones en lote",
        "filter_online": "En línea",
        "filter_offline": "Desconectado",
        "filter_warn": "Atención",
        "conn_network": "Red",
        "conn_local": "Local",
        "msg_verifying": "Verificando...",
        "guide_welcome_title": "Guía de Pestañas de Printer App",
        "guide_welcome_text": "<b>1. Dispositivos de Red:</b> Gestiona impresoras mapeadas y corporativas.<br><b>2. Dispositivos Instalados:</b> Impresoras conectadas directamente a su máquina.<br><b>3. Controladores:</b> Visualice los paquetes de controladores instalados.<br><b>4. Registros y Tareas:</b> Siga el historial de acciones y errores.<br><b>5. Info. del Sistema:</b> Verifique datos de red, IP y hardware.<br><b>6. Guías y Manuales:</b> Centro de documentación y manuales.",
        "sysinfo_os": "Sistema Operativo:",
        "sysinfo_pc_name": "Nombre del Equipo:",
        "sysinfo_user": "Usuario Actual:",
        "sysinfo_ip": "Dirección IP (Local):",
        "sysinfo_ram": "Memoria RAM:",
        "ram_free": "libre",
        "sys_unknown": "Desconocido",
        "about_version": "Versión:",
        "about_desc": "Aplicación profesional para la gestión centralizada de impresoras locales y de red. Construido con PyQt6 y win32print para ofrecer el máximo rendimiento e integración nativa.",
        "about_modules": "Módulos utilizados:",
        "about_repo": "Repositorio GitHub",
        "about_docs": "Documentación",
        "about_web": "Sitio Web Oficial",
        "about_check_updates": "Buscar Actualizaciones",
        "about_up_to_date": "Ya tienes la versión más reciente.",
        "task_sync": "Sincronización",
        "task_settings": "Configuraciones",
        "task_conn_test": "Prueba de Conexión",
        "task_install": "Instalación",
        "task_print_test": "Prueba de Impresión",
        "task_purge_queues": "Limpiar Colas",
        "task_purge_queue": "Limpiar Cola",
        "task_remove": "Remoción",
        "task_remove_single": "Remover",
        "task_repair_spooler": "Reparar Spooler",
        "task_export_csv": "Exportar CSV",
        "task_test": "Prueba",
        "target_all": "Todos",
        "target_sys": "Sistema",
        "target_dev_data": "Datos de Dispositivos",
        "target_devices": "Dispositivos",
        "msg_testing": "Probando...",
        "msg_loading_drivers": "Cargando controladores...",
        "msg_conn_failed": "{host} inaccesible",
        "msg_conn_success": "{host} conectado ({count} dispositivos)",
        "msg_guide_no_rem": "El manual predeterminado no se puede quitar.",
        "msg_pdf_not_found": "El archivo PDF no fue encontrado.",
        "msg_icon_copied": "Icono personalizado copiado y aplicado con éxito.",
        "msg_install_partial": "Instalación completada con advertencias.\n\nÉxito:\n{successes}\n\nFallos:\n{errors}",
        "msg_install_fail": "Fallo al instalar las impresoras:\n\n{errors}",
        "msg_processing": "Procesando {completed}/{total}",
        "msg_no_data_export": "No hay datos para exportar.",
        "msg_queue_purged_single": "Cola de '{printer}' limpia.",
        "msg_reinstall_success": "¡{printer} reinstalada con éxito!",
        "msg_remove_single_confirm": "¿Desea quitar la conexión seleccionada?",
    },
}

def get_os_language():
    try:
        os_lang = QLocale.system().name().lower()
        if "pt" in os_lang:
            return "pt"
        if "es" in os_lang:
            return "es"
        return "en"
    except:
        return "en"


CURRENT_LANG = "pt"


def tr(key):
    return TRANSLATIONS.get(CURRENT_LANG, TRANSLATIONS["pt"]).get(key, key)


def get_manufacturer(driver_name):
    if not driver_name or driver_name == "Desconhecido" or driver_name == tr("sys_unknown"):
        return tr("sys_unknown")

    name_upper = driver_name.upper()

    # Mapeamento avançado e exaustivo para identificação de fabricantes
    manufacturer_map = {
        "Kyocera": ["KYOCERA", "KX ", "KX(", "KX DRIVER", "FS-", "ECOSYS", "TASKALFA", " CS "],
        "FujiFilm / Fuji Xerox": ["FUJI XEROX", "FUJIFILM", "FF", "FX ", "APEOSPORT", "DOCUPRINT"],
        "Konica Minolta": ["KONICA", "BIZHUB", "MINOLTA", "ACCURIOPRINT", "C308", "C368", "C258", "MAGICOLOR", "PAGEPRO"],
        "Ricoh": ["RICOH", "AFICIO", "IM C", "MP C", "LANIER", "SAVIN", "GESTETNER", " MP "],
        "Xerox": ["XEROX", "PHASER", "VERSALINK", "ALTALINK", "WORKCENTRE", "DOCUCENTRE", "B210", "B225", "B230"],
        "HP": ["HP ", "HEWLETT-PACKARD", "HEWLETT PACKARD", "DESKJET", "LASERJET", "OFFICEJET", "DESIGNJET", "PAGEWIDE", "HP UNIVERSAL"],
        "Brother": ["BROTHER", "HL-", "MFC-", "DCP-", "QL-", "PT-"],
        "Epson": ["EPSON", "STYLUS", "ECOTANK", "WORKFORCE", "TM-", "SURECOLOR", "L1", "L3", "L4", "L5", "L8"],
        "Canon": ["CANON", "PIXMA", "IMAGECLASS", "IMAGERUNNER", "IMAGEPROGRAF", "LBP", "MAXIFY", "MF ", "IR "],
        "Lexmark": ["LEXMARK", "OPTRA", " CS", " CX", " MS", " MX"],
        "Samsung": ["SAMSUNG", "XPRESS", "PROXPRESS", "MULTIXPRESS", "ML-", "SCX-", "CLP-", "CLX-"],
        "Zebra": ["ZEBRA", "ZDESIGNER", "ZPL", "EPL", "GK420", "ZT230", "GX420"],
        "Toshiba": ["TOSHIBA", "E-STUDIO", "ESTUDIO"],
        "Sharp": ["SHARP", "MX-", "AR-", "AL-"],
        "Oki": ["OKI", "OKIDATA", "MICROLINE", "C-SERIES", "B-SERIES"],
        "Panasonic": ["PANASONIC", "KX-P", "KX-MB", "DP-"],
        "Dell": ["DELL"],
        "Pantum": ["PANTUM", "P2500", "M6500", "P2000", "M6000"],
        "Dymo": ["DYMO", "LABELWRITER", "LABELMANAGER"],
        "Star Micronics": ["STAR ", "TSP", "STAR MICRONICS"],
        "Sato": ["SATO", "CG4", "CL4NX"],
        "Datamax": ["DATAMAX", "O-NEIL"],
        "Microsoft": ["MICROSOFT", "ONENOTE", "XPS", "PDF", "FAX", "SEND TO"],
        "TSC": ["TSC "],
        "Nitro": ["NITRO"],
        "Foxit": ["FOXIT"],
        "Adobe": ["ADOBE"]
    }

    for manufacturer, keywords in manufacturer_map.items():
        if any(keyword in name_upper for keyword in keywords):
            return manufacturer

    # Fallback se não encontrar no dicionário
    parts = str(driver_name).split()
    if parts:
        first_word = parts[0].upper()
        if first_word == "KX":
            return "Kyocera"
        if first_word == "FX":
            return "FujiFilm / Fuji Xerox"
        return parts[0]
        
    return tr("sys_unknown")


# ================= UTILS E GESTÃO =================


def get_os_theme():
    try:
        registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        key = winreg.OpenKey(
            registry, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        )
        value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        return "theme_light" if value == 1 else "theme_dark"
    except:
        return "theme_light"


def get_ram_info():
    try:

        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]

        stat = MEMORYSTATUSEX()
        stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
        total_ram = stat.ullTotalPhys / (1024**3)
        avail_ram = stat.ullAvailPhys / (1024**3)
        return f"{total_ram:.1f} GB ({avail_ram:.1f} GB {tr('ram_free')})"
    except:
        return tr("sys_unknown")


class TaskLogger:
    logs = []
    callbacks = []

    @classmethod
    def log(cls, tipo_tarefa, status, alvo, start_time=None, end_time=None):
        if not start_time:
            start_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if not end_time:
            end_time = start_time
        cls.logs.insert(0, (tipo_tarefa, status, start_time, end_time, alvo))
        for cb in cls.callbacks:
            try:
                cb()
            except:
                pass


class ConfigManager:
    FILE_PATH = "printer_app_config.json"

    @classmethod
    def load(cls):
        defaults = {
            "theme": "theme_system",
            "primary_color": "#60CDFF",
            "font_family": "Segoe UI",
            "font_size": 10,
            "servers": [
                {
                    "name": "Local",
                    "enabled": True,
                    "ip": "127.0.0.1",
                    "status": "Online",
                    "qty": 0,
                }
            ],
            "language": "lang_sys",
            "auto_refresh": 0,
            "app_icon_type": "preset",
            "app_icon_val": "mdi6.flash",
            "custom_pdfs": [],
        }
        if os.path.exists(cls.FILE_PATH):
            try:
                with open(cls.FILE_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    defaults.update(data)
            except:
                pass
        return defaults

    @classmethod
    def save(cls, config_data):
        try:
            with open(cls.FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(config_data, f, indent=4)
        except Exception:
            pass


# ================= COMPONENTES VISUAIS =================


class PrinterPropertiesDialog(QDialog):
    def __init__(self, p_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Detalhes: {p_data.get('name', '')}")
        self.setMinimumSize(450, 400)
        layout = QVBoxLayout(self)

        h_header = QHBoxLayout()
        icon_lbl = QLabel()
        icon_lbl.setStyleSheet("background-color: transparent;")
        icon_lbl.setPixmap(
            qta.icon(
                "mdi6.printer", color=parent.accent_color if parent else "#60CDFF"
            ).pixmap(48, 48)
        )
        h_header.addWidget(icon_lbl, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(h_header)

        title = QLabel(f"<b>{p_data.get('name', '')}</b>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; background-color: transparent;")
        layout.addWidget(title)

        layout.addWidget(
            QFrame(frameShape=QFrame.Shape.HLine, frameShadow=QFrame.Shadow.Sunken)
        )

        form = QFormLayout()
        form.setSpacing(15)

        def L(t):
            l = QLabel(t)
            l.setStyleSheet("background-color: transparent;")
            return l

        form.addRow(L("<b>Nó Real / Path:</b>"), L(p_data.get("raw_name", "")))
        form.addRow(
            L("<b>Fabricante:</b>"), L(get_manufacturer(p_data.get("driver", "")))
        )
        form.addRow(L("<b>Driver em uso:</b>"), L(p_data.get("driver", "")))
        form.addRow(L("<b>Servidor / Host:</b>"), L(p_data.get("server", "")))
        form.addRow(L("<b>Porta / IP:</b>"), L(p_data.get("port", "")))

        self.lbl_status = L(str(p_data.get("status_code", 0)))
        form.addRow(L("<b>Código de Status:</b>"), self.lbl_status)

        layout.addLayout(form)
        layout.addStretch()

        h_btns = QHBoxLayout()
        btn_refresh = QPushButton("Atualizar Status")
        btn_refresh.setProperty("class", "StandardBtn")
        btn_refresh.clicked.connect(lambda: self.update_status(p_data))

        btn_close = QPushButton("Fechar")
        btn_close.setProperty("class", "PrimaryBtn")
        btn_close.clicked.connect(self.accept)

        h_btns.addStretch()
        h_btns.addWidget(btn_refresh)
        h_btns.addWidget(btn_close)
        layout.addLayout(h_btns)

    def update_status(self, p_data):
        self.lbl_status.setText(tr("msg_verifying"))
        QApplication.processEvents()
        try:
            handle = win32print.OpenPrinter(p_data.get("raw_name", ""))
            info = win32print.GetPrinter(handle, 2)
            win32print.ClosePrinter(handle)
            st = info.get("Status", 0)
            self.lbl_status.setText(
                f"{st} (Atualizado: {datetime.now().strftime('%H:%M:%S')})"
            )
        except Exception as e:
            self.lbl_status.setText(f"Erro ao obter status.")


class ActionCard(QFrame):
    clicked = pyqtSignal()

    def __init__(self, icon_name, title, subtitle, color):
        super().__init__()
        self.setProperty("class", "ActionCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(115)
        self.setMinimumWidth(180)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)
        top_layout = QHBoxLayout()
        self.icon_lbl = QLabel()
        self.icon_lbl.setStyleSheet("background-color: transparent; border: none;")
        self.icon_lbl.setPixmap(qta.icon(icon_name, color=color).pixmap(26, 26))
        self.icon_lbl.setFixedWidth(40)
        self.title_lbl = QLabel(title)
        self.title_lbl.setStyleSheet(
            "font-weight: bold; background-color: transparent;"
        )
        top_layout.addWidget(self.icon_lbl)
        top_layout.addWidget(self.title_lbl)
        top_layout.addStretch()
        self.sub_lbl = QLabel(subtitle)
        self.sub_lbl.setWordWrap(True)
        self.sub_lbl.setStyleSheet(
            "color: #888888; background-color: transparent; line-height: 1.2;"
        )
        self.sub_lbl.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        layout.addLayout(top_layout)
        layout.addWidget(self.sub_lbl)
        layout.addStretch()

    def set_texts(self, title, subtitle):
        self.title_lbl.setText(title)
        self.sub_lbl.setText(subtitle)

    def mouseReleaseEvent(self, event):
        self.clicked.emit()


class NavButton(QPushButton):
    def __init__(self, icon_name, text):
        super().__init__(f"  {text}")
        self.icon_name = icon_name
        self.setIcon(qta.icon(icon_name, color="#a0a0a0"))
        self.setIconSize(QSize(20, 20))
        self.setCheckable(True)
        self.setProperty("class", "NavButton")
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def update_style(self, text_color, accent_color, is_checked):
        icon_color = accent_color if is_checked else text_color
        self.setIcon(qta.icon(self.icon_name, color=icon_color))

    def update_text(self, text):
        self.setText(f"  {text}")


# ================= THREADS DE DADOS =================


class DefaultPrinterWorker(QRunnable):
    class Signals(QObject):
        result = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.signals = self.Signals()

    def run(self):
        pythoncom.CoInitialize()
        try:
            dp = win32print.GetDefaultPrinter()
        except:
            dp = ""
        self.signals.result.emit(dp)
        pythoncom.CoUninitialize()


class ServerWorkerSignals(QObject):
    result = pyqtSignal(list, dict, str)
    finished = pyqtSignal()


class ServerWorker(QRunnable):
    def __init__(self, server_obj):
        super().__init__()
        self.server_obj = server_obj
        self.signals = ServerWorkerSignals()

    def run(self):
        parsed = []
        name = self.server_obj["name"]
        if not self.server_obj.get("enabled", True):
            self.server_obj["status"] = "Desativado"
            self.signals.result.emit([], self.server_obj, "")
            self.signals.finished.emit()
            return

        try:
            self.server_obj["ip"] = (
                socket.gethostbyname(name) if name.lower() != "local" else "127.0.0.1"
            )
        except:
            self.server_obj["ip"] = "Desconhecido"

        pythoncom.CoInitialize()
        try:
            if name.lower() == "local":
                flags = (
                    win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
                )
                printers_raw = win32print.EnumPrinters(flags, None, 2)
            else:
                flags = win32print.PRINTER_ENUM_NAME
                printers_raw = win32print.EnumPrinters(flags, f"\\\\{name}", 2)

            for p in printers_raw:
                if not p:
                    continue
                if isinstance(p, dict):
                    p_name, port, driver, status_code = (
                        p.get("pPrinterName", "N/A"),
                        p.get("pPortName", "N/A"),
                        p.get("pDriverName", "N/A"),
                        p.get("Status", 0),
                    )
                else:
                    p_name, port, driver, status_code = (
                        str(p[1]),
                        str(p[3]),
                        str(p[4]),
                        (p[18] if len(p) > 18 else 0),
                    )

                clean_name = p_name
                if clean_name.startswith(f"\\\\{name}\\"):
                    clean_name = clean_name[len(f"\\\\{name}\\") :]
                elif clean_name.startswith("\\\\"):
                    clean_name = clean_name.split("\\")[-1]

                parsed.append(
                    {
                        "server": name,
                        "name": clean_name,
                        "driver": driver,
                        "port": port,
                        "status_code": status_code,
                        "raw_name": p_name,
                        "is_network": (
                            name.lower() != "local" or p_name.startswith("\\\\")
                        ),
                    }
                )

            self.server_obj["qty"] = len(parsed)
            self.server_obj["status"] = "Online"
            self.signals.result.emit(parsed, self.server_obj, "")
        except Exception as e:
            self.server_obj["qty"] = 0
            self.server_obj["status"] = "Offline"
            self.signals.result.emit([], self.server_obj, f"Erro: {str(e)}")
        finally:
            pythoncom.CoUninitialize()
            self.signals.finished.emit()


class DriverWorker(QRunnable):
    class Signals(QObject):
        result = pyqtSignal(list, str)

    def __init__(self):
        super().__init__()
        self.signals = self.Signals()

    def run(self):
        pythoncom.CoInitialize()
        try:
            drivers_raw = win32print.EnumPrinterDrivers(None, None, 2)
            parsed = []
            if drivers_raw:
                for d in drivers_raw:
                    if not d:
                        continue
                    if isinstance(d, dict):
                        parsed.append(
                            {
                                "name": d.get("Name", ""),
                                "env": d.get("Environment", ""),
                                "path": d.get("DriverPath", ""),
                            }
                        )
                    else:
                        parsed.append(
                            {"name": str(d[0]), "env": str(d[1]), "path": str(d[2])}
                        )
            self.signals.result.emit(parsed, "")
        except Exception as e:
            self.signals.result.emit([], str(e))
        finally:
            pythoncom.CoUninitialize()


# ================= JANELA PRINCIPAL =================


class PrinterManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = ConfigManager.load()
        self.setup_language()
        self.setWindowTitle(tr("app_title"))
        self.resize(1300, 850)
        self.setMinimumSize(1050, 700)

        self.all_printers_data = []
        self.default_printer = ""
        self.current_disp_filter = None
        self.current_inst_filter = None

        self.threadpool = QThreadPool.globalInstance()
        self.threadpool.setMaxThreadCount(20)
        self.auto_refresh_timer = QTimer(self)
        self.auto_refresh_timer.timeout.connect(self.refresh_all_data_silent)

        theme_val = self.config.get("theme", "theme_system")
        if theme_val == "theme_system":
            theme_val = get_os_theme()
        self.text_main = "#ffffff" if theme_val == "theme_dark" else "#1a1a1a"
        self.accent_color = self.config.get("primary_color", "#60CDFF")

        self.setup_ui()
        self.apply_fluent_theme()
        self.retranslate_ui()
        self.update_timer_settings()

        TaskLogger.callbacks.append(self.refresh_tarefas_table)
        QTimer.singleShot(100, self.refresh_all_data)

    def setup_language(self):
        global CURRENT_LANG
        CURRENT_LANG = self.config.get("language", "pt")
        if CURRENT_LANG == "lang_sys":
            CURRENT_LANG = get_os_language()
        if CURRENT_LANG not in TRANSLATIONS:
            CURRENT_LANG = "en"

    def update_timer_settings(self):
        interval = int(self.config.get("auto_refresh", 0))
        if interval > 0:
            self.auto_refresh_timer.start(interval * 1000)
        else:
            self.auto_refresh_timer.stop()

    def update_status(self, message):
        self.status_lbl.setText(message)

    def show_progress(self, show=True):
        if show:
            self.progress_bar.show()
            self.progress_bar.setRange(0, 0)
        else:
            self.progress_bar.hide()

    def update_progress(self, current, total, message):
        self.update_status(message)
        if total > 0:
            self.progress_bar.show()
            self.progress_bar.setMaximum(total)
            self.progress_bar.setValue(current)
            if current >= total:
                QTimer.singleShot(1500, self.progress_bar.hide)
        else:
            self.progress_bar.hide()

    def apply_fluent_theme(self):
        font_family = self.config.get("font_family", "Segoe UI")
        try:
            font_size = int(self.config.get("font_size", 10))
        except:
            font_size = 10
        if font_size < 8:
            font_size = 10

        font_str = f"'{font_family}', Arial, sans-serif"
        font = QFont(font_family, font_size)
        QApplication.instance().setFont(font)
        self.setFont(font)

        theme = self.config["theme"]
        if theme == "theme_system":
            theme = get_os_theme()
        self.accent_color = self.config["primary_color"]

        if theme == "theme_dark":
            self.bg_main, bg_card, bg_card_hover, border = (
                "#202020",
                "#2d2d2d",
                "#323232",
                "#3a3a3a",
            )
            self.text_main, text_muted, nav_hover, nav_selected = (
                "#ffffff",
                "#a0a0a0",
                "#333333",
                "#333333",
            )
            input_bg, header_bg, list_hover, progress_bg = (
                "#2d2d2d",
                "#202020",
                "#3f3f46",
                "#3a3a3a",
            )
            self.panel_bg = "#252525"
        else:
            self.bg_main, bg_card, bg_card_hover, border = (
                "#f3f3f3",
                "#ffffff",
                "#f9f9f9",
                "#e5e5e5",
            )
            self.text_main, text_muted, nav_hover, nav_selected = (
                "#1a1a1a",
                "#666666",
                "#e0e0e0",
                "#eaeaea",
            )
            input_bg, header_bg, list_hover, progress_bg = (
                "#ffffff",
                "#f3f3f3",
                "#e5e5e5",
                "#e5e5e5",
            )
            self.panel_bg = "#fafafa"

        for btn in getattr(self, "nav_buttons", []):
            btn.update_style(self.text_main, self.accent_color, btn.isChecked())

        stylesheet = f"""
            QMainWindow, QWidget, QDialog {{ background-color: {self.bg_main}; color: {self.text_main}; font-family: {font_str}; font-size: {font_size}pt; }}
            QLabel, QCheckBox, QRadioButton {{ background-color: transparent; }}
            
            #Sidebar {{ background-color: transparent; border-right: 1px solid {border}; }}
            #SidePanelRight {{ background-color: {self.panel_bg}; border-left: 1px solid {border}; }}
            
            QPushButton.NavButton {{ background-color: transparent; text-align: left; padding: 10px 15px; border-radius: 6px; border: none; font-weight: normal; margin-bottom: 2px; }}
            QPushButton.NavButton:hover {{ background-color: {nav_hover}; }}
            QPushButton.NavButton:checked {{ background-color: {nav_selected}; border-left: 4px solid {self.accent_color}; border-top-left-radius: 0px; border-bottom-left-radius: 0px; font-weight: bold; }}
            
            QFrame.ActionCard {{ background-color: {bg_card}; border: 1px solid {border}; border-radius: 8px; }}
            QFrame.ActionCard:hover {{ background-color: {bg_card_hover}; }}
            
            QMenu {{ background-color: {bg_card}; color: {self.text_main}; border: 1px solid {border}; border-radius: 6px; padding: 4px; }}
            QMenu::item {{ background-color: transparent; color: {self.text_main}; padding: 6px 24px 6px 24px; border-radius: 4px; margin: 2px; }}
            QMenu::item:selected {{ background-color: {list_hover}; }}
            
            QLineEdit#SearchBar {{ background-color: {input_bg}; border: 1px solid {border}; border-radius: 18px; padding: 6px 15px 6px 35px; color: {self.text_main}; }}
            QLineEdit#SearchBar:focus {{ border: 1px solid {self.accent_color}; }}
            
            QLineEdit, QSpinBox, QComboBox, QFontComboBox {{ background-color: {input_bg}; border: 1px solid {border}; border-radius: 4px; padding: 6px; color: {self.text_main}; }}
            QComboBox::drop-down, QSpinBox::up-button, QSpinBox::down-button {{ width: 25px; border: none; background: transparent; }}
            
            QComboBox QAbstractItemView, QListView, QListWidget {{ background-color: {input_bg}; color: {self.text_main}; border: 1px solid {border}; selection-background-color: {self.accent_color}; selection-color: #000; outline: none; }}
            QComboBox QAbstractItemView::item, QListView::item, QListWidget::item {{ background-color: transparent; color: {self.text_main}; padding: 8px; min-height: 25px; border-radius: 4px; }}
            QComboBox QAbstractItemView::item:selected, QListView::item:selected, QListWidget::item:selected {{ background-color: {self.accent_color}; color: #000; }}
            
            QPushButton.StandardBtn {{ background-color: {bg_card}; border: 1px solid {border}; border-radius: 6px; padding: 6px 12px; font-family: {font_str}; font-size: {font_size}pt; }}
            QPushButton.StandardBtn:hover {{ background-color: {nav_hover}; }}
            QPushButton.StandardBtn:pressed {{ background-color: {list_hover}; padding-top: 8px; padding-bottom: 4px; }}
            QPushButton.StandardBtn:disabled {{ color: {text_muted}; background-color: transparent; border-color: {border}; opacity: 0.4; }}
            
            QPushButton.PrimaryBtn {{ background-color: {self.accent_color}; color: #000000; font-weight: bold; border: none; border-radius: 6px; padding: 8px 20px; font-family: {font_str}; font-size: {font_size}pt; }}
            QPushButton.PrimaryBtn:hover {{ opacity: 0.85; }}
            QPushButton.PrimaryBtn:pressed {{ padding-top: 10px; padding-bottom: 6px; }}
            QPushButton.PrimaryBtn:disabled {{ background-color: {progress_bg}; color: #888888; opacity: 0.5; }}
            
            QPushButton.PanelActionBtn {{ background-color: transparent; text-align: left; padding: 8px 10px; border: none; border-radius: 4px; color: {self.text_main}; font-family: {font_str}; font-size: {font_size}pt; }}
            QPushButton.PanelActionBtn:hover {{ background-color: {nav_hover}; }}
            
            QTreeWidget#SidebarTree {{ background-color: transparent; border: none; margin-left: 5px; color: {text_muted}; }}
            QTreeWidget#SidebarTree::item {{ padding: 6px; border-radius: 4px; }}
            QTreeWidget#SidebarTree::item:hover {{ background-color: {nav_hover}; color: {self.text_main}; }}
            QTreeWidget#SidebarTree::item:selected {{ background-color: {list_hover}; color: {self.text_main}; font-weight: bold; }}
            
            QTableWidget {{ background-color: transparent; border: none; outline: none; }}
            QTableWidget::item {{ padding: 5px; border-bottom: 1px solid {border}; }}
            QTableWidget::item:selected {{ background-color: {list_hover}; border-radius: 4px; }}
            QHeaderView::section {{ background-color: {header_bg}; border: none; border-bottom: 1px solid {border}; padding: 10px; color: {text_muted}; font-weight: bold; text-align: center; }}
            
            QScrollBar:vertical {{ border: none; background: transparent; width: 10px; margin: 0px; }}
            QScrollBar::handle:vertical {{ background: {text_muted}; min-height: 30px; border-radius: 5px; }}
            QScrollBar::handle:vertical:hover {{ background: {self.accent_color}; }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ border: none; background: none; height: 0px; }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{ background: none; }}
            
            QScrollBar:horizontal {{ border: none; background: transparent; height: 10px; margin: 0px; }}
            QScrollBar::handle:horizontal {{ background: {text_muted}; min-width: 30px; border-radius: 5px; }}
            QScrollBar::handle:horizontal:hover {{ background: {self.accent_color}; }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ border: none; background: none; width: 0px; }}
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{ background: none; }}
        """
        self.setStyleSheet(stylesheet)

        for c in [
            self.cmb_status,
            self.cmb_server,
            self.cfg_lang,
            self.cfg_theme,
            self.cfg_color,
            self.cfg_refresh,
            getattr(self, "cfg_logo_icon", None),
            getattr(self, "cfg_font", None),
        ]:
            if hasattr(c, "view") and c.view():
                c.view().window().setWindowFlags(
                    Qt.WindowType.Popup
                    | Qt.WindowType.FramelessWindowHint
                    | Qt.WindowType.NoDropShadowWindowHint
                )
                c.view().setStyleSheet(
                    f"background-color: {input_bg}; color: {self.text_main}; border: 1px solid {border}; outline: none;"
                )
                
        # Força os ícones e textos estáticos a recarregarem
        self.retranslate_ui()
        self.update_sidebar_logo()

    def update_sidebar_logo(self):
        icon_val = self.config.get("app_icon_val", "mdi6.flash")
        if "mdi6." in icon_val:
            self.lbl_app_logo.setPixmap(
                qta.icon(icon_val, color=self.accent_color).pixmap(24, 24)
            )
        else:
            self.lbl_app_logo.setPixmap(
                QIcon(icon_val).pixmap(24, 24)
                if os.path.exists(icon_val)
                else qta.icon("mdi6.flash", color=self.accent_color).pixmap(24, 24)
            )

    def create_centered_item(self, text, tooltip=None, user_data=None):
        item = QTableWidgetItem(str(text))
        item.setTextAlignment(
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter
        )
        item.setToolTip(str(tooltip) if tooltip else str(text))
        if user_data is not None:
            item.setData(Qt.ItemDataRole.UserRole, user_data)
        return item

    def create_page_header(self, title_key, subtitle_key):
        header = QWidget()
        h_layout = QVBoxLayout(header)
        h_layout.setContentsMargins(0, 0, 0, 15)
        lbl_sub = QLabel()
        lbl_sub.setStyleSheet("color: #a0a0a0;")
        lbl_title = QLabel()
        lbl_title.setStyleSheet("font-weight: bold; font-size: 24px;")
        h_layout.addWidget(lbl_sub)
        h_layout.addWidget(lbl_title)
        setattr(self, f"hdr_title_{title_key}", lbl_title)
        setattr(self, f"hdr_sub_{subtitle_key}", lbl_sub)
        return header

    def configure_table_headers(self, table):
        header = table.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

    def adjust_tree_height(self, tree):
        count = 0
        it = QTreeWidgetItemIterator(tree)
        while it.value():
            item = it.value()
            if not item.isHidden():
                parent = item.parent()
                if parent is None or parent.isExpanded():
                    count += 1
            it += 1
        tree.setMinimumHeight(count * 32 + 10)

    def sync_table_selection(self, table, prefix):
        selected_rows = set(item.row() for item in table.selectedItems())
        table.blockSignals(True)
        for row in range(table.rowCount()):
            chk_w = table.cellWidget(row, 0)
            if chk_w:
                chk = chk_w.layout().itemAt(0).widget()
                if chk.isEnabled():
                    chk.blockSignals(True)
                    chk.setChecked(row in selected_rows)
                    chk.blockSignals(False)
        table.blockSignals(False)
        self.update_global_right_panel()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Status Bar
        self.status_bar = self.statusBar()
        self.status_lbl = QLabel(tr("msg_ready"))
        self.status_bar.addWidget(self.status_lbl)
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(250)
        self.progress_bar.setFixedHeight(6)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.hide()
        self.status_bar.addPermanentWidget(self.progress_bar)

        # Sidebar Left
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(260)
        side_layout = QVBoxLayout(self.sidebar)
        side_layout.setContentsMargins(0, 0, 0, 0)
        side_layout.setSpacing(0)

        top_side_widget = QWidget()
        top_side_layout = QVBoxLayout(top_side_widget)
        top_side_layout.setContentsMargins(15, 20, 15, 10)

        self.logo_layout = QHBoxLayout()
        self.lbl_app_logo = QLabel()
        self.lbl_app_logo.setStyleSheet("background-color: transparent;")
        self.lbl_app_logo.setFixedSize(24, 24)
        self.lbl_app_title = QLabel()
        self.lbl_app_title.setStyleSheet(
            "font-weight: bold; font-size: 16px; background-color: transparent;"
        )
        self.logo_layout.addWidget(self.lbl_app_logo)
        self.logo_layout.addWidget(self.lbl_app_title)
        self.logo_layout.addStretch()
        top_side_layout.addLayout(self.logo_layout)
        side_layout.addWidget(top_side_widget)

        scroll_nav = QScrollArea()
        scroll_nav.setWidgetResizable(True)
        scroll_nav.setFrameShape(QFrame.Shape.NoFrame)
        scroll_nav.setStyleSheet("background-color: transparent; border: none;")

        nav_content = QWidget()
        self.nav_layout = QVBoxLayout(nav_content)
        self.nav_layout.setContentsMargins(15, 0, 15, 10)
        self.nav_layout.setSpacing(5)

        self.btn_nav_devices = NavButton("mdi6.monitor-share", "")
        self.tree_nav_devices = QTreeWidget()
        self.tree_nav_devices.setObjectName("SidebarTree")
        self.tree_nav_devices.setHeaderHidden(True)
        self.tree_nav_devices.itemClicked.connect(self.on_disp_tree_clicked)
        self.tree_nav_devices.itemExpanded.connect(
            lambda _: self.adjust_tree_height(self.tree_nav_devices)
        )
        self.tree_nav_devices.itemCollapsed.connect(
            lambda _: self.adjust_tree_height(self.tree_nav_devices)
        )

        self.btn_nav_local = NavButton("mdi6.printer-pos", "")
        self.tree_nav_local = QTreeWidget()
        self.tree_nav_local.setObjectName("SidebarTree")
        self.tree_nav_local.setHeaderHidden(True)
        self.tree_nav_local.itemClicked.connect(self.on_inst_tree_clicked)
        self.tree_nav_local.itemExpanded.connect(
            lambda _: self.adjust_tree_height(self.tree_nav_local)
        )
        self.tree_nav_local.itemCollapsed.connect(
            lambda _: self.adjust_tree_height(self.tree_nav_local)
        )

        self.btn_nav_drivers = NavButton("mdi6.folder-zip-outline", "")
        self.btn_nav_tasks = NavButton("mdi6.text-box-outline", "")
        self.btn_nav_sysinfo = NavButton("mdi6.information-outline", "")
        self.btn_nav_guides = NavButton("mdi6.book-open-page-variant", "")

        self.nav_buttons = [
            self.btn_nav_devices,
            self.btn_nav_local,
            self.btn_nav_drivers,
            self.btn_nav_tasks,
            self.btn_nav_sysinfo,
            self.btn_nav_guides,
        ]

        self.nav_layout.addWidget(self.btn_nav_devices)
        self.nav_layout.addWidget(self.tree_nav_devices)
        self.nav_layout.addWidget(self.btn_nav_local)
        self.nav_layout.addWidget(self.tree_nav_local)
        self.nav_layout.addWidget(self.btn_nav_drivers)
        self.nav_layout.addWidget(self.btn_nav_tasks)
        self.nav_layout.addWidget(self.btn_nav_sysinfo)
        self.nav_layout.addWidget(self.btn_nav_guides)

        for i, btn in enumerate(self.nav_buttons):
            btn.clicked.connect(lambda checked, idx=i: self.switch_tab(idx))

        self.nav_layout.addStretch()
        scroll_nav.setWidget(nav_content)
        side_layout.addWidget(scroll_nav)

        bottom_side_widget = QWidget()
        bottom_side_layout = QVBoxLayout(bottom_side_widget)
        bottom_side_layout.setContentsMargins(15, 10, 15, 15)
        bottom_side_layout.setSpacing(5)

        self.btn_settings = NavButton("mdi6.cog-outline", "")
        self.btn_settings.clicked.connect(lambda: self.switch_tab(len(self.nav_buttons)-2))
        self.btn_about = NavButton("mdi6.help-circle-outline", "")
        self.btn_about.clicked.connect(lambda: self.switch_tab(len(self.nav_buttons)-1))

        bottom_side_layout.addWidget(self.btn_settings)
        bottom_side_layout.addWidget(self.btn_about)
        self.nav_buttons.extend([self.btn_settings, self.btn_about])

        side_layout.addWidget(bottom_side_widget)
        main_layout.addWidget(self.sidebar)

        self.right_panel = self.create_global_right_panel()

        content_wrapper = QWidget()
        content_layout = QVBoxLayout(content_wrapper)
        content_layout.setContentsMargins(0, 15, 0, 0)

        top_bar = QWidget()
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(30, 0, 30, 10)
        top_layout.addStretch()
        self.search_box = QLineEdit()
        self.search_box.setObjectName("SearchBar")
        self.search_box.setFixedWidth(400)
        self.search_box.textChanged.connect(self.global_search)
        self.search_box.addAction(
            qta.icon("mdi6.magnify", color="#a0a0a0"),
            QLineEdit.ActionPosition.LeadingPosition,
        )
        top_layout.addWidget(self.search_box)
        top_layout.addStretch()
        content_layout.addWidget(top_bar)

        (
            self.cmb_status,
            self.cmb_server,
            self.cfg_lang,
            self.cfg_theme,
            self.cfg_color,
            self.cfg_refresh,
            self.cfg_logo_icon,
        ) = [QComboBox() for _ in range(7)]
        self.cfg_font = QComboBox()
        self.cfg_font_size = QSpinBox()
        self.cfg_font_size.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
        self.cfg_font_size.setRange(8, 72)

        for c in [
            self.cmb_status,
            self.cmb_server,
            self.cfg_lang,
            self.cfg_theme,
            self.cfg_color,
            self.cfg_refresh,
            self.cfg_logo_icon,
            self.cfg_font,
        ]:
            c.setView(QListView())
            c.setItemDelegate(QStyledItemDelegate())
            c.setFixedWidth(250)

        self.cfg_font_size.setFixedWidth(250)

        self.stacked = QStackedWidget()
        content_layout.addWidget(self.stacked)

        self.build_page_dispositivos()
        self.build_page_instaladas()
        self.build_page_drivers()
        self.build_page_tarefas()
        self.build_page_sysinfo()
        self.build_page_guides()
        self.build_page_configuracoes()
        self.build_page_about()

        main_layout.addWidget(content_wrapper, stretch=1)
        main_layout.addWidget(self.right_panel)
        self.switch_tab(0)

    def switch_tab(self, index):
        for i, btn in enumerate(self.nav_buttons):
            is_checked = i == index
            btn.setChecked(is_checked)
            btn.update_style(self.text_main, self.accent_color, is_checked)

        self.tree_nav_devices.setVisible(index == 0)
        self.tree_nav_local.setVisible(index == 1)

        self.stacked.setCurrentIndex(index)
        self.search_box.clear()

        if index == 0:
            self.filter_table_view()
        elif index == 1:
            self.refresh_local_only()
        elif index == 2:
            self.refresh_drivers()
        elif index == 5:
            self.refresh_guides()
        elif index == 6:
            self.refresh_settings_servers_table()

        self.update_global_right_panel()

    def populate_disp_tree(self):
        self.tree_nav_devices.clear()
        root = QTreeWidgetItem([tr("tree_all")])
        root.setIcon(0, qta.icon("mdi6.apps", color=self.accent_color))

        filtros = QTreeWidgetItem([tr("tree_smart")])
        filtros.setIcon(0, qta.icon("mdi6.filter-variant", color=self.text_main))
        for f in [tr("filter_online"), tr("filter_offline"), tr("filter_warn")]:
            filtros.addChild(QTreeWidgetItem([f]))

        grupos = QTreeWidgetItem([tr("tree_groups")])
        grupos.setIcon(0, qta.icon("mdi6.server-network", color=self.text_main))
        servers = set(
            p["server"] for p in self.all_printers_data if p["server"] != "Local"
        )
        for s in sorted(list(servers)):
            grupos.addChild(QTreeWidgetItem([s]))

        fabricantes = QTreeWidgetItem([tr("tree_manufacturers")])
        fabricantes.setIcon(0, qta.icon("mdi6.factory", color=self.text_main))
        mans = set(
            get_manufacturer(p["driver"])
            for p in self.all_printers_data
            if p["server"] != "Local"
        )
        for m in sorted(list(mans)):
            fabricantes.addChild(QTreeWidgetItem([m]))

        self.tree_nav_devices.addTopLevelItems([root, filtros, grupos, fabricantes])
        self.tree_nav_devices.expandAll()
        QTimer.singleShot(50, lambda: self.adjust_tree_height(self.tree_nav_devices))

    def populate_inst_tree(self):
        self.tree_nav_local.clear()
        root = QTreeWidgetItem([tr("tree_all")])
        root.setIcon(0, qta.icon("mdi6.apps", color=self.accent_color))
        tipos = QTreeWidgetItem([tr("tree_conn_types")])
        tipos.setIcon(0, qta.icon("mdi6.connection", color=self.text_main))
        for f in [tr("conn_network"), tr("conn_local")]:
            tipos.addChild(QTreeWidgetItem([f]))

        fabricantes = QTreeWidgetItem([tr("tree_manufacturers")])
        fabricantes.setIcon(0, qta.icon("mdi6.factory", color=self.text_main))
        mans = set(
            get_manufacturer(p["driver"])
            for p in self.all_printers_data
            if p["server"] == "Local" or not p["is_network"]
        )
        for m in sorted(list(mans)):
            fabricantes.addChild(QTreeWidgetItem([m]))

        self.tree_nav_local.addTopLevelItems([root, tipos, fabricantes])
        self.tree_nav_local.expandAll()
        QTimer.singleShot(50, lambda: self.adjust_tree_height(self.tree_nav_local))

    def on_disp_tree_clicked(self, item, column):
        parent = item.parent()
        if parent is None:
            if item.text(0) == tr("tree_all"):
                self.current_disp_filter = None
            else:
                return
        else:
            p_text = parent.text(0)
            if p_text == tr("tree_smart"):
                self.current_disp_filter = {"type": "status", "val": item.text(0)}
            elif p_text == tr("tree_groups"):
                self.current_disp_filter = {"type": "server", "val": item.text(0)}
            elif p_text == tr("tree_manufacturers"):
                self.current_disp_filter = {"type": "manufacturer", "val": item.text(0)}
        self.filter_table_view()

    def on_inst_tree_clicked(self, item, column):
        parent = item.parent()
        if parent is None:
            if item.text(0) == tr("tree_all"):
                self.current_inst_filter = None
            else:
                return
        else:
            p_text = parent.text(0)
            if p_text == tr("tree_conn_types"):
                self.current_inst_filter = {"type": "conn", "val": item.text(0)}
            elif p_text == tr("tree_manufacturers"):
                self.current_inst_filter = {"type": "manufacturer", "val": item.text(0)}
        self.refresh_local_only()

    def create_global_right_panel(self):
        panel = QFrame()
        panel.setObjectName("SidePanelRight")
        panel.setFixedWidth(280)
        panel.hide()
        layout = QVBoxLayout(panel)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(15, 25, 15, 20)

        self.rp_icon = QLabel()
        self.rp_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rp_title = QLabel()
        self.rp_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rp_title.setStyleSheet("font-weight: bold; font-size: 15px;")
        self.rp_title.setWordWrap(True)
        self.rp_sub = QLabel()
        self.rp_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rp_sub.setStyleSheet("color: #888;")

        layout.addWidget(self.rp_icon, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.rp_title, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.rp_sub, alignment=Qt.AlignmentFlag.AlignCenter)

        self.btn_rp_props = QPushButton()
        self.btn_rp_props.setProperty("class", "StandardBtn")
        layout.addWidget(self.btn_rp_props)
        layout.addSpacing(10)
        layout.addWidget(
            QFrame(frameShape=QFrame.Shape.HLine, frameShadow=QFrame.Shadow.Sunken)
        )
        layout.addSpacing(10)

        self.chk_rp_install_machine = QCheckBox()
        self.btn_rp_install = QPushButton()
        self.btn_rp_install.setProperty("class", "PrimaryBtn")
        self.btn_rp_remove = QPushButton()
        self.btn_rp_remove.setProperty("class", "StandardBtn")

        h_inst = QHBoxLayout()
        h_inst.setSpacing(10)
        h_inst.addWidget(self.btn_rp_install)
        h_inst.addWidget(self.btn_rp_remove)

        layout.addLayout(h_inst)

        self.chk_rp_cont = QWidget()
        chk_layout = QHBoxLayout(self.chk_rp_cont)
        chk_layout.setContentsMargins(0, 0, 0, 0)
        chk_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.chk_rp_install_machine.setStyleSheet(
            "background: transparent; font-size: 11px;"
        )
        chk_layout.addWidget(self.chk_rp_install_machine)
        layout.addWidget(self.chk_rp_cont)

        layout.addSpacing(5)

        self.btn_rp_test = QPushButton()
        self.btn_rp_test.setProperty("class", "StandardBtn")
        self.btn_rp_purge = QPushButton()
        self.btn_rp_purge.setProperty("class", "StandardBtn")

        h_actions = QHBoxLayout()
        h_actions.setSpacing(10)
        h_actions.addWidget(self.btn_rp_test)
        h_actions.addWidget(self.btn_rp_purge)
        layout.addLayout(h_actions)
        layout.addSpacing(10)

        def create_action_btn(icon_n):
            btn = QPushButton()
            btn.setIcon(qta.icon(icon_n, color=self.text_main))
            btn.setProperty("class", "PanelActionBtn")
            return btn

        self.btn_rp_web = create_action_btn("mdi6.web")
        self.btn_rp_csv = create_action_btn("mdi6.file-export-outline")

        layout.addWidget(self.btn_rp_web)
        layout.addWidget(self.btn_rp_csv)

        self.btn_rp_install.clicked.connect(self.action_install_printers)
        self.btn_rp_remove.clicked.connect(self.action_remove_printers)
        self.btn_rp_test.clicked.connect(self.action_test_printers)
        self.btn_rp_purge.clicked.connect(self.action_purge_printers)
        self.btn_rp_props.clicked.connect(self.action_properties_printers)
        self.btn_rp_csv.clicked.connect(self.export_csv)
        self.btn_rp_web.clicked.connect(self.action_web_interface)

        return panel

    def action_web_interface(self):
        table = (
            self.table_disp
            if self.stacked.currentIndex() == 0
            else self.table_instaladas
        )
        for row in range(table.rowCount()):
            chk_widget = table.cellWidget(row, 0)
            if chk_widget and chk_widget.layout().itemAt(0).widget().isChecked():
                raw_name = table.item(row, 1).data(Qt.ItemDataRole.UserRole)
                p_data = next(
                    (p for p in self.all_printers_data if p["raw_name"] == raw_name),
                    None,
                )
                if p_data:
                    ip = p_data.get("port", "")
                    if ip and any(char.isdigit() for char in ip):
                        import webbrowser

                        clean_ip = ip.replace("IP_", "")
                        webbrowser.open(f"http://{clean_ip}")

    def action_properties_printers(self):
        table = (
            self.table_disp
            if self.stacked.currentIndex() == 0
            else self.table_instaladas
        )
        for row in range(table.rowCount()):
            chk_widget = table.cellWidget(row, 0)
            if chk_widget and chk_widget.layout().itemAt(0).widget().isChecked():
                raw_name = table.item(row, 1).data(Qt.ItemDataRole.UserRole)
                self.open_properties(raw_name)

    def build_page_dispositivos(self):
        page = QWidget()
        main_layout = QHBoxLayout(page)
        main_layout.setContentsMargins(20, 0, 20, 10)
        main_layout.setSpacing(15)

        center_widget = QWidget()
        layout = QVBoxLayout(center_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.create_page_header("title_devices", "sub_devices"))

        cards_layout = QHBoxLayout()
        c_color = self.config.get("primary_color", "#60CDFF")
        self.card1 = ActionCard("mdi6.sync", "", "", c_color)
        self.card1.clicked.connect(self.refresh_all_data)
        self.card2 = ActionCard("mdi6.network-pos", "", "", c_color)
        self.card2.clicked.connect(self.map_printer)
        self.card3 = ActionCard("mdi6.tools", "", "", c_color)
        self.card3.clicked.connect(self.repair_spooler)
        self.card4 = ActionCard("mdi6.file-delimited-outline", "", "", c_color)
        self.card4.clicked.connect(self.export_csv)
        cards_layout.addWidget(self.card1)
        cards_layout.addWidget(self.card2)
        cards_layout.addWidget(self.card3)
        cards_layout.addWidget(self.card4)
        cards_layout.addStretch()
        layout.addLayout(cards_layout)
        layout.addSpacing(15)

        tools_layout = QHBoxLayout()
        self.cmb_status.currentIndexChanged.connect(self.filter_table_view)
        self.cmb_server.currentIndexChanged.connect(self.filter_table_view)
        tools_layout.addWidget(self.cmb_status)
        tools_layout.addWidget(self.cmb_server)
        tools_layout.addStretch()
        layout.addLayout(tools_layout)

        self.table_disp = QTableWidget(0, 8)
        self.table_disp.verticalHeader().setVisible(False)
        self.table_disp.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.table_disp.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_disp.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table_disp.customContextMenuRequested.connect(
            lambda pos: self.show_context_menu(pos, self.table_disp)
        )
        self.table_disp.itemDoubleClicked.connect(self.handle_table_double_click)
        self.table_disp.itemSelectionChanged.connect(
            lambda: self.sync_table_selection(self.table_disp, "disp")
        )
        self.table_disp.setShowGrid(False)

        self.table_disp.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Interactive
        )
        self.table_disp.horizontalHeader().setStretchLastSection(True)
        self.table_disp.setColumnWidth(0, 40)
        self.table_disp.setColumnWidth(1, 250)
        self.table_disp.setColumnWidth(2, 120)
        self.table_disp.setColumnWidth(3, 200)
        self.table_disp.setColumnWidth(4, 120)
        self.table_disp.setColumnWidth(5, 120)
        self.table_disp.setColumnWidth(6, 120)
        self.table_disp.setColumnWidth(7, 80)
        self.configure_table_headers(self.table_disp)

        layout.addWidget(self.table_disp)
        main_layout.addWidget(center_widget)
        self.stacked.addWidget(page)

    def build_page_instaladas(self):
        page = QWidget()
        main_layout = QHBoxLayout(page)
        main_layout.setContentsMargins(20, 0, 20, 10)
        main_layout.setSpacing(15)

        center_widget = QWidget()
        layout = QVBoxLayout(center_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.create_page_header("title_local", "sub_local"))

        self.table_instaladas = QTableWidget(0, 6)
        self.table_instaladas.verticalHeader().setVisible(False)
        self.table_instaladas.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.table_instaladas.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.table_instaladas.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.table_instaladas.customContextMenuRequested.connect(
            lambda pos: self.show_context_menu(pos, self.table_instaladas)
        )
        self.table_instaladas.itemDoubleClicked.connect(self.handle_table_double_click)
        self.table_instaladas.itemSelectionChanged.connect(
            lambda: self.sync_table_selection(self.table_instaladas, "inst")
        )
        self.table_instaladas.setShowGrid(False)

        self.table_instaladas.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Interactive
        )
        self.table_instaladas.horizontalHeader().setStretchLastSection(True)
        self.table_instaladas.setColumnWidth(0, 40)
        self.table_instaladas.setColumnWidth(1, 280)
        self.table_instaladas.setColumnWidth(2, 120)
        self.table_instaladas.setColumnWidth(3, 100)
        self.table_instaladas.setColumnWidth(4, 200)
        self.table_instaladas.setColumnWidth(5, 120)
        self.configure_table_headers(self.table_instaladas)

        layout.addWidget(self.table_instaladas)
        main_layout.addWidget(center_widget)
        self.stacked.addWidget(page)

    def build_page_drivers(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 0, 40, 0)
        layout.addWidget(self.create_page_header("title_drivers", "sub_drivers"))

        self.table_drivers = QTableWidget(0, 3)
        self.table_drivers.verticalHeader().setVisible(False)
        self.table_drivers.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.table_drivers.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_drivers.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table_drivers.customContextMenuRequested.connect(
            lambda pos: self.show_context_menu(pos, self.table_drivers)
        )
        self.table_drivers.setShowGrid(False)
        self.table_drivers.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        self.table_drivers.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeMode.Stretch
        )
        self.table_drivers.setColumnWidth(1, 150)
        self.configure_table_headers(self.table_drivers)
        layout.addWidget(self.table_drivers)
        self.stacked.addWidget(page)

    def build_page_tarefas(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 0, 40, 0)
        layout.addWidget(self.create_page_header("title_tasks", "sub_tasks"))

        h_layout = QHBoxLayout()
        h_layout.addStretch()
        self.btn_export_logs = QPushButton()
        self.btn_export_logs.setProperty("class", "StandardBtn")
        self.btn_export_logs.clicked.connect(self.export_logs_csv)
        self.btn_clear_logs = QPushButton()
        self.btn_clear_logs.setProperty("class", "StandardBtn")
        self.btn_clear_logs.clicked.connect(self.clear_tarefas)
        h_layout.addWidget(self.btn_export_logs)
        h_layout.addWidget(self.btn_clear_logs)
        layout.addLayout(h_layout)

        self.table_tarefas = QTableWidget(0, 5)
        self.table_tarefas.verticalHeader().setVisible(False)
        self.table_tarefas.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.table_tarefas.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_tarefas.setShowGrid(False)
        self.table_tarefas.horizontalHeader().setSectionResizeMode(
            4, QHeaderView.ResizeMode.Stretch
        )
        self.table_tarefas.setColumnWidth(0, 180)
        self.table_tarefas.setColumnWidth(1, 120)
        self.table_tarefas.setColumnWidth(2, 140)
        self.table_tarefas.setColumnWidth(3, 140)
        self.configure_table_headers(self.table_tarefas)
        layout.addWidget(self.table_tarefas)
        self.stacked.addWidget(page)

    def build_page_sysinfo(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 0, 40, 0)
        layout.addWidget(self.create_page_header("title_sysinfo", "sub_sysinfo"))

        self.info_layout = QFormLayout()
        self.info_layout.setSpacing(20)
        
        self.lbl_key_os = QLabel()
        self.lbl_val_os = QLabel()
        self.lbl_key_pc_name = QLabel()
        self.lbl_val_pc_name = QLabel()
        self.lbl_key_user = QLabel()
        self.lbl_val_user = QLabel()
        self.lbl_key_ip = QLabel()
        self.lbl_val_ip = QLabel()
        self.lbl_key_ram = QLabel()
        self.lbl_val_ram = QLabel()
        
        self.info_layout.addRow(self.lbl_key_os, self.lbl_val_os)
        self.info_layout.addRow(self.lbl_key_pc_name, self.lbl_val_pc_name)
        self.info_layout.addRow(self.lbl_key_user, self.lbl_val_user)
        self.info_layout.addRow(self.lbl_key_ip, self.lbl_val_ip)
        self.info_layout.addRow(self.lbl_key_ram, self.lbl_val_ram)

        container = QFrame()
        container.setProperty("class", "ActionCard")
        container.setStyleSheet("QFrame.ActionCard { padding: 30px; height: auto; }")
        container.setLayout(self.info_layout)
        layout.addWidget(container)
        layout.addStretch()
        self.stacked.addWidget(page)

    def build_page_guides(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 0, 40, 20)
        layout.addWidget(self.create_page_header("title_guides", "sub_guides"))

        actions_layout = QHBoxLayout()
        self.btn_add_pdf = QPushButton()
        self.btn_add_pdf.setProperty("class", "StandardBtn")
        self.btn_add_pdf.clicked.connect(self.add_custom_pdf)
        self.btn_rem_pdf = QPushButton()
        self.btn_rem_pdf.setProperty("class", "StandardBtn")
        self.btn_rem_pdf.clicked.connect(self.remove_custom_pdf)
        self.btn_open_pdf = QPushButton()
        self.btn_open_pdf.setProperty("class", "PrimaryBtn")
        self.btn_open_pdf.clicked.connect(self.open_selected_pdf)
        
        actions_layout.addWidget(self.btn_add_pdf)
        actions_layout.addWidget(self.btn_rem_pdf)
        actions_layout.addStretch()
        actions_layout.addWidget(self.btn_open_pdf)
        layout.addLayout(actions_layout)

        self.list_pdfs = QListWidget()
        self.list_pdfs.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.list_pdfs.itemDoubleClicked.connect(self.open_selected_pdf)
        layout.addWidget(self.list_pdfs)

        self.refresh_guides()
        self.stacked.addWidget(page)

    def build_page_configuracoes(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 0, 40, 20)
        layout.addWidget(self.create_page_header("title_settings", "sub_settings"))

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(20)

        grp_aparencia = QFrame()
        grp_aparencia.setProperty("class", "ActionCard")
        grp_aparencia.setStyleSheet(
            "QFrame.ActionCard { padding: 20px; height: auto; }"
        )
        form_ap = QFormLayout(grp_aparencia)
        self.lbl_cfg_app = QLabel()
        self.lbl_cfg_app.setStyleSheet("font-weight: bold; margin-bottom: 10px;")
        form_ap.addRow(self.lbl_cfg_app)

        self.lbl_lang = QLabel()
        form_ap.addRow(self.lbl_lang, self.cfg_lang)
        self.lbl_theme = QLabel()
        form_ap.addRow(self.lbl_theme, self.cfg_theme)
        self.lbl_color = QLabel()
        form_ap.addRow(self.lbl_color, self.cfg_color)

        self.lbl_font = QLabel()
        form_ap.addRow(self.lbl_font, self.cfg_font)

        self.lbl_size = QLabel()
        form_ap.addRow(self.lbl_size, self.cfg_font_size)

        self.lbl_logo_sel = QLabel()
        self.btn_custom_icon = QPushButton()
        self.btn_custom_icon.setProperty("class", "StandardBtn")
        self.btn_custom_icon.clicked.connect(self.choose_custom_icon)
        icon_row = QHBoxLayout()
        icon_row.addWidget(self.cfg_logo_icon)
        icon_row.addWidget(self.btn_custom_icon)
        form_ap.addRow(self.lbl_logo_sel, icon_row)
        scroll_layout.addWidget(grp_aparencia)

        grp_behavior = QFrame()
        grp_behavior.setProperty("class", "ActionCard")
        grp_behavior.setStyleSheet("QFrame.ActionCard { padding: 20px; height: auto; }")
        form_bh = QFormLayout(grp_behavior)
        self.lbl_cfg_bh = QLabel()
        self.lbl_cfg_bh.setStyleSheet("font-weight: bold; margin-bottom: 10px;")
        form_bh.addRow(self.lbl_cfg_bh)
        self.lbl_refresh = QLabel()
        form_bh.addRow(self.lbl_refresh, self.cfg_refresh)
        scroll_layout.addWidget(grp_behavior)

        grp_servidores = QFrame()
        grp_servidores.setProperty("class", "ActionCard")
        grp_servidores.setStyleSheet(
            "QFrame.ActionCard { padding: 20px; height: auto; }"
        )
        srv_layout = QVBoxLayout(grp_servidores)
        self.lbl_cfg_srv = QLabel()
        self.lbl_cfg_srv.setStyleSheet("font-weight: bold; margin-bottom: 10px;")
        srv_layout.addWidget(self.lbl_cfg_srv)

        self.table_cfg_servers = QTableWidget(0, 6)
        self.table_cfg_servers.verticalHeader().setVisible(False)
        self.table_cfg_servers.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.table_cfg_servers.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.table_cfg_servers.setShowGrid(False)
        self.table_cfg_servers.setFixedHeight(220)
        self.table_cfg_servers.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.Stretch
        )
        self.table_cfg_servers.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeMode.Stretch
        )
        self.table_cfg_servers.setColumnWidth(0, 60)
        self.table_cfg_servers.setColumnWidth(3, 120)
        self.table_cfg_servers.setColumnWidth(4, 60)
        self.table_cfg_servers.setColumnWidth(5, 100)
        self.configure_table_headers(self.table_cfg_servers)
        srv_layout.addWidget(self.table_cfg_servers)

        srv_tools = QHBoxLayout()
        self.txt_new_srv = QLineEdit()
        self.btn_add_srv = QPushButton()
        self.btn_add_srv.setProperty("class", "StandardBtn")
        self.btn_add_srv.clicked.connect(self.add_cfg_server)
        self.btn_rem_srv = QPushButton()
        self.btn_rem_srv.setProperty("class", "StandardBtn")
        self.btn_rem_srv.clicked.connect(self.remove_cfg_server)
        srv_tools.addWidget(self.txt_new_srv)
        srv_tools.addWidget(self.btn_add_srv)
        srv_tools.addWidget(self.btn_rem_srv)
        srv_layout.addLayout(srv_tools)

        scroll_layout.addWidget(grp_servidores)
        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        ft = QHBoxLayout()
        ft.addStretch()
        self.btn_save = QPushButton()
        self.btn_save.setProperty("class", "PrimaryBtn")
        self.btn_save.clicked.connect(self.save_settings)
        ft.addWidget(self.btn_save)
        layout.addLayout(ft)
        self.stacked.addWidget(page)

    def build_page_about(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 0, 40, 0)
        layout.addWidget(self.create_page_header("title_about", "sub_about"))

        container = QFrame()
        container.setProperty("class", "ActionCard")
        container.setStyleSheet("QFrame.ActionCard { padding: 40px; height: auto; }")
        v_layout = QVBoxLayout(container)
        v_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        v_layout.setSpacing(20)

        h_header = QHBoxLayout()
        icon_lbl = QLabel()
        icon_lbl.setStyleSheet("background-color: transparent;")
        icon_lbl.setPixmap(
            qta.icon(
                "mdi6.printer-3d", color=self.config.get("primary_color", "#60CDFF")
            ).pixmap(64, 64)
        )
        titles_vbox = QVBoxLayout()
        self.lbl_about_title = QLabel()
        self.lbl_about_version = QLabel()
        titles_vbox.addWidget(self.lbl_about_title)
        titles_vbox.addWidget(self.lbl_about_version)
        h_header.addWidget(icon_lbl)
        h_header.addSpacing(15)
        h_header.addLayout(titles_vbox)
        h_header.addStretch()

        self.lbl_about_desc = QLabel()
        self.lbl_about_desc.setWordWrap(True)
        
        self.links_layout = QHBoxLayout()
        self.lbl_about_repo = QLabel()
        self.lbl_about_docs = QLabel()
        self.lbl_about_web = QLabel()
        for l in [self.lbl_about_repo, self.lbl_about_docs, self.lbl_about_web]:
            l.setOpenExternalLinks(True)
            self.links_layout.addWidget(l)
            self.links_layout.addSpacing(20)
        self.links_layout.addStretch()

        self.btn_about_update = QPushButton()
        self.btn_about_update.setProperty("class", "StandardBtn")
        self.btn_about_update.clicked.connect(
            lambda: QMessageBox.information(
                self, tr("about_check_updates"), tr("about_up_to_date")
            )
        )
        
        self.lbl_about_modules = QLabel()

        v_layout.addLayout(h_header)
        v_layout.addSpacing(10)
        v_layout.addWidget(self.lbl_about_desc)
        v_layout.addSpacing(10)
        v_layout.addWidget(self.lbl_about_modules)
        v_layout.addSpacing(20)
        v_layout.addLayout(self.links_layout)
        v_layout.addSpacing(20)
        v_layout.addWidget(self.btn_about_update, alignment=Qt.AlignmentFlag.AlignLeft)

        layout.addWidget(container)
        layout.addStretch()
        self.stacked.addWidget(page)

    def retranslate_ui(self):
        self.setWindowTitle(tr("app_title"))
        self.lbl_app_title.setText(f" {tr('app_title')}")
        self.search_box.setPlaceholderText(tr("search_ph"))

        for idx, key in enumerate(
            ["nav_devices", "nav_local", "nav_drivers", "nav_tasks", "nav_sysinfo", "nav_guides"]
        ):
            if idx < len(self.nav_buttons) - 2:
                self.nav_buttons[idx].update_text(tr(key))
                
        self.btn_settings.update_text(tr("nav_settings"))
        self.btn_about.update_text(tr("nav_about"))

        for view in [
            "devices",
            "local",
            "drivers",
            "tasks",
            "sysinfo",
            "guides",
            "settings",
            "about",
        ]:
            getattr(self, f"hdr_title_title_{view}").setText(tr(f"title_{view}"))
            getattr(self, f"hdr_sub_sub_{view}").setText(tr(f"sub_{view}"))

        self.card1.set_texts(tr("card_sync"), tr("card_sync_sub"))
        self.card2.set_texts(tr("card_map"), tr("card_map_sub"))
        self.card3.set_texts(tr("card_repair"), tr("card_repair_sub"))
        self.card4.set_texts(tr("card_export"), tr("card_export_sub"))

        self.table_disp.setHorizontalHeaderLabels(
            [
                "",
                tr("col_name"),
                tr("col_manufacturer"),
                tr("col_driver"),
                tr("col_port"),
                tr("col_server"),
                tr("col_status"),
                tr("col_installed"),
            ]
        )
        self.table_instaladas.setHorizontalHeaderLabels(
            [
                "",
                tr("col_name"),
                tr("col_manufacturer"),
                tr("col_type"),
                tr("col_driver"),
                tr("col_port"),
            ]
        )
        self.table_drivers.setHorizontalHeaderLabels(
            [tr("col_name"), tr("col_env"), tr("col_path")]
        )
        self.table_tarefas.setHorizontalHeaderLabels(
            [
                tr("col_task_type"),
                tr("col_status"),
                tr("col_started"),
                tr("col_finished"),
                tr("col_target"),
            ]
        )
        self.table_cfg_servers.setHorizontalHeaderLabels(
            [
                tr("col_active"),
                tr("col_name"),
                tr("col_ip"),
                tr("col_status"),
                tr("col_qty"),
                tr("col_test"),
            ]
        )

        self.txt_new_srv.setPlaceholderText("IP / Hostname...")

        def repopulate_combo(combo, items_dict, current_val):
            combo.blockSignals(True)
            combo.clear()
            if (
                current_val
                and isinstance(current_val, str)
                and current_val not in items_dict
                and os.path.exists(current_val)
            ):
                items_dict[current_val] = (os.path.basename(current_val), None, None)
            for key, (text, icon_name, color) in items_dict.items():
                if icon_name:
                    combo.addItem(qta.icon(icon_name, color=color), text, key)
                elif isinstance(key, str) and os.path.exists(key):
                    combo.addItem(QIcon(key), text, key)
                else:
                    combo.addItem(text, key)
                if key == current_val:
                    combo.setCurrentIndex(combo.count() - 1)
            combo.blockSignals(False)

        repopulate_combo(
            self.cmb_status,
            {
                "all": (tr("status_all"), "mdi6.format-list-bulleted", self.text_main),
                "ok": (tr("status_ok"), "mdi6.check-circle", "#10b981"),
                "warn": (tr("status_warn"), "mdi6.alert", "#d97706"),
                "off": (tr("status_off"), "mdi6.close-circle", "#999999"),
            },
            self.cmb_status.currentData() or "all",
        )
        srv_dict = {"all": (tr("server_all"), "mdi6.server-network", self.text_main)}
        for p in self.all_printers_data:
            if p["server"] != "Local":
                srv_dict[p["server"]] = (p["server"], "mdi6.server", self.text_main)
        repopulate_combo(
            self.cmb_server, srv_dict, self.cmb_server.currentData() or "all"
        )

        repopulate_combo(
            self.cfg_lang,
            {
                "lang_sys": (tr("lang_sys"), None, None),
                "pt": ("Português", None, None),
                "en": ("English", None, None),
                "es": ("Español", None, None),
            },
            self.config.get("language", "lang_sys"),
        )
        repopulate_combo(
            self.cfg_theme,
            {
                "theme_system": (tr("theme_system"), None, None),
                "theme_light": (tr("theme_light"), None, None),
                "theme_dark": (tr("theme_dark"), None, None),
            },
            self.config.get("theme", "theme_system"),
        )
        repopulate_combo(
            self.cfg_color,
            {
                "#60CDFF": (tr("color_blue"), None, None),
                "#10b981": (tr("color_green"), None, None),
                "#8b5cf6": (tr("color_purple"), None, None),
                "#94a3b8": (tr("color_gray"), None, None),
            },
            self.config.get("primary_color", "#60CDFF"),
        )
        repopulate_combo(
            self.cfg_refresh,
            {
                0: (tr("ref_off"), None, None),
                30: (tr("ref_30s"), None, None),
                60: (tr("ref_60s"), None, None),
                300: (tr("ref_300s"), None, None),
            },
            self.config.get("auto_refresh", 0),
        )
        # CORREÇÃO MODO CLARO: self.text_main é utilizado ao invés de self.accent_color para contrastar
        repopulate_combo(
            self.cfg_logo_icon,
            {
                "mdi6.flash": ("Lightning (⚡)", "mdi6.flash", self.text_main),
                "mdi6.printer": ("Printer (🖨️)", "mdi6.printer", self.text_main),
                "mdi6.star": ("Star (⭐)", "mdi6.star", self.text_main),
                "mdi6.lan": ("Network (🌐)", "mdi6.lan", self.text_main),
                "mdi6.shield-check": (
                    "Shield (🛡️)",
                    "mdi6.shield-check",
                    self.text_main,
                ),
            },
            self.config.get("app_icon_val", "mdi6.flash"),
        )

        self.cfg_font.blockSignals(True)
        self.cfg_font.clear()
        font_families = QFontDatabase.families()
        if not font_families:
            font_families = ["Segoe UI", "Arial", "Verdana", "Sans Serif", "Tahoma"]
        self.cfg_font.addItems(font_families)

        pref_font = self.config.get("font_family", "Segoe UI")
        if pref_font in font_families:
            self.cfg_font.setCurrentText(pref_font)
        elif font_families:
            self.cfg_font.setCurrentIndex(0)
        self.cfg_font.blockSignals(False)

        try:
            fs = int(self.config.get("font_size", 10))
        except:
            fs = 10
        if fs < 8:
            fs = 10
        self.cfg_font_size.blockSignals(True)
        self.cfg_font_size.setRange(8, 72)
        self.cfg_font_size.setValue(fs)
        self.cfg_font_size.blockSignals(False)

        self.lbl_cfg_app.setText(tr("cfg_appearance"))
        self.lbl_cfg_bh.setText(tr("cfg_behavior"))
        self.lbl_cfg_srv.setText(tr("cfg_servers"))
        self.lbl_lang.setText(tr("cfg_lang"))
        self.lbl_theme.setText(tr("cfg_theme"))
        self.lbl_color.setText(tr("cfg_color"))
        self.lbl_refresh.setText(tr("cfg_refresh"))
        self.lbl_font.setText(tr("cfg_font"))
        self.lbl_size.setText(tr("cfg_size"))
        self.lbl_logo_sel.setText(tr("cfg_icon_sidebar"))
        self.btn_custom_icon.setText(tr("cfg_icon_custom"))
        self.btn_add_srv.setText(tr("cfg_btn_add"))
        self.btn_rem_srv.setText(tr("cfg_btn_rem"))
        self.btn_save.setText(tr("cfg_save"))
        self.btn_clear_logs.setText(tr("btn_clear_logs"))
        self.btn_export_logs.setText(tr("btn_export_logs"))
        self.btn_add_pdf.setText(tr("btn_add_pdf"))
        self.btn_open_pdf.setText(tr("btn_open_pdf"))
        self.btn_rem_pdf.setText(tr("btn_rem_pdf"))

        self.btn_rp_install.setText(f"  {tr('btn_install')}")
        self.btn_rp_remove.setText(f"  {tr('btn_batch_remove')}")
        self.btn_rp_test.setText(f"  {tr('btn_batch_test')}")
        self.btn_rp_purge.setText(f"  {tr('btn_batch_purge')}")
        self.btn_rp_web.setText(f"  {tr('btn_web_interface')}")
        self.btn_rp_props.setText(f"  {tr('btn_properties')}")
        self.btn_rp_csv.setText(f"  {tr('btn_export_csv')}")
        self.chk_rp_install_machine.setText(tr("chk_per_machine"))

        # System Info Updates
        try:
            os_info = f"{platform.system()} {platform.release()} ({platform.architecture()[0]})"
        except:
            os_info = tr("sys_unknown")
        try:
            pc_name = platform.node()
        except:
            pc_name = tr("sys_unknown")
        try:
            current_user = os.getlogin()
        except:
            current_user = tr("sys_unknown")
        try:
            ip_addr = socket.gethostbyname(socket.gethostname())
        except:
            ip_addr = tr("sys_unknown")
            
        self.lbl_key_os.setText(f"<b>{tr('sysinfo_os')}</b>")
        self.lbl_val_os.setText(os_info)
        self.lbl_key_pc_name.setText(f"<b>{tr('sysinfo_pc_name')}</b>")
        self.lbl_val_pc_name.setText(pc_name)
        self.lbl_key_user.setText(f"<b>{tr('sysinfo_user')}</b>")
        self.lbl_val_user.setText(current_user)
        self.lbl_key_ip.setText(f"<b>{tr('sysinfo_ip')}</b>")
        self.lbl_val_ip.setText(ip_addr)
        self.lbl_key_ram.setText(f"<b>{tr('sysinfo_ram')}</b>")
        self.lbl_val_ram.setText(get_ram_info())
        
        # About Updates
        self.lbl_about_title.setText(f"<b>{tr('app_title')}</b>")
        self.lbl_about_version.setText(f"{tr('about_version')} 2.1.0 • WinUI Edition Pro")
        self.lbl_about_desc.setText(tr("about_desc"))
        self.lbl_about_modules.setText(f"<b>{tr('about_modules')}</b> PyQt6, pywin32, qtawesome, ctypes.")
        
        link_style = f"color: {self.config.get('primary_color', '#60CDFF')}; text-decoration: none; font-weight: bold;"
        def format_link(text):
            return f'<a href="https://github.com/" style="{link_style}"><span style="text-decoration: underline;">{text}</span></a>'
            
        self.lbl_about_repo.setText(format_link(tr("about_repo")))
        self.lbl_about_docs.setText(format_link(tr("about_docs")))
        self.lbl_about_web.setText(format_link(tr("about_web")))
        
        self.btn_about_update.setText(tr("about_check_updates"))

        self.update_status(tr("msg_ready"))

        self.update_global_right_panel()
        self.populate_disp_tree()
        self.populate_inst_tree()
        self.refresh_guides()

    def update_global_right_panel(self):
        idx = self.stacked.currentIndex()
        if idx == 0:
            table = self.table_disp
            is_local = False
            prefix = "disp"
        elif idx == 1:
            table = self.table_instaladas
            is_local = True
            prefix = "inst"
        else:
            self.right_panel.hide()
            return

        checked_rows = []
        has_installed, has_not_installed = False, False
        for row in range(table.rowCount()):
            chk_w = table.cellWidget(row, 0)
            if chk_w and chk_w.layout().itemAt(0).widget().isChecked():
                checked_rows.append(row)
                if not is_local:
                    inst_str = table.item(row, 7).text()
                    if (
                        "Sim" in inst_str
                        or "Yes" in inst_str
                        or "Sí" in inst_str
                        or "✅" in inst_str
                    ):
                        has_installed = True
                    else:
                        has_not_installed = True
                else:
                    has_installed = True

        if not checked_rows:
            self.right_panel.hide()
            return

        self.right_panel.show()
        if len(checked_rows) == 1:
            name = table.item(checked_rows[0], 1).text().replace("⭐ ", "")
            ip = (
                table.item(checked_rows[0], 4).text()
                if not is_local
                else table.item(checked_rows[0], 5).text()
            )
            self.rp_icon.setPixmap(
                qta.icon("mdi6.printer", color=self.text_main).pixmap(50, 50)
            )
            self.rp_title.setText(name)
            self.rp_sub.setText(ip)
            self.btn_rp_web.show()
            self.btn_rp_props.show()
        else:
            self.rp_icon.setPixmap(
                qta.icon("mdi6.printer-3d", color=self.accent_color).pixmap(50, 50)
            )
            self.rp_title.setText(f"{len(checked_rows)} Dispositivos")
            self.rp_sub.setText(tr("batch_actions"))
            self.btn_rp_web.hide()
            self.btn_rp_props.hide()

        if is_local:
            self.chk_rp_cont.hide()
            self.btn_rp_install.hide()
            self.btn_rp_remove.show()
        else:
            if has_installed and not has_not_installed:
                self.btn_rp_install.hide()
                self.chk_rp_cont.hide()
                self.btn_rp_remove.show()
            elif has_not_installed and not has_installed:
                self.btn_rp_install.show()
                self.chk_rp_cont.show()
                self.btn_rp_remove.hide()
            else:
                self.btn_rp_install.hide()
                self.chk_rp_cont.hide()
                self.btn_rp_remove.hide()

    def refresh_all_data_silent(self):
        self.refresh_all_data(silent=True)

    def refresh_all_data(self, silent=False):
        servers = self.config.get("servers", [])
        if not silent:
            self.show_progress(True)
            self.update_progress(0, len(servers) + 1, tr("msg_syncing"))

        self.all_printers_data = []
        self.table_disp.setSortingEnabled(False)
        self.table_disp.setRowCount(0)
        self.table_instaladas.setSortingEnabled(False)
        self.table_instaladas.setRowCount(0)
        self.dp_worker = DefaultPrinterWorker()
        self.dp_worker.signals.result.connect(self.on_default_printer_fetched)
        self.threadpool.start(self.dp_worker)
        self.workers_completed = 0
        self.workers_total = len(servers)
        if self.workers_total == 0:
            self.update_progress(1, 1, tr("msg_success"))
            return

        for srv in servers:
            worker = ServerWorker(srv)
            worker.signals.result.connect(self.on_server_worker_result)
            worker.signals.finished.connect(self.on_server_worker_finished)
            self.threadpool.start(worker)

    def on_default_printer_fetched(self, dp):
        self.default_printer = dp

    def on_server_worker_result(self, parsed_printers, srv_obj, err_msg):
        if err_msg:
            TaskLogger.log(tr("task_sync"), "status_err", srv_obj["name"])
        self.all_printers_data.extend(parsed_printers)
        for s in self.config["servers"]:
            if s["name"] == srv_obj["name"]:
                s.update(srv_obj)
                break
        self.update_server_filter()
        self.filter_table_view()
        if self.stacked.currentIndex() == 1:
            self.refresh_local_only()
        elif self.stacked.currentIndex() == 6:
            self.refresh_settings_servers_table()

    def on_server_worker_finished(self):
        self.workers_completed += 1
        self.update_progress(
            self.workers_completed,
            self.workers_total,
            tr("msg_processing").format(completed=self.workers_completed, total=self.workers_total),
        )
        if self.workers_completed >= self.workers_total:
            TaskLogger.log(
                tr("task_sync"),
                "status_ok",
                tr("target_all"),
                end_time=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            )
            self.populate_disp_tree()
            self.populate_inst_tree()
            self.filter_table_view()
            if self.stacked.currentIndex() == 2: # Old index was 1 for local
                self.refresh_local_only()
            elif self.stacked.currentIndex() == 0:
                self.refresh_dashboard()
            self.update_progress(
                self.workers_total, self.workers_total, tr("msg_ready")
            )

    def update_server_filter(self):
        current = self.cmb_server.currentData() or "all"
        srv_dict = {"all": (tr("server_all"), "mdi6.server-network", self.text_main)}
        for p in self.all_printers_data:
            if p["server"] != "Local":
                srv_dict[p["server"]] = (p["server"], "mdi6.server", self.text_main)
        self.cmb_server.blockSignals(True)
        self.cmb_server.clear()
        for key, (text, icon_name, color) in srv_dict.items():
            self.cmb_server.addItem(qta.icon(icon_name, color=color), text, key)
            if key == current:
                self.cmb_server.setCurrentIndex(self.cmb_server.count() - 1)
        self.cmb_server.blockSignals(False)

    def create_status_badge(self, status_code_or_str):
        if isinstance(status_code_or_str, int):
            if status_code_or_str == 0:
                text, color, st = tr("status_ok"), "#6ccb5f", "ok"
            elif (
                status_code_or_str & win32print.PRINTER_STATUS_OFFLINE
                or status_code_or_str & win32print.PRINTER_STATUS_NOT_AVAILABLE
            ):
                text, color, st = tr("status_off"), "#999999", "off"
            elif (
                status_code_or_str & win32print.PRINTER_STATUS_ERROR
                or status_code_or_str & win32print.PRINTER_STATUS_PAPER_JAM
                or status_code_or_str & win32print.PRINTER_STATUS_PAPER_OUT
            ):
                text, color, st = tr("msg_error"), "#ef4444", "err"
            else:
                text, color, st = tr("status_warn"), "#d97706", "warn"
        else:
            if status_code_or_str == "Online":
                text, color, st = "Online", "#6ccb5f", "ok"
            elif status_code_or_str in ["Offline", "Offline/Erro"]:
                text, color, st = "Offline", "#ef4444", "err"
            else:
                text, color, st = status_code_or_str, "#d97706", "warn"
        lbl = QLabel(f"● {text}")
        lbl.setStyleSheet(
            f"color: {color}; font-weight: bold; background: transparent;"
        )
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return lbl, st

    def global_search(self):
        self.filter_table_view()
        if self.stacked.currentIndex() == 1:
            self.refresh_local_only()
        elif self.stacked.currentIndex() == 2:
            self.refresh_drivers()

    def filter_table_view(self):
        self.table_disp.setSortingEnabled(False)
        query = self.search_box.text().lower()
        f_status = self.cmb_status.currentData()
        f_server = self.cmb_server.currentData()
        self.table_disp.setRowCount(0)

        for p in self.all_printers_data:
            if p["server"] == "Local":
                continue
            status_lbl, st_type = self.create_status_badge(p["status_code"])

            # Aplicação dos filtros do ComboBox (Status e Server)
            if f_status and f_status != "all" and f_status != st_type:
                continue
            if f_server and f_server != "all" and p["server"] != f_server:
                continue

            if self.current_disp_filter:
                ftype = self.current_disp_filter["type"]
                fval = self.current_disp_filter["val"]
                if ftype == "status":
                    if fval == tr("filter_online") and st_type != "ok":
                        continue
                    if fval == tr("filter_offline") and st_type != "off":
                        continue
                    if fval == tr("filter_warn") and st_type != "warn":
                        continue
                elif ftype == "server" and p["server"] != fval:
                    continue
                elif ftype == "manufacturer" and get_manufacturer(p["driver"]) != fval:
                    continue

            if query and not any(
                query in str(v).lower()
                for v in [p["name"], p["port"], p["driver"], p["server"]]
            ):
                continue

            row = self.table_disp.rowCount()
            self.table_disp.insertRow(row)
            self.table_disp.setRowHeight(row, 45)
            name_formatted = (
                f"⭐ {p['name']}"
                if p["raw_name"] == self.default_printer
                else p["name"]
            )
            is_installed = any(
                lp["name"] == p["name"] or lp["name"] == p["raw_name"].split("\\")[-1]
                for lp in self.all_printers_data
                if lp["server"] == "Local"
            )

            chk_container = QWidget()
            chk_layout = QHBoxLayout(chk_container)
            chk_layout.setContentsMargins(0, 0, 0, 0)
            chk_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            chk = QCheckBox()
            chk.stateChanged.connect(lambda _: self.update_global_right_panel())
            chk_layout.addWidget(chk)
            self.table_disp.setCellWidget(row, 0, chk_container)

            man = get_manufacturer(p["driver"])
            self.table_disp.setItem(
                row,
                1,
                self.create_centered_item(name_formatted, user_data=p["raw_name"]),
            )
            self.table_disp.setItem(row, 2, self.create_centered_item(man))
            self.table_disp.setItem(row, 3, self.create_centered_item(str(p["driver"])))
            self.table_disp.setItem(row, 4, self.create_centered_item(str(p["port"])))
            self.table_disp.setItem(row, 5, self.create_centered_item(str(p["server"])))
            self.table_disp.setCellWidget(row, 6, status_lbl)
            self.table_disp.setItem(
                row,
                7,
                self.create_centered_item("✅ Sim" if is_installed else "❌ Não"),
            )

        self.table_disp.setSortingEnabled(True)
        self.update_global_right_panel()

    def export_csv(self):
        if not self.all_printers_data:
            QMessageBox.warning(self, tr("msg_error"), tr("msg_no_data_export"))
            return
        path, _ = QFileDialog.getSaveFileName(
            self, tr("card_export"), "", "CSV Files (*.csv)"
        )
        if path:
            try:
                with open(path, mode="w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f, delimiter=";")
                    writer.writerow(
                        [
                            tr("col_name"),
                            tr("col_driver"),
                            tr("col_port"),
                            tr("col_server"),
                            "Status ID",
                        ]
                    )
                    for p in self.all_printers_data:
                        writer.writerow(
                            [
                                p["name"],
                                p["driver"],
                                p["port"],
                                p["server"],
                                p["status_code"],
                            ]
                        )
                TaskLogger.log(tr("task_export_csv"), "status_ok", tr("target_dev_data"))
                QMessageBox.information(self, tr("msg_success"), tr("msg_success"))
            except Exception as e:
                TaskLogger.log(tr("task_export_csv"), "status_err", str(e))

    def export_logs_csv(self):
        if not TaskLogger.logs:
            QMessageBox.warning(self, tr("msg_error"), tr("msg_error"))
            return
        path, _ = QFileDialog.getSaveFileName(
            self, tr("btn_export_logs"), "", "CSV Files (*.csv)"
        )
        if path:
            try:
                with open(path, mode="w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f, delimiter=";")
                    writer.writerow(
                        [
                            tr("col_task_type"),
                            tr("col_status"),
                            tr("col_started"),
                            tr("col_finished"),
                            tr("col_target"),
                        ]
                    )
                    for log in TaskLogger.logs:
                        writer.writerow([log[0], tr(log[1]), log[2], log[3], log[4]])
                QMessageBox.information(self, tr("msg_success"), tr("msg_success"))
            except Exception as e:
                QMessageBox.warning(self, tr("msg_error"), f"Erro: {e}")

    def refresh_local_only(self):
        self.table_instaladas.setSortingEnabled(False)
        query = self.search_box.text().lower()
        self.table_instaladas.setRowCount(0)

        added_names = set()
        for p in self.all_printers_data:
            if p["server"] == "Local" or not p["is_network"]:
                t_conn = tr("conn_network") if p["is_network"] else tr("conn_local")
                if self.current_inst_filter:
                    ftype = self.current_inst_filter["type"]
                    fval = self.current_inst_filter["val"]
                    if ftype == "conn" and fval != t_conn:
                        continue
                    if (
                        ftype == "manufacturer"
                        and get_manufacturer(p["driver"]) != fval
                    ):
                        continue

                if query and not any(
                    query in str(v).lower() for v in [p["name"], p["port"], p["driver"]]
                ):
                    continue
                if p["name"] in added_names:
                    continue
                added_names.add(p["name"])
                row = self.table_instaladas.rowCount()
                self.table_instaladas.insertRow(row)
                self.table_instaladas.setRowHeight(row, 45)

                chk_container = QWidget()
                chk_layout = QHBoxLayout(chk_container)
                chk_layout.setContentsMargins(0, 0, 0, 0)
                chk_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                chk = QCheckBox()
                chk.stateChanged.connect(lambda _: self.update_global_right_panel())
                chk_layout.addWidget(chk)
                self.table_instaladas.setCellWidget(row, 0, chk_container)

                name_formatted = (
                    f"⭐ {p['name']}"
                    if p["raw_name"] == self.default_printer
                    else p["name"]
                )
                man = get_manufacturer(p["driver"])

                self.table_instaladas.setItem(
                    row,
                    1,
                    self.create_centered_item(name_formatted, user_data=p["raw_name"]),
                )
                self.table_instaladas.setItem(row, 2, self.create_centered_item(man))
                self.table_instaladas.setItem(row, 3, self.create_centered_item(t_conn))
                self.table_instaladas.setItem(
                    row, 4, self.create_centered_item(str(p["driver"]))
                )
                self.table_instaladas.setItem(
                    row, 5, self.create_centered_item(str(p["port"]))
                )
        self.table_instaladas.setSortingEnabled(True)
        self.update_global_right_panel()

    def refresh_drivers(self):
        self.table_drivers.setSortingEnabled(False)
        self.table_drivers.setRowCount(0)
        self.show_progress(True)
        self.update_status(tr("msg_loading_drivers"))
        self.driver_worker = DriverWorker()
        self.driver_worker.signals.result.connect(self.on_drivers_fetched)
        self.threadpool.start(self.driver_worker)

    def on_drivers_fetched(self, parsed_drivers, err):
        self.show_progress(False)
        self.update_status(tr("msg_ready"))
        query = self.search_box.text().lower()
        for d in parsed_drivers:
            if query and not any(query in str(v).lower() for v in d.values()):
                continue
            row = self.table_drivers.rowCount()
            self.table_drivers.insertRow(row)
            self.table_drivers.setRowHeight(row, 45)
            self.table_drivers.setItem(
                row, 0, self.create_centered_item(str(d["name"]))
            )
            self.table_drivers.setItem(row, 1, self.create_centered_item(str(d["env"])))
            self.table_drivers.setItem(
                row, 2, self.create_centered_item(str(d["path"]))
            )
        self.table_drivers.setSortingEnabled(True)

    def refresh_tarefas_table(self):
        self.table_tarefas.setSortingEnabled(False)
        self.table_tarefas.setRowCount(0)
        for t in TaskLogger.logs:
            row = self.table_tarefas.rowCount()
            self.table_tarefas.insertRow(row)
            self.table_tarefas.setRowHeight(row, 45)
            self.table_tarefas.setItem(row, 0, self.create_centered_item(t[0]))

            if t[1] == "status_ok":
                color = "#10b981"
            elif t[1] == "status_warn":
                color = "#d97706"
            elif t[1] == "status_err":
                color = "#ef4444"
            else:
                color = self.accent_color

            status_item = self.create_centered_item(tr(t[1]))
            status_item.setForeground(QBrush(QColor(color)))
            font = status_item.font()
            font.setBold(True)
            status_item.setFont(font)

            self.table_tarefas.setItem(row, 1, status_item)
            self.table_tarefas.setItem(row, 2, self.create_centered_item(t[2]))
            self.table_tarefas.setItem(row, 3, self.create_centered_item(t[3]))
            self.table_tarefas.setItem(row, 4, self.create_centered_item(t[4]))

        self.table_tarefas.setSortingEnabled(True)

    def clear_tarefas(self):
        TaskLogger.logs.clear()
        self.refresh_tarefas_table()
        
    def refresh_guides(self):
        self.list_pdfs.clear()
        
        # 1. Inserir Guia Default
        item_default = QListWidgetItem(qta.icon("mdi6.book-open-variant", color=self.accent_color), tr("default_guide_name"))
        item_default.setToolTip(tr("default_guide_desc"))
        item_default.setData(Qt.ItemDataRole.UserRole, "DEFAULT_GUIDE")
        self.list_pdfs.addItem(item_default)
        
        # 2. Inserir PDFs Customizados
        pdfs = self.config.get("custom_pdfs", [])
        for pdf_path in pdfs:
            if os.path.exists(pdf_path):
                name = os.path.basename(pdf_path)
                item = QListWidgetItem(qta.icon("mdi6.file-pdf-box", color="#ef4444"), name)
                item.setToolTip(pdf_path)
                item.setData(Qt.ItemDataRole.UserRole, pdf_path)
                self.list_pdfs.addItem(item)
                
    def add_custom_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, tr("btn_add_pdf"), "", "PDF Files (*.pdf)"
        )
        if file_path:
            pdfs = self.config.get("custom_pdfs", [])
            if file_path not in pdfs:
                pdfs.append(file_path)
                self.config["custom_pdfs"] = pdfs
                ConfigManager.save(self.config)
                self.refresh_guides()
                
    def remove_custom_pdf(self):
        selected = self.list_pdfs.selectedItems()
        if not selected:
            return
        item = selected[0]
        path = item.data(Qt.ItemDataRole.UserRole)
        
        if path == "DEFAULT_GUIDE":
            QMessageBox.warning(self, tr("msg_warning"), tr("msg_guide_no_rem"))
            return
            
        pdfs = self.config.get("custom_pdfs", [])
        if path in pdfs:
            pdfs.remove(path)
            self.config["custom_pdfs"] = pdfs
            ConfigManager.save(self.config)
            self.refresh_guides()
            
    def open_selected_pdf(self, item=None):
        # Ignora sinais booleanos vindo do click do botão
        if item is None or isinstance(item, bool):
            selected = self.list_pdfs.selectedItems()
            if not selected:
                return
            item = selected[0]
            
        path = item.data(Qt.ItemDataRole.UserRole)
        if path == "DEFAULT_GUIDE":
            msg = QMessageBox(self)
            msg.setWindowTitle(tr("guide_welcome_title"))
            msg.setTextFormat(Qt.TextFormat.RichText)
            msg.setText(tr("guide_welcome_text"))
            msg.setIcon(QMessageBox.Icon.Information)
            msg.exec()
            return
            
        if os.path.exists(path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))
        else:
            QMessageBox.warning(self, tr("msg_error"), tr("msg_pdf_not_found"))
            self.remove_custom_pdf() # Remove arquivo orfão da lista

    def refresh_settings_servers_table(self):
        self.table_cfg_servers.setSortingEnabled(False)
        self.table_cfg_servers.setRowCount(0)
        servers = self.config.get("servers", [])
        for i, srv in enumerate(servers):
            row = self.table_cfg_servers.rowCount()
            self.table_cfg_servers.insertRow(row)
            self.table_cfg_servers.setRowHeight(row, 50)
            chk_container = QWidget()
            chk_layout = QHBoxLayout(chk_container)
            chk_layout.setContentsMargins(0, 0, 0, 0)
            chk_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            chk = QCheckBox()
            chk.setChecked(srv.get("enabled", True))
            chk.stateChanged.connect(
                lambda state, idx=i: self.toggle_server_enabled(idx, state)
            )
            chk_layout.addWidget(chk)
            self.table_cfg_servers.setCellWidget(row, 0, chk_container)
            self.table_cfg_servers.setItem(
                row, 1, self.create_centered_item(srv.get("name", ""))
            )
            self.table_cfg_servers.setItem(
                row, 2, self.create_centered_item(srv.get("ip", ""))
            )
            status_lbl, _ = self.create_status_badge(srv.get("status", "?"))
            self.table_cfg_servers.setCellWidget(row, 3, status_lbl)
            qty_item = self.create_centered_item("")
            qty_item.setData(Qt.ItemDataRole.DisplayRole, int(srv.get("qty", 0)))
            self.table_cfg_servers.setItem(row, 4, qty_item)
            btn_test = QPushButton(tr("btn_test"))
            btn_test.setProperty("class", "StandardBtn")
            btn_test.clicked.connect(
                lambda checked, name=srv.get("name", ""): self.test_single_server(name)
            )
            btn_container = QWidget()
            btn_layout = QHBoxLayout(btn_container)
            btn_layout.setContentsMargins(4, 4, 4, 4)
            btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            btn_layout.addWidget(btn_test)
            self.table_cfg_servers.setCellWidget(row, 5, btn_container)
        self.table_cfg_servers.setSortingEnabled(True)

    def toggle_server_enabled(self, idx, state):
        servers = self.config.get("servers", [])
        if 0 <= idx < len(servers):
            servers[idx]["enabled"] = state == 2
            self.config["servers"] = servers

    def add_cfg_server(self):
        srv_name = self.txt_new_srv.text().strip()
        if srv_name:
            servers = self.config.get("servers", [])
            if not any(s.get("name") == srv_name for s in servers):
                servers.append(
                    {"name": srv_name, "enabled": True, "status": "?", "qty": 0}
                )
                self.config["servers"] = servers
                self.refresh_settings_servers_table()
            self.txt_new_srv.clear()

    def remove_cfg_server(self):
        selected = self.table_cfg_servers.selectedItems()
        if selected:
            row = selected[0].row()
            name = self.table_cfg_servers.item(row, 1).text()
            if name != "Local":
                servers = self.config.get("servers", [])
                servers = [s for s in servers if s.get("name") != name]
                self.config["servers"] = servers
                self.refresh_settings_servers_table()

    def test_single_server(self, host):
        self.update_status(f"{tr('msg_testing')} {host}")
        self.show_progress(True)
        self.update_progress(0, 1, f"{tr('msg_testing')} {host}")
        servers_temp = [s for s in self.config.get("servers", []) if s["name"] == host]
        if not servers_temp:
            return
        self.test_worker = ServerWorker(servers_temp[0])
        self.test_worker.signals.result.connect(self.on_test_complete)
        self.threadpool.start(self.test_worker)

    def on_test_complete(self, printers, server_obj, err):
        self.show_progress(False)
        servers = self.config.get("servers", [])
        host = server_obj["name"]
        for s in servers:
            if s["name"] == host:
                s.update(server_obj)
                break
        self.config["servers"] = servers
        self.refresh_settings_servers_table()
        if "Offline" in server_obj.get("status", "") or err:
            self.update_status(tr("msg_conn_failed").format(host=host))
            TaskLogger.log(tr("task_conn_test"), "status_err", host)
        else:
            self.update_status(
                tr("msg_conn_success").format(host=host, count=len(printers))
            )
            TaskLogger.log(tr("task_conn_test"), "status_ok", host)

    def save_settings(self):
        self.config["theme"] = self.cfg_theme.currentData()
        self.config["primary_color"] = self.cfg_color.currentData()
        self.config["language"] = self.cfg_lang.currentData()
        self.config["auto_refresh"] = self.cfg_refresh.currentData()
        self.config["font_family"] = self.cfg_font.currentText()
        self.config["font_size"] = self.cfg_font_size.value()
        val = self.cfg_logo_icon.currentData()
        if val:
            self.config["app_icon_val"] = val
            self.config["app_icon_type"] = "preset" if "mdi6." in val else "custom"

        global CURRENT_LANG
        CURRENT_LANG = (
            get_os_language()
            if self.config["language"] == "lang_sys"
            else self.config["language"]
        )
        ConfigManager.save(self.config)
        TaskLogger.log(tr("task_settings"), "status_ok", tr("target_sys"))
        self.update_timer_settings()
        self.apply_fluent_theme()
        self.retranslate_ui()
        self.refresh_all_data_silent()
        QMessageBox.information(self, tr("msg_success"), tr("msg_success"))

    def action_install_printers(self):
        idx = self.stacked.currentIndex()
        if idx == 0:
            table_ref = self.table_disp
        elif idx == 1:
            table_ref = self.table_instaladas
        else:
            return

        per_machine = self.chk_rp_install_machine.isChecked()
        mode_str = tr("msg_install_machine") if per_machine else tr("msg_install_user")

        count = 0
        printers_to_install = []
        for row in range(table_ref.rowCount()):
            chk_widget = table_ref.cellWidget(row, 0)
            if chk_widget and chk_widget.layout().itemAt(0).widget().isChecked():
                raw_name = table_ref.item(row, 1).data(Qt.ItemDataRole.UserRole)
                printers_to_install.append(raw_name)
                count += 1

        if count == 0:
            return

        confirm_msg = tr("msg_install_confirm").replace("{count}", str(count))
        reply = QMessageBox.question(
            self,
            "Confirmação",
            f"{tr('msg_install_mode')}: {mode_str}\n\n{confirm_msg}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        start_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        successes = []
        errors = []

        for raw_name in printers_to_install:
            try:
                if per_machine:
                    try:
                        h = win32print.OpenPrinter(raw_name)
                        win32print.ClosePrinter(h)
                    except pywintypes.error as e:
                        raise Exception(f"Erro de acesso: {e.strerror}")

                    res = subprocess.run(
                        f'rundll32 printui.dll,PrintUIEntry /ga /n "{raw_name}"',
                        shell=True,
                        capture_output=True,
                        text=True,
                    )
                    if res.returncode != 0:
                        raise Exception(
                            f"Falha na instrução do Windows (Cod: {res.returncode})"
                        )
                else:
                    win32print.AddPrinterConnection(raw_name)
                successes.append(raw_name)
            except pywintypes.error as e:
                errors.append(f"{raw_name} ({e.strerror})")
            except Exception as e:
                errors.append(f"{raw_name} ({str(e)})")

        if successes:
            TaskLogger.log(
                tr("task_install"),
                "status_ok",
                f"{len(successes)} {tr('target_devices')}",
                start_time=start_time,
                end_time=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            )
        if errors:
            TaskLogger.log(
                tr("task_install"),
                "status_err",
                f"{len(errors)} {tr('target_devices')}",
                start_time=start_time,
                end_time=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            )

        if successes and not errors:
            QMessageBox.information(
                self,
                tr("msg_success"),
                tr("msg_install_batch_success") + "\n\n" + "\n".join(successes),
            )
        elif errors and not successes:
            QMessageBox.warning(
                self,
                tr("msg_error"),
                tr("msg_install_fail").format(errors="\n".join(errors)),
            )
        elif successes and errors:
            QMessageBox.warning(
                self,
                tr("msg_warning"),
                tr("msg_install_partial").format(successes="\n".join(successes), errors="\n".join(errors)),
            )

        self.refresh_all_data()

    def action_test_printers(self):
        idx = self.stacked.currentIndex()
        if idx == 0:
            table_ref = self.table_disp
        elif idx == 1:
            table_ref = self.table_instaladas
        else:
            return
        count = 0
        for row in range(table_ref.rowCount()):
            chk_widget = table_ref.cellWidget(row, 0)
            if chk_widget and chk_widget.layout().itemAt(0).widget().isChecked():
                raw_name = table_ref.item(row, 1).data(Qt.ItemDataRole.UserRole)
                try:
                    subprocess.Popen(
                        f'rundll32 printui.dll,PrintUIEntry /k /n "{raw_name}"',
                        shell=True,
                    )
                except:
                    pass
                count += 1
        if count > 0:
            TaskLogger.log(tr("task_print_test"), "status_ok", f"{count} {tr('target_devices')}")
            msg = tr("msg_test_batch_success").replace("{count}", str(count))
            QMessageBox.information(self, tr("msg_success"), msg)

    def action_purge_printers(self):
        idx = self.stacked.currentIndex()
        if idx == 0:
            table_ref = self.table_disp
        elif idx == 1:
            table_ref = self.table_instaladas
        else:
            return
        count = 0
        for row in range(table_ref.rowCount()):
            chk_widget = table_ref.cellWidget(row, 0)
            if chk_widget and chk_widget.layout().itemAt(0).widget().isChecked():
                raw_name = table_ref.item(row, 1).data(Qt.ItemDataRole.UserRole)
                self.purge_printer_silent(raw_name)
                count += 1
        if count > 0:
            TaskLogger.log(tr("task_purge_queues"), "status_ok", f"{count} {tr('target_devices')}")
            msg = tr("msg_purge_batch_success").replace("{count}", str(count))
            QMessageBox.information(self, tr("msg_success"), msg)
            self.refresh_all_data()

    def action_remove_printers(self):
        idx = self.stacked.currentIndex()
        if idx == 0:
            table_ref = self.table_disp
        elif idx == 1:
            table_ref = self.table_instaladas
        else:
            return
        
        count = 0
        for row in range(table_ref.rowCount()):
            chk_widget = table_ref.cellWidget(row, 0)
            if chk_widget and chk_widget.layout().itemAt(0).widget().isChecked():
                count += 1
                
        reply = QMessageBox.question(
            self,
            tr("msg_warning"),
            tr("msg_remove_batch_confirm").replace("{count}", str(count)),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return
            
        start_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        for row in range(table_ref.rowCount()):
            chk_widget = table_ref.cellWidget(row, 0)
            if chk_widget and chk_widget.layout().itemAt(0).widget().isChecked():
                raw_name = table_ref.item(row, 1).data(Qt.ItemDataRole.UserRole)
                self.remove_printer_silent(raw_name)
                
        if count > 0:
            TaskLogger.log(
                tr("task_remove"),
                "status_ok",
                f"{count} {tr('target_devices')}",
                start_time=start_time,
                end_time=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            )
            QMessageBox.information(self, tr("msg_success"), tr("msg_remove_batch_success"))
            self.refresh_all_data()

    def purge_printer_silent(self, printer_name):
        try:
            defaults = {"DesiredAccess": win32print.PRINTER_ALL_ACCESS}
            handle = win32print.OpenPrinter(printer_name, defaults)
            win32print.SetPrinter(handle, 0, None, win32print.PRINTER_CONTROL_PURGE)
            win32print.ClosePrinter(handle)
        except:
            pass

    def remove_printer_silent(self, printer_name):
        try:
            win32print.DeletePrinterConnection(printer_name)
        except:
            pass

    def reinstall_printer(self, printer_name):
        start_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        try:
            win32print.DeletePrinterConnection(printer_name)
            win32print.AddPrinterConnection(printer_name)
            TaskLogger.log(
                tr("ctx_reinstall"),
                "status_ok",
                printer_name,
                start_time=start_time,
                end_time=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            )
            QMessageBox.information(
                self, tr("msg_success"), tr("msg_success")
            )
            self.refresh_all_data()
        except Exception as e:
            TaskLogger.log(
                tr("ctx_reinstall"),
                "status_err",
                printer_name,
                start_time=start_time,
                end_time=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            )
            QMessageBox.warning(self, tr("msg_error"), f"Erro na reinstalação: {e}")

    def choose_custom_icon(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            tr("cfg_icon_custom"),
            "",
            "Image Files (*.png *.jpg *.jpeg *.ico *.svg)",
        )
        if file_path:
            icons_dir = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "icons"
            )
            os.makedirs(icons_dir, exist_ok=True)
            dest_path = os.path.join(icons_dir, os.path.basename(file_path))
            try:
                shutil.copy2(file_path, dest_path)
                self.config["app_icon_type"] = "custom"
                self.config["app_icon_val"] = dest_path
                self.update_sidebar_logo()
                self.retranslate_ui()
                QMessageBox.information(
                    self,
                    tr("msg_success"),
                    tr("msg_icon_copied"),
                )
            except Exception as e:
                QMessageBox.warning(self, tr("msg_error"), f"Erro ao copiar ícone: {e}")

    # ================= AÇÕES DE CONTEXTO =================

    def handle_table_double_click(self, item):
        table = item.tableWidget()
        row = item.row()
        if table in [self.table_disp, self.table_instaladas]:
            raw_name_item = table.item(row, 1)
            if raw_name_item:
                raw_name = raw_name_item.data(Qt.ItemDataRole.UserRole)
                if raw_name:
                    self.open_properties(raw_name)

    def show_context_menu(self, pos, table_widget):
        item = table_widget.itemAt(pos)
        if not item:
            return
        row = item.row()
        table_widget.selectRow(row)

        menu = QMenu(self)
        menu.setProperty("class", "WinUIContextMenu")

        cell_text = item.toolTip() if item.toolTip() else item.text()
        act_copy = QAction(
            qta.icon("mdi6.content-copy", color=self.text_main), tr("ctx_copy"), self
        )
        act_copy.triggered.connect(lambda: QApplication.clipboard().setText(cell_text))
        menu.addAction(act_copy)

        if table_widget in [self.table_disp, self.table_instaladas]:
            raw_name = table_widget.item(row, 1).data(Qt.ItemDataRole.UserRole)
            if raw_name:
                menu.addSeparator()
                act_props = QAction(
                    qta.icon("mdi6.cogs", color=self.text_main), tr("ctx_props"), self
                )
                act_props.triggered.connect(lambda: self.open_properties(raw_name))
                menu.addAction(act_props)

                act_test = QAction(
                    qta.icon("mdi6.file-document-outline", color=self.text_main),
                    tr("ctx_test"),
                    self,
                )
                act_test.triggered.connect(
                    lambda: self.print_test_page_single(raw_name)
                )
                menu.addAction(act_test)

                menu.addSeparator()

                act_reinstall = QAction(
                    qta.icon("mdi6.refresh", color=self.text_main),
                    tr("ctx_reinstall"),
                    self,
                )
                act_reinstall.triggered.connect(
                    lambda: self.reinstall_printer(raw_name)
                )
                menu.addAction(act_reinstall)

                act_purge = QAction(
                    qta.icon("mdi6.broom", color=self.text_main), tr("ctx_purge"), self
                )
                act_purge.triggered.connect(lambda: self.purge_printer_single(raw_name))
                menu.addAction(act_purge)

                act_default = QAction(
                    qta.icon("mdi6.star-outline", color=self.text_main),
                    tr("ctx_default"),
                    self,
                )
                act_default.triggered.connect(
                    lambda: self.set_default_printer(raw_name)
                )
                menu.addAction(act_default)

                act_remove = QAction(
                    qta.icon("mdi6.trash-can-outline", color=self.text_main),
                    tr("ctx_remove"),
                    self,
                )
                act_remove.triggered.connect(
                    lambda: self.remove_printer_single(raw_name)
                )
                menu.addAction(act_remove)

        menu.exec(table_widget.viewport().mapToGlobal(pos))

    def open_properties(self, printer_name):
        p_data = next(
            (p for p in self.all_printers_data if p["raw_name"] == printer_name), None
        )
        if p_data:
            dlg = PrinterPropertiesDialog(p_data, self)
            dlg.setStyleSheet(self.styleSheet())
            dlg.exec()
        else:
            try:
                subprocess.Popen(
                    f'rundll32 printui.dll,PrintUIEntry /p /n "{printer_name}"',
                    shell=True,
                )
            except Exception as e:
                TaskLogger.log(tr("ctx_props"), "status_err", str(e))

    def print_test_page_single(self, printer_name):
        start_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        try:
            subprocess.Popen(
                f'rundll32 printui.dll,PrintUIEntry /k /n "{printer_name}"', shell=True
            )
            TaskLogger.log(
                tr("task_test"),
                "status_ok",
                printer_name,
                start_time=start_time,
                end_time=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            )
        except Exception as e:
            TaskLogger.log(
                tr("task_test"),
                "status_err",
                printer_name,
                start_time=start_time,
                end_time=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            )

    def purge_printer_single(self, printer_name):
        start_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        try:
            defaults = {"DesiredAccess": win32print.PRINTER_ALL_ACCESS}
            handle = win32print.OpenPrinter(printer_name, defaults)
            win32print.SetPrinter(handle, 0, None, win32print.PRINTER_CONTROL_PURGE)
            win32print.ClosePrinter(handle)
            TaskLogger.log(
                tr("task_purge_queue"), "status_ok", printer_name, start_time=start_time
            )
            QMessageBox.information(
                self, tr("msg_success"), tr("msg_queue_purged_single").format(printer=printer_name)
            )
        except Exception as e:
            TaskLogger.log(
                tr("task_purge_queue"), "status_err", printer_name, start_time=start_time
            )
            QMessageBox.warning(self, tr("msg_error"), f"Erro: {e}")

    def set_default_printer(self, printer_name):
        try:
            win32print.SetDefaultPrinter(printer_name)
            self.default_printer = printer_name
            self.refresh_all_data_silent()
        except:
            pass

    def map_printer(self):
        text, ok = QInputDialog.getText(
            self, tr("card_map"), "IP / Path (Ex: \\\\servidor\\nome):"
        )
        if ok and text and text.startswith("\\\\"):
            start_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            try:
                win32print.AddPrinterConnection(text)
                TaskLogger.log(
                    tr("task_install"), "status_ok", text, start_time=start_time
                )
                self.refresh_all_data()
            except Exception as e:
                TaskLogger.log(
                    tr("task_install"), "status_err", text, start_time=start_time
                )

    def remove_printer_single(self, printer_name):
        reply = QMessageBox.question(
            self,
            tr("msg_warning"),
            tr("msg_remove_single_confirm"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            start_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    def reinstall_printer(self, printer_name):
        start_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        try:
            win32print.DeletePrinterConnection(printer_name)
            win32print.AddPrinterConnection(printer_name)
            TaskLogger.log(
                tr("ctx_reinstall"),
                "status_ok",
                printer_name,
                start_time=start_time,
                end_time=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            )
            QMessageBox.information(
                self, tr("msg_success"), tr("msg_reinstall_success").format(printer=printer_name)
            )
            self.refresh_all_data()
        except Exception as e:
                try:
                    defaults = {"DesiredAccess": win32print.PRINTER_ALL_ACCESS}
                    handle = win32print.OpenPrinter(printer_name, defaults)
                    win32print.DeletePrinter(handle)
                    win32print.ClosePrinter(handle)
                    TaskLogger.log(
                        tr("task_remove_single"),
                        "status_ok",
                        printer_name,
                        start_time=start_time,
                    )
                    self.refresh_all_data()
                except Exception as e2:
                    TaskLogger.log(
                        tr("task_remove_single"),
                        "status_err",
                        printer_name,
                        start_time=start_time,
                    )

    def repair_spooler(self):
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        except:
            is_admin = False
        if not is_admin:
            QMessageBox.warning(
                self, tr("msg_warning"), tr("msg_admin_req")
            )
            return
        reply = QMessageBox.question(
            self,
            tr("msg_warning"),
            tr("msg_spooler_warn"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            start_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            TaskLogger.log(
                tr("task_repair_spooler"), "status_run", tr("target_sys"), start_time=start_time
            )
            cmds = [
                "net stop spooler",
                r"del /Q /F /S %systemroot%\System32\Spool\Printers\*.*",
                "net start spooler",
            ]
            try:
                subprocess.run(
                    ["cmd.exe", "/c", " & ".join(cmds)],
                    capture_output=True,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                )
                TaskLogger.log(
                    tr("task_repair_spooler"), "status_ok", tr("target_sys"), start_time=start_time
                )
                self.refresh_all_data()
            except Exception as e:
                TaskLogger.log(
                    tr("task_repair_spooler"), "status_err", tr("target_sys"), start_time=start_time
                )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PrinterManagerApp()
    window.show()
    sys.exit(app.exec())
