import bluetooth
import os
import dotenv

dotenv.load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')


def send_to_robot(to_send):
    f = True
    i = 3
    print('Bluetooth включен, время поиска:', i, 'секунды')
    while f:
        target_name = "ESP32BT-EGGR"
        target_address = None
        nearby_devices = bluetooth.discover_devices(lookup_names=True, lookup_class=True, duration=i)
        print('Найдены устройства:', nearby_devices)
        for btaddr, btname, btclass in nearby_devices:
            if target_name == btname:
                target_address = btaddr
                break
        if target_address is not None:
            serverMACAddress = target_address
            port = 1
            s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            s.connect((serverMACAddress, port))
            print("Подключено к {}".format(target_name))
            s.send(bytes(SECRET_KEY + to_send, 'UTF-8'))
            s.close()
            print('Путь отправлен на робота')
            f = False
        else:
            i += 3
            print("Робот не найден, новое время поиска:", i, 'секунд')
