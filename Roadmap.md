🚀 Roadmap de Arquitetura e Evolução (PrintOps Suite)
​Este documento mapeia as próximas evoluções arquiteturais e funcionais do sistema. O objetivo principal é escalar a aplicação para ambientes corporativos complexos, garantindo segurança, facilidade de manutenção do código-fonte (S.O.L.I.D) e fornecendo telemetria avançada de hardware.
​🛠️ Fase 0: Segurança, Qualidade de Código e Refatoração Base
​Ações imediatas para corrigir vulnerabilidades, preparar o terreno para as novas funcionalidades e limpar o ficheiro principal.
​Segurança em Subprocessos (Remoção do shell=True):
​Problema: O uso atual de shell=True com strings formatadas (ex: f'rundll32 printui.dll,PrintUIEntry /ga /n "{raw_name}"') abre brechas severas para injeção de comandos no Windows.
​Solução: Refatorar todas as chamadas do módulo subprocess para utilizar listas de argumentos explícitos e check=True.
​Exemplo: subprocess.run(["rundll32.exe", "printui.dll,PrintUIEntry", "/ga", "/n", raw_name], check=True)
​Sistema de Idiomas (i18n):
​Problema: O dicionário TRANSLATIONS consome centenas de linhas no código principal, poluindo o ficheiro e dificultando a adição de novos idiomas.
​Solução: Migrar a internacionalização para ficheiros externos. Utilizar a abordagem nativa do Qt (ficheiros .ts e .qm com QTranslator) ou guardar os dicionários em ficheiros JSON separados (ex: /locales/pt_PT.json, /locales/en_US.json).
​Tipagem (Type Hinting) e PEP 8:
​Implementar "Type Hints" do Python nas funções principais para maior clareza e prevenção de erros via IDE.
​Exemplo: def get_manufacturer(driver_name: str) -> str:
​Reestruturação de Configurações e Nomenclatura:
​Isolar ficheiros de configuração administrativos (servers.json, ui_tabs_config.json) numa nova subpasta /Configuration no diretório raiz da app.
​Manter preferências do utilizador (user_preferences_config.json) no %APPDATA%.
​Renomear o separador/aba atual "Dispositivos de Rede" para "Impressoras em Servidor".
​🏗️ Fase 1: Separação de Responsabilidades (Arquitetura Modular)
​Desmembramento do código monolítico atual (>1.000 linhas na classe PrinterManagerApp) aplicando o princípio Separation of Concerns (SoC) e conceitos de MVC/MVVM.
​Nova Estrutura de Diretórios: O código será dividido em pacotes lógicos:
​📂 core/ -> Configurações globais, gestor de logs (logger.py), utilitários de sistema.
​📂 services/ -> Regras de negócio e comunicação com o SO. Ex: printer_service.py (isolando totalmente a biblioteca win32print), network_service.py.
​📂 ui/ -> Interface gráfica pura.
​main_window.py (Apenas o esqueleto da janela principal).
​📂 views/ -> As páginas individuais (devices_view.py, tasks_view.py).
​📂 components/ -> Widgets reutilizáveis (action_card.py, nav_button.py).
​Lazy Loading (Carregamento sob Demanda): Com o uso do QStackedWidget, a MainWindow irá instanciar as views apenas quando o utilizador clicar no separador pela primeira vez, reduzindo o tempo de arranque (startup) e o consumo de RAM.
​Comunicação Desacoplada: Utilização massiva de Signals e Slots do PyQt para que a interface (UI) não chame diretamente os serviços, mas sim reaja às emissões de estado.
​📡 Fase 2: Escaneamento Avançado de Rede (Network IP Scanner)
​Criação de um separador focado na descoberta (Discovery) de hardware físico, semelhante ao BRAdmin da Brother.
​Varredura Local e Personalizada: Detecção na sub-rede atual (ex: 192.168.0.0/24) via multicast/RAW port, além de permitir notação CIDR manual para procurar noutras VLANs e filiais.
​Métricas de Hardware (SNMP v1/v2c/v3): Consulta direta ao IP das impressoras para obter dados que o Spooler do Windows não fornece:
​Modelo real da máquina, Fabricante e MAC Address.
​Níveis exatos de suprimentos (Toner, Tambor, Bandejas de Papel).
​Assincronicidade e Persistência: As varreduras vão correr em Background Threads (QThreadPool). Os dispositivos detetados serão guardados numa base de dados local (ex: SQLite) para permitir filtros inteligentes e refresh automático.
​🖨️ Fase 3: Controlos Estendidos e Granulares de Fila/Hardware
​Aprofundamento da integração com o Windows e controlo de rede.
​Gestão de Jobs Individuais: Em vez de apenas "Limpar Fila" (Purge), a aplicação listará os documentos em curso (via EnumJobs). O utilizador poderá colocar em pausa, retomar, cancelar ou alterar a prioridade de impressões específicas.
​Interface Web Embutida (EWS View): Utilização do QWebEngineView para abrir a interface web nativa de administração da impressora diretamente dentro do painel da aplicação.
​Ações Remotas Avançadas: Comandos SNMP para reinicialização física (Reboot) do hardware e capacidade de deploy remoto de ficheiros de driver (.inf) via app.
​📊 Fase 4: Dashboards Analíticos e Relatórios Inteligentes
​Transformação de dados operacionais em inteligência visual.
​Painel Visual (Dashboard Home): Utilização de PyQtGraph (ou ECharts embutido) para:
​Gráficos de disponibilidade (Online vs. Offline).
​Distribuição da frota por fabricante/modelo.
​Ranking de impressoras com maior incidência de erros.
​Relatórios Corporativos (PDF): Substituição do CSV básico por relatórios em PDF ricamente formatados (via ReportLab ou pandas), ideais para prestação de contas e SLA.
​Auditoria: Sistema de logs com filtros por data, ação, utilizador ativo e severidade.