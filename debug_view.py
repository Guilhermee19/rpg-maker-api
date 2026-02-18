#!/usr/bin/env python
"""
Script para testar a view de schema diretamente
"""

import os
import django
from pathlib import Path
import sys
import traceback

# Setup básico do Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rpg_api.settings')

try:
    django.setup()
    print("Django setup completed")
    
    # Tenta chamar a view espectacular diretamente
    from django.test import RequestFactory
    from drf_spectacular.views import SpectacularAPIView
    
    print("Creating request factory...")
    factory = RequestFactory()
    request = factory.get('/api/schema/')
    
    print("Creating view...")
    view = SpectacularAPIView.as_view()
    
    print("Executing view...")
    response = view(request)
    
    print(f"Response status code: {response.status_code}")
    
    if response.status_code != 200:
        print(f"ERROR: Got status {response.status_code}")
        # Try to render the response to trigger any errors
        response.render()
        print(f"Response content: {response.content[:500]}")
    else:
        print("SUCCESS! Schema view works")
        print(f"Response content length: {len(response.content)}")
    
except Exception as e:
    print(f"ERROR: {type(e).__name__}")
    print(f"Message: {str(e)}")
    print("\nFull traceback:")
    traceback.print_exc()
