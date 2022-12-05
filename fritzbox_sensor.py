#!/usr/bin/env python3
"""
Fritz!Box sensor based on the TR-064 protocol.

Examples:
  https://znil.net/index.php?title=FritzBox_Status_Informationen_per_Upnp_mit_Linux_Bash-Script_auslesen
"""

from os import getenv
from http.client import HTTPConnection
from xml.etree import ElementTree


FRITZ_HOST = getenv('SENSORIC_FRITZ_HOST')
FRITZ_PORT = int(getenv('SENSORIC_FRITZ_PORT') or 49000)
if not FRITZ_HOST or not FRITZ_PORT:
    print('SENSORIC_FRITZ_HOST and/or SENSORIC_FRITZ_PORT environment variable not set.')
    exit(-1)

COUNTERS = {'NewTotalBytesSent': 'bytes_sent',
            'NewTotalBytesReceived': 'bytes_recv'}

REQ = """<?xml version="1.0" encoding="utf-8" ?>
         <s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
           <s:Body>
              <u:GetCommonLinkProperties xmlns:u="urn:schemas-upnp-org:service:WANCommonInterfaceConfig:1" />
           </s:Body>
         </s:Envelope>"""
XPATH = ".//{urn:schemas-upnp-org:service:WANCommonInterfaceConfig:1}GetAddonInfosResponse/"


def setup():
    pass


def get_measurement_name():
    return 'net'


def get_sensor_tags():
    return {'sensor': 'net'}


def get_sensor_fields():
    c = HTTPConnection(FRITZ_HOST, FRITZ_PORT)
    c.request('PUT', url='/igdupnp/control/WANCommonIFC1', body=REQ,
              headers={'Content-Type': 'text/xml; charset="utf-8"',
                       'SoapAction': 'urn:schemas-upnp-org:service:WANCommonInterfaceConfig:1#GetAddonInfos'})
    response = c.getresponse()
    if response.status == 200:
        pass
    else:
        print(f'WARNING: Cannot obtain statistics from '
              f'{FRITZ_HOST}:{FRITZ_PORT} '
              f'{response.reason} ({response.status}).')

    result = {}
    data = response.read()
    tree = ElementTree.fromstring(data.decode('utf-8'))
    for element in tree.findall(XPATH):
        if element.tag in COUNTERS:
            key = 'fritz_' + COUNTERS[element.tag]
            result[key] = int(element.text)

    return result


if __name__ == '__main__':
    setup()
    print('Measure:', get_sensor_fields())
