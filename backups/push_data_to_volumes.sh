#!/bin/bash

DATA_ID="eeadockerbisecatalogue_data_1"
echo "Processing $DATA_ID"

echo "Copying PG data"
# Copy Postgres files to the data container
docker run --rm -v `pwd`/$DATA_ID/postgresql-data:/host --volumes-from=$DATA_ID busybox sh -c 'cp -R /host/* /var/lib/postgresql/data'
# Fix permissions
docker run --rm --volumes-from=$DATA_ID busybox chown 999:999 /var/lib/postgresql -R
docker run --rm --volumes-from=$DATA_ID busybox chmod 700 /var/lib/postgresql/data
# Fix remote access, from other hosts
docker run --rm --volumes-from=$DATA_ID busybox sed -ri "s/^#(listen_addresses\s*=\s*)\S+/\1'*'/" /var/lib/postgresql/data/postgresql.conf
docker run --rm --volumes-from=$DATA_ID busybox sh -c 'echo "host all all 0.0.0.0/0 trust" >> /var/lib/postgresql/data/pg_hba.conf'

echo "Copying uploads"
docker run --rm -v `pwd`/$DATA_ID/uploads:/host --volumes-from=$DATA_ID busybox cp -R /host/document /app/public/uploads
docker run --rm -v `pwd`/$DATA_ID/uploads:/host --volumes-from=$DATA_ID busybox cp -R /host/tmp /app/public/uploads

#echo "Copying ES data for $DATA_ID"
# Copy Elasticsearch files to the data container
#docker run --rm -v `pwd`/$DATA_ID/elasticsearch:/host --volumes-from=$DATA_ID busybox sh -c 'cp -R /host/* /usr/share/elasticsearch/data/'
# Fix state. Not needed if using the same ES version (1.3)
#docker run --rm --volumes-from=$DATA_ID busybox sh -c 'find "/usr/share/elasticsearch/data/Catalogue Cluster/nodes/0/" -name "state-*" -not -name "state-*.st" -exec rm \{\} \;'


#DATA_ID="eeadockerbisecatalogue_dataw1_1"
#echo "Processing $DATA_ID"
#echo "Copying ES data for $DATA_ID"
#docker run --rm -v `pwd`/$DATA_ID/elasticsearch:/host --volumes-from=$DATA_ID busybox sh -c 'cp -R /host/* /usr/share/elasticsearch/data/'

#DATA_ID="eeadockerbisecatalogue_dataw2_1"
#echo "Processing $DATA_ID"
#echo "Copying ES data for $DATA_ID"
#docker run --rm -v `pwd`/$DATA_ID/elasticsearch:/host --volumes-from=$DATA_ID busybox sh -c 'cp -R /host/* /usr/share/elasticsearch/data'
