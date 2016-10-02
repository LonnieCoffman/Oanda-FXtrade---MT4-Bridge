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
