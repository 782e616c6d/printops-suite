# Gerenciador de Impressoras - Python + CustomTkinter

Uma interface gráfica interativa para **instalar, desinstalar e baixar drivers** de impressoras via rede local (por IP), utilizando arquivos `.INF`. A ferramenta verifica o status (online/offline), presença do driver e realiza o gerenciamento completo com poucos cliques.

---

## Funcionalidades

- Verificação de status da impressora (online/offline via IP)
- Instalação automática com associação IP + driver
- Desinstalação de impressoras instaladas
- Download automático de drivers (ZIP)
- Extração automática do driver
- Logs de todas as ações realizadas
- Interface leve e responsiva com CustomTkinter
- Suporte a múltiplos modelos e múltiplas instâncias

---

## Requisitos

- **Python 3.9+**
- **Windows (com `rundll32` e `printui.dll`)**
- Módulos Python:
  - `customtkinter`
  - `Pillow`
  - `requests`

Instale com:

```bash
pip install customtkinter pillow requests ping3 rarfile
```
