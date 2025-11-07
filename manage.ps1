# Urban-Loom - Script de gestión para Windows PowerShell

param(
    [Parameter(Position=0)]
    [string]$Command
)

function Show-Help {
    Write-Host "====================================" -ForegroundColor Cyan
    Write-Host "Urban-Loom - Comandos Disponibles" -ForegroundColor Cyan
    Write-Host "====================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Uso: .\manage.ps1 <comando>" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Comandos:" -ForegroundColor Green
    Write-Host "  setup           - Configuración inicial completa"
    Write-Host "  build           - Construir imagen Docker"
    Write-Host "  up              - Levantar contenedores"
    Write-Host "  down            - Detener contenedores"
    Write-Host "  restart         - Reiniciar contenedores"
    Write-Host "  logs            - Ver logs en tiempo real"
    Write-Host "  shell           - Acceder al shell del contenedor"
    Write-Host "  migrate         - Ejecutar migraciones"
    Write-Host "  createsuperuser - Crear superusuario"
    Write-Host "  collectstatic   - Recolectar archivos estáticos"
    Write-Host "  test            - Ejecutar tests"
    Write-Host "  clean           - Limpiar archivos generados"
    Write-Host "  dev             - Modo desarrollo local"
    Write-Host ""
}

function Setup {
    Write-Host "🚀 Configurando Urban-Loom..." -ForegroundColor Green
    
    if (!(Test-Path .env)) {
        Write-Host "📝 Creando archivo .env..." -ForegroundColor Yellow
        Copy-Item .env.example .env
        Write-Host "⚠️  Edita el archivo .env con tus configuraciones" -ForegroundColor Yellow
    }
    
    Write-Host "🐳 Construyendo imagen Docker..." -ForegroundColor Green
    docker-compose build
    
    Write-Host "▶️  Levantando contenedores..." -ForegroundColor Green
    docker-compose up -d
    
    Write-Host "🔄 Ejecutando migraciones..." -ForegroundColor Green
    docker-compose exec web python manage.py migrate
    
    Write-Host "📦 Recolectando archivos estáticos..." -ForegroundColor Green
    docker-compose exec web python manage.py collectstatic --noinput
    
    Write-Host ""
    Write-Host "✅ Urban-Loom está listo!" -ForegroundColor Green
    Write-Host "Accede a: http://localhost:8000" -ForegroundColor Cyan
}

function Build {
    Write-Host "🏗️  Construyendo imagen Docker..." -ForegroundColor Green
    docker-compose build
}

function Up {
    Write-Host "▶️  Levantando contenedores..." -ForegroundColor Green
    docker-compose up -d
    Write-Host "✅ Contenedores iniciados" -ForegroundColor Green
}

function Down {
    Write-Host "⏹️  Deteniendo contenedores..." -ForegroundColor Yellow
    docker-compose down
    Write-Host "✅ Contenedores detenidos" -ForegroundColor Green
}

function Restart {
    Write-Host "🔄 Reiniciando contenedores..." -ForegroundColor Yellow
    docker-compose restart
    Write-Host "✅ Contenedores reiniciados" -ForegroundColor Green
}

function Show-Logs {
    Write-Host "📋 Mostrando logs (Ctrl+C para salir)..." -ForegroundColor Cyan
    docker-compose logs -f
}

function Enter-Shell {
    Write-Host "🖥️  Accediendo al shell..." -ForegroundColor Cyan
    docker-compose exec web bash
}

function Run-Migrate {
    Write-Host "🔄 Ejecutando migraciones..." -ForegroundColor Green
    docker-compose exec web python manage.py migrate
}

function Create-Superuser {
    Write-Host "👤 Creando superusuario..." -ForegroundColor Green
    docker-compose exec web python manage.py createsuperuser
}

function Collect-Static {
    Write-Host "📦 Recolectando archivos estáticos..." -ForegroundColor Green
    docker-compose exec web python manage.py collectstatic --noinput
}

function Run-Tests {
    Write-Host "🧪 Ejecutando tests..." -ForegroundColor Green
    docker-compose exec web python manage.py test
}

function Clean {
    Write-Host "🧹 Limpiando archivos generados..." -ForegroundColor Yellow
    Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
    Get-ChildItem -Path . -Recurse -File -Filter "*.pyc" | Remove-Item -Force
    if (Test-Path htmlcov) { Remove-Item -Recurse -Force htmlcov }
    if (Test-Path .coverage) { Remove-Item -Force .coverage }
    Write-Host "✅ Limpieza completada" -ForegroundColor Green
}

function Dev-Mode {
    Write-Host "🔧 Iniciando modo desarrollo..." -ForegroundColor Green
    python manage.py runserver
}

# Ejecutar comando
switch ($Command) {
    "setup" { Setup }
    "build" { Build }
    "up" { Up }
    "down" { Down }
    "restart" { Restart }
    "logs" { Show-Logs }
    "shell" { Enter-Shell }
    "migrate" { Run-Migrate }
    "createsuperuser" { Create-Superuser }
    "collectstatic" { Collect-Static }
    "test" { Run-Tests }
    "clean" { Clean }
    "dev" { Dev-Mode }
    default { Show-Help }
}
