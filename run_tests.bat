@echo off
echo 🧪 Executando testes do RPG Maker API...
echo.

python manage.py test --verbosity=2

if %errorlevel% equ 0 (
    echo.
    echo ✅ Todos os testes passaram!
) else (
    echo.
    echo ❌ Alguns testes falharam!
)

pause