#!/usr/bin/env python

import requests
import sys


_sn_tpl = """
Snapshot: {} @ {} - {}
\tIndexes: {}
\tShards: {}/{}
"""


def create_snapshot_location(server):
    settings = {
        "type": "fs",
        "settings": {
            "compress": "true",
            "location": "/snapshots/"
        }
    }
    print("Creating snapshot location")
    url = 'http://{}:9200/_snapshot/backup'.format(server)
    req = requests.put(url, json=settings)
    assert req.json()['acknowledged'] is True


def _openclose_indices(server, close=True):
    url = 'http://{}:9200/_all/_settings'.format(server)
    all = requests.get(url).json().keys()

    op = {
        False: '_open',
        True: '_close',
    }[close]

    for ix in all:
        print("{} index ".format(op, ix))
        url = 'http://{}:9200/{}/{}'.format(server, ix, op)
        req = requests.post(url)
        assert req.json()['acknowledged'] is True


def make_backup(server, name):
    url = ('http://{}:9200/_snapshot/backup/{}?wait_for_completion=true'
           .format(server, name))
    res = requests.put(url).json()
    print(res)


def restore_backup(server, name):
    _openclose_indices(server, close=True)
    url = 'http://{}:9200/_snapshot/backup/{}/_restore'.format(server, name)
    res = requests.post(url).json()
    _openclose_indices(server, close=False)
    print(res)


def show_backups(server):
    print("Showing existing snapshots:\r")
    url = 'http://{}:9200/_snapshot/backup/_all'.format(server)
    req = requests.get(url)
    resp = req.json()
    snaps = resp['snapshots']
    for sn in snaps:
        print(_sn_tpl.format(
            sn['snapshot'],
            sn['start_time'],
            sn['state'],
            len(sn['indices']),
            sn['shards']['total'],
            sn['shards']['successful']
        ))


def main():
    if not len(sys.argv) >= 3:
        print("Please provide ip address and "
              "an operation [view|backup|restore]")
        sys.exit(1)

    cmd = sys.argv[2]

    server = sys.argv[1].strip()
    create_snapshot_location(server)

    if cmd == "view":
        show_backups(server)

    elif cmd == "backup":
        name = sys.argv[3].strip()
        make_backup(server, name)

    elif cmd == "restore":
        name = sys.argv[3].strip()
        restore_backup(server, name)


if __name__ == "__main__":
    main()
