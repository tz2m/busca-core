# SPEC — Especificação Técnica  
Projeto: Busca Core

Este documento descreve os detalhes técnicos do funcionamento interno do Busca Core.

---

## 1. Stack Tecnológica

- Python 3.12  
- FastAPI  
- SQLAlchemy 2.x  
- PostgreSQL 15  
- dependency_injector  
- pytest  
- uvicorn  

---

## 2. Arquitetura em Camadas

```

Interface (FastAPI)
↓
Application (Use Cases + Resolvers)
↓
Core (Entidades + Portas)
↓
Infrastructure (SQL, CSV, FTS, Triggers)

````

---

## 3. Mecanismo de Busca (FTS)

### 3.1 Coluna de índice

```sql
document TSVECTOR
````

---

### 3.2 Trigger de indexação

* Tipo: BEFORE INSERT OR UPDATE
* Linguagem: PL/pgSQL
* Função: update_items_document
* Atualiza a coluna `document` automaticamente

---

### 3.3 Query de busca

```sql
plainto_tsquery('portuguese', :query)
ts_rank(document, ts_query)
ts_headline('portuguese', texto_descritivo_ri, ts_query)
```

---

## 4. Contrato HTTP

### 4.1 Buscar

**Endpoint**

```
GET /api/{domain}/search
```

**Query Params**

| Nome   | Tipo   | Obrigatório | Default |
| ------ | ------ | ----------- | ------- |
| q      | string | sim         | -       |
| limit  | int    | não         | 10      |
| offset | int    | não         | 0       |

**Resposta**

```json
[
  {
    "item": { ... },
    "score": 0.52,
    "highlight": "..."
  }
]
```

---

### 4.2 Contar

**Endpoint**

```
GET /api/{domain}/count
```

**Resposta**

```json
{
  "count": 1234
}
```

---

### 4.3 Health

**Endpoint**

```
GET /api/health/{domain}
```

**Resposta**

```json
{
  "status": "ok",
  "domain": "nota_ri",
  "database": "ok",
  "fts_trigger": "ok"
}
```

---

## 5. Use Cases

### SearchUseCase

```python
class SearchUseCase:
    def execute(self, q: str, limit: int, offset: int) -> List[SearchResultDTO]
```

---

### CountUseCase

```python
class CountUseCase:
    def execute(self) -> int
```

---

## 6. Repositórios

### SearchRepository (porta)

```python
class SearchRepository(Protocol):
    def search(self, query: str, limit: int, offset: int) -> List[SearchResultDTO]
```

---

### NotaRIRepositorySql (infra)

* SQLAlchemy
* Session real
* Mapeia entidade ↔ SQL
* Não conhece FastAPI

---

## 7. DI Container

* Providers por domínio
* Engine singleton
* Session factory singleton
* Resolvers dinâmicos

---

## 8. Bootstrap

Responsável por:

* Carregar config.yml
* Resolver DatabaseConfig
* Criar engine
* Criar schema
* Aplicar trigger
* Wire DI
* Validar saúde

---

## 9. Testes

### 9.1 Unitários

* Core
* Use Cases
* DTOs

---

### 9.2 Integração

* Banco real
* Trigger real
* SQL real

---

### 9.3 E2E

* HTTP real
* FastAPI real
* DI real

---

## 10. Observabilidade (Planejado)

* Logs estruturados
* Métricas
* Tracing
* Cache hit/miss

---

## 11. Segurança (Planejado)

* JWT
* Rate limit
* RBAC
* Auditoria

---

## 12. Performance (Planejado)

* Redis
* Materialized views
* Autocomplete
* Pré-cálculo de ranking

```
