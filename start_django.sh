#!/bin/bash

# Script para iniciar Django com PM2
# Para usar: pm2 start start_django.sh --name rpg-maker-api

# Definir diretório do projeto
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$PROJECT_DIR"

# Verificar se existe ambiente virtual e ativar
if [ -d "venv" ]; then
    echo "Ativando ambiente virtual..."
    source venv/bin/activate
elif [ -d ".venv" ]; then
    echo "Ativando ambiente virtual..."
    source .venv/bin/activate
elif [ -d "env" ]; then
    echo "Ativando ambiente virtual..."
    source env/bin/activate
fi

# Verificar se requirements.txt existe e instalar dependências
if [ -f "requirements.txt" ]; then
    echo "Verificando dependências..."
    pip install -r requirements.txt --quiet
fi

# Executar migrações
echo "Executando migrações..."
python manage.py migrate --noinput

# Coletar arquivos estáticos (caso necessário em produção)
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --clear

# Configurar variáveis de ambiente para produção
export DEBUG=False
export DJANGO_SETTINGS_MODULE=rpg_api.settings

# Verificar se gunicorn está instalado, se não, usar o servidor do Django
if command -v gunicorn &> /dev/null; then
    echo "Iniciando servidor com Gunicorn..."
    # Usar gunicorn para produção (recomendado)
    exec gunicorn rpg_api.wsgi:application \
        --bind 0.0.0.0:8000 \
        --workers 3 \
        --timeout 30 \
        --keep-alive 5 \
        --max-requests 1000 \
        --max-requests-jitter 50 \
        --access-logfile - \
        --error-logfile -
else
    echo "Gunicorn não encontrado. Instalando..."
    pip install gunicorn
    echo "Iniciando servidor com Gunicorn..."
    exec gunicorn rpg_api.wsgi:application \
        --bind 0.0.0.0:8000 \
        --workers 3 \
        --timeout 30 \
        --keep-alive 5 \
        --max-requests 1000 \
        --max-requests-jitter 50 \
        --access-logfile - \
        --error-logfile -
fi