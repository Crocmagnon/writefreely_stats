from flask import Flask, request
import csv
from io import StringIO
from influxdb import InfluxDBClient
import datetime
import os


INFLUX_USER = os.getenv("INFLUX_USER")
INFLUX_PASSWORD = os.getenv("INFLUX_PASSWORD")
INFLUX_DB = os.getenv("INFLUX_DB")

app = Flask(__name__)

@app.route("/stats", methods=["POST"])
def hello_world():
    client = InfluxDBClient('localhost', 8086, INFLUX_USER, INFLUX_PASSWORD, INFLUX_DB)
    influx_data = []
    time = datetime.datetime.now().astimezone().isoformat()

    data = request.data.decode("utf-8").split("\r\n")
    reader = csv.DictReader(data, delimiter=",", quotechar='"')
    for line in reader:
        try:
            view_count = int(line["view_count"])
            id_ = line["id"]
            slug = line["slug"]
            title = line["title"]
        except (ValueError, KeyError):
            continue
        
        influx_data.append({
            "measurement": "blog_stats",
            "time": time,
            "tags": {
                "id": id_,
                "slug": slug,
                "title": title
            },
            "fields": {
                "value": view_count
            }
        })
    
    if influx_data:
        client.write_points(influx_data)
        return "written"
    return "nothing to write"
