from djitellopy import Tello

def test_connect():
    tello = Tello()
    tello.connect()

    battery = tello.get_battery()

    print(tello.get_battery())

    assert isinstance(battery, int)