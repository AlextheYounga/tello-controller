import sys


def main():
    sys.argv.pop(0)

    args = [arg.strip() for arg in sys.argv]

    if (args[0] == 'basic'):
        import controllers.basic

    if (args[0] == 'facetrack'):
        import controllers.face_tracking


if __name__ == '__main__':
    main()
