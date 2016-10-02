import os
import oandapy
import static
import time


# create a lock file to prevent mt4 from accessing data
def create_lock_file():
    try:
        file = open(static.filepath+"bridge_lock","w")
        file.close()
    except Exception as e:
        print(e)
    return


# delete the above lock file
def delete_lock_file():
    try:
        if os.path.isfile(static.filepath+"bridge_lock"):
            os.remove(static.filepath+"bridge_lock")
    except Exception as e:
        print(e)
    return


# close all positions for an instrument
def close_positions():

    if not is_directory_locked():
        try:
            for fn in os.listdir(static.filepath): # loop through files in directory
                if 'closeall-' in fn:
                    create_lock_file()
                    cmd,instrument = fn.split('-')
                    response = static.oanda.close_position(static.account_id, instrument)
                    if response.get("totalUnits") > 0:
                        print("POSITIONS CLOSED: "+str(response.get("totalUnits"))+" Units on "+response.get("instrument"))

                    # delete file
                    if os.path.isfile(static.filepath+fn):
                        os.remove(static.filepath+fn)

                    # delete minmax file
                    if os.path.isfile(static.filepath+'minmax-'+instrument+'.txt'):
                        os.remove(static.filepath+'minmax-'+instrument+'.txt')

                    # update positions
                    update_positions()
                    update_account()
                    delete_lock_file()
        except Exception as e:
            print(e)
    return


# close individual trade
def close_trades():

    if not is_directory_locked():
        try:
            for fn in os.listdir(static.filepath): # loop through files in directory
                if 'close-' in fn:
                    create_lock_file()
                    cmd,ticket = fn.split('-')
                    response = static.oanda.get_trade(static.account_id, ticket)
                    print(response)

                    # delete file
                    if os.path.isfile(static.filepath+fn):
                        os.remove(static.filepath+fn)

                    # update positions
                    update_positions()
                    update_account()
                    delete_lock_file()
        except Exception as e:
            print(e)

    return


# open orders
def open_trades():
    if not is_directory_locked():
        try:
           for fn in os.listdir(static.filepath): # loop through files in directory
               if 'openmarket-' in fn:
                    create_lock_file()
                    cmd,instrument,side,units = fn.split('-')

                    response = static.oanda.create_order(static.account_id,
                                                         instrument=instrument,
                                                         units=int(units),
                                                         side=side,
                                                         type='market')

                    data = response.get("tradeOpened")
                    trade_id = data.get("id")

                    # return success or failure message
                    if trade_id > 1:
                        print("ORDER SUCCESS: "+side+" "+units+" units of "+instrument)
                    else:
                        print("ORDER FAILURE: "+side+" "+units+" units of "+instrument)

                    # delete file
                    if os.path.isfile(static.filepath+fn):
                        os.remove(static.filepath+fn)

                    # update positions
                    update_positions()
                    update_account()
                    delete_lock_file()
        except Exception as e:
            print(e)
    return


def get_minmax_trades(instrument):

    if not is_directory_locked():
        create_lock_file()
        try:
            # delete all current positions prior to update
            for fn in os.listdir(static.filepath): # loop through files in directory
                if 'minmax-'+instrument in fn:
                    os.remove(static.filepath+fn)

            trades = []
            response = static.oanda.get_trades(static.account_id, instrument=instrument)

            for trade in response.get("trades"):

                trades.append(trade.get("price"))

            file = open(static.filepath+"minmax-"+instrument+".txt","w")
            file.write(str(min(trades))+","+str(max(trades)))
            file.close()
        except Exception as e:
            print(e)

    delete_lock_file()

# update all positions
def update_positions():

    if not is_directory_locked():
        create_lock_file()
        try:
            # delete all current positions prior to update
            for fn in os.listdir(static.filepath): # loop through files in directory
                if 'position-' in fn:
                    os.remove(static.filepath+fn)

            response = static.oanda.get_positions(static.account_id)

            # loop through positions
            for position in response.get("positions"):
                # create file position-EUR_USD-buy-2500-1.13041
                file = open(static.filepath+"position-"+position.get("instrument")+".txt","w")
                file.write(position.get("side")+","+
                           str(position.get("units"))+","+
                           str(position.get("avgPrice")))
                file.close()

                get_minmax_trades(position.get("instrument"))

            print("UPDATE: Positions Updated")
            print("UPDATE: Trades Updated")
        except Exception as e:
            print(e)
        delete_lock_file()
    return


def update_account():

    if not is_directory_locked():
        create_lock_file()
        try:
            response = static.oanda.get_account(static.account_id)

            file = open(static.filepath+"account.txt","w")
            file.write(str(response.get("balance"))+","+
                       str(response.get("openTrades"))+","+
                       str(response.get("marginAvail"))+","+
                       str(response.get("marginUsed"))+","+
                       str(response.get("realizedPl"))
                       )
            file.close()

            print("UPDATE: Account Updated")
        except Exception as e:
            print(e)
        delete_lock_file()


# is directory locked by MT4?
def is_directory_locked():
    locked = False
    try:
        if os.path.isfile(static.filepath+'MT4-Locked'):
            locked = True
    except Exception as e:
        print(e)
    return locked

