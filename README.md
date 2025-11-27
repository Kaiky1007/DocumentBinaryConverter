# DocumentBinaryConverter

![Badge Python](https://img.shields.io/badge/Python-3.9-blue) ![Badge Flask](https://img.shields.io/badge/Flask-Web%20App-green) ![Badge Docker](https://img.shields.io/badge/Docker-Ready-blue)

O **DocumentBinaryConverter** é uma aplicação web desenvolvida para transformar o conteúdo textual de documentos (PDF, DOCX e TXT) em sua representação binária (0s e 1s). O resultado é exportado automaticamente em um novo arquivo PDF estilizado.

## 🚀 Funcionalidades

* **Upload de Arquivos:** Suporte para arquivos `.pdf`, `.docx` e `.txt`.
* **Processamento de Texto:**
    * Extração automática de texto de PDFs usando `PyPDF2`.
    * Leitura de documentos Word usando `python-docx`.
    * Suporte a codificações UTF-8 e Latin-1 para arquivos de texto.
* **Conversão Binária:** Transforma cada caractere do texto extraído em sua sequência binária de 8 bits.
* **Geração de PDF:** Cria um novo PDF contendo o código binário formatado utilizando a biblioteca `ReportLab`.
* **Interface Responsiva:** Design limpo e interativo com animações CSS.

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3.9, Flask
* **Processamento de Arquivos:** PyPDF2, python-docx, ReportLab
* **Servidor WSGI:** Gunicorn
* **Frontend:** HTML5, CSS3, JavaScript
* **Infraestrutura:** Docker

## 📦 Como Executar o Projeto

Você pode rodar a aplicação localmente com Python ou via Docker.

### Pré-requisitos
* Python 3.9+
* Pip
* Docker (opcional)

### 🔧 Instalação Local

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/kaiky1007/documentbinaryconverter.git](https://github.com/kaiky1007/documentbinaryconverter.git)
    cd documentbinaryconverter
    ```

2.  **Crie um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    # No Windows:
    venv\Scripts\activate
    # No Linux/Mac:
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute a aplicação:**
    ```bash
    python app.py
    ```
    O servidor iniciará em `http://127.0.0.1:5000`.

### 🐳 Executando com Docker

Como o projeto já possui um `dockerfile` configurado, você pode construir e rodar o container facilmente:

1.  **Construa a imagem:**
    ```bash
    docker build -t binary-converter .
    ```

2.  **Execute o container:**
    ```bash
    docker run -p 5000:5000 binary-converter
    ```
    Acesse a aplicação em `http://localhost:5000`.

## 📂 Estrutura do Projeto

```text
DocumentBinaryConverter/
├── app.py                # Lógica principal do servidor Flask
├── dockerfile            # Configuração da imagem Docker
├── requirements.txt      # Dependências do Python
├── static/
│   ├── style.css         # Estilos da interface
│   └── script.js         # Lógica de drag-and-drop
├── templates/
│   └── index.html        # Página principal
└── uploads/              # Diretório temporário para processamento
```

## 👥 Autores

Desenvolvido pela equipe **MKI**:

* **Maria Waleska**
* **Kaiky Bruno**
* **Isabela Donald**

&copy; 2025 Document Binary Converter.
