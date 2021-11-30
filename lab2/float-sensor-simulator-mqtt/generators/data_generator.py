import json
import random
import datetime

id_counter = 1
def generate_data(device_id):
    global id_counter
    id_counter += 1
    id = id_counter % 2 + 3
    mqtt_data = {
            "id": id,
            "report_time": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            "people_walked": random.randrange(100),
            "avg_time_near_panel": round(random.uniform(0.1, 2.5), 1)
        }
    return json.dumps(mqtt_data)
