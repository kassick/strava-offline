# strava-offline

## Overview

strava-offline is a tool to keep a local mirror of Strava activities for
further analysis/processing:

* synchronizes metadata about your bikes and activities to an [SQLite][]
  database

* downloads all your activities as [GPX][] (and supports not downloading [bulk
  exported][strava-bulk-export] activities again)

[SQLite]: https://www.sqlite.org/
[GPX]: https://en.wikipedia.org/wiki/GPS_Exchange_Format

Example of what you can do with the data:

![sql-yearly-summary](https://user-images.githubusercontent.com/300342/94435822-ec3e5a00-019b-11eb-84db-01d61eacfb56.png)

## Installation

```
pipx ensurepath
pipx install --spec git+https://github.com/liskin/strava-offline strava_offline
```

To keep a local git clone around:

```
git clone https://github.com/liskin/strava-offline
make -C strava-offline pipx
```

Alternatively, if you don't need the isolated virtualenv that [pipx][]
provides, feel free to just:

```
pip install git+https://github.com/liskin/strava-offline
```

[pipx]: https://github.com/pipxproject/pipx

## Preparation

* You'll need to obtain Client ID and Client Secret from
  <https://www.strava.com/settings/api> and then pass these as `--client-id`
  and `--client-secret` command line arguments or export as `STRAVA_CLIENT_ID`
  and `STRAVA_CLIENT_SECRET` environment variables.

  That settings page also lists Your Access Token but this won't let you
  download private activities or see names of bikes. Therefore its use is not
  supported in strava-offline.

* For GPX downloading, you'll also need to get the `_strava4_session` cookie
  from your web browser session. Open <https://strava.com/> in your browser
  and then follow a guide for your browser to obtain the cookie value:

  * [Chrome](https://developers.google.com/web/tools/chrome-devtools/storage/cookies)
  * [Firefox](https://developer.mozilla.org/en-US/docs/Tools/Storage_Inspector)
  * [Edge](https://docs.microsoft.com/en-us/microsoft-edge/devtools-guide-chromium/storage/cookies)

## Mirror activities metadata

```
$ strava-offline sqlite --help
usage: strava-offline sqlite [-h] [--client-id XXX] [--client-secret XXX] [--token-file FILE]
                             [--http-host HOST] [--http-port PORT] [--full] [--database FILE]

Synchronize bikes and activities metadata to local sqlite3 database. Unless --full is given, the
sync is incremental, i.e. only new activities are synchronized and deletions aren't detected.

optional arguments:
  -h, --help           show this help message and exit
  --full               perform full sync instead of incremental

Strava API:
  --client-id XXX      strava oauth2 client id (default: genenv('STRAVA_CLIENT_ID'))
  --client-secret XXX  strava oauth2 client secret (default: genenv('STRAVA_CLIENT_SECRET'))
  --token-file FILE    strava oauth2 token store (default: token.json)
  --http-host HOST     oauth2 http server host (default: 127.0.0.1)
  --http-port PORT     oauth2 http server port (default: 12345)

strava-offline database:
  --database FILE      sqlite database file (default: strava.sqlite)
```

## Mirror activities as GPX

**Important:** To avoid overloading Strava servers (and possibly getting
noticed), first download all your existing activities using the [Bulk Export
feature of Strava][strava-bulk-export]. Then use `--dir-activities-backup` at
least once to let strava-offline reuse these downloaded files.

[strava-bulk-export]: https://support.strava.com/hc/en-us/articles/216918437-Exporting-your-Data-and-Bulk-Export#Bulk

```
$ strava-offline gpx --help
usage: strava-offline gpx [-h] [--strava4-session XX] [--dir-activities DIR]
                          [--dir-activities-backup DIR] [--database FILE]

Download known (previously synced using the "sqlite" command) activities in GPX format. It's
recommended to only use this incrementally to download the latest activities every day or week,
and download the bulk of your historic activities directly from Strava. Use --dir-activities-
backup to avoid downloading activities already downloaded in the bulk.

optional arguments:
  -h, --help            show this help message and exit

Strava web:
  --strava4-session XX  '_strava4_session' cookie value (default:
                        genenv('STRAVA_COOKIE_STRAVA4_SESSION'))

strava-offline gpx storage:
  --dir-activities DIR  directory to store gpx files indexed by activity id (default:
                        strava_data/activities)
  --dir-activities-backup DIR
                        optional path to activities in Strava backup (no need to redownload these)

strava-offline database:
  --database FILE       sqlite database file (default: strava.sqlite)
```

## Donations (♥ = €)

If you like this tool and wish to support its development and maintenance,
please consider [a small donation](https://www.paypal.me/lisknisi/10EUR).

By donating, you'll also support the development of my other projects. You
might like these:

* <https://github.com/liskin/strava-map-switcher> - Map switcher for Strava website
* <https://github.com/liskin/locus-graphhopper-gpx> - Convert GraphHopper JSON to GPX with Locus nav. instructions
* <https://github.com/liskin/leaflet-tripreport> - A simple tool for visualization of bikepacking trips, both planned and ridden
