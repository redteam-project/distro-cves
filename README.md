# distro-cves
Utility to import Linux distro CVE data into BigQuery

## Under development

This repo is being actively developed, check back soon for updates.

As of this commit, Debian is the only supported distro.

## Setup

* Set up a GCP account and login
* Run locally

```
git clone https://github.com/redteam-project/distro-cves
cd distro-cves
python3 ./distro-cves.py
bq mk cves
bq mk cves.debian
gsutil mb yourbucket
gsutil cp debian/newline.json gs://yourbucket/debian/newline.json
bq load --autodetect --source_format=NEWLINE_DELIMITED_JSON red-team-project:cves.debian gs://yourbucket/debian/newline.json
bq query --format=prettyjson "select * from cves.debian limit 1"
```