# Desafio MBA Engenharia de Software com IA - Full Cycle

Este projeto permite fazer perguntas em linguagem natural sobre um documento PDF. O PDF é processado, dividido em trechos e armazenado como vetores no PostgreSQL. A cada pergunta, os trechos mais relevantes são recuperados e enviados a um modelo de linguagem (OpenAI), que responde com base exclusivamente no conteúdo do documento.

## Requisitos

- Python 3.12+
- Docker

## Configuração

Copie o arquivo de variáveis de ambiente e preencha com sua API Key da OpenAI:

```bash
cp .env.example .env
```

Instale as dependências:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Suba o banco de dados:

```bash
docker compose up -d
```

## Executando

**1. Ingestão do PDF** — divide em chunks e armazena no PostgreSQL:

```bash
python src/ingest.py
```

**2. Inicie o chat** — faça perguntas sobre o documento:

```bash
python src/chat.py
```

Digite `exit` para encerrar o chat.