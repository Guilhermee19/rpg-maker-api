# 🗺️ Roadmap & Arquitetura: Projeto ÉpicoRPG

Este documento descreve as fases de desenvolvimento, a estrutura de dados e a organização do Back-end para o sistema de VTT (Virtual Tabletop) do ÉpicoRPG.

---

## 🚀 1. Roadmap de Desenvolvimento (Front-end & UX)

| Fase | Foco | Principais Entregas |
| :--- | :--- | :--- |
| **Fase 1** | **Base** | Login/Cadastro, Layout (Sidebar/Topbar), CRUD de Personagens e Perfil. |
| **Fase 2** | **Sessões** | Listagem de mesas, Criação de Sessão, Sistema de Convites via código. |
| **Fase 3** | **Preview** | Tela do Jogador, Chat/Feed de eventos, Notas e logs de rolagem. |
| **Fase 4** | **Mestre** | Gerenciamento de Mapas, Posicionamento de Tokens e Fog of War (nevoeiro). |
| **Fase 5** | **Real-time** | Movimentação sincronizada, rolagens instantâneas e atualizações via Socket. |

---

## ⚙️ 2. Roadmap Back-end (Django)

### Fase 1: Core & Auth
* [ ] Custom User Model (AbstractUser) com autenticação JWT.
* [ ] CRUD de Personagens com sistema de atributos dinâmicos.

### Fase 2: Gestão de Mesas
* [ ] Lógica de Convites (Geração de códigos únicos, expiração e limites).
* [ ] Associação de `User + Personagem + Sessão`.

### Fase 3: Conteúdo e Assets
* [ ] Engine de Upload para Mapas e Imagens.
* [ ] CRUD de NPCs e Itens internos da sessão (JSON dinâmico).

### Fase 4: O Tabuleiro (VTT)
* [ ] Lógica de coordenadas para Tokens (x, y, rotação).
* [ ] Sistema de permissões de visibilidade (quem vê qual token).

### Fase 5: Sincronização
* [ ] Implementação de **Django Channels + Redis**.
* [ ] Shared Event Log para auditoria de jogadas.

---

## 📊 3. Estrutura de Dados (Database Schema)

### A. Usuários & Personagens
* **`User`**: Custom model (auth).
* **`Character`**: Core do personagem (id, owner, name, system).
* **`CharacterAttribute`**: EAV Model (key, value, group) para flexibilidade de atributos.

### B. Sessões e Acessos
| Tabela | Campos Chave |
| :--- | :--- |
| `RPGSession` | `id, system, gm_user, status, created_at` |
| `SessionInvite` | `code, session_id, expires_at, max_uses, is_active` |
| `SessionMember` | `session_id, user_id, role (GM/Player)` |

### C. O Tabuleiro (Mapas & Tokens)
* **`SessionMap`**: Armazena a imagem de fundo, `grid_size` e se está ativo.
* **`MapToken`**: Referencia um `Character` ou `NPC`. Guarda `x, y, rotation, scale`.
* **`TokenVisibility`**: Tabela pivot para definir `can_see` entre `Token` e `User`.

### D. Eventos e Logs
* **`DiceRoll`**: Registro de rolagens (`expression`, `result_total`, `detail_json`).
* **`SessionEvent`**: Tabela central de eventos para Replay e WebSocket (Tipo de evento + Payload JSON).

---

## 🏗️ 4. Organização do Projeto Django

A estrutura de pastas seguirá o padrão modular para facilitar a manutenção:

```bash
backend/
├── core/                 # Configurações do projeto (settings, wsgi, asgi)
├── apps/
│   ├── accounts/         # Auth, Perfis e Permissões globais
│   ├── characters/       # Fichas, Atributos e Inventário
│   ├── sessions/         # Gerenciamento de salas, convites e notas
│   ├── maps/             # Tabuleiro, Tokens, Assets e Fog of War
│   └── realtime/         # Consumers (WebSockets), Signals e Dice Engine
├── services/             # Regras de negócio complexas (ex: processar rolagens)
├── api/                  # Serializers e Viewsets (DRF)
└── requirements.txt
```

## 🔐 5. Regras de Permissão (Business Logic)

***Nota Importante:***

Mestre (GM): Possui controle total da sessão. Pode alterar qualquer MapToken, SessionMap e visualizar todos os CharacterAttributes.

Jogador: Permissão de escrita apenas no seu SessionCharacter e em SessionNote privadas. Só recebe via WebSocket dados de tokens onde is_hidden = False ou possua entrada em TokenVisibility.

🛠️ Tecnologias Sugeridas
API: Django REST Framework + SimpleJWT.

Real-time: Django Channels + Redis.

Database: PostgreSQL (pela excelente performance com campos JSONB).

Storage: S3 compatível (DigitalOcean Spaces, AWS ou MinIO) para os mapas.