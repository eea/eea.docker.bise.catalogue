#!/usr/bin/env python

import json
import os
import shutil
import subprocess

#   "Volumes": {
#       "/app/public/uploads": "/var/lib/docker/vfs/dir/e9aface12b8fe62a85c5bdb080cb1dada43957503a1c6163a55683aa95c0c901",
#       "/usr/share/elasticsearch/data": "/var/lib/docker/vfs/dir/580ce2ddc4cc2bbb5734c0c1e34195eb6202909792c03aafead56f2903557063",
#       "/var/lib/postgresql": "/var/lib/docker/vfs/dir/9c0949f885faf067e7d4add21958baa4f03266ba2449d6efcea50feeac159576",
#       "/var/lib/postgresql/data": "/var/lib/docker/vfs/dir/7f3103f87c6a89c9acd45f4a62553fa6327caa900b719e5efa2c74911b9ff08c"
#   },


def get_volumes(container_name):
    cmd = ['docker', 'inspect', '--format="{{json .Volumes}}"', container_name]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    resp = proc.stdout.read()
    data = json.loads(resp)
    return data


DESTINATIONS = {
    "/var/lib/postgresql": 'postgresql',
    "/var/lib/postgresql/data": 'postgresql-data',
#   "/usr/share/elasticsearch/data": 'elasticsearch',
    "/app/public/uploads": 'uploads',
}


CONTAINERS = [
    'eeadockerbisecatalogue_data_1',
#   'eeadockerbisecatalogue_dataw1_1',
#   'eeadockerbisecatalogue_dataw2_1'
]


def main():

    for name in CONTAINERS:
        volumes = get_volumes(name)
        print "*" * 20
        print name, "=>"
        print volumes
        for dest, vfs in sorted(volumes.items()):
            here = name + '/' + DESTINATIONS[dest]
            cmd = ['cp', '-Rfp', vfs, here]
            print "Copying ", vfs, " => ", here
            shutil.copytree(vfs, here)


if __name__ == "__main__":
    main()

# vim: set ts=4 sw=4 si et:
