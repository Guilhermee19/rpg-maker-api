# Teste dos Endpoints de Autenticação

## Executar o servidor
```bash
python manage.py runserver
```

## 1. Registrar usuário
```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "jogador01", 
    "email": "jogador@email.com", 
    "password": "senha123"
  }'
```

## 2. Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "jogador01", 
    "password": "senha123"
  }'
```

## 3. Obter dados do usuário
```bash
curl -X GET http://localhost:8000/api/v1/auth/get-user/ \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN"
```

## 4. Renovar token
```bash
curl -X POST http://localhost:8000/api/v1/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "SEU_REFRESH_TOKEN"
  }'
```

## 5. Logout
```bash
curl -X POST http://localhost:8000/api/v1/auth/logout/ \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "SEU_REFRESH_TOKEN"
  }'
```

## Exemplo de Response (Login/Register)
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