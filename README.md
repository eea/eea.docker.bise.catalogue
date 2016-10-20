# eea.docker.bise.catalogue

[BISE Catalogue](https://github.com/eea/bise.catalogue) docker orchestration

A BISE Catalogue deployment requires [Docker](https://docs.docker.com/installation/) at least 1.6 and [Docker Compose](https://docs.docker.com/compose/install/) at least 1.2 running on a host with a Linux Kernel 3.16 or newer.

## Development instance

    docker-compose -f development.yml build
    docker-compose -f development.yml run --rm web bundle exec rake db:create db:migrate db:seed

To get admin rights, start the instance, login with Eionet LDAP account, then:

    docker-compose -f development.yml run db psql -U postgres -h db
    \c catalogue_development;
    update users set role_admin='t';
    CTRL+D

This updates the catalogue_development database and sets the admin flag for all existing users.

## Prerequisites

Copy `bise-catalogue/config/ldap.example.yml` into `bise-catalogue/config/ldap.yml` and modify it with the LDAP admin credentials for EIONET.

**IMPORTANT**: Use the ldap server in the same network/as close as posible to the production.

Edit a `.secret` file for Postfix SMTP authentication, see: http://github.com/eea/eea.docker.postfix for more details.

## Start

    docker-compose up

Check the web application is running on localhost:80 (default port, can be changed in development.yml file).

### Production deployment

### Initial setup

**Step 1**: Clone the repo. Setup secrets

    git clone https://github.com/eea/eea.docker.bise.catalogue.git
    cd eea.docker.bise.catalogue
    cp bise-catalogue/config/ldap.example.yml bise-catalogue/config/ldap.yml
    # edit ldap.yml, add authentication and ldap server
    touch .secret
    # edit .secret, add authentication to the email server, see https://github.com/eea/eea.docker.postfix/blob/master/.secret.example for more details

**Step 2**: Start the containers

(we need to start them once so the data volumes are created)

     docker-compose up -d

**Step 3a**: Initialise database (for new setup only)

     docker exec -it eeadockerbisecatalogue_web_1 bundle exec rake db:create db:migrate

**Step 3b**: Migrate existing database (for migrating data from an existing installation)

TODO: this information is old, update instructions.

(we are using two scripts to fetch data from an existing instance and another one to push it into the data containers)

     docker-compose stop
     cd data
     ./fetch.sh
     for DATA_ID in eeadockerbisecatalogue_data_1 eeadockerbisecatalogue_dataw1_1 eeadockerbisecatalogue_dataw2_1; do
     ./put.sh
     done
     cd -
     docker-compose up -d

**Step 4**: Check installation

     curl localhost

**Extra**: How to get admin rights

Login using your EIONET ldap account, then issue:

    docker exec -it eeadockerbisecatalogue_db_1 bash
    su postgres
    psql
    \c catalogue_production;
    update users set role_admin='t';
    CTRL+D

The Docker service should expose a frontend nginx container on the port 80.

### Migrating between servers

**Step0**: Locate where the instrumentation checkout sits on the disk. This should be a git clone of this project. Try /root or /var/local/deploy

**Step1**: In this location, use the data/make_backups.py script to make a backup of the proper Docker volumes.

**Step2**: Copy this location to the new server. It will have all necesarry configuration files already setup. Optional: use eeacms/rsync Docker image to perform the copy operation between servers.

**Step3**: Use 'sh install.sh' script to install the containers on this new server.

If anything goes wrong, use 'sh uninstall.sh' script to remove all containers and start all over again.

**Step4**: See elasticsearch.txt on how to migrate ES data using snapshots


### Code changes / re-deployment

Any changes to the eea/bise.catalogue repository will trigger a new build in Docker Hub: https://registry.hub.docker.com/u/eeacms/bise.catalogue/

To apply them on production, run:

    cd eea.docker.bise.catalogue
    docker pull eeacms/bise.catalogue:latest
    docker-compose stop
    docker-compose up -d
    docker exec -it eeadockerbisecatalogue_web_1 rake db:migrate
