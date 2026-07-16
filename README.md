# URL Shortener API

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-blue)

Solução para o desafio [`backend-br/desafios/url-shortener`](https://github.com/backend-br/desafios/blob/master/url-shortener/PROBLEM.md): encurtar URLs longas em códigos curtos, com persistência, expiração e redirecionamento.

## Como funciona

```
POST /shorten-url {"url": "https://exemplo.com"} -> gera codigo alfanumerico unico (5-10 chars)
                                                   -> salva no banco com data de expiracao
                                                   -> retorna {"url": "https://host/CODIGO"}

GET /CODIGO -> busca no banco
            -> nao existe ou expirado? 404
            -> valido? redirect 307 para a URL original
```

## Regras implementadas

| Requisito                        | Implementação                                       |
|-------------------------------------|---------------------------------------------------------|
| Código com 5-10 caracteres              | `code_generator.py`, tamanho padrão 6, ajustável            |
| Apenas letras e números                  | Alfabeto restrito a `[a-zA-Z0-9]`                              |
| Salvo no banco com prazo de validade       | Coluna `expires_at`, padrão 30 dias (`URL_EXPIRATION_DAYS`)      |
| Redireciona para a URL original               | `RedirectResponse` (307) na rota `GET /{codigo}`                   |
| 404 se não encontrada ou expirada               | Verificação de existência + comparação de `expires_at`                |

## Stack

- **FastAPI** para a API REST
- **SQLAlchemy 2.0** + SQLite para persistência (trocar `DATABASE_URL` para Postgres/MySQL em produção)
- Geração de código isolada em `code_generator.py`, com checagem de unicidade e retry

## Estrutura

```
app/
├── main.py             # endpoints POST /shorten-url e GET /{codigo}
├── models.py             # entidade ShortenedUrl
├── schemas.py              # request/response (Pydantic)
├── database.py               # conexao SQLAlchemy
└── code_generator.py           # geracao de codigo curto unico
```

## Como rodar

```bash
git clone <seu-repo>
cd url-shortener-api
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8004
```

## Exemplo

```bash
curl -X POST http://localhost:8004/shorten-url \
  -H "Content-Type: application/json" \
  -d '{"url":"https://backendbrasil.com.br"}'
```
```json
{"url": "http://localhost:8004/4HUi86"}
```

```bash
curl -i http://localhost:8004/4HUi86
```
```
HTTP/1.1 307 Temporary Redirect
location: https://backendbrasil.com.br/
```

## Deploy

Pronto para subir no [Railway](https://railway.app): start command `uvicorn app.main:app --host 0.0.0.0 --port $PORT`, variáveis `DATABASE_URL` e `URL_EXPIRATION_DAYS` configuráveis no serviço.

---

© 2026 Gabriel Teramae Chan
