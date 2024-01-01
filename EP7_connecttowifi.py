import network
from wlan import do_connect
import socket

try:
    ip=do_connect()
    print(ip)
except keyboardInterrupt:
    pass