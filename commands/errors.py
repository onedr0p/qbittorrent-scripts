import re

import typer
from loguru import logger

FILTERED_TRACKER_URLS = {
    '** [DHT] **',
    '** [PeX] **',
    '** [LSD] **'
}

FILTERED_TRACKER_MESSAGES = {
    'unregistered',
    'unregistered torrent',
    'torrent not found',
    'torrent is not found',
    'not registered',
    'not exist',
    'unknown torrent',
    'trump',
    'retitled',
    'truncated',
    'not authorized'
}

app = typer.Typer()

@app.command()
def tag(ctx: typer.Context):
    # Iterate thru all the torrents
    for torrent in ctx.obj.client.torrents.info():
        # Filter out DHT, PeX & LSD torrents
        trackers = [tracker for tracker in torrent.trackers if torrent.tracker not in FILTERED_TRACKER_URLS]  
        # Build array of tags      
        tags = torrent.tags.split(', ')
        # Iterate thru add the trackers in a torrent
        for tracker in trackers:
            # Tag unregistered torrents
            if any(re.search(pattern, tracker.msg, re.IGNORECASE) for pattern in FILTERED_TRACKER_MESSAGES):
                logger.debug(f"Tagging torrent {torrent.name} as Unregistered")
                if "Unregistered" not in tags: torrent.addTags("Unregistered")
            # Tag errored torrents
            elif tracker.status == 4:
                logger.debug(f"Tagging {torrent.name} as Errored")
                if "Errored" not in tags: torrent.addTags("Errored")
            # Untag unregistered and errored torrents
            else:
                if "Errored" in tags: torrent.removeTags("Errored")
                if "Unregistered" not in tags: torrent.removeTags("Unregistered")

@app.command()
def delete(ctx: typer.Context):
    # Iterate thru all the torrents
    for torrent in ctx.obj.client.torrents.info():
        # Filter out DHT, PeX & LSD torrents
        trackers = [tracker for tracker in torrent.trackers if torrent.tracker not in FILTERED_TRACKER_URLS]
        # Iterate thru add the trackers in a torrent
        for tracker in trackers:
            # Delete unregistered torrents
            if any(re.search(pattern, tracker.msg, re.IGNORECASE) for pattern in FILTERED_TRACKER_MESSAGES):
                logger.debug(f"Deleting torrent {torrent.name} - {tracker.msg}")
                # torrent.delete(delete_files=True)
                break
                

if __name__ == "__main__":
    app()
