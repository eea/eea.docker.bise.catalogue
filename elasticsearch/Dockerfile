#FROM elasticsearch:2.4.0
FROM elasticsearch:1.4.5

# for ES 1.7
# RUN plugin -install elasticsearch/elasticsearch-mapper-attachments/2.7.1

# for ES 1.4
RUN plugin -install elasticsearch/elasticsearch-mapper-attachments/2.4.3

# for eeacms.elasticsearch:bise
# RUN plugin install mapper-attachments

RUN plugin -install mobz/elasticsearch-head

RUN echo 'cluster.name: "Catalogue Cluster"' >> /usr/share/elasticsearch/config/elasticsearch.yml
RUN mkdir -p /snapshots
RUN echo 'repo.path: ["/snapshots"]' >> /usr/share/elasticsearch/config/elasticsearch.yml
