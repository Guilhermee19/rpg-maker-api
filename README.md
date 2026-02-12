# RPG Maker API

Uma API REST para sistema de RPG desenvolvida em Django com Django Rest Framework.

## 🚀 Características

- **Django Rest Framework** com ViewSets
- **Documentação Swagger** integrada
- **Sistema de autenticação** completo
- **Modelos RPG** (Personagens, Classes, Itens, Habilidades)
- **CORS** configurado para frontend
- **Filtros e pesquisa** em todas as APIs

## 📋 Estrutura do Projeto

```
rpg-maker-api/
├── rpg_api/           # Configurações principais do Django
├── core/              # App base (usuários, perfis)
├── authentication/    # Sistema de autenticação
├── game/             # Modelos e APIs do jogo
├── requirements.txt  # Dependências Python
└── README.md
```

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
copy .env.example .env

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

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **Schema JSON**: http://localhost:8000/api/schema/

## 🎮 Endpoints Principais

### Autenticação
- `POST /api/v1/auth/register/` - Registrar usuário
- `POST /api/v1/auth/login/` - Login
- `POST /api/v1/auth/logout/` - Logout

### Core
- `GET /api/v1/core/users/me/` - Dados do usuário atual
- `GET /api/v1/core/profiles/` - Perfis do usuário

### Game
- `GET /api/v1/game/character-classes/` - Classes de personagem
- `GET/POST /api/v1/game/characters/` - Personagens
- `GET /api/v1/game/items/` - Itens do jogo
- `GET /api/v1/game/skills/` - Habilidades
- `GET/POST /api/v1/game/inventory/` - Inventário dos personagens

## 🎯 Modelos Principais

### Character (Personagem)
```python
{
    "id": 1,
    "name": "Aragorn",
    "character_class": 1,
    "level": 5,
    "experience": 0,
    "current_health": 150,
    "current_mana": 75,
    "max_health": 150,
    "max_mana": 75,
    "attack": 20,
    "defense": 10,
    "speed": 15
}
```

### Item
```python
{
    "id": 1,
    "name": "Espada de Ferro",
    "item_type": "weapon",
    "rarity": "common",
    "value": 100,
    "attack_bonus": 10,
    "defense_bonus": 0
}
```

## 🔧 Próximos Passos

Este projeto fornece a base para:

1. **Sistema de batalha** - Implementar combate entre personagens
2. **Sistema de quests** - Adicionar missões e objetivos
3. **Mapas e dungeons** - Sistema de navegação
4. **Guilds** - Sistema social
5. **Economia** - Loja e comércio entre jogadores
6. **Sistema de chat** - Comunicação em tempo real

## 📦 Dependências

- Django 4.2.0
- Django Rest Framework 3.14.0
- drf-spectacular (Swagger)
- django-cors-headers
- python-decouple
- Pillow
- django-filter

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.