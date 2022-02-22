#!/usr/bin/env python
# coding: utf-8

# In[ ]:


##########################################################################################
# PROJECT JEMMY
# AUTHOR: RUSLAN MASINJILA
##########################################################################################
import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import time
import os

import winsound
duration = 100
freq = 1000

# NUMBER OF COLUMNS TO BE DISPLAYED
pd.set_option('display.max_columns', 500)

# MAXIMUM TABLE WIDTH TO DISPLAY
pd.set_option('display.width', 1500)      
 
# ESTABLISH CONNECTION TO MT5 TERMINAL
if not mt5.initialize():
    print("initialize() FAILED, ERROR CODE =",mt5.last_error())
    quit()


# In[ ]:


# MT5 TIMEFRAME
D1  = mt5.TIMEFRAME_D1
H12 = mt5.TIMEFRAME_H12
H8  = mt5.TIMEFRAME_H8
H6  = mt5.TIMEFRAME_H6
H4  = mt5.TIMEFRAME_H4
H3  = mt5.TIMEFRAME_H3
H2  = mt5.TIMEFRAME_H2
H1  = mt5.TIMEFRAME_H1
M30 = mt5.TIMEFRAME_M30
M20 = mt5.TIMEFRAME_M20
M15 = mt5.TIMEFRAME_M15
M12 = mt5.TIMEFRAME_M12
M10 = mt5.TIMEFRAME_M10
M6  = mt5.TIMEFRAME_M6
M5  = mt5.TIMEFRAME_M5
M4  = mt5.TIMEFRAME_M4
M3  = mt5.TIMEFRAME_M3
M2  = mt5.TIMEFRAME_M2
M1  = mt5.TIMEFRAME_M1

currency_pairs = [ "EURUSD.r","GBPUSD.r","AUDUSD.r","NZDUSD.r",
                   "USDJPY.r","USDCHF.r","USDCAD.r",
                   "XAUUSD.r",
                   "US30","US500"]
mt5Timeframe   = [M1,M2,M3,M4,M5,M6,M10,M12,M15,M20,M30,H1]
strTimeframe   = ["M1","M2","M3","M4","M5","M6","M10","M12","M15","M20","M30","H1"]
numCandles     = 15
offset = 1
DeMarkSignals = []
DeMarkSignalsTF = []

##########################################################################################


# In[ ]:


def getSignals(rates_frame,strTimeframe):
    
    Time, Open, Close, High, Low = getTOCHL(rates_frame)
    
    ################################################################################################
    
    DeMax = [High[i + 1] - High[i] for i in range(len(High)-1)]
    DeMax = [0 if i < 0 else i for i in DeMax]
    
    DeMin = [Low[i] - Low[i+1] for i in range(len(Low)-1)]
    DeMin = [0 if i < 0 else i for i in DeMin]
    
    SMA20DeMax = np.mean(DeMax)
    SMA20DeMin = np.mean(DeMin)
    
    DeMark = SMA20DeMax/(SMA20DeMax+SMA20DeMin)         
      
    if(DeMark<=0.3):
        DeMarkSignals.append("BUY")
        DeMarkSignalsTF.append(strTimeframe)
        
    
    if(DeMark>=0.7):
        DeMarkSignals.append("SELL")
        DeMarkSignalsTF.append(strTimeframe)
    
    ################################################################################################


# In[ ]:


# Gets the most recent <numCandles> prices for a specified <currency_pair> and <mt5Timeframe>
# Excludes the bar that has not finished forming <i.e offset = 1>
def getRates(currency_pair, mt5Timeframe, numCandles):
    rates_frame =  mt5.copy_rates_from_pos(currency_pair, mt5Timeframe, offset, numCandles)
    rates_frame = pd.DataFrame(rates_frame)
    return rates_frame

##########################################################################################


# In[ ]:


# Decomposes the DataFrame into individual lists for Time, Close, High and Low
def getTOCHL(rates_frame):
    return  (list(rates_frame["time"]), 
            list(rates_frame["open"]), 
            list(rates_frame["close"]),
            list(rates_frame["high"]),
            list(rates_frame["low"]))

##########################################################################################


# In[ ]:


banner = ""
banner+="##############################\n"
banner+="           SIGNALS            \n"
banner+="##############################\n"
while(True):
    
    display = banner
    for cp in currency_pairs:
        display+="["+cp+"]"+"\n"
        DeMarkSignals =[]
        DeMarkSignalsTF =[]
        for t in range(len(mt5Timeframe)):
            rates_frame = getRates(cp, mt5Timeframe[t], numCandles)
            getSignals(rates_frame,strTimeframe[t])
        if(all(x == DeMarkSignals[0] for x in DeMarkSignals)):
            if(len(DeMarkSignals)>=7):
                if(DeMarkSignalsTF[0]=="M1"):
                    display+="DeMark Matches: "+str(len(DeMarkSignals))+"\n"
                    display+=" ".join(DeMarkSignals)+"\n"
                    display+=" ".join(DeMarkSignalsTF)+"\n"
                    winsound.Beep(freq, duration)
                    
        display+="==============================\n"
    print(display)
    time.sleep(60)
    os.system('cls' if os.name == 'nt' else 'clear') 
##########################################################################################

