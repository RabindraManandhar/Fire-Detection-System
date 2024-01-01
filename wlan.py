def do_connect():
    import network
    import time
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network')
        wlan.connect('syco','syclops789')
        print('....')
        while wlan.isconnected() == False:
            print('Waiting for connection...')
            time.sleep(1)
    print('connected to network',wlan.ifconfig())
    #ip=wlan.ifconfig()[0]
    #return ip