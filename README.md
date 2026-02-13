# RPG Maker API - Auth

Uma API REST de autenticação para sistema de RPG desenvolvida em Django com Django Rest Framework e JWT.

## 🚀 Características

- **JWT Authentication** com tokens de acesso e refresh
- **Django Rest Framework** com views customizadas
- **Documentação Swagger** integrada
- **Sistema de autenticação completo** (registro, login, logout)
- **CORS** configurado para frontend
- **Token refresh** automático

## 📋 Estrutura do Projeto

```
rpg-maker-api/
├── rpg_api/           # Configurações principais do Django
└── authentication/    # Sistema de autenticação com JWT
    ├── views.py        # Endpoints de autenticação
    └── urls.py         # Rotas da API
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

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **Schema JSON**: http://localhost:8000/api/schema/

## 🎮 Endpoints Disponíveis

### Autenticação
- `POST /api/v1/auth/register/` - Registrar novo usuário
- `POST /api/v1/auth/login/` - Login do usuário
- `POST /api/v1/auth/logout/` - Logout do usuário
- `GET /api/v1/auth/get-user/` - Obter dados do usuário atual
- `POST /api/v1/auth/token/refresh/` - Renovar token de acesso

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

### Get User Response
```json
{
    "user": {
        "id": 1,
        "username": "jogador01",
        "email": "jogador@email.com",
        "first_name": "",
        "last_name": "",
        "date_joined": "2026-02-13T10:00:00Z"
    }
}
```

## 🔧 Próximos Passos

Este projeto fornece uma base de autenticação JWT limpa para:

1. **Adicionar modelos de negócio** - Personagens, items, etc.
2. **Implementar permissões** - Baseadas em grupos/roles
3. **Expandir perfil de usuário** - Campos adicionais
4. **Sistema de refresh automático** - Frontend
5. **Validações personalizadas** - Senhas, emails
6. **Rate limiting** - Proteção contra ataques

## 📦 Dependências

- Django 4.2.0
- Django Rest Framework 3.14.0
- djangorestframework-simplejwt 5.2.2
- drf-spectacular (Swagger)
- django-cors-headers
- python-decouple

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.