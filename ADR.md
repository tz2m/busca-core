# ADR — Architectural Decision Records  
Projeto: Busca Core

Este documento registra as principais decisões arquiteturais do projeto Busca Core, seus contextos, alternativas consideradas e racional técnico.

---

## ADR-001 — Uso de Clean Architecture

**Status:** Aceito  
**Data:** 2026-01-XX  

### Contexto  
O sistema precisa:

- Suportar múltiplos domínios  
- Evoluir sem acoplamento à infraestrutura  
- Ser testável de ponta a ponta  
- Permitir troca de banco, API ou cache  
- Manter regras de negócio estáveis  

### Decisão  
Adotar Clean Architecture com camadas:

- Interface (FastAPI)  
- Application (Use Cases + Resolvers)  
- Core (Entidades + Portas)  
- Infrastructure (SQL, CSV, FTS)  

### Consequências  
✅ Independência de frameworks  
✅ Testes isoláveis  
✅ Facilidade de evolução  
❌ Mais arquivos e boilerplate  

---

## ADR-002 — PostgreSQL como motor de busca

**Status:** Aceito  

### Contexto  
Era necessário um motor de busca:

- Já disponível na infraestrutura  
- Com custo zero adicional  
- Com suporte a ranking  
- Com suporte a highlight  
- Com suporte a idioma pt-BR  

### Decisão  
Usar PostgreSQL Full-Text Search (FTS) nativo.

### Alternativas Consideradas  

| Opção | Motivo da Rejeição |
|------|--------------------|
| ElasticSearch | Custo e complexidade |
| Meilisearch | Infra adicional |
| Whoosh | Performance |
| SQLite FTS | Escala |

### Consequências  
✅ Zero dependência externa  
✅ Menor latência  
❌ Menos recursos avançados que Elastic  

---

## ADR-003 — Trigger para indexação automática

**Status:** Aceito  

### Contexto  
Os dados chegam por:

- CSV  
- Jobs  
- Scripts  
- APIs futuras  

Era necessário garantir:

- Consistência do índice  
- Zero dependência da aplicação  
- Atualização automática  

### Decisão  
Criar trigger PostgreSQL para popular `tsvector`.

### Consequências  
✅ Indexação automática  
✅ Zero código duplicado  
❌ Debug mais complexo  
❌ Dependência do schema  

---

## ADR-004 — dependency_injector como DI

**Status:** Aceito  

### Contexto  
O projeto precisava:

- Resolver dependências por domínio  
- Suportar overrides em teste  
- Ser explícito e declarativo  
- Integrar com FastAPI  

### Decisão  
Usar `dependency_injector`.

### Alternativas  

| Opção | Motivo da Rejeição |
|------|--------------------|
| FastAPI Depends puro | Acoplamento à infra |
| punq | Poucos recursos |
| wired | Pouca maturidade |

### Consequências  
✅ Container centralizado  
✅ Overrides simples  
❌ Curva de aprendizado  

---

## ADR-005 — Multi-domínio por subpath

**Status:** Aceito  

### Contexto  
O sistema precisava servir múltiplos domínios sem duplicar rotas.

### Decisão  
Usar padrão:

