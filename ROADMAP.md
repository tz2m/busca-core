# ROADMAP — Busca Core

Este roadmap descreve a evolução planejada do Busca Core, desde a fundação arquitetural até recursos avançados de busca semântica.

---

## 🟢 Fase 1 — Fundação Arquitetural (Concluída)

Objetivo: Estabelecer base sólida, limpa e testável.

### Entregas

- Clean Architecture
- FastAPI
- PostgreSQL FTS
- Trigger automático TSVECTOR
- SearchUseCase / CountUseCase
- SearchResultDTO
- Multi-domínio por subpath
- dependency_injector
- Bootstrap centralizado
- Healthcheck funcional
- Testes de integração SQL
- Testes E2E HTTP
- Configuração por YAML
- Ambiente dev/test/prod

---

## 🟡 Fase 2 — Motor de Busca FTS (Atual)

Objetivo: Consolidar funcionalidade central do produto.

### Entregas

- Ranking por relevância
- Highlight de termos
- Normalização de input
- Paginação (limit / offset)
- Campos com pesos (A, B, C, D)
- Índices FTS otimizados
- Múltiplos idiomas
- Logs de queries
- Parâmetros de busca avançados

---

## 🟠 Fase 3 — Performance & Escala

Objetivo: Garantir desempenho sob carga.

### Entregas Planejadas

- Redis para cache de buscas
- TTL configurável por domínio
- Circuit breaker
- Timeouts de query
- Pool tuning do SQLAlchemy
- Bulk fetch
- Cache warming

---

## 🔵 Fase 4 — Observabilidade

Objetivo: Tornar o sistema operável em produção.

### Entregas Planejadas

- Logs estruturados (JSON)
- Métricas Prometheus
- OpenTelemetry tracing
- Dashboard Grafana
- Alertas de erro e latência
- SLOs por domínio

---

## 🟣 Fase 5 — Segurança

Objetivo: Proteger dados e acesso.

### Entregas Planejadas

- Autenticação JWT
- Autorização por domínio
- Rate limiting
- API keys
- Auditoria de queries
- Mascaramento de dados

---

## 🔴 Fase 6 — Governança de Dados

Objetivo: Controlar evolução de schema e índices.

### Entregas Planejadas

- Alembic migrations
- Versionamento de índices FTS
- Versionamento de triggers
- Rollback de schema
- Backups automáticos
- Validação de integridade

---

## 🟤 Fase 7 — Developer Experience (DX)

Objetivo: Facilitar uso e extensão do sistema.

### Entregas Planejadas

- CLI de administração
- Gerador de domínio
- Hot reload de config.yml
- Templates de novos domínios
- Scripts de bootstrap
- Documentação automática
- Makefile (`make dev`, `make test`)

---

## ⚫ Fase 8 — Evolução do Motor de Busca

Objetivo: Tornar a busca mais inteligente.

### Entregas Planejadas

- Fuzzy search
- Sinônimos
- Boost por campo
- Autocomplete
- Spellcheck
- Busca semântica
- Vetorização (embeddings)
- Relevância adaptativa
- Feedback loop de ranking

---

## 📅 Marcos Sugeridos

| Fase | Prazo Estimado |
|------|----------------|
| Fase 2 | 2–4 semanas |
| Fase 3 | 4–6 semanas |
| Fase 4 | 6–8 semanas |
| Fase 5 | 8–10 semanas |
| Fase 6 | 10–12 semanas |
| Fase 7 | 12–14 semanas |
| Fase 8 | 14–20 semanas |

---

## 📊 Métricas de Progresso

- % endpoints implementados
- Latência média
- Cobertura de testes
- Domínios suportados
- Queries por minuto
- Taxa de erro
- Cache hit rate
- Tempo de bootstrap

---

## 🧭 Princípios de Evolução

- Zero breaking changes sem versão
- Infra sempre testada
- Trigger nunca manual
- Bootstrap sempre obrigatório
- Configuração externa sempre vence código
- Segurança antes de features
- Performance antes de escala
- Testes antes de deploy

---

## 🧱 Regra de Ouro Final

> “Se não passar em testes de integração reais, não é feature.”

---

## 🔚 Fim

Este roadmap é um documento vivo.  
Ele deve evoluir conforme novos domínios, requisitos e feedback de uso real.

