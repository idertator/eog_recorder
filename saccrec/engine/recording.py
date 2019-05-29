import time
import pandas as pd
from openbci_interface import Cyton
from serial import Serial

sample_rate = 250

puerto = '/dev/ttyUSB0'
port = Serial(port=puerto,baudrate=115200,timeout=2)

print("configurando placa...\n")

with Cyton(port) as board:
    board.set_board_mode('default')
    board.set_sample_rate(sample_rate)
    board.start_streaming()
    print(board.cycle)
    for x in range(10):
        sample = board.read_sample()
        print('muestra {} tomada'.format(x+1))
        print(sample)
        print('\n')
        time.sleep(0.85 / sample_rate)
    board.stop_streaming()