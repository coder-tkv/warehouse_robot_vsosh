import socket

path = [[20, 12, 11, 3, 2], 2, [2, 3, 11, 12], 1 , [12, 20, 19, 18], 3, [18, 19, 20, 12, 13], 1]

target_name = "ESP32BT"
target_address = None
nearby_devices = bluetooth.discover_devices(lookup_names=True, lookup_class=True)
print(nearby_devices)
for btaddr, btname, btclass in nearby_devices:
    if target_name == btname:
        target_address = btaddr
        break
if target_address is not None:
    print("found target {} bluetooth device with address {} ".format(target_name, target_address))
    serverMACAddress = target_address
    port = 1
    s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    s.connect((serverMACAddress, port))
    print("connected to {}".format(target_name))
    text = "tkv"
    for i in range(len(path)):
        if i % 2 == 0:
            text += 'p'
            for j in path[i]:
                text += str(j) + '-'
        else:
            text += 'd' + str(path[i])
    text += 'r19-s0e'
    print(text)
    s.send(bytes(text, 'UTF-8'))
    s.close()
    print('sended')
else:
    print("could not find target bluetooth device nearby")
