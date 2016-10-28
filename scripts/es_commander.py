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


def create_snapshot_location(args):
    settings = {
        "type": "fs",
        "settings": {
            "compress": "true",
            "location": "/snapshots/"
        }
    }
    print("Creating snapshot location")
    url = 'http://{}:9200/_snapshot/backup'.format(args.hostname)
    req = requests.put(url, json=settings)
    assert req.json()['acknowledged'] is True


def _openclose_indices(server, close=True):
    ixs = _get_indices(server)

    op = {
        False: '_open',
        True: '_close',
    }[close]

    for ix in ixs:
        # print("{} index {}".format(op, ix))
        url = 'http://{}:9200/{}/{}'.format(server, ix, op)
        req = requests.post(url)
        assert req.json()['acknowledged'] is True


def make_backup(args):
    server = args.hostname
    name = args.snapshot
    url = ('http://{}:9200/_snapshot/backup/{}?wait_for_completion=true'
           .format(server, name))
    res = requests.put(url).json()
    assert res.json()['accepted'] is True
    print "Snapshot restored"


def restore_backup(args):
    server = args.hostname
    name = args.snapshot
    _openclose_indices(server, close=True)
    url = 'http://{}:9200/_snapshot/backup/{}/_restore'.format(server, name)
    res = requests.post(url).json()
    _openclose_indices(server, close=False)
    print(res)


def del_all(args):
    server = args.hostname
    _openclose_indices(server, close=False)
    url = 'http://{}:9200/_all/_settings'.format(server)
    all = requests.get(url).json().keys()

    for ix in all:
        print("Deleting {} index ".format(ix))
        url = 'http://{}:9200/{}'.format(server, ix)
        req = requests.delete(url)
        assert req.json()['acknowledged'] is True


def show_backups(args):
    server = args.hostname
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


def _get_matching_indexes(server, match=""):
    url = 'http://{}:9200/_all/_settings'.format(server)
    all = requests.get(url).json().keys()

    matches = []
    for ix in all:
        if match in ix:
            matches.append(ix)

    if not matches:
        print "No matches"
        return []

    return matches


def del_indexes(args):
    server = args.hostname
    match = args.match
    _openclose_indices(server, close=False)

    matches = _get_matching_indexes(server, match)

    print "This will delete the following indexes: ", ", ".join(matches)
    inp = input("Are you sure you want to continue? y/n [n]")
    if inp.lower() != 'y':
        return

    for ix in matches:
        print("Deleting {} index ".format(ix))
        url = 'http://{}:9200/{}'.format(server, ix)
        req = requests.delete(url)
        assert req.json()['acknowledged'] is True


def set_replicas(args):
    server = args.hostname
    match = args.match

    if not args.replicas.isdigit():
        print "Please set --replicas to a valid number"
        sys.exit(1)

    replicas = int(args.replicas)
    _openclose_indices(server, close=False)
    matches = _get_matching_indexes(server, match)

    settings = {"index": {"number_of_replicas": replicas}}
    for ix in matches:
        url = 'http://{}:9200/{}/_settings'.format(server, ix)
        req = requests.put(url, json=settings)
        assert req.json()['acknowledged'] is True


def main():
    handlers = {
        'init': create_snapshot_location,
        'view': show_backups,
        'backup': make_backup,
        'restore': restore_backup,
        'delall': del_all,
        'del': del_indexes,
        'setreplicas': set_replicas,
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
    parser.add_argument("--match",
                        help="Match indexes to delete",
                        default="")
    parser.add_argument("--replicas",
                        help="Number of replicas to set",
                        default="0")
    args = parser.parse_args()

    def fallback(*args):
        print "Not a command"
        return sys.exit(1)

    cmd = args.command
    handlers.get(cmd, fallback)(args)


if __name__ == "__main__":
    main()
