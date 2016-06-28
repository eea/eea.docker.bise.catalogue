docker-compose stop

echo "Stopping services"
docker stop $(docker-compose ps -q)

echo "Removing services"
docker rm -f $(docker-compose ps -q)

echo "Removing dangling volumes"
docker volume rm $(docker volume ls -qf dangling=true)
