#!/bin/bash
if [ -z $CFG ]; then
	echo "Please set \$CFG name";
	exit 1
fi

echo "Creating containers with $CFG"

echo "Starting docker stack to create containers"
docker-compose -f $CFG up -d

echo "Stoping docker stack"
docker-compose -f $CFG stop

echo "Copy backup data to containers"
cd backups/
./push_data_to_volumes.sh

echo "Starting back docker stack"
cd -
docker-compose -f $CFG start
