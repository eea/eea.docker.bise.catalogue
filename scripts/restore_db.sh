echo "Warning: This will drop the existing databases!!!"

docker exec -it eeadockerbisecatalogue_db_1 sh -c "dropdb -i -U postgres catalogue_development"
docker exec -it eeadockerbisecatalogue_db_1 sh -c "dropdb -i -U postgres catalogue_production"

docker exec -it eeadockerbisecatalogue_db_1 sh -c "createdb -U postgres catalogue_development"
docker exec -it eeadockerbisecatalogue_db_1 sh -c "createdb -U postgres catalogue_production"

docker exec eeadockerbisecatalogue_db_1 sh -c "/usr/bin/psql -U postgres catalogue_production < /tmp/db.sql"
docker exec eeadockerbisecatalogue_db_1 sh -c "/usr/bin/psql -U postgres catalogue_development < /tmp/db.sql"
