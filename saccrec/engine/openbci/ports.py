import logging
import re

from serial import Serial
from serial.tools.list_ports import comports

_log = logging.getLogger(__name__)


def _get_firmware_string(port, timeout=2):
    with Serial(port=port, baudrate=115200, timeout=timeout) as ser:
        ser.write(b'v')
        return ser.read_until(b'$$$').decode('utf-8', errors='ignore')


def list_ports() -> list[str]:
    filter_regex = 'OpenBCI'
    devices = [p.device for p in comports()]

    ports = []
    for device in devices:
        msg = _get_firmware_string(device)
        if 'Device failed to poll Host' in msg:
            _log.error(
                'Found USB dongle at "%s", '
                'but it failed to poll message from a board; %s',
                device, repr(msg)
            )
        elif re.search(filter_regex, msg):
            _log.info('Matched   [%s] %s "%s"', filter_regex, device, msg)
            ports.append(device)
        else:
            _log.info('Unmatched [%s] %s "%s"', filter_regex, device, msg)

    return ports
