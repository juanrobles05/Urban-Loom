# 🚀 Guía de Despliegue - Urban-Loom

Esta guía te ayudará a desplegar Urban-Loom usando Docker en producción.

## 📋 Requisitos Previos

- Docker >= 20.10
- Docker Compose >= 2.0
- Git

## 🔧 Configuración Inicial

### 1. Clonar el repositorio

```bash
git clone https://github.com/juanrobles05/Urban-Loom.git
cd Urban-Loom
```

### 2. Configurar variables de entorno

Copia el archivo de ejemplo y configúralo:

```bash
cp .env.example .env
```

Edita el archivo `.env` y configura las siguientes variables:

```env
SECRET_KEY=your-super-secret-key-here-change-this
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,localhost

# Para producción, considera usar PostgreSQL
# DATABASE_ENGINE=django.db.backends.postgresql
# DATABASE_NAME=urbanloom
# DATABASE_USER=urbanloom_user
# DATABASE_PASSWORD=your_secure_password
# DATABASE_HOST=db
# DATABASE_PORT=5432
```

### 3. Generar SECRET_KEY seguro

Puedes generar una clave secura con Python:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 🐳 Despliegue con Docker

### Opción 1: Solo Django (SQLite)

Esta es la opción más simple para empezar:

```bash
# Construir la imagen
docker build -t urbanloom:latest .

# Ejecutar el contenedor
docker run -d \
  --name urbanloom \
  -p 8000:8000 \
  -v $(pwd)/mediafiles:/app/mediafiles \
  -v $(pwd)/db.sqlite3:/app/db.sqlite3 \
  --env-file .env \
  urbanloom:latest
```

La aplicación estará disponible en: `http://localhost:8000`

### Opción 2: Con Docker Compose (Recomendado)

```bash
# Construir y levantar todos los servicios
docker-compose up -d --build

# Ver logs
docker-compose logs -f web

# Verificar estado
docker-compose ps
```

Servicios disponibles:
- **Django**: `http://localhost:8000`
- **Nginx**: `http://localhost:80` (si está habilitado)

### Opción 3: Con PostgreSQL

1. Descomenta la sección `db` en `docker-compose.yml`
2. Actualiza las variables de entorno en `.env`:

```env
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=urbanloom
DATABASE_USER=urbanloom_user
DATABASE_PASSWORD=your_secure_password
DATABASE_HOST=db
DATABASE_PORT=5432
```

3. Levanta los servicios:

```bash
docker-compose up -d --build
```

## 🔐 Configuración de Seguridad

### Superusuario por defecto

El script de entrypoint crea automáticamente un superusuario:

- **Email**: `admin@urbanloom.com`
- **Password**: `admin123`

⚠️ **IMPORTANTE**: Cambia estas credenciales inmediatamente después del primer acceso:

```bash
docker-compose exec web python manage.py changepassword admin@urbanloom.com
```

### HTTPS (Producción)

Para habilitar HTTPS:

1. Obtén certificados SSL (Let's Encrypt, etc.)
2. Coloca los certificados en `nginx/ssl/`
3. Descomenta la configuración HTTPS en `nginx/nginx.conf`
4. Actualiza las variables de entorno:

```env
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
```

## 📊 Comandos Útiles

### Gestión de contenedores

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Logs de un servicio específico
docker-compose logs -f web

# Reiniciar servicios
docker-compose restart

# Detener servicios
docker-compose stop

# Detener y eliminar contenedores
docker-compose down

# Detener y eliminar contenedores + volúmenes
docker-compose down -v
```

### Gestión de Django

```bash
# Acceder al shell de Django
docker-compose exec web python manage.py shell

# Crear migraciones
docker-compose exec web python manage.py makemigrations

# Aplicar migraciones
docker-compose exec web python manage.py migrate

# Crear superusuario
docker-compose exec web python manage.py createsuperuser

# Recolectar archivos estáticos
docker-compose exec web python manage.py collectstatic --noinput
```

### Backup de la base de datos

**SQLite:**
```bash
# Backup
docker cp urbanloom_web:/app/db.sqlite3 ./backup_db.sqlite3

# Restore
docker cp ./backup_db.sqlite3 urbanloom_web:/app/db.sqlite3
```

**PostgreSQL:**
```bash
# Backup
docker-compose exec db pg_dump -U urbanloom_user urbanloom > backup.sql

# Restore
docker-compose exec -T db psql -U urbanloom_user urbanloom < backup.sql
```

## 🔍 Monitoreo y Troubleshooting

### Health Check

```bash
# Verificar estado de salud
curl http://localhost:8000

# Con nginx
curl http://localhost/health/
```

### Ver logs de errores

```bash
# Logs de Django
docker-compose exec web tail -f logs/django.log

# Logs de Nginx
docker-compose exec nginx tail -f /var/log/nginx/error.log
```

### Problemas comunes

1. **Puerto 8000 ya en uso**
   ```bash
   # Cambiar puerto en docker-compose.yml
   ports:
     - "8001:8000"  # Usa 8001 en lugar de 8000
   ```

2. **Error de permisos en archivos**
   ```bash
   # Ajustar permisos
   sudo chown -R $USER:$USER mediafiles staticfiles logs
   ```

3. **Migraciones pendientes**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

## 🌐 Despliegue en Producción

### Checklist de Producción

- [ ] `DEBUG=False` en `.env`
- [ ] `SECRET_KEY` único y seguro
- [ ] `ALLOWED_HOSTS` configurado correctamente
- [ ] HTTPS habilitado
- [ ] Certificados SSL válidos
- [ ] Credenciales por defecto cambiadas
- [ ] Base de datos con backup automático
- [ ] Monitoreo configurado
- [ ] Logs rotando correctamente
- [ ] Firewall configurado
- [ ] Variables sensibles en `.env` (no en código)

### Proveedores Cloud Recomendados

- **AWS ECS/Fargate**: Para despliegue con Docker
- **Google Cloud Run**: Serverless containers
- **DigitalOcean App Platform**: Simple y económico
- **Azure Container Instances**: Integración con Azure
- **Railway/Render**: Deployment fácil con Git

### Ejemplo: DigitalOcean

```bash
# 1. Crear un Droplet con Docker
# 2. Clonar el repositorio
# 3. Configurar .env
# 4. docker-compose up -d --build
# 5. Configurar firewall
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable
```

## 📈 Escalabilidad

### Aumentar workers de Gunicorn

Edita el `Dockerfile` o `docker-compose.yml`:

```yaml
command: gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 5
```

Fórmula recomendada: `(2 x CPU cores) + 1`

### Load Balancing

Para múltiples instancias, usa un load balancer (nginx, HAProxy, AWS ALB, etc.)

## 🆘 Soporte

Para problemas o preguntas:
- **Issues**: https://github.com/juanrobles05/Urban-Loom/issues
- **Email**: admin@urbanloom.com

## 📝 Licencia

Ver archivo `LICENSE` en el repositorio.
