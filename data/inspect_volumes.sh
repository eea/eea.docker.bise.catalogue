# A script to list volumes mounted in the docker stack
docker inspect --format="{{json .Mounts}}" eeadockerbisecatalogue_data_1 | python -c 'import sys, json, pprint;  print pprint.pformat(json.load(sys.stdin))'
