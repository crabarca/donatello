#!/usr/bin/zsh

if [ -z $(docker images -q postgres:10) ]; then
  echo "Pulling image..."
  docker pull postgres:10
fi

docker run -p 5433:5432 \
-e POSTGRES_PASSWORD="postgres" \
-e PGDATA=/var/lib/postgresql/data \
-e POSTGRES_DB="donatello" \
postgres:10