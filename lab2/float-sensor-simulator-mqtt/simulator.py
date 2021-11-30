import time
import random
import datetime

from configs.gcp_configs import *
from configs.mqtt_configs import *
from configs.device_configs import *

import paho.mqtt.client as mqtt
from paho.mqtt.client import ssl

from generators.jwt_generator import create_jwt
from generators.data_generator import generate_data

should_backoff = True
minimum_backoff_time = 1
maximum_backoff_time = 4


def error_str(rc):
    return "{}: {}".format(rc, mqtt.error_string(rc))


def on_connect(unused_client, unused_userdata, unused_flags, rc):
    print("Device " + DEVICE_ID + " successfully connected! ", mqtt.connack_string(rc))

    global should_backoff
    global minimum_backoff_time

    should_backoff = False
    minimum_backoff_time = 1


def on_disconnect(unused_client, unused_userdata, rc):
    print("Device " + DEVICE_ID + " disconnected! ", error_str(rc))

    global should_backoff
    should_backoff = True


def on_publish(unused_client, unused_userdata, unused_mid):
    print("Message published at " + str(datetime.datetime.utcnow()))


def get_client(
        project_id,
        cloud_region,
        registry_id,
        device_id,
        private_key_file,
        algorithm,
        ca_certs,
        mqtt_bridge_hostname,
        mqtt_bridge_port,
        jwt_expires_minutes
):
    client_id = "projects/{}/locations/{}/registries/{}/devices/{}".format(
        project_id, cloud_region, registry_id, device_id
    )
    print("Device client_id is '{}'".format(client_id))

    client = mqtt.Client(client_id=client_id)

    client.username_pw_set(
        username="unused", password=create_jwt(project_id, private_key_file, algorithm, jwt_expires_minutes)
    )

    client.tls_set(ca_certs=ca_certs, tls_version=ssl.PROTOCOL_TLSv1_2)

    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect

    client.connect(mqtt_bridge_hostname, mqtt_bridge_port)

    return client


def publish_data(
        jwt_expires_minutes,
        device_id,
        project_id,
        registry_id,
        cloud_region,
        ca_certs,
        algorithm,
        private_key_file,
        mqtt_bridge_port,
        mqtt_bridge_hostname,
):
    jwt_iat = datetime.datetime.utcnow()
    jwt_exp_seconds = jwt_expires_minutes * 60
    client = get_client(
        project_id,
        cloud_region,
        registry_id,
        device_id,
        private_key_file,
        algorithm,
        ca_certs,
        mqtt_bridge_hostname,
        mqtt_bridge_port,
        jwt_expires_minutes
    )

    global minimum_backoff_time

    while True:
        client.loop()

        if should_backoff:
            if minimum_backoff_time > maximum_backoff_time:
                print("Exceeded maximum backoff time. Giving up.")
                break

            delay = minimum_backoff_time + random.randint(0, 1000) / 1000.0
            print("Waiting for {} before reconnecting.".format(delay))
            time.sleep(delay)
            minimum_backoff_time *= 2
            client.connect(mqtt_bridge_hostname, mqtt_bridge_port)

        seconds_since_issue = (datetime.datetime.utcnow() - jwt_iat).seconds
        if seconds_since_issue > jwt_exp_seconds:
            print("Refreshing token after {}s".format(seconds_since_issue))
            jwt_iat = datetime.datetime.utcnow()
            client.loop()
            client.disconnect()
            client = get_client(
                project_id,
                cloud_region,
                registry_id,
                device_id,
                private_key_file,
                algorithm,
                ca_certs,
                mqtt_bridge_hostname,
                mqtt_bridge_port,
                jwt_expires_minutes
            )

        payload = generate_data(device_id)
        # breakpoint()
        client.publish("/devices/{}/{}".format(device_id, TELEMETRY_TOPIC), payload, qos=1)

        time.sleep(float(PUBLISHING_FREQUENCY_IN_SECONDS))


if __name__ == '__main__':
    publish_data(
        jwt_expires_minutes=5,
        project_id=PROJECT_ID,
        cloud_region=REGION,
        registry_id=REGISTRY_ID,
        device_id=DEVICE_ID,
        algorithm="RS256",
        ca_certs=CERTIFICATE_FILE_PATH,
        private_key_file=PRIVATE_KEY_FILE_PATH,
        mqtt_bridge_port=MQTT_BRIDGE_PORT,
        mqtt_bridge_hostname=MQTT_BRIDGE_HOSTNAME,
    )
