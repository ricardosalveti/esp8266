#
# Copyright: Ricardo Salveti <rsalveti@rsalveti.net>
#
# SPDX-License-Identifier: MIT

import time
import machine
import dht
import ubinascii
import utils
from umqtt.robust import MQTTClient

def main():
    config = utils.Config()

    # On board LED
    led = machine.Pin(2, machine.Pin.OUT, machine.Pin.PULL_UP)

    sensor = dht.DHT22(machine.Pin(config.get("dht_gpio", 4)))

    client_id = "esp8266_" + ubinascii.hexlify(machine.unique_id()).format()
    client = MQTTClient(client_id, config.get("mqtt_broker"),
                        config.get("mqtt_port"), config.get("mqtt_user"),
                        config.get("mqtt_passwd"))
    try:
        client.connect()
    except OSError as e:
        # Just report and continue, since publish will try to reconnect
        print("Error when connecting to the MQTT broker")
    else:
        print("Connected to {}".format(config.get("mqtt_broker")))

    # Iterate and publish
    while True:
        sensor.measure()
        led.low()
        client.publish("{}/temperature".format(config.get("mqtt_topic")),
                                      str(sensor.temperature()))
        client.publish("{}/humidity".format(config.get("mqtt_topic")),
                                      str(sensor.humidity()))
        led.high()
        time.sleep(5)

if __name__ == '__main__':
    main()
