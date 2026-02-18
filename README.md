# RPG Maker API - Sistema Completo

Uma API REST completa para sistema de RPG desenvolvida em Django com Django Rest Framework, JWT e múltiplos sistemas de RPG.

## 🚀 Características

- **JWT Authentication** com tokens de acesso e refresh
- **Django Rest Framework** com views customizadas
- **Documentação Swagger** integrada
- **Sistema de autenticação completo** (registro, login, logout)
- **Múltiplos Sistemas de RPG** com templates de ficha personalizados
- **Gerenciamento de Personagens** com fichas dinâmicas
- **Sistema de Sessões** com convidados e mapas
- **CORS** configurado para frontend

## 📋 Estrutura do Projeto

```
rpg-maker-api/
├── rpg_api/           # Configurações principais do Django
├── authentication/    # Sistema de autenticação com JWT
├── core/             # Views principais e perfis de usuário
├── characters/       # Personagens e Sistemas de RPG
├── session/          # Sessões de jogo, convites e membros
└── maps/             # Mapas das sessões
```

## 🎲 Sistemas de RPG Disponíveis

- **D&D 5ª Edição** (Sistema padrão) - Ficha completa com atributos, skills, equipamentos e magias
- **Sistema Genérico** - Template básico compatível com qualquer RPG
- **Call of Cthulhu** - Sistema investigativo com sanidade e ocupações
- **Extensível** - Adicione novos sistemas facilmente

## 🛠️ Setup do Projeto

### 1. Clone e prepare o ambiente

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente

```bash
# Copiar arquivo de exemplo
.env.example .env

# Editar .env com suas configurações
```

### 3. Executar migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Criar superusuário (opcional)

```bash
python manage.py createsuperuser
```

### 5. Executar servidor

```bash
python manage.py runserver
```

## 📚 Documentação da API

Após executar o servidor, acesse:

- **Swagger UI**: http://localhost:8001/api/docs/
- **ReDoc**: http://localhost:8001/api/redoc/
- **Schema JSON**: http://localhost:8001/api/schema/

## 🎮 Endpoints Disponíveis

### 🔐 Autenticação
- `POST /api/v1/auth/register/` - Registrar novo usuário
- `POST /api/v1/auth/login/` - Login do usuário
- `POST /api/v1/auth/logout/` - Logout do usuário
- `GET /api/v1/auth/get-user/` - Obter dados do usuário atual
- `POST /api/v1/auth/token/refresh/` - Renovar token de acesso

### 👤 Perfil de Usuário
- `GET /api/v1/core/users/me/` - Obter perfil do usuário
- `PUT /api/v1/core/users/me/` - Atualizar perfil completo
- `PATCH /api/v1/core/users/me/` - Atualizar perfil parcial

### 🎲 Sistemas de RPG
- `GET /api/v1/core/rpg-systems/` - Listar sistemas disponíveis
- `GET /api/v1/core/rpg-systems/{id}/` - Detalhes do sistema
- `GET /api/v1/core/rpg-systems/default/` - Obter sistema padrão
- `GET /api/v1/core/rpg-systems/{id}/template/` - Template base do sistema

### 🧙‍♂️ Personagens
- `GET /api/v1/core/characters/` - Listar personagens do usuário
- `POST /api/v1/core/characters/` - Criar novo personagem
- `GET /api/v1/core/characters/{id}/` - Detalhes do personagem
- `PUT /api/v1/core/characters/{id}/` - Atualizar personagem
- `DELETE /api/v1/core/characters/{id}/` - Excluir personagem
- `POST /api/v1/core/characters/{id}/reset_sheet/` - Resetar ficha
- `POST /api/v1/core/characters/{id}/change_system/` - Trocar sistema do personagem

### 🎯 Sessões
- `GET /api/v1/session/sessions/` - Listar sessões do usuário
- `POST /api/v1/session/sessions/` - Criar nova sessão
- `GET /api/v1/session/sessions/{id}/` - Detalhes completos da sessão
- `POST /api/v1/session/sessions/{id}/create_invite/` - Criar convite
- `POST /api/v1/session/join-by-code/` - Entrar na sessão por código
- `POST /api/v1/session/select-character/` - Selecionar personagem

### 🗺️ Mapas
- `GET /api/v1/maps/maps/` - Listar mapas das sessões
- `POST /api/v1/maps/maps/` - Criar novo mapa (mestres)
- `GET /api/v1/maps/maps/{id}/` - Detalhes do mapa
- `PUT /api/v1/maps/maps/{id}/` - Atualizar mapa
- `DELETE /api/v1/maps/maps/{id}/` - Remover mapa
- `POST /api/v1/maps/maps/{id}/toggle_active/` - Ativar/desativar mapa

## 🎯 Estrutura de Resposta

### Login/Register Response
```json
{
    "message": "Login realizado com sucesso",
    "user": {
        "id": 1,
        "username": "jogador01",
        "email": "jogador@email.com",
        "first_name": "",
        "last_name": "",
        "date_joined": "2026-02-13T10:00:00Z"
    },
    "tokens": {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
}
```

### Sistemas de RPG Response
```json
{
    "id": "uuid-do-sistema",
    "name": "D&D 5ª Edição",
    "slug": "dnd5e",
    "description": "Sistema oficial de Dungeons & Dragons 5ª edição",
    "base_sheet_data": {
        "basic_info": {
            "level": 1,
            "class": "",
            "race": ""
        },
        "attributes": {
            "strength": 10,
            "dexterity": 10,
            "constitution": 10,
            "intelligence": 10,
            "wisdom": 10,
            "charisma": 10
        },
        "derived_stats": {
            "hit_points": {
                "max": 10,
                "current": 10
            },
            "armor_class": 10,
            "speed": 30
        }
    },
    "is_active": true,
    "is_default": true
}
```

### Criar Personagem Request
```json
{
    "player_name": "Eldrin Pedraverde",
    "rpg_system": "uuid-do-sistema-dnd5e",
    "description": "Um elfo ranger experiente",
    "avatar_url": "https://exemplo.com/avatar.jpg"
}
```

### Personagem Response
```json
{
    "id": "uuid-do-personagem",
    "player_name": "Eldrin Pedraverde",
    "rpg_system": "uuid-do-sistema",
    "rpg_system_info": {
        "id": "uuid-do-sistema",
        "name": "D&D 5ª Edição",
        "slug": "dnd5e",
        "description": "Sistema oficial de Dungeons & Dragons"
    },
    "system_key": "DND5E",
    "xp_total": 0,
    "description": "Um elfo ranger experiente",
    "sheet_data": {
        "basic_info": {
            "level": 1,
            "class": "Ranger",
            "race": "Elfo"
        },
        "attributes": {
            "strength": 12,
            "dexterity": 16,
            "constitution": 14,
            "intelligence": 13,
            "wisdom": 15,
            "charisma": 10
        }
    },
    "created_at": "2026-02-18T10:00:00Z",
    "user_info": {
        "id": 1,
        "username": "jogador01",
        "email": "jogador@email.com"
    }
}
```

## 🚀 Exemplos de Uso

### 1. Criando um PersonagemSimplificado

```bash
# 1. Listar sistemas disponíveis
GET /api/v1/core/rpg-systems/

# 2. Criar personagem (automaticamente usa template do sistema)
POST /api/v1/core/characters/
{
    "player_name": "Gandalf",
    "rpg_system": "uuid-do-dnd5e",
    "description": "Um mago poderoso"
}

# 3. O personagem já vem com a ficha base do D&D 5e preenchida!
```

### 2. Trocando Sistema do Personagem

```bash
# Trocar sistema e aplicar novo template
POST /api/v1/core/characters/{id}/change_system/
{
    "rpg_system_id": "uuid-do-call-of-cthulhu",
    "apply_template": true
}
```

### 3. Resetando Ficha para Template

```bash
# Resetar ficha para template original do sistema
POST /api/v1/core/characters/{id}/reset_sheet/
```

## 🔧 Próximos Passos

Este projeto oferece uma API completa para RPGs com:

1. **Sistema Extensível** - Adicione novos sistemas de RPG facilmente
2. **Fichas Dinâmicas** - Templates automáticos baseados no sistema
3. **Sessões Colaborativas** - Mestres e jogadores em tempo real
4. **Mapas Interativos** - Sistema de mapas por sessão
5. **Autenticação Robusta** - JWT com refresh automático
6. **Documentação Swagger** - API totalmente documentada

## 🛠️ Comandos Úteis

```bash
# Executar migrações
python manage.py migrate

# Popular sistemas de RPG padrão
python manage.py populate_rpg_systems

# Criar superusuário
python manage.py createsuperuser

# Executar servidor
python manage.py runserver
```

## 📦 Dependências Principais

- Django 4.2.0
- Django Rest Framework 3.14.0
- djangorestframework-simplejwt 5.2.2
- drf-spectacular (Swagger)
- django-cors-headers
- python-decouple

## 🎯 Funcionalidades Implementadas

- ✅ **Autenticação JWT** completa
- ✅ **Sistemas de RPG** com templates de ficha
- ✅ **Personagens** com fichas dinâmicas  
- ✅ **Sessões** com convites e membros
- ✅ **Mapas** por sessão
- ✅ **Admin Interface** completa
- ✅ **Documentação Swagger**
- ✅ **Permissões** detalhadas
- ✅ **API REST** padronizada

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.