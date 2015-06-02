#!/bin/bash

./_init.sh

# Upload local data from the host to the data container

if [ "$DATA_ID" == '' ]; then
    echo "Please export the data docker container id as DATA_ID."
    exit 1
fi

# Copy Postgres files to the data container
docker run --rm -v `pwd`/postgresql:/host --volumes-from=$DATA_ID busybox cp -r /host/data /var/lib/postgresql
# Fix permissions
docker run --rm --volumes-from=$DATA_ID busybox chown 999:999 /var/lib/postgresql -R
# Fix access
docker run --rm --volumes-from=$DATA_ID busybox sed -ri "s/^#(listen_addresses\s*=\s*)\S+/\1'*'/" /var/lib/postgresql/data/postgresql.conf
docker run --rm --volumes-from=$DATA_ID busybox sh -c 'echo "host all all 0.0.0.0/0 trust" >> /var/lib/postgresql/data/pg_hba.conf'

# Copy Elasticsearch files to the data container
docker run --rm -v `pwd`/elasticsearch:/host --volumes-from=$DATA_ID busybox cp -r /host/data /usr/share/elasticsearch
# Fix state. Not needed if using the same ES version (1.3)
#docker run --rm --volumes-from=$DATA_ID busybox sh -c 'find "/usr/share/elasticsearch/data/Catalogue Cluster/nodes/0/" -name "state-*" -not -name "state-*.st" -exec rm \{\} \;'

# Copy uploads
docker run --rm -v `pwd`/uploads:/host --volumes-from=$DATA_ID busybox cp -r /host/document /app/public/uploads
