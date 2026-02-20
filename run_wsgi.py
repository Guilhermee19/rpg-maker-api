#!/usr/bin/env python
"""
Script para rodar o servidor Django com WSGI ao invés de ASGI.
Use este script para desenvolvimento quando não precisar de WebSockets.
"""
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rpg_api.settings")
    
    # Remover temporariamente o Daphne dos INSTALLED_APPS
    from django.conf import settings
    if 'daphne' in settings.INSTALLED_APPS:
        installed_apps = list(settings.INSTALLED_APPS)
        installed_apps.remove('daphne')
        settings.INSTALLED_APPS = installed_apps
    
    # Rodar com o runserver padrão do Django (WSGI)
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
