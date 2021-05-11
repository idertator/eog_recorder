from saccrec.recording import CytonBoard
from time import sleep


def main():
    board = CytonBoard(port='/dev/ttyUSB0')

    filename = board.create_sd_file()
    print(f'Recording at {filename}')

    board.marker('c')
    board.start()
    for i in range(10):
        sleep(1)
        board.marker('l')
        sleep(1)
        board.marker('r')
    sleep(1)
    board.marker('c')
    sleep(1)
    board.stop()

    board.marker('c')
    board.start()
    for i in range(20):
        sleep(1)
        board.marker('l')
        sleep(1)
        board.marker('r')
    sleep(1)
    board.marker('c')
    sleep(1)
    board.stop()

    board.marker('c')
    board.start()
    for i in range(10):
        sleep(1)
        board.marker('l')
        sleep(1)
        board.marker('r')
    sleep(1)
    board.marker('c')
    sleep(1)
    board.stop()

    board.close_sd_file()


if __name__ == '__main__':
    main()
