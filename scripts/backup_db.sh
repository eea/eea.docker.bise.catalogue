docker exec -it eeadockerbisecatalogue_db_1 sh -c "pg_dump -U postgres catalogue_production > /app/public/uploads/out.sql"
