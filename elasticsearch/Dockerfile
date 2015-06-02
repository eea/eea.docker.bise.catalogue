FROM elasticsearch:1.3

RUN plugin -install elasticsearch/elasticsearch-mapper-attachments/2.3.2
RUN plugin -install mobz/elasticsearch-head

RUN echo 'cluster.name: "Catalogue Cluster"' >> /usr/share/elasticsearch/config/elasticsearch.yml