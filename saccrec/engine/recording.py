import time
import pandas as pd
from openbci_interface import Cyton
from openbci_interface import util
from serial import Serial
import pickle


def list_ports():
    ports = []
    for port in util.list_devices():
        ports.append(port)
    return ports

print(list_ports())

def init_board():
    sample_rate = 250
    puerto = '/dev/ttyUSB0'
    port = Serial(port=puerto,baudrate=115200,timeout=2)

    print("configurando placa...\n")

    with Cyton(port) as board:
        board.set_board_mode('default')
        board.set_sample_rate(sample_rate)
        board.disable_channel(5)
        board.disable_channel(6)
        board.disable_channel(7)
        board.disable_channel(8)
        board.configure_channel(1, power_down='ON', gain=24, input_type='NORMAL', bias=0, srb2=0, srb1=1)
        board.configure_channel(2, power_down='ON', gain=24, input_type='NORMAL', bias=0, srb2=0, srb1=1)
        board.configure_channel(3, power_down='ON', gain=24, input_type='NORMAL', bias=0, srb2=0, srb1=1)
        board.configure_channel(4, power_down='ON', gain=24, input_type='NORMAL', bias=0, srb2=0, srb1=1)
        print(board.get_config())
        """
        board.start_streaming()
        for x in range(500):
            sample = board.read_sample()
            lista.append(sample)
            time.sleep(0.85 / sample_rate)
        board.stop_streaming()
        fichero = open('datos.pickle', 'wb') 
        pickle.dump(lista,fichero)
        fichero.close()

        """
#class Board:
