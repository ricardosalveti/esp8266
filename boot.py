def do_connect():
    import network

    SSID = "foo"
    PASSWORD = "foobar"

    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)
    if ap_if.active():
        print("Disabling AP...");
        ap_if.active(False)
    if not sta_if.isconnected():
        print("Connecting to the network...")
        sta_if.active(True)
        sta_if.connect(SSID, PASSWORD)
        while not sta_if.isconnected():
            pass
    print("Network configuration: ", sta_if.ifconfig())

do_connect()
