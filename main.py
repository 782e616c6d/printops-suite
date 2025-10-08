import os
import json
import subprocess
import zipfile
import rarfile
import requests
import shutil
import socket
import threading
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image  # Mantido por compatibilidade
from ping3 import ping

# Importar win32print para lidar com impressoras no Windows
import win32print
import win32con

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

CONFIG_FILE = "printer_config.json"
LOG_FILE = "printer_installer.log"
DOWNLOAD_DIR = "C:\Drivers"

# Utilitários globais
downloading_set = set()


def log(msg):
    """Escreve uma mensagem no arquivo de log."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")


def is_host_online(ip):
    """Verifica se um host está online via ping ou tentativa de conexão na porta 9100."""
    try:
        response = ping(ip, timeout=1)
        if response:
            return True
    except Exception:
        pass

    try:
        socket.setdefaulttimeout(2)
        with socket.create_connection((ip, 9100), timeout=2):
            return True
    except Exception:
        return False


def extract_driver(archive_path, extract_to):
    """
    Extrai o conteúdo de um arquivo .zip, .rar ou tenta .exe como ZIP.
    Retorna True em caso de sucesso, False em caso de erro.
    """
    try:
        if archive_path.lower().endswith(".zip"):
            with zipfile.ZipFile(archive_path, "r") as zip_ref:
                zip_ref.extractall(extract_to)
            log(f"Extração ZIP de '{archive_path}' concluída para '{extract_to}'.")
            return True
        elif archive_path.lower().endswith(".rar"):
            # Certifique-se de que rarfile está configurado para encontrar o unrar.dll ou 7z.exe
            # Ex: pip install unrar-dll
            with rarfile.RarFile(archive_path, "r") as rar_ref:
                rar_ref.extractall(extract_to)
            log(f"Extração RAR de '{archive_path}' concluída para '{extract_to}'.")
            return True
        elif archive_path.lower().endswith(".exe"):
            # Tenta extrair o .exe como um ZIP autoextraível.
            # Isso só funcionará se o .exe for de fato um ZIP com um stub.
            # Para instaladores complexos (como da Brother), esta tentativa falhará.
            try:
                with zipfile.ZipFile(archive_path, "r") as zf:
                    zf.extractall(extract_to)
                log(
                    f"Extração EXE (como ZIP) de '{archive_path}' concluída para '{extract_to}'."
                )
                return True
            except zipfile.BadZipFile:
                log(
                    f"AVISO: '{archive_path}' não é um arquivo ZIP válido. Não foi possível extrair o EXE diretamente."
                )
                log(
                    "É provável que este EXE seja um instalador complexo (e.g., Inno Setup, NSIS, MSI) que requer execução ou uma ferramenta externa como 7-Zip para extração."
                )
                return False
            except Exception as e_exe:
                log(
                    f"Erro inesperado ao tentar extrair EXE (como ZIP) '{archive_path}': {e_exe}"
                )
                return False
        else:
            log(f"Formato de arquivo não suportado para extração: {archive_path}")
            return False
    except Exception as e:
        log(f"Erro geral ao extrair driver '{archive_path}': {e}")
        return False


def download_driver(url, model_folder, callback=None):
    """
    Baixa um arquivo de driver de uma URL, o salva na pasta de download,
    e tenta extraí-lo.
    """
    if url in downloading_set:
        log(
            f"Download para '{url}' já está em andamento. Ignorando solicitação duplicada."
        )
        return

    downloading_set.add(url)
    log(f"Iniciando download para: {url}")

    def _download():
        local_filename = url.split("/")[-1]

        # A pasta específica para o modelo dentro de DOWNLOAD_DIR
        model_download_extract_path = os.path.join(DOWNLOAD_DIR, model_folder)
        # O caminho final do arquivo baixado dentro da pasta do modelo
        download_path = os.path.join(model_download_extract_path, local_filename)

        try:
            # Garante que a pasta específica do modelo existe
            os.makedirs(model_download_extract_path, exist_ok=True)

            # Baixa o arquivo
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()

            total_size = int(response.headers.get("content-length", 0))
            downloaded = 0

            with open(download_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
            log(f"Download de '{local_filename}' concluído em '{download_path}'.")

            # Após o download, tenta extrair o driver
            if not extract_driver(download_path, model_download_extract_path):
                log(f"Não foi possível extrair o conteúdo de '{download_path}'.")
                messagebox.showwarning(
                    "Aviso de Extração",
                    f"O arquivo '{local_filename}' não pôde ser extraído automaticamente.\n"
                    "Se for um instalador .exe, ele pode precisar ser executado para instalar o driver.\n"
                    f"Você pode tentar executá-lo manualmente de: {download_path}",
                )

            if callback:
                callback(success=True)

        except requests.exceptions.Timeout:
            log(f"Erro de timeout ao baixar driver: {url}")
            messagebox.showerror(
                "Erro de Download",
                f"O download de '{local_filename}' excedeu o tempo limite. Verifique sua conexão ou a URL.",
            )
            if callback:
                callback(success=False)
        except requests.exceptions.RequestException as e:
            log(f"Erro de requisição ao baixar driver: {e}")
            messagebox.showerror(
                "Erro de Download", f"Erro ao baixar '{local_filename}': {e}"
            )
            if callback:
                callback(success=False)
        except Exception as e:
            log(f"Erro inesperado ao baixar ou processar driver: {e}")
            messagebox.showerror(
                "Erro Inesperado",
                f"Ocorreu um erro inesperado ao baixar/processar '{local_filename}': {e}",
            )
            if callback:
                callback(success=False)

        finally:
            downloading_set.discard(url)
            log(f"Download para '{url}' finalizado.")

    threading.Thread(target=_download, daemon=True).start()


def install_printer(name, ip, driver_name, driver_inf):
    """Instala uma impressora usando rundll32 printui.dll."""
    cmd = [
        "rundll32",
        "printui.dll,PrintUIEntry",
        "/if",  # Instalar driver
        "/b",  # Nome da impressora
        name,
        "/f",  # Caminho para o arquivo .inf do driver
        driver_inf,
        "/r",  # Nome da porta (IP_xxxx)
        f"IP_{ip}",
        "/m",  # Nome do modelo do driver
        driver_name,
        "/z",  # Para que a impressora seja padrão (se for a primeira)
    ]
    try:
        log(f"Tentando instalar impressora: {' '.join(cmd)}")
        subprocess.run(cmd, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        log(f"Impressora instalada com sucesso: {name} - {ip}")
        messagebox.showinfo("Sucesso", f"Impressora '{name}' instalada com sucesso.")
    except subprocess.CalledProcessError as e:
        log(
            f"Erro no subprocesso ao instalar {name}: {e}\nSTDOUT: {e.stdout}\nSTDERR: {e.stderr}"
        )
        messagebox.showerror(
            "Erro de Instalação",
            f"Erro ao instalar {name}\n{e}\nVerifique o log para mais detalhes.",
        )
    except Exception as e:
        log(f"Erro geral ao instalar {name}: {e}")
        messagebox.showerror(
            "Erro de Instalação", f"Erro inesperado ao instalar {name}\n{e}"
        )


def uninstall_printer(name):
    """Desinstala uma impressora usando rundll32 printui.dll."""
    cmd = ["rundll32", "printui.dll,PrintUIEntry", "/dl", "/n", name]
    try:
        log(f"Tentando desinstalar impressora: {' '.join(cmd)}")
        subprocess.run(cmd, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        log(f"Impressora desinstalada com sucesso: {name}")
        messagebox.showinfo("Sucesso", f"Impressora '{name}' desinstalada com sucesso.")
    except subprocess.CalledProcessError as e:
        log(
            f"Erro no subprocesso ao desinstalar {name}: {e}\nSTDOUT: {e.stdout}\nSTDERR: {e.stderr}"
        )
        messagebox.showerror(
            "Erro de Desinstalação",
            f"Erro ao desinstalar {name}\n{e}\nVerifique o log para mais detalhes.",
        )
    except Exception as e:
        log(f"Erro geral ao desinstalar {name}: {e}")
        messagebox.showerror(
            "Erro de Desinstalação", f"Erro inesperado ao desinstalar {name}\n{e}"
        )


def get_installed_printers_details():
    """
    Detecta e retorna detalhes de impressoras instaladas (Nome, Tipo, Porta/IP, Driver).
    Retorna uma lista de dicionários.
    """
    printers_list = []
    try:
        # Get list of printer names
        printers = win32print.EnumPrinters(
            win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
        )

        for flags, description, name, comment in printers:
            printer_info = {
                "name": name,
                "type": "Desconhecido",
                "port": "N/A",
                "driver": "N/A",
            }
            try:
                # Get more detailed info for each printer
                phandle = win32print.OpenPrinter(name)
                details = win32print.GetPrinter(
                    phandle, 2
                )  # Level 2 provides more info

                # Extract port name
                port_name = details["pPortName"]
                printer_info["port"] = port_name

                # Extract driver name
                driver_name = details["pDriverName"]
                printer_info["driver"] = driver_name

                # Determine type (USB vs. Network)
                if port_name.startswith("USB") or port_name.startswith("DOT4"):
                    printer_info["type"] = "USB"
                    # For USB, we might want to try to get status (e.g., online/offline)
                    # This often requires WMI or specific device API calls, which is more complex.
                    # For simplicity, we'll just show "Status: N/A" or "Online/Offline" if a more complex check is added.
                elif (
                    port_name.lower().startswith("ip_") or ":" in port_name
                ):  # IP_xxx or Standard TCP/IP Port with IP
                    printer_info["type"] = "Rede"
                    # Try to parse IP from port name
                    if port_name.lower().startswith("ip_"):
                        ip_address = port_name[3:]
                    elif ":" in port_name:  # Handle Standard TCP/IP ports
                        try:
                            # This part is tricky. Standard TCP/IP ports might have complex names like "IP_192.168.1.10" or "WSD-..."
                            # We can try to extract IP if it's clearly an IP address.
                            # More reliably, use WMI to get the port details.
                            # For now, let's assume if it contains digits and dots, it's an IP
                            ip_candidates = [
                                p
                                for p in port_name.split(":")
                                if "." in p and p.count(".") == 3
                            ]
                            ip_address = ip_candidates[0] if ip_candidates else "N/A"
                        except Exception:
                            ip_address = "N/A"
                    else:
                        ip_address = "N/A"

                    printer_info["port"] = f"IP: {ip_address}"
                else:
                    printer_info["type"] = "Outro"  # LPT, COM, WSD, etc.

                win32print.ClosePrinter(phandle)

            except Exception as e:
                log(f"Erro ao obter detalhes da impressora '{name}': {e}")
                # Keep partial info if details retrieval fails
            printers_list.append(printer_info)

    except Exception as e:
        log(f"Erro ao enumerar impressoras: {e}")
        messagebox.showerror(
            "Erro de Leitura", f"Não foi possível listar impressoras instaladas: {e}"
        )

    return printers_list


class PrinterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gerenciador de Impressoras")
        self.geometry("970x750")  # Aumentado o tamanho para acomodar a nova aba
        self.resizable(False, False)

        logo = ctk.CTkLabel(
            self,
            text="\U0001f5a8\ufe0f Impressoras - Instalação/Remoção",
            font=("Arial", 24, "bold"),
        )
        logo.pack(pady=15)

        # Criar as abas
        self.tab_view = ctk.CTkTabview(
            self, width=950, height=550
        )  # Ajuste a altura conforme necessário
        self.tab_view.pack(pady=10)

        self.tab_view.add("Instalar/Remover")
        self.tab_view.add("Impressoras Instaladas")

        # --- Conteúdo da Aba "Instalar/Remover" ---
        self.install_remove_frame = self.tab_view.tab("Instalar/Remover")

        header_frame_install = ctk.CTkFrame(self.install_remove_frame)
        header_frame_install.pack(pady=5)

        ctk.CTkLabel(
            header_frame_install,
            text="Modelo",
            width=240,
            anchor="w",
            font=("Arial", 14, "bold"),
        ).grid(row=0, column=0)
        ctk.CTkLabel(
            header_frame_install,
            text="IP",
            width=150,
            anchor="w",
            font=("Arial", 14, "bold"),
        ).grid(row=0, column=1)
        ctk.CTkLabel(
            header_frame_install,
            text="Status",
            width=100,
            anchor="w",
            font=("Arial", 14, "bold"),
        ).grid(row=0, column=2)
        ctk.CTkLabel(
            header_frame_install,
            text="Ações",
            width=400,
            anchor="center",
            font=("Arial", 14, "bold"),
        ).grid(row=0, column=3)

        self.install_container = ctk.CTkScrollableFrame(
            self.install_remove_frame, width=920, height=380
        )  # Ajuste a altura
        self.install_container.pack(pady=10)

        footer_install = ctk.CTkFrame(self.install_remove_frame)
        footer_install.pack(pady=8)

        ctk.CTkButton(
            footer_install, text="Atualizar Lista", command=self.populate_install_tab
        ).pack(side="left", padx=5)
        ctk.CTkButton(
            footer_install,
            text="Abrir Pasta de Drivers",
            command=self.open_driver_folder,
        ).pack(side="left", padx=5)

        # --- Conteúdo da Aba "Impressoras Instaladas" ---
        self.installed_printers_frame = self.tab_view.tab("Impressoras Instaladas")

        header_installed = ctk.CTkFrame(self.installed_printers_frame)
        header_installed.pack(pady=5)

        ctk.CTkLabel(
            header_installed,
            text="Nome",
            width=300,
            anchor="w",
            font=("Arial", 14, "bold"),
        ).grid(row=0, column=0)
        ctk.CTkLabel(
            header_installed,
            text="Tipo",
            width=100,
            anchor="w",
            font=("Arial", 14, "bold"),
        ).grid(row=0, column=1)
        ctk.CTkLabel(
            header_installed,
            text="Porta/IP",
            width=200,
            anchor="w",
            font=("Arial", 14, "bold"),
        ).grid(row=0, column=2)
        ctk.CTkLabel(
            header_installed,
            text="Driver",
            width=250,
            anchor="w",
            font=("Arial", 14, "bold"),
        ).grid(row=0, column=3)

        self.installed_printers_container = ctk.CTkScrollableFrame(
            self.installed_printers_frame, width=920, height=380
        )  # Ajuste a altura
        self.installed_printers_container.pack(pady=10)

        footer_installed = ctk.CTkFrame(self.installed_printers_frame)
        footer_installed.pack(pady=8)
        ctk.CTkButton(
            footer_installed,
            text="Atualizar Impressoras Instaladas",
            command=self.populate_installed_printers,
        ).pack(side="left", padx=5)

        # Define a aba padrão
        self.tab_view.set("Instalar/Remover")

        # Popula ambas as abas ao iniciar
        self.populate_install_tab()
        self.populate_installed_printers()  # Adiciona a chamada para popular a nova aba

    def open_driver_folder(self):
        """Abre a pasta de downloads de drivers no explorador de arquivos."""
        if os.path.exists(DOWNLOAD_DIR):
            try:
                os.startfile(DOWNLOAD_DIR)
            except Exception as e:
                messagebox.showerror(
                    "Erro", f"Não foi possível abrir a pasta de drivers: {e}"
                )
        else:
            messagebox.showinfo(
                "Aviso", f"A pasta de drivers '{DOWNLOAD_DIR}' ainda não foi criada."
            )

    def populate_install_tab(self):
        """Popula a aba 'Instalar/Remover' com as informações das impressoras."""
        for widget in self.install_container.winfo_children():
            widget.destroy()

        try:
            with open(CONFIG_FILE, encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            messagebox.showerror(
                "Erro",
                f"Arquivo de configuração '{CONFIG_FILE}' não encontrado. Crie-o ou verifique o caminho.",
            )
            log(f"Erro: Arquivo de configuração '{CONFIG_FILE}' não encontrado.")
            return
        except json.JSONDecodeError as e:
            messagebox.showerror(
                "Erro", f"Erro ao decodificar JSON no arquivo de configuração:\n{e}"
            )
            log(f"Erro ao decodificar JSON: {e}")
            return
        except Exception as e:
            messagebox.showerror(
                "Erro", f"Erro ao carregar arquivo de configuração:\n{e}"
            )
            log(f"Erro geral ao carregar config: {e}")
            return

        row = 0
        for model, info in data.items():
            driver_name = info["driver_name"]

            # Ajuste aqui para garantir que o driver_file seja o caminho completo dentro da pasta do modelo
            driver_filename_only = os.path.basename(info["driver_file"])
            driver_inf_path = os.path.join(DOWNLOAD_DIR, model, driver_filename_only)

            driver_url = info["driver_url"]

            for instance in info["instances"]:
                name = instance["name"]
                ip = instance["ip"]
                # Inicia a verificação de status em uma thread para não travar a GUI
                status_label = ctk.CTkLabel(
                    self.install_container, text="Verificando...", width=100
                )
                status_label.grid(row=row, column=2, padx=5)
                threading.Thread(
                    target=self._update_status_label,
                    args=(ip, status_label),
                    daemon=True,
                ).start()

                ctk.CTkLabel(
                    self.install_container, text=name, width=240, anchor="w"
                ).grid(row=row, column=0, padx=5, pady=5)
                ctk.CTkLabel(
                    self.install_container, text=ip, width=150, anchor="w"
                ).grid(row=row, column=1, padx=5)
                # O status_label já foi criado e posicionado

                actions = ctk.CTkFrame(self.install_container)
                actions.grid(row=row, column=3, padx=5, pady=5)

                def make_callback(
                    n=name,
                    i=ip,
                    dn=driver_name,
                    df=driver_inf_path,
                    du=driver_url,
                    m=model,
                ):
                    return lambda: self.handle_install(n, i, dn, df, du, m)

                ctk.CTkButton(actions, text="Instalar", command=make_callback()).pack(
                    side="left", padx=2
                )
                ctk.CTkButton(
                    actions,
                    text="Desinstalar",
                    command=lambda n=name: uninstall_printer(n),
                ).pack(side="left", padx=2)
                ctk.CTkButton(
                    actions,
                    text="Baixar Driver",
                    command=lambda u=driver_url, m=model: download_driver(u, m),
                ).pack(side="left", padx=2)

                row += 1

    def populate_installed_printers(self):
        """Popula a aba 'Impressoras Instaladas' com as impressoras detectadas."""
        for widget in self.installed_printers_container.winfo_children():
            widget.destroy()

        printers_data = get_installed_printers_details()

        if not printers_data:
            ctk.CTkLabel(
                self.installed_printers_container,
                text="Nenhuma impressora instalada encontrada ou erro ao listar.",
                font=("Arial", 12),
            ).pack(pady=20)
            return

        row = 0
        for printer in printers_data:
            ctk.CTkLabel(
                self.installed_printers_container,
                text=printer["name"],
                width=300,
                anchor="w",
            ).grid(row=row, column=0, padx=5, pady=2)
            ctk.CTkLabel(
                self.installed_printers_container,
                text=printer["type"],
                width=100,
                anchor="w",
            ).grid(row=row, column=1, padx=5, pady=2)
            ctk.CTkLabel(
                self.installed_printers_container,
                text=printer["port"],
                width=200,
                anchor="w",
            ).grid(row=row, column=2, padx=5, pady=2)
            ctk.CTkLabel(
                self.installed_printers_container,
                text=printer["driver"],
                width=250,
                anchor="w",
            ).grid(row=row, column=3, padx=5, pady=2)
            row += 1

    def _update_status_label(self, ip, label):
        """Atualiza o status de uma impressora na GUI (executado em thread)."""
        status = "Online" if is_host_online(ip) else "Offline"
        status_color = "green" if status == "Online" else "red"
        # Usar after() para atualizar a GUI na thread principal
        self.after(0, lambda: label.configure(text=status, text_color=status_color))

    def handle_install(self, name, ip, driver_name, driver_inf_path, driver_url, model):
        """
        Lida com o processo de instalação: verifica o driver e o baixa se necessário,
        depois inicia a instalação da impressora.
        """
        # Verifica se a pasta do modelo existe e se o arquivo .inf está lá
        model_driver_folder = os.path.dirname(driver_inf_path)

        # O arquivo INF pode estar diretamente na pasta do modelo OU em uma subpasta de extração
        # Ex: C:/Drivers/Brother_1212W/brother1212.inf
        # Ou C:/Drivers/Brother_1212W/Win64/brh1210.inf

        # Precisamos de uma forma mais robusta de encontrar o INF
        found_inf = None
        if os.path.exists(model_driver_folder):
            # Procura pelo arquivo INF na pasta do modelo e suas subpastas
            for root, _, files in os.walk(model_driver_folder):
                if os.path.basename(driver_inf_path) in files:
                    found_inf = os.path.join(root, os.path.basename(driver_inf_path))
                    break

        if not found_inf:
            resp = messagebox.askyesno(
                "Driver ausente",
                f"O driver para '{name}' (arquivo .inf: '{os.path.basename(driver_inf_path)}') não foi encontrado na pasta esperada:\n'{model_driver_folder}'\n\nDeseja baixá-lo agora?",
            )
            if resp:
                download_driver(
                    driver_url,
                    model,  # Passa o nome do modelo para criar a subpasta correta
                    callback=lambda success: self.post_download_install(
                        success, name, ip, driver_name, driver_inf_path
                    ),
                )
            return

        # Se o driver já existe e foi encontrado, procede com a instalação
        threading.Thread(
            target=install_printer,
            args=(name, ip, driver_name, found_inf),  # Usar o caminho real encontrado
            daemon=True,
        ).start()

    def post_download_install(
        self, success, name, ip, driver_name, original_driver_inf_path_from_config
    ):
        """
        Callback executado após o download do driver. Se bem-sucedido,
        tenta encontrar o arquivo .inf e inicia a instalação da impressora.
        """
        if success:
            model_driver_folder = os.path.dirname(original_driver_inf_path_from_config)
            expected_inf_filename = os.path.basename(
                original_driver_inf_path_from_config
            )

            found_inf = None
            if os.path.exists(model_driver_folder):
                for root, _, files in os.walk(model_driver_folder):
                    if expected_inf_filename in files:
                        found_inf = os.path.join(root, expected_inf_filename)
                        break

            if found_inf:
                messagebox.showinfo(
                    "Download Concluído",
                    f"Driver para '{name}' baixado e .inf encontrado! Iniciando instalação...",
                )
                threading.Thread(
                    target=install_printer,
                    args=(name, ip, driver_name, found_inf),
                    daemon=True,
                ).start()
            else:
                messagebox.showwarning(
                    "Aviso de Instalação",
                    f"O download do driver para '{name}' foi concluído, mas o arquivo INF esperado '{expected_inf_filename}' não foi encontrado na pasta '{model_driver_folder}' ou suas subpastas após a extração.\n"
                    "Isso pode indicar que o arquivo EXE não foi extraído corretamente, ou o INF tem um nome diferente, ou está em um local inesperado.\n"
                    "Você precisará verificar manualmente a pasta do driver para encontrar o INF correto.",
                )
                log(
                    f"AVISO: {expected_inf_filename} não encontrado em {model_driver_folder} após download/extração para {name}."
                )

        else:  # not success
            messagebox.showerror(
                "Erro de Download",
                f"Não foi possível baixar o driver para '{name}'. Por favor, tente novamente ou verifique o log.",
            )


if __name__ == "__main__":
    # Garante que a pasta de download raiz existe ao iniciar o app
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    app = PrinterApp()
    app.mainloop()
