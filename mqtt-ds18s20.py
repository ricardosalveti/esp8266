#
# Copyright: Ricardo Salveti <rsalveti@rsalveti.net>
#
# SPDX-License-Identifier: MIT

import time
import machine
import onewire, ds18x20
import ubinascii
import utils
from umqtt.robust import MQTTClient

def main():
    config = utils.Config()

    ds_data = machine.Pin(config.get("w1_gpio"), 14)
    ds = ds18x20.DS18X20(onewire.OneWire(ds_data))

    # Scan for devices on the bus
    roms = ds.scan()
    if roms:
        print("Found DS18S20 sensors:",
                "".join("%s " % ubinascii.hexlify(b).format() for b in roms))
    else:
        print("No DS18S20 sensor found, nothing to be reported")
        return

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
        ds.convert_temp()
        time.sleep_ms(750)
        for rom in roms:
            ds_id = ubinascii.hexlify(rom).format()
            ds_topic = "w1_" + ds_id
            client.publish("{}/{}/temperature".format(config.get("mqtt_topic"),
                                          config.get(ds_topic, ds_id)),
                                          bytes(str(ds.read_temp(rom)),
                                          'utf-8'))
        time.sleep(5)

if __name__ == '__main__':
    main()
