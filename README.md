# qBittorrent Scripts

Collection of Python scripts to be used with qBittorrent.

## Scripts

### tag-tracker-errors

Checks all torrents and then tags them with a tag name you provide when the tracker is not working.

```sh
python3 scripts/tag-tracker-errors.py \
    --qb-host "" \
    --qb-username "" \
    --qb-password "" \
    --qb-tag "Broken Torrents" \
    --debug
```

Inspiration from [JakeWharton/qbt-tracker-hound](https://github.com/JakeWharton/qbt-tracker-hound)
