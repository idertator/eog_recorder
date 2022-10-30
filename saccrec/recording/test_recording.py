from saccrec.recording import CytonBoard
from time import sleep


def main():
    board = CytonBoard(port="/dev/ttyUSB0")

    filename = board.create_sd_file()
    print(f"Recording at {filename}")

    board.marker("c")
    board.start()
    for i in range(10):
        sleep(1)
        board.marker("l")
        board.read()
        sleep(1)
        board.marker("r")
        board.read()
    sleep(1)
    board.marker("c")
    board.read()
    sleep(1)
    board.read()
    board.stop()

    board.marker("c")
    board.start()
    for i in range(20):
        sleep(1)
        board.marker("l")
        board.read()
        sleep(1)
        board.marker("r")
        board.read()
    sleep(1)
    board.marker("c")
    board.read()
    sleep(1)
    board.read()
    board.stop()

    board.marker("c")
    board.start()
    for i in range(10):
        sleep(1)
        board.marker("l")
        board.read()
        sleep(1)
        board.marker("r")
        board.read()
    sleep(1)
    board.marker("c")
    board.read()
    sleep(1)
    board.read()
    board.stop()

    board.close_sd_file()


if __name__ == "__main__":
    main()
