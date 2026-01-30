# Busca Core

Backend de busca full-text (FTS) multi-domínio, baseado em Clean Architecture, projetado para servir como motor de busca corporativo para diferentes fontes de dados (ex: Nota RI, SINPET).

---

## 🎯 Objetivo

Prover um motor de busca FTS reutilizável, extensível e observável, com:

- PostgreSQL Full-Text Search  
- Trigger automático para indexação  
- Arquitetura limpa  
- DI com dependency_injector  
- Multi-domínio via subpath  
- Testes de integração reais  
- Healthcheck funcional  

---

## 🏗 Arquitetura

```

src/busca/
├── app/                # Application layer
│   ├── bootstrap.py   # Orquestra startup
│   ├── container.py   # DI container
│   └── services/      # Resolvers (Search, Count, Health)
├── core/               # Domain-agnostic core
│   ├── use_case/       # SearchUseCase, CountUseCase
│   └── repository/    # Interfaces (SearchRepository, etc.)
├── domains/            # Domínios concretos
│   └── nota_ri/
│       ├── core/       # Entidades
│       └── repository/ # SQL, CSV, FTS
├── interface/          # HTTP layer (FastAPI)
│   └── api/
│       ├── main.py
│       ├── search_routes.py
│       ├── count_routes.py
│       └── health_routes.py
└── tests/
├── integration/    # Testes reais (DB + HTTP)

````

---

## 🚀 Subindo em modo dev

```bash
BUSCA_ENV=dev uvicorn busca.interface.api.main:app --reload
````

Swagger:

```
http://localhost:8000/docs
```

---

## 🔎 Endpoints

### Buscar

```
GET /api/{domain}/search?q=texto&limit=10&offset=0
```

Exemplo:

```bash
curl "http://localhost:8000/api/nota_ri/search?q=bomba"
```

---

### Contar

```
GET /api/{domain}/count
```

---

### Healthcheck

```
GET /api/health/{domain}
```

---

## 🧪 Testes

### Integração SQL

```bash
pytest tests/integration/test_search_use_case_sql.py
```

### E2E HTTP

```bash
pytest tests/integration/test_search_http.py
```

---

## ⚙ Configuração

Arquivo: `data/config.yml`

Exemplo:

```yaml
nota_ri:
  database:
    user: postgres
    password: postgres
    host: localhost
    port: 5432
    db_name: nota_ri
    drop_all: false

  infra:
    fts_init_sql_file: src/domains/nota_ri/repository/db/init_fts.sql
```

---

## 🧱 Regras de Ouro

* Router não conhece SQL
* Use case não conhece HTTP
* Infra não vaza para core
* API nunca expõe alias de CSV
* Trigger sempre validado em testes
* Bootstrap sempre roda em dev/test/prod
* Healthcheck testa capacidade funcional
