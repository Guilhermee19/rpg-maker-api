#!/usr/bin/env python
"""
Debug script para verificar erros na geração do schema
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
    
    # Tenta gerar schema diretamente
    from drf_spectacular.generators import SchemaGenerator
    
    print("Attempting to generate schema...")
    generator = SchemaGenerator(title='RPG Maker API')
    schema = generator.get_schema()
    
    print("SUCCESS! Schema generated without errors")
    print(f"Schema has {len(schema.get('paths', {}))} endpoints")
    
except Exception as e:
    print(f"ERROR: {type(e).__name__}")
    print(f"Message: {str(e)}")
    print("\nFull traceback:")
    traceback.print_exc()
