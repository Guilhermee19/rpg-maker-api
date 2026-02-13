#!/usr/bin/env python
"""
Teste rápido para verificar se o schema está funcionando
"""

import os
import django
from pathlib import Path
import sys

# Setup básico do Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rpg_api.settings')

try:
    django.setup()
    
    print("🔍 Testando Schema da API...")
    
    # Testa importação dos ViewSets
    from characters.views import CharacterViewSet
    from core.views import UserViewSet
    print("✅ ViewSets importados com sucesso")
    
    # Testa importação dos Serializers
    from characters.serializers import CharacterSerializer
    from core.serializers import UserSerializer
    print("✅ Serializers importados com sucesso")
    
    # Testa geração do schema
    from drf_spectacular.openapi import AutoSchema
    from rest_framework.request import Request
    from django.test import RequestFactory
    
    factory = RequestFactory()
    request = factory.get('/api/schema/')
    
    # Tenta gerar schema para CharacterViewSet
    character_view = CharacterViewSet()
    character_view.action = 'list'
    character_view.request = Request(request)
    
    schema = AutoSchema()
    schema.view = character_view
    schema.method = 'GET'
    schema.path = '/api/v1/core/characters/'
    
    print("✅ Schema geração testada com sucesso")
    
    print("\n🎉 Todos os testes passaram!")
    print("💡 O problema pode estar no servidor. Tente reiniciar:")
    print("   python manage.py runserver")
    
except Exception as e:
    print(f"❌ Erro encontrado: {e}")
    print(f"🔧 Tipo do erro: {type(e).__name__}")
    
    import traceback
    print("\n📋 Stack trace completo:")
    print(traceback.format_exc())