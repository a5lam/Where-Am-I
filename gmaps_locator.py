#!/usr/bin/python3

import re
import subprocess

# add wifi info to request if available
payload = {'considerIp': 'true'}
try:
    cmdout = subprocess.check_output('netsh wlan show networks mode=bssid').decode(encoding='utf_8')
    macs = re.findall(r'(?:[0-9a-fA-F]:?){12}', cmdout)
    signals = re.findall(r'([\d]+)(%)', cmdout)
    channels = re.findall(r'(Channel[\W]+: )([\d]+)', cmdout)
    if not (len(macs) == len(signals) == len(channels)):
        raise
except:
    print('Could not retrieve WiFi Access Points...')
else:
    print('Using {0} WiFi Access Point{1}...'.format(len(macs), 's' if (len(macs) > 1) else ''))
    wifi_list = []
    for i in range(len(macs)):
        wifi_list.append({'macAddress': macs[i],
                                            # convert signal strength to RSSI dBm
                          'signalStrength': str(int(signals[i][0]) / 2 - 100),
                          'channel': channels[i][1]})
    payload['wifiAccessPoints'] = wifi_list
