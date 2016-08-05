docker-compose -f docker-compose.dev.yml stop

echo "Stopping services"
docker stop $(docker-compose -f docker-compose.dev.yml ps -q)

echo "Removing services"
docker rm -f $(docker-compose -f docker-compose.dev.yml ps -q)

echo "Removing dangling volumes"
docker volume rm $(docker volume ls -qf dangling=true)
