## Run in dev
```bash
docker compose -f docker-compose-dev.yml up -d
```

## Run without docker compose
### 1. Create network
```bash
docker network create series-bot
```
### 2. Pull and run postgresql
```bash
docker run \
  --name series-bot-postgresql \
  -p 5432:5432 \
  -v series_bot_postgresql_data:/var/lib/postgresql/data \
  --env-file ./.env.dev \
  --init \
  --network series-bot \
  postgres:16.1-alpine
```

### 3. Build and run backend
```bash
docker build \
  -t series-bot-backend:1.1 ./backend && \
docker run \
  --name series-bot-backend \
  --env-file ./config/postgresql/.env.dev \
  --env-file ./backend/config/.env.dev \
  -p 8000:8000 \
  -v ./backend:/backend \
  --network series-bot \
  series-bot-backend:1.1
```

### 4. Pull and run nginx
```bash
docker run \
  --name series-bot-nginx \
  -p 80:80 \
  -v ./config/nginx/nginx.dev.conf:/etc/nginx/conf.d/default.conf \
  --network series-bot \
  nginx:1.25.3-alpine
```

## TODO
* Add healthcheck to docker compose

## TODO (backend):
<del>* Add unique title validation to 'Series' model