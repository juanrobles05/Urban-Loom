.PHONY: help build up down restart logs shell migrate createsuperuser collectstatic test clean

help: ## Mostrar este mensaje de ayuda
	@echo "Comandos disponibles para Urban-Loom:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Construir la imagen Docker
	docker-compose build

up: ## Levantar los contenedores en modo detached
	docker-compose up -d

down: ## Detener y eliminar los contenedores
	docker-compose down

restart: ## Reiniciar los contenedores
	docker-compose restart

logs: ## Ver logs en tiempo real
	docker-compose logs -f

logs-web: ## Ver logs solo del servicio web
	docker-compose logs -f web

shell: ## Acceder al shell del contenedor web
	docker-compose exec web bash

django-shell: ## Acceder al shell de Django
	docker-compose exec web python manage.py shell

migrate: ## Ejecutar migraciones de base de datos
	docker-compose exec web python manage.py migrate

makemigrations: ## Crear nuevas migraciones
	docker-compose exec web python manage.py makemigrations

createsuperuser: ## Crear un superusuario
	docker-compose exec web python manage.py createsuperuser

collectstatic: ## Recolectar archivos estáticos
	docker-compose exec web python manage.py collectstatic --noinput

test: ## Ejecutar tests
	docker-compose exec web python manage.py test

test-coverage: ## Ejecutar tests con coverage
	docker-compose exec web coverage run --source='.' manage.py test
	docker-compose exec web coverage report
	docker-compose exec web coverage html

clean: ## Limpiar archivos generados
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete 2>/dev/null || true
	rm -rf htmlcov/ .coverage 2>/dev/null || true

clean-docker: ## Limpiar contenedores, imágenes y volúmenes Docker
	docker-compose down -v --rmi all

install: ## Instalar dependencias localmente
	pip install -r requirements.txt

setup: build up migrate collectstatic ## Setup completo: build, up, migrate y collectstatic
	@echo "✅ Urban-Loom está listo!"
	@echo "Accede a: http://localhost:8000"

dev: ## Modo desarrollo - ejecutar servidor local
	python manage.py runserver

prod-check: ## Verificar configuración de producción
	docker-compose exec web python manage.py check --deploy
