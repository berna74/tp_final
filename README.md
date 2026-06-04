# tp_final

## Backend

El backend de este proyecto se ejecuta solo con Docker Compose desde [backend/docker-compose.yml](backend/docker-compose.yml).

Comandos utiles:

```bash
cd backend
docker compose up -d
docker compose exec backend python manage.py check
./bin/migrations.sh
./bin/shell.sh
```

El entorno virtual local `.venv` no es necesario para correr el backend.
