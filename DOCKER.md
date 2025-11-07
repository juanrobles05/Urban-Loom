# 🐳 Docker Quick Start

## Construcción y ejecución rápida

### 1. Preparar entorno
```bash
# Copiar variables de entorno
cp .env.example .env

# Editar .env con tus configuraciones
# Especialmente cambiar SECRET_KEY y DEBUG=False para producción
```

### 2. Construir imagen Docker
```bash
docker build -t urbanloom:latest .
```

### 3. Ejecutar contenedor
```bash
docker run -d \
  --name urbanloom \
  -p 8000:8000 \
  -v $(pwd)/mediafiles:/app/mediafiles \
  -v $(pwd)/staticfiles:/app/staticfiles \
  -v $(pwd)/db.sqlite3:/app/db.sqlite3 \
  -v $(pwd)/logs:/app/logs \
  --env-file .env \
  urbanloom:latest
```

### 4. Verificar
```bash
# Ver logs
docker logs -f urbanloom

# Verificar estado
curl http://localhost:8000
```

## Usando Docker Compose (Recomendado)

### Levantar todos los servicios
```bash
docker-compose up -d --build
```

### Comandos útiles
```bash
# Ver logs
docker-compose logs -f

# Reiniciar
docker-compose restart

# Detener
docker-compose down

# Ejecutar comandos Django
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

## Acceso

- **Aplicación**: http://localhost:8000
- **Admin**: http://localhost:8000/admin
- **Credenciales por defecto**: 
  - Email: `admin@urbanloom.com`
  - Password: `admin123`

⚠️ **Cambiar credenciales en producción!**

## Ver documentación completa

Para más detalles, ver [DEPLOYMENT.md](./DEPLOYMENT.md)
