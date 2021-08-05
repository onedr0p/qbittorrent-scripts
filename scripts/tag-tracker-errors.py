#!/usr/bin/python3 -u

import logging

import click
from qbittorrentapi import Client

IGNORED_TRACKER_URLS = {'** [DHT] **', '** [PeX] **', '** [LSD] **'}

@click.command()
@click.option(
    "--qb-host", envvar="QB_HOST",
    required=True,
    help="qBittorrent host"
)
@click.option(
    "--qb-username", envvar="QB_USERNAME",
    required=False,
    help="qBittorrent username"
)
@click.option(
    "--qb-password", envvar="QB_PASSWORD",
    required=False,
    help="qBittorrent password"
)
@click.option(
    "--qb-tag", envvar="QB_TAG",
    required=True,
    help="Tag to apply to torrents with tracker errors"
)
@click.option(
    "--debug", envvar="DEBUG",
    is_flag=True,
    default=False,
    required=False,
    help="Turn on debug logging"
)

@click.pass_context
def cli(ctx, qb_host, qb_username, qb_password, qb_tag, debug):
    ctx.obj = {
        "qb_host": qb_host,
        "qb_username": qb_username,
        "qb_password": qb_password,
        "qb_tag": qb_tag,
        "debug": debug
    }

    # pylint: disable=no-value-for-parameter
    log = logger()

    client = Client(host=qb_host, username=qb_username, password=qb_password)

    for torrent in client.torrents.info():
        if debug:
            log.debug(f"--- {torrent.name} ---")
            log.debug(f"Tags {torrent.tags}")

        has_working_trackers = False
        for tracker in torrent.trackers:
            tracker_working = tracker.status != 4 and tracker.url not in IGNORED_TRACKER_URLS
            if debug:
                log.debug(f"Tracker: {tracker.url} {tracker_working} {tracker.status} {tracker.msg}")
            if tracker_working:
                has_working_trackers = True

        torrent_tags = torrent.tags.split(', ')
        if has_working_trackers:
            if qb_tag in torrent_tags:
                log.debug(f"Clearing {torrent.name}")
                torrent.removeTags(qb_tag)
        else:
            if qb_tag not in torrent_tags:
                log.debug(f"Tagging {torrent.name}")
                torrent.addTags(qb_tag)

@click.pass_context
def logger(ctx):
    """Set up logging
    """
    logging.basicConfig(
        level=(logging.DEBUG if ctx.obj["debug"] else logging.INFO),
        format="%(asctime)s %(name)s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    return logging.getLogger("Tag Tracker Errors")

if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    cli()
