## MT4 to Oanda FXtrade Bridge

This Python script to act as a bridge from MT4 to Oanda FXtrade. I use this to
allow my MT4 expert advisors to send trades to Oanda's FXtrade API. Using this
I can place trades as small as 1 unit.

The MQL script writes files to the files/FXtrade folder and this Python script
reads them and manipulates orders via the Oanda API. Reading and writing files
to communicate orders was the most consistent method that I found to get data
from MT4 to Python. It is also unlikely that a future MT4 update will disable
file usage.

To use the script you will need to add your account number and api token to the
static.py file. The below functions can be called from within your expert
advisors to open and close trades and positions.

This script uses [oandapy](https://github.com/oanda/oandapy) to connect to
Oanda's API, so you will need this package.

This is the first program that I have ever written in Python, so if the coding
is bloated or amateurish be kind.

```c++
//================================================//
// FXtrade Bridge Functions                       //
//================================================//
// create order file
bool OpenMarketOrder(string fuInstrument, string fuSide, int fuUnits){
   int fuFilehandle;
   bool fuOrder;
   string fuCommand = "openmarket-"+fuInstrument+"-"+fuSide+"-"+IntegerToString(fuUnits);
   LockDirectory();
   fuFilehandle=FileOpen("FXtrade\\"+fuCommand,FILE_WRITE|FILE_TXT);
   if(fuFilehandle!=INVALID_HANDLE){
      FileClose(fuFilehandle);
      SendNotification(fuInstrument+" "+fuSide+" opened: "+IntegerToString(fuUnits)+" units");
      fuOrder = True;
   } else fuOrder = False;
   UnlockDirectory();
   return fuOrder;
}

// create close file
bool CloseTrade(int fuNumber){
   int fuFilehandle;
   bool fuOrder;
   fuFilehandle=FileOpen("FXtrade\\close-"+IntegerToString(fuNumber),FILE_WRITE|FILE_TXT);
   LockDirectory();
   if(fuFilehandle!=INVALID_HANDLE){
      FileClose(fuFilehandle);
      fuOrder = True;
   } else fuOrder = False;
   UnlockDirectory();
   return fuOrder;
}

// create close position file
bool ClosePosition(string fuInstrument){
   int fuFilehandle;
   fuFilehandle=FileOpen("FXtrade\\closeall-"+fuInstrument,FILE_WRITE|FILE_TXT);
   if(fuFilehandle!=INVALID_HANDLE){
      FileClose(fuFilehandle);
      return True;
   } else return False;
}

// lock directory so python does not access files
bool LockDirectory(){
   int fuFilehandle;
   fuFilehandle=FileOpen("FXtrade\\MT4-Locked",FILE_WRITE|FILE_TXT);
   if(fuFilehandle!=INVALID_HANDLE){
      FileClose(fuFilehandle);
      return True;
   } else return False;
}

// unlock directory so python can access files
bool UnlockDirectory(){
   int fuFilehandle;
   fuFilehandle=FileDelete("FXtrade\\MT4-Locked");
   if (fuFilehandle == False) return False;
      else return True;
}
```
