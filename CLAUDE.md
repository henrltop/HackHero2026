# Regras de Colaboração

> **OBRIGATÓRIO antes de qualquer criação de arquivo ou pasta:**
> Mostrar ao usuário a lista completa do que será criado (arquivos, diretórios, conteúdo relevante) e aguardar aprovação explícita antes de executar. Nunca criar estruturas de pastas ou arquivos sem confirmação prévia.
>
> **Sempre sugerir commit** ao final de qualquer conjunto de mudanças em arquivos.
>
> **Sempre apontar alternativa melhor** se houver abordagem superior à proposta pelo usuário, antes de executar.

---

# ✦ Aura — Planejamento Técnico

> Proteção digital parental com IA: monitoramento de jogos + análise Vision + alerta textual ao responsável legal.

| | |
|---|---|
| **Nome** | Aura |
| **Repositório** | https://github.com/Namem/HackHero2026 |
| **Atualizado** | 2026-05-16 |
| **Fase** | 🟡 Em desenvolvimento — backend Django pronto, Flutter pendente |

## Escopo (definido com mentores)
- **Somente jogos** — não monitora todos os apps, apenas jogos instalados
- **Criança é informada** na abertura do jogo (popup no app filho)
- **Pai concorda** durante cadastro que informará a criança (checkbox obrigatório — ECA Digital)
- **Pai não configura filtros** — a IA classifica tudo automaticamente por categorias da literatura
- **Dashboard do pai**: Alto / Médio / Baixo risco — ao clicar mostra "pode ser" + recomendações

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
│  Backend (Django + DRF / Python) ✅ PRONTO                      │
│  - Recebe imagem em memória                                     │
│  - Envia à IA Vision (Mistral API → modelo local futuramente)   │
│  - DESTRÓI a imagem imediatamente após análise                  │
│  - Persiste apenas: { categoria, nível, descrição, timestamp }  │
│  - Admin Django = painel web dos pais                           │
└──────────────────────────────┬──────────────────────────────────┘
                               │ Push notification (texto apenas)
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│  App dos Pais (Flutter mobile + Django Admin web)               │
│  - Recebe alerta: "14h32 · Risco Alto · apostas detectadas"     │
│  - Gerencia lista de apps monitorados remotamente               │
│  - Cadastra gatilhos e palavras-chave                           │
│  - Sem imagens — apenas histórico textual de alertas            │
└─────────────────────────────────────────────────────────────────┘

Banco: PostgreSQL
Tabelas: accounts_user · devices_device · devices_monitoredapp · monitoring_trigger · monitoring_alert
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
              ▼ POST /api/analyze/ com image + device_token
              │
              ▼ Backend: Mistral Vision analisa + gatilhos dos pais
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
2. Faz login como responsável legal (POST /api/auth/login/)
3. Exibe tela de ciência ao menor (linguagem simples — ECA Digital Art. 19 §1)
4. Vê lista de apps instalados no device
5. Marca quais quer monitorar (WhatsApp ✅ TikTok ✅ Calculadora ❌)
6. Lista sincroniza no backend (POST /api/devices/{token}/apps/)
7. Serviço inicia silencioso com ícone discreto na status bar

Depois: pai edita a lista remotamente pelo próprio app ou pelo Django Admin,
sem precisar pegar o celular da criança de novo.
```

---

## 4. Módulos

### App da Criança

| Módulo | Responsabilidade |
|---|---|
| `foreground_service` | ForegroundService Android, inicia no boot, roda silencioso |
| `app_monitor` | UsageStatsManager — verifica app em foreground a cada tick |
| `capture_service` | Se app na lista: captura RAM → POST /api/analyze/ → descarta. Se offline: descarta. |

### Backend (Django)

| App / Endpoint | Responsabilidade |
|---|---|
| `POST /api/analyze/` | Recebe bytes → IA → destrói imagem → salva alerta se risco |
| `services/ai_agent.py` | Prompt + gatilhos + imagem → Mistral Vision → dict resultado |
| `GET /api/alerts/` | Histórico textual de alertas por device (auth obrigatória) |
| `GET/POST /api/devices/` | Vínculo device filho ↔ responsável |
| `GET/POST /api/devices/{token}/apps/` | Apps monitorados por device |
| `GET/POST /api/devices/{token}/triggers/` | Gatilhos e palavras-chave |
| `/admin/` | Django Admin — painel web dos pais |

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

### Backend (Python — open source) ✅ IMPLEMENTADO

| Biblioteca | Versão | Uso |
|---|---|---|
| `django` | 5.0.4 | Framework web + ORM + Admin |
| `djangorestframework` | 3.15.1 | API REST |
| `djangorestframework-simplejwt` | 5.3.1 | Auth JWT (register + login) |
| `django-cors-headers` | 4.3.1 | CORS para Flutter |
| `psycopg2-binary` | 2.9.9 | Driver PostgreSQL |
| `mistralai` | 1.7.0 | Cliente API Vision |
| `pillow` | 10.3.0 | Manipulação de imagem em memória |
| `gunicorn` | 22.0.0 | WSGI server (produção) |
| `python-dotenv` | 1.0.1 | Variáveis de ambiente |

### Infraestrutura

| Serviço | Uso |
|---|---|
| PostgreSQL 16 | Banco principal |
| Docker + Docker Compose | Ambiente local e produção |
| Coolify (self-hosted) | Deploy — substitui Railway/Heroku, gratuito |
| Firebase FCM | Push notifications — gratuito até 1M msgs/mês |

---

## 6. Estrutura de Diretórios Atual

```
HACKAHERO/
├── backend/
│   ├── manage.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env.example
│   ├── vigilia/                  ← projeto Django
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── accounts/                 ← User + auth JWT
│   │   ├── models.py             (AbstractUser com email)
│   │   ├── serializers.py
│   │   ├── views.py              (register, login, me)
│   │   ├── urls.py
│   │   └── admin.py
│   ├── devices/                  ← Device + MonitoredApp
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── admin.py              (painel dos pais — devices e apps)
│   ├── monitoring/               ← Trigger + Alert + /analyze
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py              (POST /analyze, GET /alerts, triggers)
│   │   ├── urls.py
│   │   └── admin.py              (painel dos pais — alertas e gatilhos)
│   └── services/
│       └── ai_agent.py           (mock sem API key, Mistral com API key)
├── docker-compose.yml
├── .gitignore
├── CLAUDE.md
└── docs/
    ├── brainstorm inicial.txt
    ├── vigilia_planejamento.md / .pdf
    ├── Apresentação grupo de whats.pptx / .pdf
    ├── lei1.txt                  ← Lei 15.211/2025 (ECA Digital) — texto oficial
    └── lei2.txt                  ← Decreto 12.880/2026 — regulamentação
```

---

## 7. Agente de IA

### Fase 1 — MVP (Mistral API)

Modelo: **mistral-small-latest** (open-weight, empresa europeia, não usa dados de API para treino).
Sem API key → retorna mock automaticamente, sem quebrar o fluxo.

```python
# services/ai_agent.py — síncrono (compatível com Django)
def analyze_image(image_bytes: bytes, triggers: list[str]) -> dict:
    client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])
    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": [
            {"type": "text", "text": SYSTEM_PROMPT.format(triggers=triggers)},
            {"type": "image_url", "image_url": f"data:image/jpeg;base64,{image_b64}"}
        ]}]
    )
    return json.loads(response.choices[0].message.content)
    # image_bytes destruído no finally
```

### Fase 2 — Modelo Local (pós-hackathon)

Objetivo: rodar 100% na própria infraestrutura, sem custo de API, imagem nunca sai do servidor.
Trocar apenas o endpoint em `ai_agent.py`: `api.mistral.ai` → `localhost` (Ollama).

---

## 8. Hackathon — Status

### ✅ Concluído
- **T01** — Docker Compose com Django + PostgreSQL rodando
- **T02** — Banco modelado: User, Device, MonitoredApp, Trigger, Alert
- **T03** — Auth JWT (register + login + me)
- **T04** — `POST /api/analyze/` com mock RiskReport + integração Mistral
- **T04+** — Django Admin configurado como painel web dos pais

### 🔲 Pendente (ordem de prioridade)
- **T05** — App Flutter filho: ForegroundService básico rodando
- **T06** — UsageStatsManager detectando app em foreground
- **T07** — Captura em RAM + envio ao backend
- **T08** — Mistral Vision real validado end-to-end
- **T09** — Prompt com gatilhos retornando RiskReport real
- **T10** — Alerta persistido + push FCM
- **T11** — App filho: tela de setup com seleção de apps instalados
- **T12** — App pais (Flutter): tela de alertas textuais
- **T13** — Push notification FCM chegando no app dos pais
- **T14** — App pais: tela de cadastro de gatilhos
- **T15** — Fluxo E2E: celular filho → backend → alerta no celular dos pais
- **T16** — Cenário de demo preparado
- **T17** — Bugs críticos
- **T18** — Slides / pitch
- **T19** — Demo ao vivo ensaiada

### Definição de "pronto" para o hackathon
1. App filho captura tela de um app da lista
2. Backend analisa com IA e detecta conteúdo de risco
3. App dos pais recebe push com alerta textual em tempo real

### ⚠️ O que NÃO fazer nas 48h
- ❌ Não implementar anonimização Presidio — deixar para depois
- ❌ Não fazer QR code de vínculo — usar código fixo ou login manual
- ❌ Não fazer CI/CD — não precisa para demo
- ❌ Não treinar modelo local — usar Mistral API direto
- ❌ Não se preocupar com deploy em produção — rodar local com ngrok

---

## 9. Legalidade

> ⚠️ Consultar advogado especializado antes de publicar. Este resumo é informativo, não é parecer jurídico.
> Leis verificadas com texto oficial: Lei 15.211/2025 (docs/lei1.txt) + Decreto 12.880/2026 (docs/lei2.txt).

### Por que a arquitetura é juridicamente sólida

| Decisão técnica | Benefício jurídico |
|---|---|
| Verifica app antes de capturar | LGPD Art. 6 III — minimização de dados |
| Imagem destruída imediatamente | Elimina responsabilidade por vazamento |
| Alerta apenas textual aos pais | Art. 19 exige inviolabilidade de imagens "transmitidas aos pais" — não transmitimos |
| Ícone na status bar | ECA Digital Art. 19 §1 — criança informada |
| Tela de ciência no setup | Registro documentado de que o menor foi informado |
| Consentimento do responsável no setup | LGPD Art. 14 — consentimento específico |

### O que a lei diz exatamente (texto oficial)

**Lei 15.211/2025, Art. 2, II — PERMITE e DEFINE o Vigília:**
> *"produto ou serviço de monitoramento infantil: destinado ao acompanhamento, por pais ou responsáveis legais, das ações executadas por crianças e adolescentes em ambientes digitais, **a partir do registro ou da transmissão de imagens**, de sons, de informações de localização, de atividade ou de outros dados"*

**Lei 15.211/2025, Art. 19 — Condições para produtos de monitoramento:**
> *"Os produtos ou serviços de monitoramento infantil deverão conter mecanismos para garantir a **inviolabilidade das imagens... transmitidas aos pais ou responsáveis legais**."*
> *§1º — "deverão conter mecanismos que informem as crianças e os adolescentes, em linguagem apropriada, acerca da realização do monitoramento."*

O Vigília supera esse requisito: a lei exige inviolabilidade de imagens transmitidas aos pais — o Vigília **nunca transmite imagem aos pais**.

**Lei 15.211/2025, Art. 34 §1 e Art. 37 §único — "Vigilância massiva":**
> *"A regulamentação não poderá... autorizar mecanismos de vigilância massiva, genérica ou indiscriminada..."*

⚠️ Dirigido ao **Poder Executivo ao regulamentar**, não a apps privados diretamente.

**Decreto 12.880/2026, Art. 24 §3 — Princípio de eliminação imediata:**
> *"vedado o armazenamento... da imagem... que deverá ser **eliminada de modo imediato e irreversível** após a captura da informação necessária"*

Contexto: verificação de idade. Mas o princípio reforça a arquitetura do Vigília.

### Zonas cinzentas

**1. Imagem trafega pelo Mistral (terceiro)**
LGPD Art. 26 — transferência a terceiro processador. Mistral declara não treinar com dados de API.
→ Documentar DPA com Mistral antes de lançar.
→ Solução definitiva: modelo local (Fase 2).

**2. "Ciência do menor" ainda é vaga**
Nenhum tribunal definiu o mínimo suficiente. Ícone + tela de ciência cobrem tecnicamente.
→ Guardar log de que o menor visualizou a tela de ciência.

**3. Adolescentes 12–18 têm capacidade relativa**
Sem jurisprudência específica no Brasil ainda.
→ Termo de Uso com linguagem por faixa etária.

**4. Responsabilidade civil**
Se o app falhar em detectar um risco, pais podem acionar o desenvolvedor.
→ Disclaimer: ferramenta de apoio, não garantia.

### Checklist antes de lançar

- [ ] Advogado LGPD/ECA → Termos de Uso + Política de Privacidade
- [ ] RIPD (Relatório de Impacto à Proteção de Dados)
- [ ] Tela de ciência com log de visualização do menor
- [ ] DPA documentado com Mistral AI
- [ ] Disclaimer de limitações nos Termos de Uso
- [ ] Endpoint de exclusão total de dados (LGPD Art. 18)

---

## 10. Como subir o projeto

```bash
git clone https://github.com/Namem/HackHero2026.git
cd HackHero2026
cp backend/.env.example backend/.env
# editar .env e adicionar MISTRAL_API_KEY se tiver
docker compose up --build

# API:   http://localhost:8000/api/
# Admin: http://localhost:8000/admin/
# Criar superuser para o admin:
docker compose exec api python manage.py createsuperuser
```

Sem API key o `/api/analyze/` retorna mock e tudo funciona para desenvolvimento.

# Vigília — Contexto para o Claude Code

Hackathon 48h. App de monitoramento parental com IA.

## Stack atual
- **Backend**: Django 5.0 + DRF + simplejwt (✅ pronto)
- **Apps**: Flutter Android (🔲 pendente)
- **Infra**: Docker Compose local + ngrok para demo

## Endpoints principais
- `POST /api/analyze/` — sem auth, recebe image + device_token
- `GET /api/alerts/?device_token=` — auth obrigatória
- `POST /api/auth/register/` e `POST /api/auth/login/`
- `/admin/` — painel dos pais

## Banco
- accounts_user, devices_device, devices_monitoredapp, monitoring_trigger, monitoring_alert
- Sem tabela de imagens

## Prioridade absoluta
Fluxo E2E: captura → IA → push no celular dos pais.
Sem polish, sem over-engineering. É hackathon.
