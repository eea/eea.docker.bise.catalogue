#!/bin/bash

SERVER=termite.eea.europa.eu

./_init.sh

rsync -avz $SERVER':/var/lib/pgsql/data/*' ./postgresql/data
rsync -avz $SERVER':/var/lib/elasticsearch/*' ./elasticsearch/data
rsync -avz $SERVER':/var/local/apps/catalogue/shared/uploads/document/*' ./uploads/document

