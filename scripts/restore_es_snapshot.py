#!/usr/bin/env python

import argparse
import requests
import sys


_sn_tpl = """
Snapshot: {} @ {} - {}
\tIndexes: {}
\tShards: {}/{}
"""


def _get_indices(server):
    url = 'http://{}:9200/_cluster/state'.format(server)
    ixs = requests.get(url).json()['metadata']['indices'].keys()
    return ixs


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
    ixs = _get_indices(server)

    op = {
        False: '_open',
        True: '_close',
    }[close]

    for ix in ixs:
        print("{} index {}".format(op, ix))
        url = 'http://{}:9200/{}/{}'.format(server, ix, op)
        req = requests.post(url)
        assert req.json()['acknowledged'] is True


def make_backup(server, name):
    url = ('http://{}:9200/_snapshot/backup/{}?wait_for_completion=true'
           .format(server, name))
    res = requests.put(url).json()
    assert res.json()['accepted'] is True
    print "Snapshot restored"


def restore_backup(server, name):
    _openclose_indices(server, close=True)
    url = 'http://{}:9200/_snapshot/backup/{}/_restore'.format(server, name)
    res = requests.post(url).json()
    _openclose_indices(server, close=False)
    print(res)


def del_all(server):
    _openclose_indices(server, close=False)
    url = 'http://{}:9200/_all/_settings'.format(server)
    all = requests.get(url).json().keys()

    for ix in all:
        print("Deleting {} index ".format(ix))
        url = 'http://{}:9200/{}'.format(server, ix)
        req = requests.delete(url)
        assert req.json()['acknowledged'] is True


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
    handlers = {
        'view': lambda args: show_backups(args.hostname),
        'backup': lambda args: make_backup(args.hostname, args.snapshot),
        'restore': lambda args: restore_backup(args.hostname, args.snapshot),
        'delall': lambda args: del_all(args.hostname),
    }

    parser = argparse.ArgumentParser()
    parser.add_argument("hostname",
                        help="Server hostname")
    parser.add_argument(
        "command",
        help="The command you want performed. One of: " +
             ", ".join(handlers.keys())
    )
    parser.add_argument("--snapshot",
                        help="Snapshot name you want restored")
    args = parser.parse_args()

    server = args.hostname
    create_snapshot_location(server)

    def fallback(*args):
        print "Not a command"
        return sys.exit(1)

    cmd = args.command
    handlers.get(cmd, fallback)(args)


if __name__ == "__main__":
    main()
