# eea.docker.bise.catalogue

BISE Catalogue docker orchestration

## Development instance

    docker-compose -f docker-compose.dev.yml -p bisedev build
    docker-compose -f docker-compose.dev.yml -p bisedev run web bundle exec rake db:create
    docker-compose -f docker-compose.dev.yml -p bisedev run web bundle exec rake db:migrate
    docker-compose -f docker-compose.dev.yml -p bisedev run web bundle exec rake db:seed

To get admin rights, start the instance, login with eionet, then:

   docker-compose -f docker-compose.dev.yml -p bisedev run db psql -U postgres -h db
   \c catalogue_development;
   update users set role_admin='t';
   CTRL+D

## Prerequisites

Copy `bise-catalogue/config/ldap.example.yml` into `bise-catalogue/config/ldap.yml` and modify it
with the LDAP admin credentials for EIONET.

## Start

    docker-compose up
