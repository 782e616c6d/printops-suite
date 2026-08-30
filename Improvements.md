# 🚀 Roadmap de Desenvolvimento e Melhorias Futuras

Este documento mapeia as próximas evoluções arquiteturais e funcionais do sistema, visando escalar a aplicação para ambientes de infraestrutura de TI mais complexos e facilitar a manutenção do código-fonte.

Separar e criar novos arquivos de configuração ex: ".json" e etc, a medida do necessário, armazenando em uma subpasta chamada Configuration no mesmo local do app. Para as que o usuário tem poder de edição armazenar no %APPDATA% (Verificar se esta é a abordagem ideal para arquivos de configuração que o usuário possa editar, mas por enquanto vamos seguir com esta).

Adicionar método de verificação de modelos de impressora semelhante ao app BR Admin da Brother para a aba de impressoras detectadas via print servers, além de métricas como nível/níveis de tinta.

## 📡 1. Escaneamento Avançado de Rede (Network IP Scanner)
Expansão das capacidades de descoberta de dispositivos (Discovery), permitindo mapear impressoras físicas não listadas no Spooler local ou no Servidor de Impressão, utilizando protocolos como SNMP (v1/v2c/v3) e portas RAW (9100).

*   **Varredura na Rede Atual:** Detecção automática da sub-rede do host local (ex: `192.168.0.0/24`) utilizando *multicast* ou varredura ARP para identificar hardware de impressão.
*   **Varredura por Faixa Específica (Custom Range):** Capacidade de input de notação CIDR ou faixa inicial/final de IPs para vasculhar impressoras em VLANs específicas de outras filiais ou andares.
*   **Consulta Direta (Single IP/Hostname):** Ferramenta de *ping/query* profundo para um IP individual, trazendo modelo, fabricante, MAC Address e status de suprimentos.
*   **Assincronicidade:** Implementação do scanner em *Background Threads* (QThreadPool) com barra de progresso real, garantindo que a interface não congele durante varreduras em ranges amplos.

*   **Permitir refresh automático de scan, esta aba deve ser separada das impressoras mapeadas por servidor, já que podem haver redundância e talvez incompatibilidade.
*   ** Aproveitar ao máximo esta funcionalidade para implementar e agregar o máximo de informações disponíveis possíveis sobre as impressoras. Assim como a aplicação BR Admin4 da Brother.

## 🏗️ 2. Modularização da Arquitetura (Micro-Frontends / Módulos)
Refatoração do código monolítico atual (onde todas as telas residem no arquivo principal) para uma arquitetura baseada em componentes acoplados via injeção de dependências ou *Signals/Slots* dinâmicos.

*   **Separação por Contexto:** Cada aba do menu lateral (Dispositivos de Rede, Dispositivos Locais, Drivers, Tasks, etc.) será convertida em um pacote Python isolado (`/modules/network`, `/modules/drivers`).
*   **Lazy Loading (Carregamento sob Demanda):** A interface principal instanciará as telas apenas quando o usuário clicar na aba pela primeira vez, reduzindo drasticamente o consumo de memória RAM e o tempo de inicialização (startup) do aplicativo.
*   **Facilidade de Extensão (Plugins):** Arquitetura desenhada para permitir que novas funcionalidades (como um futuro módulo de Active Directory) sejam plugadas adicionando apenas um novo arquivo na pasta de módulos, sem alterar a lógica do `MainWindow`.

## 📊 3. Dashboards Analíticos e Relatórios Inteligentes
Transformação de dados brutos (logs e status) em inteligência operacional e visual para líderes de TI e analistas de infraestrutura.

*   **Painel Visual (Dashboard UI):** Criação de uma aba inicial (Home) utilizando bibliotecas de plotagem (como `PyQtGraph` ou integração com HTML/JS via `QWebEngineView`) para exibir:
    *   Gráficos de pizza com o percentual de frota Online vs. Offline.
    *   Topologia de fabricantes (Ex: 40% HP, 30% Kyocera, 30% Zebra).
    *   Gráfico de barras com as impressoras que mais apresentam erros diários.
*   **Geração de Relatórios (PDF/Excel):** Exportação robusta de inventário e SLA de disponibilidade. Transição de relatórios em CSV simples para PDFs formatados corporativamente com tabelas ricas, utilizando bibliotecas como `ReportLab` ou `pandas`.
*   **Alertas:** Histórico de logs exportáveis com filtros por período e severidade (Critical, Warning, Info).

## 🖨️ 4. Controles Estendidos e Granulares de Hardware/Fila
Aprofundamento da integração com a API do Windows (`win32print`) e protocolos de rede para oferecer microgerenciamento das filas de impressão e dos dispositivos físicos.

*   **Gerenciamento de Jobs Individuais:** Em vez de apenas "Limpar toda a Fila" (Purge), permitir a visualização da fila atual em tempo real. O usuário poderá pausar, retomar, cancelar ou alterar a prioridade de documentos específicos que estão travando a fila.
*   **Interface Web Embutida (EWS View):** Utilização do `QWebEngineView` para abrir a interface web nativa da impressora diretamente dentro do painel lateral direito do aplicativo, eliminando a necessidade de abrir o navegador externo.
*   **Ações de Hardware via SNMP:** Capacidade de reiniciar fisicamente o hardware da impressora remotamente (Reboot Command) e consultar níveis exatos de toner e papel diretamente do equipamento.
*   **Deploy de Drivers Avançado:** Opção para injetar novos arquivos de driver `.inf` remotamente nos servidores de impressão via interface do aplicativo.
*   **Adicionar método de verificação de modelos de impressora semelhante ao app BR Admin da Brother, além de métricas como nível/níveis de tinta.
