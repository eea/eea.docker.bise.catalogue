echo "Starting docker stack to create containers"
docker-compose up -d

echo "Stoping docker stack"
docker-compose stop

echo "Copy backup data to containers"
cd data
for DATA_ID in eeadockerbisecatalogue_data_1 eeadockerbisecatalogue_dataw1_1 eeadockerbisecatalogue_dataw2_1; do export DATA_ID; ./put.sh; done

echo "Starting back docker stack"
cd -
docker-compose up -d
