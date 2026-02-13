#!/usr/bin/env python
"""
Verificação do sistema de sessões - Admin
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
    
    print("🔍 Verificando configuração das Sessões...")
    
    # Verifica se o app está instalado
    from django.conf import settings
    if 'session' in settings.INSTALLED_APPS:
        print("✅ App 'session' instalado corretamente")
    else:
        print("❌ App 'session' não encontrado nos INSTALLED_APPS")
        
    # Testa importação dos modelos
    from session.models import Session, SessionMember, SessionInvite, SessionCharacter
    print("✅ Modelos importados com sucesso")
    
    # Testa importação do admin
    from session.admin import SessionAdmin, SessionMemberAdmin, SessionInviteAdmin, SessionCharacterAdmin
    print("✅ Admin classes importadas com sucesso")
    
    # Verifica se os modelos têm __str__ methods
    session_str = hasattr(Session, '__str__')
    member_str = hasattr(SessionMember, '__str__')
    invite_str = hasattr(SessionInvite, '__str__')
    character_str = hasattr(SessionCharacter, '__str__')
    
    if all([session_str, member_str, invite_str, character_str]):
        print("✅ Todos os modelos têm métodos __str__")
    else:
        print("⚠️ Alguns modelos não têm métodos __str__")
    
    # Verifica verbose names
    print(f"✅ Verbose names configurados:")
    print(f"   Session: {Session._meta.verbose_name}")
    print(f"   SessionMember: {SessionMember._meta.verbose_name}")
    print(f"   SessionInvite: {SessionInvite._meta.verbose_name}")
    print(f"   SessionCharacter: {SessionCharacter._meta.verbose_name}")
    
    print("\n🎉 Configuração das sessões verificada com sucesso!")
    print("\n📋 Próximos passos:")
    print("1. python manage.py migrate")
    print("2. python manage.py runserver")
    print("3. Acesse /admin/ e vá para a seção 'SESSÕES DE RPG'")
    
except Exception as e:
    print(f"❌ Erro encontrado: {e}")
    print(f"🔧 Tipo do erro: {type(e).__name__}")
    
    import traceback
    print("\n📋 Stack trace:")
    print(traceback.format_exc())