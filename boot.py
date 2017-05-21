#
# Copyright: Ricardo Salveti <rsalveti@rsalveti.net>
#
# SPDX-License-Identifier: MIT

def do_connect():
    import network
    import utils
    import machine

    config = utils.Config()
    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)

    # On board LED
    led = machine.Pin(2, machine.Pin.OUT)

    if ap_if.active():
        print("Disabling AP...");
        ap_if.active(False)
    if not sta_if.isconnected():
        print("Connecting to the network...")
        sta_if.active(True)
        sta_if.connect(config.get("wifi_ssid"),
                        config.get("wifi_passwd"))
        while not sta_if.isconnected():
            pass
    print("Network configuration: ", sta_if.ifconfig())
    led.low()

do_connect()
