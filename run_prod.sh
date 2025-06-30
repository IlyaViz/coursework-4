docker compose -f docker-compose.prod.yml up certbot --build
docker compose -f docker-compose.prod.yml up --build --scale certbot=0