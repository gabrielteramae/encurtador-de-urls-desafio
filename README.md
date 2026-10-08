# Encurtador de URLs — código aleatório com prazo

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688?logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.35-D71F00)

Encurta uma URL em um código de 6 caracteres (letras e dígitos) e redireciona enquanto não expirar. O prazo padrão é 30 dias (`URL_EXPIRATION_DAYS`). Não há contagem de clique nem alias escolhido pelo cliente.

## Por que código aleatório

| Escolha | Efeito |
| --- | --- |
| 6 caracteres aleatórios, unicidade checada no banco | Não entrega a quantidade de URLs. Em colisão, tenta de novo até 10 vezes e então estoura `RuntimeError`. |
| Id sequencial na URL | Sem colisão, mas enumerável. |
| Hash da URL | A mesma URL geraria o mesmo código. Este POST grava uma entrada nova a cada chamada. |

A expiração é conferida no GET. Não existe job que apague linha vencida: o registro continua na tabela e a rota responde 404.

`HttpUrl` recusa URL sem esquema e com usuário ou senha. O validador local recusa mais de 2048 caracteres.

## Stack

- Python (sem versão pinada no repositório)
- FastAPI 0.115.0 e Uvicorn 0.30.6
- SQLAlchemy 2.0.35
- SQLite em `sqlite:///./urls.db`, trocável por `DATABASE_URL`

## Estrutura

```
app/
├── main.py            # POST /shorten-url e GET /{short_code}
├── code_generator.py  # alfabeto, tamanho 5–10, padrão 6
├── models.py          # short_code, original_url, expires_at
├── schemas.py
└── database.py
.env.example
requirements.txt
```

## Como rodar

```bash
git clone https://github.com/gabrielteramae/encurtador-de-urls-desafio.git
cd encurtador-de-urls-desafio
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL="${DATABASE_URL:-sqlite:///./urls.db}"
export URL_EXPIRATION_DAYS="${URL_EXPIRATION_DAYS:-30}"
uvicorn app.main:app --reload
```

## Endpoints

| Método | Rota | Resposta |
| --- | --- | --- |
| POST | `/shorten-url` | JSON `{"url":"<base>/<code>"}`. Corpo: `{"url":"https://..."}` |
| GET | `/{short_code}` | 302 para a URL original, ou 404 se não existe ou expirou |

Não há listagem nem DELETE.

## O que não tem

Não há testes automatizados, nem estatística de acesso, nem remoção das URLs vencidas.

---

© 2026 Gabriel Teramae Chan
