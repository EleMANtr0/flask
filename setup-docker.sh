docker build -t flask-web .
#network
docker network create flask_db-net
#db
docker run -d --name flask_db --restart unless-stopped --net flask_db-net -p 5432:5432 --env-file .env -e POSTGRES_USER=${POSTGRES_USER} -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} -e POSTGRES_DB=${POSTGRES_DB} -e DOCKER_ENV=true -v pgdata:/var/lib/postgresql/data postgres:16
#app
docker run -d --name flask-web --restart unless-stopped --net flask_db-net -p 5000:5000 --env-file .env -e FLASK_APP=main.py -e FLASK_ENV=development -e DATABASE_URL="postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${DB_HOST}:5432/${POSTGRES_DB}" -v "./flask learn:/opt/flask learn" flask-web python3 main.py
