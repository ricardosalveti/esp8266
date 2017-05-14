import time
import machine
import onewire, ds18x20
import ubinascii
from umqtt.simple import MQTTClient

# Defaults are overwritten with the contents of /config.json by load_config()
CONFIG = {
    "broker": "192.168.1.30",
    "port": 1883,
    "user": "foo",
    "password": "bar",
    "gpio": 12,
    "topic": "brew/temperature",
}

def load_config():
    import ujson as json
    try:
        with open("/config.json") as f:
            config = json.loads(f.read())
    except (OSError, ValueError):
        print("Couldn't load /config.json, saving defaults")
        save_config()
    else:
        CONFIG.update(config)
        print("Loaded config from /config.json")

def save_config():
    import ujson as json
    try:
        with open("/config.json", "w") as f:
            f.write(json.dumps(CONFIG))
    except OSError:
        print("Couldn't save /config.json")

def main():
    client_id = "esp8266_" + ubinascii.hexlify(machine.unique_id()).format()
    client = MQTTClient(client_id, CONFIG['broker'], CONFIG['port'],
                        CONFIG['user'], CONFIG['password'])
    client.connect()
    print("Connected to {}".format(CONFIG['broker']))

    ds_data = machine.Pin(CONFIG['gpio'])
    ds = ds18x20.DS18X20(onewire.OneWire(ds_data))

    # Scan for devices on the bus
    roms = ds.scan()
    if roms:
        print("Found DS devices:",
                "".join("%s " % ubinascii.hexlify(b).format() for b in roms))
    else:
        print("No DS sensor found")

    # Iterate and publish
    while True:
        ds.convert_temp()
        time.sleep_ms(750)
        for rom in roms:
            client.publish("{}/{}".format(CONFIG['topic'],
                                          ubinascii.hexlify(rom).format()),
                                          bytes(str(ds.read_temp(rom)),
                                          'utf-8'))
        time.sleep(5)

if __name__ == '__main__':
    load_config()
    main()
