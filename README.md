# eea.docker.bise.catalogue

BISE Catalogue docker orchestration

## Development instance

    docker-compose -f docker-compose.dev.yml build
    docker-compose -f docker-compose.dev.yml run web bundle exec rake db:create
    docker-compose -f docker-compose.dev.yml run web bundle exec rake db:migrate
    docker-compose -f docker-compose.dev.yml run web bundle exec rake db:seed

To get admin rights, start the instance, login with eionet, then:

   docker-compose -f docker-compose.dev.yml run db psql -U postgres -h db
   \c catalogue_development;
   update users set role_admin='t';
   CTRL+D

## Prerequisites

Copy `bise-catalogue/config/ldap.example.yml` into `bise-catalogue/config/ldap.yml` and modify it
with the LDAP admin credentials for EIONET.

Edit a `.secret` file for Postfix SMTP authentication, see: http://github.com/eea/eea.docker.postfix for more details.

## Start

    docker-compose up
