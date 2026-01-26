# PRD — Busca Core

## 1. Visão Geral

O Busca Core é um backend corporativo de busca full-text (FTS) projetado para unificar o acesso a múltiplas fontes de dados estruturados e semiestruturados, oferecendo busca performática, extensível e observável.

Ele serve como motor de busca reutilizável para domínios como:

- Nota de Manutenção (Nota RI)  
- Padrões corporativos (ex: SINPET)  
- Documentações internas  
- Catálogos técnicos  

---

## 2. Problema

Hoje, as informações relevantes estão:

- Espalhadas em múltiplos bancos  
- Indexadas de forma inconsistente  
- Sem ranking semântico  
- Sem API unificada  
- Sem governança de busca  
- Sem observabilidade  

Isso gera:

- Baixa produtividade  
- Retrabalho  
- Erros operacionais  
- Dependência de ferramentas externas  
- Falta de controle sobre dados sensíveis  

---

## 3. Objetivo do Produto

Criar um serviço central de busca que:

- Forneça uma API única para busca textual  
- Seja facilmente extensível para novos domínios  
- Use PostgreSQL FTS nativo  
- Mantenha consistência via trigger  
- Suporte múltiplos formatos de origem (CSV, SQL, API)  
- Permita cache e escala horizontal  
- Seja testável de ponta a ponta  

---

## 4. Público-Alvo

- Analistas operacionais  
- Engenheiros de manutenção  
- Times de TI  
- Desenvolvedores internos  
- Sistemas legados que precisam de busca  

---

## 5. Casos de Uso

### UC-01 — Buscar informações

**Ator:** Usuário final / Sistema  
**Descrição:** Realizar busca textual em um domínio  
**Entrada:** Texto de busca  
**Saída:** Lista ranqueada de resultados  

---

### UC-02 — Contar documentos

**Ator:** Sistema  
**Descrição:** Retornar número total de registros de um domínio  
**Entrada:** Nome do domínio  
**Saída:** Número inteiro  

---

### UC-03 — Verificar saúde

**Ator:** Sistema  
**Descrição:** Verificar se o domínio está operacional  
**Entrada:** Nome do domínio  
**Saída:** Status (ok/down)  

---

### UC-04 — Sincronizar dados

**Ator:** Job / Operador  
**Descrição:** Importar dados externos (ex: CSV)  
**Entrada:** Fonte externa  
**Saída:** Banco atualizado e indexado  

---

## 6. Requisitos Funcionais

- RF-01: API REST para busca  
- RF-02: API REST para contagem  
- RF-03: API REST para healthcheck  
- RF-04: Ranking por relevância  
- RF-05: Destaque de termos (highlight)  
- RF-06: Suporte a múltiplos domínios  
- RF-07: Trigger automático de indexação  
- RF-08: Cache opcional por query  
- RF-09: Limite e paginação  
- RF-10: Suporte a múltiplos idiomas  

---

## 7. Requisitos Não-Funcionais

- RNF-01: Tempo de resposta < 300ms  
- RNF-02: Suporte a 10k QPS (com cache)  
- RNF-03: Alta disponibilidade  
- RNF-04: Observabilidade completa  
- RNF-05: Segurança por domínio  
- RNF-06: Escalabilidade horizontal  
- RNF-07: Testes de integração reais  
- RNF-08: Zero-downtime deploy  
- RNF-09: Idempotência em sync  
- RNF-10: Logs estruturados  

---

## 8. Métricas de Sucesso

- Tempo médio de busca  
- Taxa de acerto no cache  
- Uso por domínio  
- Queries por usuário  
- Taxa de erro  
- Tempo de sincronização  
- Crescimento de novos domínios  
- Adoção por times internos  

---

## 9. Fora de Escopo (MVP)

- Autenticação JWT  
- Autorização por perfil  
- UI web  
- Machine learning  
- Vetorização semântica  
- ElasticSearch  
- Multi-região  

---

## 10. Riscos

- Crescimento de volume  
- Performance sem cache  
- Qualidade dos dados  
- Dependência de triggers  
- Custo operacional  
- Governança de acesso  
- Mudanças no schema  

---

## 11. Roadmap Resumido

| Fase | Descrição |
|------|----------|
| 1 | Arquitetura base |
| 2 | Motor FTS |
| 3 | Performance |
| 4 | Observabilidade |
| 5 | Segurança |
| 6 | Governança |
| 7 | DX |
| 8 | Evolução semântica |

---

## 12. Stakeholders

- TI Corporativo  
- Engenharia de Manutenção  
- Operações  
- Segurança da Informação  
- Arquitetura  
