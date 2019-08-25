from serial import Serial
from openbci_interface import Cyton
from openbci_interface import util
from threading import Timer
import time

sample_freq = 250

def openPort():
    ports = []
    for i in util.list_devices():
        ports.append(i)
    print(ports[0])
    puerto = Serial(port=ports[0],baudrate=115200,timeout=2)
    return puerto


def bciConfig():
    port = openPort()
    board = Cyton(port,0)
    board.set_board_mode('default')
    board.set_sample_rate(250)

    board.disable_channel(5)
    board.disable_channel(6)
    board.disable_channel(7)
    board.disable_channel(8)
    board.configure_channel(1, power_down='ON', gain=24, input_type='NORMAL', bias=0, srb2=0, srb1=1)
    board.configure_channel(2, power_down='ON', gain=24, input_type='NORMAL', bias=0, srb2=0, srb1=1)
    board.configure_channel(3, power_down='ON', gain=24, input_type='NORMAL', bias=0, srb2=0, srb1=1)
    board.configure_channel(4, power_down='ON', gain=24, input_type='NORMAL', bias=0, srb2=0, srb1=1)
    return board

samples = []

def single_read(board):
    sample = board.read_sample()
    samples.append(sample)


def principal():
    board = bciConfig()
    timer = Timer(0.85/sample_freq, single_read, [board])
    board.start_streaming()
    timer.start()
    time.sleep(5)
    timer.cancel()
    board.stop_streaming()
    board.terminate()
    print(samples)

#openPort()
principal()
