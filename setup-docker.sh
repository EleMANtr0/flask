docker build -t elemantro/flask_learn .
#network
docker network create flask_learn-net
docker network create flask_db-net
#es
docker run -d --name es --net flask_learn-net -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:6.3.2
#db
docker volume create pgdata
docker run -d --name db --net flask_db-net -p 5432:5432 --env-file .env -v pgdata:/var/lib/postgresql/data postgres:16
#app
docker run -d --net flask_learn-net -p 5000:5000 --name flask_learn --env-file .env elemantro/flask_learn

docker network connect flask_db-net flask_learn