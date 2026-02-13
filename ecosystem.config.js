module.exports = {
  apps: [{
    name: 'rpg-maker-api',
    script: 'bash',
    args: './start_django.sh', // Passamos o script como argumento para o bash
    cwd: '/root/projects/rpg-maker-api',
    
    // Configurações de ambiente
    env: {
      NODE_ENV: 'production',
      DEBUG: 'False',
      PORT: 8000
    },
    
    // Configurações do PM2
    instances: 1, // Ou 'max' para usar todos os cores
    exec_mode: 'fork', // ou 'cluster' se tiver múltiplas instâncias
    
    // Configurações de logs
    log_file: './logs/combined.log',
    out_file: './logs/out.log',
    error_file: './logs/error.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
    
    // Auto restart configurações
    autorestart: true,
    watch: false, // Não usar watch em produção
    max_memory_restart: '500M',
    
    // Configurações de restart
    min_uptime: '10s',
    max_restarts: 10,
    
    // Configurações avançadas
    kill_timeout: 5000,
    wait_ready: true,
    listen_timeout: 3000,
    
    // Configurações de saúde
    health_check_http: {
      url: 'http://localhost:8001',
      interval: 30000,
      timeout: 5000
    }
  }]
};