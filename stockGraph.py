import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import urllib
import numpy as np
import datetime as dt

def bdate2num(fmt, encoding='utf-8'):
    str_converter = mdates.strpdate2num(fmt)
    def bconverter(b):
        s = b.decode(encoding)
        return str_converter(s)
    return bconverter
    
    
def getFunction(fun):
    outputsize= ''
    interval= ''
    if(fun==1):
        print('Function: Intraday') 
        fun = 'TIME_SERIES_INTRADAY'        #REQ - value for query
        stock = input('Stock: ')                          #REQ - stock value (ticket)
        ##Interval
        print('-----------------------------------------------------')
        interval = input('Interval (1, 5, 15, 30, 60 min): ') #REQ (time)
        ##Outputsize (OPT, only daily)
        print('-----------------------------------------------------')
        outputsize = input('Outputsize - compact/full (default:compact): ') #OPT
        print('-----------------------------------------------------')
        
    elif(fun==2):
        print('Function: Daily')
        fun = 'TIME_SERIES_DAILY'
        stock = input('Stock: ')
        ##Outputsize (OPT, only daily)
        print('-----------------------------------------------------')
        outputsize = input('Outputsize - compact/full (default:compact): ') #OPT
        print('-----------------------------------------------------')
    elif(fun==3):
        print('Function: Daily Adjusted')
        fun = 'TIME_SERIES_DAILY_ADJUSTED'
        stock = input('Stock: ')
        ##Outputsize (OPT, only daily)
        print('-----------------------------------------------------')
        outputsize = input('Outputsize - compact/full (default:compact): ') #OPT
        print('-----------------------------------------------------')
    elif(fun==4):
        print('Function: Weekly')
        fun ='TIME_SERIES_WEEKLY'
        stock = input('Stock: ')
    elif(fun==5):
        print('Function: Weekly Adjusted')
        fun = 'TIME_SERIES_WEEKLY_ADJUSTED'
        stock = input('Stock: ')
    elif(fun==6):
        print('Function: Monthly')
        fun = 'TIME_SERIES_MONTHLY'
        stock = input('Stock: ')
    elif(fun==7):
        print('Function: Monthly Adjusted')
        fun = 'TIME_SERIES_MONTHLY_ADJUSTED'
        stock = input('Stock: ')
    elif(fun==8):
        print('Batch Stock Quotes')
        fun = 'BATCH_STOCK_QUOTES'
        a= []
        prompt = '>'
        print('Stocks: ')
        line = input(prompt)
        while line:
            a.append(line)
            line = input(prompt)
        stock = ','.join(str(e) for e in a)
    
    print(stock)
    print('-----------------------------------------------------')
    return fun, stock, interval, outputsize

def graph_data ():
    
    #Basic Information
    ##Query Base (REQ)
    base = 'https://www.alphavantage.co/query?'

    print('=============================')
    print('Options:\n1) Intraday\n2) Daily\n3) Daily Adjusted (Not Implemented)\n4) Weekly')
    print('5) Weekly Adjusted (Not Implemented)\n6) Monthly\n7) Monthly Adjusted (Not Implemented)\n8) Batch Stock Quotes')
    
    ##Get function
    fun = False
    while (fun == False):
        print('-----------------------------------------------------')
        fun = input('Select the function: ')
        fun = int(fun)
        if (fun == 3):
            print('Function: ', fun ,' isn\'t a valid operation (yet)')
            fun=False
        elif(fun ==5):
            print('Function: ',fun , ' isn\'t a valid operation (yet)')
            fun=False
        elif(fun==7):
            print('Function: ',fun ,' isn\'t a valid operation (yet)')
            fun=False
        
    aux, stock, inter, output = getFunction(fun)
        
    print(aux, '>>>', stock)
    
    ##Function (REQ)
    function = 'function='+aux
    print(function)
    
    ##Symbol (REQ)
    if(fun==8):
        symbol = '&symbols='+stock
    else:
        symbol  = '&symbol='+stock
    print(symbol)

    ##Interval - Only INTRADAY (REQ)
    print(inter)
    print(output)
    if(inter!=''):
        print('Entrou no inter ===')
        interval = '&interval='+inter+'min'
        print(interval)
    else:
        interval=''

    ##Outputsize
    if(output!=''):
        print('Entrou no inter ===')
        outputsize = '&outputsize='+output
        print(outputsize)
    else:
        outputsize=''
    print('-----------------------------------------------------')
    
    ##Datatype - CSV or Json (not used)
    datatype = '&datatype=json'
    ##API Key (REQ)
    api = 'XDESS96825BHFYQE'
    api_key = '&apikey='+api
    url = base + function + symbol + interval+ outputsize + api_key + datatype
    print(url)
    print('>>>>>>>>>>>>>>>FIM<<<<<<<<<<<<<<<')
    print('>>>>>>>>>>>>>>>FIM<<<<<<<<<<<<<<<\n')


#Main code
while(True):
    graph_data()
