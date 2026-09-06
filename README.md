# Recon-Scout: Ferramenta de Reconhecimento Multifuncional

Um "canivete suíço" de reconhecimento em Python que automatiza diversas tarefas de coleta de informações (Recon) contra um único domínio-alvo.

Em Cibersegurança, a fase de reconhecimento é crucial. Esta ferramenta foi construída para automatizar esse processo, combinando múltiplas técnicas de coleta de informações em um único script, economizando tempo e fornecendo um relatório consolidado.

O projeto foi desenvolvido com foco em portabilidade, funcionando tanto em ambientes **Linux** quanto **Windows**.

## Tech Stack
[![My Skills](https://skillicons.dev/icons?i=python,linux)](https://skillicons.dev)

## Funcionalidades
Esta ferramenta orquestra 5 tarefas de reconhecimento em sequência:

1.  **Resolução de DNS:** Encontra o endereço IP do domínio (`socket`).
2.  **Scan de Portas Comuns:** Verifica uma lista de portas TCP essenciais (21, 22, 80, 443, etc.) no IP encontrado.
3.  **Coleta de Informações Web:** Busca o cabeçalho `Server` e verifica a existência/conteúdo do `robots.txt` (`requests`).
4.  **Web Scraping:** "Raspa" a página inicial em busca de todos os links (`href`) e extrai endereços de e-mail usando Regex.
5.  **Scan Nmap (Automação):** Utiliza o módulo `subprocess` para comandar o Nmap instalado no sistema e executar um scan rápido (`-F`) no alvo.

## Pré-requisitos

Para que a ferramenta funcione completamente, você precisa ter o **Nmap** instalado no seu sistema e acessível pelo terminal (PATH).

* **Linux (Debian/Ubuntu):** `sudo apt install nmap`
* **Windows:** Baixe e instale a versão oficial em [nmap.org/download](https://nmap.org/download.html).

## Instalação e Configuração

Siga os passos abaixo de acordo com o seu sistema operacional.

### 1. Clone o repositório
```bash
   git clone https://github.com/BrennoSantAnna/BrennoSantAnna.git
   cd nome-do-repositorio
```

### 2. Crie e ative o ambiente virtual
#### Linux / macOS:
```bash
   python3 -m venv venv
   source venv/bin/activate
```
#### Windows (PowerShell ou CMD):
```powershell
   python -m venv venv
   .\venv\Scripts\activate
```

### 3. Instale as dependências
Com o ambiente virtual ativo, instale as bibliotecas necessárias:
```bash
   pip install -r requirements.txt
```
_(Dependências incluem: `requests`, `beautifulsoup4`, `lxml` e `scapy`)_

## Como executar
Para utilizar todas as funcionalidades (especialmente o Nmap e scans de rede), recomenda-se executar com privilégios elevados.

#### Linux / macOS
Execute usando sudo apontando para o Python do seu ambiente virtual:
```bash
   sudo venv/bin/python3 recon_scout.py <domínio.com>
```

#### Windows
Abra o seu terminal (CMD ou PowerShell) como Administrador (Botão direito -> "Executar como Administrador").

Com a venv ativa:

```powershell
   python recon_scout.py <domínio.com>
```

## Exemplo de saída
```bash
   --- Starting Reconnaissance on google.com ---

--- Resolving IP for google.com ---
[+] IP address found: 142.250.218.142

--- Scanning Common Ports on 142.250.218.142 ---
[+] Port 80 is OPEN
[+] Port 443 is OPEN
--- Port Scan Finished ---

--- Analyzing Web Info for [http://google.com](http://google.com) ---
[+] Server Header: gws
[*] Checking for: [http://google.com/robots.txt](http://google.com/robots.txt)
[+] robots.txt found (showing first 5 lines):
User-agent: *
Disallow: /search
...

--- Scraping Page [http://google.com](http://google.com) ---
[*] Finding Links...
[+] Found 25 total links.
  - [http://google.com/imghp?hl=en&tab=wi](http://google.com/imghp?hl=en&tab=wi)
...

--- Running Nmap Fast Scan on 142.250.218.142 ---
Starting Nmap 7.94 ( [https://nmap.org](https://nmap.org) )
...
PORT    STATE SERVICE
80/tcp  open  http
443/tcp open  https
...
```

## Estrutura de arquivos
```bash
   📂 python-recon-scout/
   ├── recon_scout.py                 # Arquivo principal com toda a lógica
   ├── requirements.txt               # Lista de dependências
   └── README.md                      # Documentação
```
