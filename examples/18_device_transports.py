"""No connection occurs without explicit command-line approval and a chosen endpoint."""
import argparse
from alfarouqai import Client,Config
p=argparse.ArgumentParser();p.add_argument('--serial-port');p.add_argument('--approve-device',action='store_true');a=p.parse_args()
if not a.serial_port or not a.approve_device:
    p.error('Supply --serial-port and --approve-device only after checking the physical protocol/safety.')
print(Client(Config(timeout=2)).run('robotics.serial',port=a.serial_port,read_bytes=128,consent=True).to_dict())
