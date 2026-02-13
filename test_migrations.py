#!/usr/bin/env python
"""
Teste de migrations - verifica se as dependências estão corretas
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
    
    print("🔍 Verificando estrutura de migrations...")
    
    from django.db import migrations
    from django.db.migrations.loader import MigrationLoader
    from django.db import connections, DEFAULT_DB_ALIAS
    
    # Testa se o loader consegue construir o grafo sem erros
    try:
        loader = MigrationLoader(connections[DEFAULT_DB_ALIAS])
        print("✅ Grafo de migrations carregado com sucesso")
        
        # Lista migrations por app
        for app_name in ['characters', 'session', 'core']:
            if app_name in loader.migrated_apps:
                app_migrations = loader.disk_migrations
                app_migs = [key for key in app_migrations.keys() if key[0] == app_name]
                print(f"📦 {app_name}: {len(app_migs)} migrations")
                for migration_key in sorted(app_migs):
                    print(f"   - {migration_key[1]}")
        
        print("\n🎉 Estrutura de migrations válida!")
        print("💡 Agora você pode executar:")
        print("   python manage.py migrate")
        print("   python manage.py runserver")
        
    except Exception as migration_error:
        print(f"❌ Erro no grafo de migrations: {migration_error}")
        return False
        
    return True
        
except Exception as e:
    print(f"❌ Erro de setup: {e}")
    print(f"🔧 Tipo do erro: {type(e).__name__}")
    
    import traceback
    print("\n📋 Stack trace:")
    print(traceback.format_exc())
    return False

if __name__ == "__main__":
    success = True
    if not success:
        sys.exit(1)