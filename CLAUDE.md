# 🛡️ Vigília — Planejamento Técnico

> Monitoramento parental com IA: captura efêmera + análise Vision + alerta textual ao responsável legal.

| | |
|---|---|
| **Repositório** | https://github.com/Namem/HackHero2026 |
| **Atualizado** | 2026-05-16 |
| **Fase** | 🔵 Concepção — nenhum código produzido ainda |

---

## 1. Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│  App da Criança (Flutter / Android)                             │
│  - Serviço em background, inicia no boot                        │
│  - Verifica qual app está em uso (UsageStatsManager)            │
│  - Se app estiver na lista → captura tela em RAM                │
│  - Envia imagem via HTTPS → aguarda resultado → descarta        │
│  - Ícone discreto na status bar (obrigatório Android + ECA)     │
└──────────────────────────────┬──────────────────────────────────┘
                               │ HTTPS — imagem em bytes, nunca em disco
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│  Backend (FastAPI / Python)                                     │
│  - Recebe imagem em memória                                     │
│  - Anonimiza PII em RAM (Pillow + Presidio)                     │
│  - Envia à IA Vision (Mistral API → modelo local futuramente)   │
│  - DESTRÓI a imagem imediatamente após análise                  │
│  - Persiste apenas: { categoria, nível, descrição, timestamp }  │
│  - Dispara push notification ao responsável (FCM)               │
└──────────────────────────────┬──────────────────────────────────┘
                               │ Push notification (texto apenas)
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│  App dos Pais (Flutter)                                         │
│  - Recebe alerta: "14h32 · Risco Alto · apostas detectadas"     │
│  - Gerencia lista de apps monitorados remotamente               │
│  - Cadastra gatilhos e palavras-chave                           │
│  - Sem imagens — apenas histórico textual de alertas            │
└─────────────────────────────────────────────────────────────────┘

Banco: PostgreSQL
Tabelas: Users · Devices · MonitoredApps · Triggers · Alerts
❌ Sem tabela de imagens — imagens nunca são persistidas
```

---

## 2. Fluxo Principal

```
[Serviço em background — a cada X segundos]
     │
     ▼ Qual app está em uso agora?
     │
     ├── NÃO está na lista → ignora completamente, nada acontece
     │
     └── ESTÁ na lista →
              │
              ▼ Captura tela (RAM only, nunca em disco)
              │
              ▼ Envia via HTTPS ao backend
              │
              ▼ Backend: anonimiza PII em memória
              │
              ▼ Agente IA analisa imagem + gatilhos dos pais
              │
              ▼ IMAGEM DESTRUÍDA — sempre, sem exceção
              │
              ├── Sem risco → silêncio total, pais não sabem
              │
              └── Com risco →
                       Persiste: categoria + nível + descrição + timestamp
                       Push ao responsável: "14h32 · Risco Alto · apostas"
                       ❌ Nenhuma imagem transmitida ou armazenada
```

---

## 3. Setup Inicial (instalação no device da criança)

```
Pai com celular da criança em mãos:

1. Instala o app
2. Faz login como responsável legal
3. Exibe tela de ciência ao menor (linguagem simples — ECA Digital)
4. Vê lista de apps instalados no device
5. Marca quais quer monitorar (WhatsApp ✅ TikTok ✅ Calculadora ❌)
6. Lista sincroniza no backend
7. Serviço inicia silencioso com ícone discreto na status bar

Depois: pai edita a lista remotamente pelo próprio app,
sem precisar pegar o celular da criança de novo.
```

---

## 4. Módulos

### App da Criança

| Módulo | Responsabilidade |
|---|---|
| `foreground_service` | ForegroundService Android, inicia no boot, roda silencioso |
| `app_monitor` | UsageStatsManager — verifica app em foreground a cada tick |
| `capture_service` | Se app na lista: captura RAM → envia → descarta. Se offline: descarta. |

### Backend

| Módulo | Responsabilidade |
|---|---|
| `POST /analyze` | Recebe bytes → anonimiza → IA → destrói imagem → retorna RiskReport |
| `ai_agent` | Prompt + gatilhos dos pais + imagem → API Vision → parseia resultado |
| `alert_service` | Persiste alerta textual + dispara push FCM |
| `GET /alerts` | Histórico textual de alertas por device |
| `triggers` | CRUD de gatilhos e palavras-chave |
| `devices` | Vínculo device filho ↔ responsável (QR code) |
| `monitored_apps` | Lista e seleção de apps a monitorar |

### App dos Pais

| Módulo | Responsabilidade |
|---|---|
| `alerts_screen` | Lista de alertas textuais com nível, categoria e hora |
| `monitored_apps_screen` | Seleção e edição remota de apps monitorados |
| `triggers_screen` | Cadastro de palavras-chave e categorias de risco |

---

## 5. Stack Tecnológica

### Apps (Flutter — open source)

| Pacote | Licença | Uso |
|---|---|---|
| `flutter_foreground_task` | MIT | ForegroundService silencioso no Android |
| `usage_stats` | MIT | Detecta app em foreground via UsageStatsManager |
| `media_projection` | Apache 2.0 | Captura de tela em RAM via MediaProjection API |
| `dio` | MIT | HTTP client async para envio efêmero |
| `flutter_secure_storage` | BSD | Armazena token JWT |
| `riverpod` | MIT | Gerenciamento de estado |
| `auto_start_flutter` | MIT | Reinicia serviço no boot do device |
| `firebase_messaging` | Apache 2.0 | Push notifications (FCM) |

### Backend (Python — open source)

| Biblioteca | Licença | Uso |
|---|---|---|
| `fastapi` + `uvicorn` | MIT | API REST async |
| `sqlalchemy` + `alembic` | MIT | ORM + migrations |
| `python-jose` + `passlib` | MIT | JWT auth + hash de senhas |
| `pydantic v2` | MIT | Validação e schemas |
| `pillow` | MIT | Manipulação de imagem em memória |
| `presidio-image-redactor` | MIT | Anonimização de PII antes de enviar à IA |
| `mistralai` | MIT | Cliente API Vision (fase MVP) |
| `pytest` + `httpx` | MIT | Testes |

### Infraestrutura

| Serviço | Uso |
|---|---|
| PostgreSQL | Banco principal |
| Docker + Docker Compose | Ambiente local e produção |
| Coolify (self-hosted) | Deploy — substitui Railway/Heroku, gratuito |
| Firebase FCM | Push notifications — gratuito até 1M msgs/mês |

---

## 6. Agente de IA

### Fase 1 — MVP (Mistral API)

Modelo principal: **Mistral Small 3.2 Vision** (open-weight, empresa europeia, não usa dados de API para treino).
Re-análise de risco alto: **GPT-4o Vision** (só casos críticos — reduz custo ~80%).

```python
async def analyze(image_bytes: bytes, triggers: list[str]) -> RiskReport:
    # 1. Anonimizar PII em memória
    clean_bytes = anonymize_in_memory(image_bytes)

    # 2. Enviar à IA
    image_b64 = base64.b64encode(clean_bytes).decode("utf-8")
    response = mistral_client.chat.complete(
        model="mistral-small-latest",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": SYSTEM_PROMPT.format(triggers=triggers)},
                {"type": "image_url", "image_url": f"data:image/jpeg;base64,{image_b64}"}
            ]
        }]
    )
    # image_bytes e clean_bytes destruídos — só o resultado persiste
    return RiskReport.parse(response)
```

### Prompt Base

```python
SYSTEM_PROMPT = """
Você é um agente de segurança parental. Analise a captura de tela
e identifique se o conteúdo é inadequado para crianças/adolescentes.

Gatilhos definidos pelos pais: {triggers}

Responda APENAS em JSON:
{
  "risk_level": "safe|attention|high_risk",
  "confidence": 0.0,
  "detected_triggers": [],
  "description": "descrição curta em português"
}
"""
```

### Fase 2 — Modelo Local (em paralelo desde agora)

Objetivo: rodar 100% na própria infraestrutura, sem custo de API, imagem nunca sai do servidor.

| Etapa | Ação |
|---|---|
| Coleta `safe` | Frames de gameplay infantil do YouTube via `yt-dlp` + `ffmpeg` |
| Coleta `attention` / `high_risk` | Criado sinteticamente — nunca usar imagens reais de crianças |
| Rotulagem | Label Studio — `safe` / `attention` / `high_risk` |
| Augmentation | Albumentations — multiplicar dataset ~5x |
| Fine-tuning | LoRA sobre InternVL2 ou LLaVA-NeXT |
| Deploy | Ollama local — trocar endpoint `api.mistral.ai` → `localhost` |
| Meta | F1 > 0.85 vs Mistral API → substituir completamente |

```bash
# Extrair 1 frame/segundo de gameplay infantil (classe safe)
yt-dlp -o "video.mp4" "URL_DO_VIDEO"
ffmpeg -i video.mp4 -vf fps=1 dataset/safe/frame_%04d.jpg
```

---

## 7. Estrutura de Diretórios

```
vigilia/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── analyze.py           # POST /analyze — efêmero, sem persistência de imagem
│   │   │   ├── alerts.py            # GET  /alerts  — histórico textual
│   │   │   ├── triggers.py          # CRUD gatilhos
│   │   │   ├── devices.py           # Vínculo device ↔ responsável
│   │   │   └── monitored_apps.py    # Apps selecionados para monitorar
│   │   ├── models/                  # User, Device, MonitoredApp, Trigger, Alert
│   │   ├── schemas/                 # Pydantic — sem schema de imagem
│   │   ├── services/
│   │   │   ├── ai_agent.py          # bytes → anonimiza → IA → destrói → RiskReport
│   │   │   └── alert_service.py     # Persiste alerta + push FCM
│   │   └── core/                    # Config, DB, Auth JWT
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
│
├── app-child/
│   ├── lib/
│   │   ├── services/
│   │   │   ├── foreground_service.dart   # Boot + ForegroundService silencioso
│   │   │   ├── app_monitor.dart          # UsageStatsManager
│   │   │   └── capture_service.dart      # Captura RAM → envia → descarta
│   │   └── main.dart
│   └── pubspec.yaml
│
├── app-parent/
│   ├── lib/
│   │   ├── screens/
│   │   │   ├── alerts_screen.dart
│   │   │   ├── monitored_apps_screen.dart
│   │   │   └── triggers_screen.dart
│   │   └── main.dart
│   └── pubspec.yaml
│
├── dataset/
│   ├── collect/     # yt-dlp + ffmpeg
│   ├── label/       # Label Studio
│   └── train/       # LoRA fine-tuning
│
├── docker-compose.yml
├── .github/workflows/
└── README.md
```

---

## 8. Hackathon — 48h

> Foco total em ter o fluxo principal funcionando para demonstração.
> Qualidade de produção, segurança avançada e modelo local ficam para depois.

```
Hora 00–08  →  Fundação
Hora 08–20  →  Fluxo principal (captura + IA + alerta)
Hora 20–36  →  Apps funcionando (filho + pais)
Hora 36–44  →  Integração + demo funcionando
Hora 44–48  →  Apresentação + ajustes finais
```

### ⏱ Hora 00–08 — Fundação
- [ ] **T01** — Monorepo criado, Docker Compose com FastAPI + PostgreSQL rodando
- [ ] **T02** — Banco modelado: Users, Devices, MonitoredApps, Triggers, Alerts
- [ ] **T03** — Auth JWT simples (registro + login do responsável)
- [ ] **T04** — Endpoint `POST /analyze` esqueleto (recebe bytes, retorna mock)
- [ ] **T05** — App Flutter filho criado com ForegroundService básico rodando

### ⏱ Hora 08–20 — Fluxo Principal
- [ ] **T06** — UsageStatsManager detectando app em foreground
- [ ] **T07** — Lógica de captura: só se app está na lista, em RAM, envia, descarta
- [ ] **T08** — Integração Mistral Vision no `/analyze` (imagem → resultado real)
- [ ] **T09** — Prompt com gatilhos funcionando, retornando RiskReport real
- [ ] **T10** — Alerta textual persistido no banco ao detectar risco

### ⏱ Hora 20–36 — Apps
- [ ] **T11** — App filho: tela de setup com seleção de apps instalados
- [ ] **T12** — App pais: tela de alertas textuais (lista + detalhe)
- [ ] **T13** — Push notification FCM chegando no app dos pais
- [ ] **T14** — App pais: tela de cadastro de gatilhos

### ⏱ Hora 36–44 — Integração + Demo
- [ ] **T15** — Fluxo E2E funcionando: app filho → backend → alerta no app dos pais
- [ ] **T16** — Cenário de demo preparado (app de risco na lista, gatilho configurado)
- [ ] **T17** — Ajustes de bugs críticos

### ⏱ Hora 44–48 — Apresentação
- [ ] **T18** — Slides / pitch com problema, solução, demo ao vivo e diferenciais
- [ ] **T19** — Demo ao vivo ensaiada (celular físico com app filho + celular pais vendo alerta)

---

### 🎯 Definição de "pronto" para o hackathon

O projeto está pronto para apresentar quando:
1. App filho captura tela de um app da lista
2. Backend analisa com IA e detecta conteúdo de risco
3. App dos pais recebe push com alerta textual em tempo real

Tudo mais é polish — foco no fluxo funcionando.

---

### ⚠️ O que NÃO fazer nas 48h (economize tempo)
- ❌ Não implementar anonimização Presidio — deixar para depois
- ❌ Não fazer QR code de vínculo — usar código fixo ou login manual
- ❌ Não implementar múltiplos níveis de risco — binário: seguro ou risco
- ❌ Não fazer CI/CD — não precisa para demo
- ❌ Não treinar modelo local — usar Mistral API direto
- ❌ Não se preocupar com deploy em produção — rodar local com ngrok

---

## 9. Legalidade

> ⚠️ Consultar advogado especializado antes de publicar. Este resumo é informativo, não é parecer jurídico.

### Por que a arquitetura atual é juridicamente sólida

| Decisão técnica | Benefício jurídico |
|---|---|
| Verifica app antes de capturar | LGPD Art. 6 III — minimização: coleta só o estritamente necessário |
| Imagem nunca armazenada | Elimina responsabilidade por vazamento de dados visuais de menor |
| Imagem destruída sempre | Sem tratamento de dados prolongado — LGPD exige finalidade + necessidade |
| Alerta apenas textual | Sem transmissão de imagem de menor — ECA Art. 17 respeitado |
| Ícone visível na status bar | ECA Digital Art. 19 §1 — criança informada sobre o monitoramento |
| Tela de ciência no setup | Registro documentado de que o menor foi informado |
| Pais configuram na instalação | Consentimento do responsável legal rastreável |

### Leis aplicáveis

| Lei | Artigo | Impacto direto |
|---|---|---|
| **ECA** Lei 8.069/1990 | Art. 17 | Inviolabilidade da imagem do menor — arquitetura sem transmissão respeita isso |
| **ECA** | Art. 18 | Finalidade protetiva, não punitiva |
| **ECA Digital** Lei 15.211/2025 | Art. 19 | Produtos de monitoramento devem garantir inviolabilidade das imagens transmitidas aos pais — Vigília vai além: nunca transmite imagem |
| **ECA Digital** | Art. 19 §1 | Criança informada em linguagem apropriada — ícone + tela de ciência |
| **LGPD** Lei 13.709/2018 | Art. 6 III | Minimização: coleta só o estritamente necessário — base para monitorar apenas apps da lista |
| **LGPD** | Art. 14 | Dados de crianças exigem consentimento específico do responsável legal |
| **ECA Digital** | Art. 34 §1 e Art. 37 §único | Proibição de vigilância massiva/indiscriminada — dirigida ao governo ao regulamentar, não diretamente aos apps, mas reforça o espírito da lei |

> **Nota:** A proibição de "vigilância massiva, genérica ou indiscriminada" (Art. 34 §1 e Art. 37 §único) é dirigida ao Poder Executivo ao regulamentar a lei, não diretamente aos apps privados. O argumento jurídico correto para o Vigília é o Art. 19 (imagens nunca transmitidas aos pais) + LGPD Art. 6 III (minimização via lista de apps).

### Zonas cinzentas

**1. "Ciência do menor" ainda é vaga**
ECA Digital exige informar, mas nenhum tribunal definiu o mínimo suficiente. Ícone na status bar cumpre tecnicamente, mas pode ser questionado.
→ Tela de ciência no setup com linguagem simples + registro de que o menor visualizou.

**2. Adolescentes 12–18 têm capacidade relativa**
Um adolescente de 15 anos pode argumentar que seu consentimento importa. Sem jurisprudência específica no Brasil ainda.
→ Termo de Uso com linguagem específica por faixa etária + assinatura do responsável via CPF.

**3. No MVP a imagem trafega pela API Mistral/OpenAI**
LGPD Art. 26 regula transferência de dados a terceiros — mesmo que a imagem seja destruída no servidor, ela passa pela infraestrutura do Mistral.
→ Usar Mistral (não usa dados de API para treino) + documentar DPA.
→ Solução definitiva: modelo local (Fase 2).

**4. Responsabilidade civil do desenvolvedor**
Se o app falhar em detectar um risco e a criança sofrer dano, os pais podem acionar o desenvolvedor.
→ Disclaimer nos Termos: o app é ferramenta de apoio, não garantia de segurança.

### Checklist obrigatório antes de lançar

- [ ] Advogado LGPD/ECA → Termos de Uso + Política de Privacidade
- [ ] RIPD (Relatório de Impacto à Proteção de Dados) por DPO — exigido pelo ECA Digital
- [ ] Tela de ciência do menor no setup com registro de visualização
- [ ] DPA documentado com Mistral AI
- [ ] Disclaimer de limitações nos Termos de Uso
- [ ] Botão de exclusão total de dados (LGPD Art. 18)

---

## 10. Próximos Passos

### Decisões a tomar antes do Sprint 0

| Decisão | Opção A | Opção B |
|---|---|---|
| Auth | JWT próprio | Firebase Auth |
| Push | Firebase FCM | ntfy.sh self-hosted |
| Modelo IA MVP | Mistral Small 3.2 | GPT-4o Vision |

### Esta semana
1. Definir as 3 decisões acima
2. Criar estrutura de pastas no repositório
3. Modelar banco de dados e criar migrations iniciais
4. POC da captura de tela Android em RAM (MediaProjection)
5. Iniciar coleta do dataset — script `yt-dlp + ffmpeg` com gameplay infantil

# Vigília — Contexto para o Claude Code

Hackathon 48h. App de monitoramento parental.

## Fluxo principal
1. Serviço Android verifica app em foreground via UsageStatsManager
2. Se app está na lista dos pais → captura tela em RAM
3. Envia via HTTPS ao backend
4. Backend: anonimiza em memória → Mistral Vision analisa → DESTRÓI imagem
5. Se risco: persiste alerta textual + push FCM ao responsável
6. Imagem NUNCA é armazenada, transmitida ou logada

## Stack
- Backend: FastAPI + PostgreSQL + SQLAlchemy + Mistral API
- Apps: Flutter (Android)
- Infra: Docker Compose local + ngrok para demo

## Banco (sem tabela de imagens)
- Users, Devices, MonitoredApps, Triggers, Alerts

## Prioridade absoluta
Fluxo E2E funcionando: captura → IA → push no celular dos pais.
Sem polish, sem over-engineering. É hackathon.