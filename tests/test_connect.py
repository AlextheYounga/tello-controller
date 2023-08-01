from djitellopy import Tello

def test_connect():
    drone = Tello()
    drone.connect()

    battery = drone.get_battery()

    print(battery)

    assert isinstance(battery, int)