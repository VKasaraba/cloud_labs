import requests
import random
import time
import datetime

while True:
    for id in [1, 2]:
        http_data = {
            "report_time": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            "people_walked": random.randrange(100),
            "avg_time_near_panel": round(random.uniform(0.1, 2.5), 1),
            "apiKey": 'iovds8we47y48qq3uvjfdi8su'
        }
        requests.put(f'https://flask-server-w63pnhql7q-ey.a.run.app/sensors/{id}', json = http_data)
        print(f'sending data for sensor {id}')
    time.sleep(1)