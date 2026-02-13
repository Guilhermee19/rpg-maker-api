# Instruções de Deploy com PM2

## Arquivos criados para PM2

1. **start_django.sh** - Script de inicialização do Django
2. **ecosystem.config.js** - Configuração avançada do PM2
3. **logs/** - Diretório para logs da aplicação

## Como usar

### Opção 1: Comando direto com PM2
```bash
pm2 start start_django.sh --name finance-django
```

### Opção 2: Usando arquivo de configuração (Recomendado)
```bash
pm2 start ecosystem.config.js
```

## Comandos úteis do PM2

### Gerenciar a aplicação
```bash
# Verificar status
pm2 status

# Ver logs em tempo real
pm2 logs finance-django

# Parar a aplicação
pm2 stop finance-django

# Reiniciar a aplicação
pm2 restart finance-django

# Deletar a aplicação
pm2 delete finance-django

# Monitorar recursos
pm2 monit
```

### Configurar PM2 para iniciar com o sistema
```bash
pm2 startup
pm2 save
```

## Configurações importantes

- **Porta padrão**: 8000
- **Servidor**: Gunicorn (produção) ou Django dev server (fallback)
- **Logs**: Salvos em `./logs/`
- **Ambiente**: Produção (DEBUG=False)

## Antes do deploy

1. Certifique-se que as variáveis de ambiente estão configuradas
2. Configure banco de dados de produção se necessário
3. Configure um servidor web (Nginx) como proxy reverso
4. Configure SSL/HTTPS para produção

## Estrutura de logs

- `combined.log` - Logs combinados (stdout + stderr)
- `out.log` - Logs de saída
- `error.log` - Logs de erro