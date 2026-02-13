#!/usr/bin/env python
"""
Script para configurar o projeto inicial
"""

import os
import sys
import subprocess

def run_command(command, description):
    """Executa um comando e imprime o resultado"""
    print(f"\n🔄 {description}...")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ {description} - Concluído!")
        if result.stdout:
            print(result.stdout)
    else:
        print(f"❌ Erro ao {description}")
        print(result.stderr)
        return False
    return True

def main():
    print("🎮 Configurando projeto RPG Maker API...")
    
    commands = [
        ("python manage.py makemigrations", "Criando migrações"),
        ("python manage.py migrate", "Aplicando migrações"),
        ("python manage.py loaddata game/fixtures/initial_data.json", "Carregando dados iniciais"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            print("\n❌ Setup falhou! Verifique os erros acima.")
            return
    
    print("\n🎉 Setup completo!")
    print("\n📚 Próximos passos:")
    print("1. Criar superusuário: python manage.py createsuperuser")
    print("2. Executar servidor: python manage.py runserver")
    print("3. Acessar documentação: http://localhost:8001/api/docs/")
    

if __name__ == "__main__":
    main()