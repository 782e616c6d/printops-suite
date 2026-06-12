Printer App - Gerenciador Centralizado de Impressoras 🖨️⚡

Printer App é uma aplicação desktop profissional e robusta construída em Python (PyQt6). Foi desenhada para facilitar a vida de administradores de sistemas e equipas de TI corporativas na gestão, mapeamento e resolução de problemas de impressoras de rede e locais num ambiente Windows.

Com uma interface moderna, responsiva e inspirada no Fluent Design (com suporte nativo a temas Claro e Escuro), a aplicação oferece funcionalidades avançadas de processamento em lote e relatórios detalhados.

✨ Principais Funcionalidades

Gestão Centralizada: Visualize e controle simultaneamente impressoras de múltiplos servidores de impressão e dispositivos instalados localmente.

Ações em Lote (Batch Processing): Instale (por máquina ou utilizador), desinstale, imprima páginas de teste e limpe filas de impressão de múltiplos dispositivos com apenas um clique.

Filtros e Grupos Inteligentes: Navegue pelas impressoras através de agrupamentos dinâmicos gerados automaticamente (por Servidor, Status de Conexão, Fabricante ou Tipo de Conexão).

Reparo Rápido de Spooler: Ferramenta integrada (requer privilégios de Administrador) para parar o serviço de spooler, limpar arquivos corrompidos da fila nativa do Windows e reiniciar o serviço de forma segura.

Logs e Exportação CSV: Monitorização em tempo real de todas as ações executadas pela aplicação, com a possibilidade de exportar grelhas de impressoras e histórico de tarefas para arquivos .csv.

Interface Web Dinâmica: Abra o painel de administração Web de qualquer impressora de rede diretamente a partir da aplicação com um único clique.

Multilingue: Suporte nativo a Português, Inglês e Espanhol, com deteção automática baseada no idioma do sistema operacional.

Personalização Visual: Escolha as suas próprias cores de destaque, famílias e tamanhos de fonte, logotipo na barra lateral (via ficheiro customizado) e intervalo de atualização em background.

🛠️ Tecnologias e Dependências

O projeto baseia-se nas seguintes tecnologias e bibliotecas:

Python 3.8+ (Requerido)

PyQt6: Para a construção de toda a Interface Gráfica de Utilizador (GUI).

pywin32: Interação robusta de baixo nível com as APIs do Windows (win32print, pythoncom) para controlo de filas e polling de portas.

QtAwesome: Fornecimento de ícones vetoriais modernos para a interface.

⚙️ Pré-requisitos e Instalação

Certifique-se de que possui o Python 3.8 ou superior instalado no seu sistema Windows.

Clone ou faça download deste repositório para o seu computador local.

Abra o terminal (Prompt de Comando ou PowerShell) na pasta raiz do projeto.

(Opcional, mas recomendado) Crie um ambiente virtual (venv):

python -m venv venv
venv\Scripts\activate


Instale as dependências executando:

pip install -r requirements.txt


🚀 Como Executar

Após a instalação das dependências, basta executar o ficheiro principal da aplicação:

python app.py


Nota para funcionalidades avançadas: Se pretender utilizar a funcionalidade "Reparar Spooler", certifique-se de abrir o terminal ou a aplicação com privilégios de Administrador (Run as Administrator).

📂 Estrutura de Arquivos Gerados Automáticamente

Ao executar a aplicação e guardar as definições, são criados/utilizados os seguintes recursos na mesma pasta do app.py:

printer_app_config.json: Ficheiro de configurações contendo dados de servidores, temas, fontes e taxa de sincronização.

icons/: (Opcional) Pasta criada automaticamente caso importe um logotipo lateral customizado através da aba Configurações.

🤝 Contribuições

Contribuições, relato de problemas (issues) e Pull Requests são sempre bem-vindos! Para grandes mudanças, por favor abra uma issue primeiro para discutirmos o que gostaria de alterar.
