# Writefreely stats
Simple flask app to receive Writefreely blog stats as CSV and send them to InfluxDB

## Crontask

Send your stats every 10 minutes:

```
*/10 * * * * sqlite3 /srv/writefreely/writefreely.db ".mode csv" ".header on" "select id, slug, view_count, title from posts order by view_count desc;" | curl -X POST -H "Content-Type: text/csv" -m 30 --data-binary @- "http://<YOUR_INSTANCE>:<PORT>/stats"
```

## systemd service

```
# /etc/systemd/system/blog_stats.service

[Unit]
Description=Blog stats
After=network-online.target influxdb.service

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/blog_stats
ExecStart=/home/pi/blog_stats/.venv/bin/uwsgi --http [::]:<PORT> --wsgi-file main.py --callable app
Environment="INFLUX_USER=<USER>"
Environment="INFLUX_PASSWORD=<PWD>"
Environment="INFLUX_DB=<DB>"

[Install]
WantedBy=multi-user.target
```


# Reuse
If you do reuse my work, please consider linking back to this repository 🙂