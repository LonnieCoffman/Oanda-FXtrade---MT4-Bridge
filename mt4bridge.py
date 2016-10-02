import oandapy
import os
import time
import functions as bridge
import static

bridge.update_positions()
bridge.update_account()

while True:

    bridge.close_positions()
    bridge.open_trades()

    time.sleep(1)
