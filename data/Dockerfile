FROM busybox

RUN mkdir -p /var/lib/postgresql/data
RUN mkdir -p /usr/share/elasticsearch/data
RUN mkdir -p /app/public/uploads

VOLUME ["/var/lib/postgresql", "/var/lib/postgresql/data"]
VOLUME /usr/share/elasticsearch/data
VOLUME /app/public/uploads

