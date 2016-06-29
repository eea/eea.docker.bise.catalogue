echo "Creating containers"

echo "Starting docker stack to create containers"
docker-compose up -d

echo "Stoping docker stack"
docker-compose stop

echo "Copy backup data to containers"
cd data
./push_data_to_volumes.sh

echo "Starting back docker stack"
cd -
docker-compose start
