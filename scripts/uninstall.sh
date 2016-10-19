#!/bin/bash
if [ -z $CFG ]; then
	echo "Please set \$CFG name";
	exit 1
fi

echo "Stopping services"
docker-compose -f $CFG stop

echo "Removing services"
docker-compose -f $CFG down

echo "Removing dangling volumes"
docker volume rm $(docker volume ls -qf dangling=true)

#docker stop $(docker-compose -f $CFG ps -q)
#docker rm -f $(docker-compose -f $CFG ps -q)
