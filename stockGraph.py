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
        print('----------------------------------------------------------------------------------------------------------')
        interval = input('Interval (1, 5, 15, 30, 60 min): ') #REQ (time)
        ##Outputsize (OPT, only daily)
        print('----------------------------------------------------------------------------------------------------------')
        outputsize = input('Outputsize - compact/full (default:compact): ') #OPT
        
    elif(fun==2):
        print('Function: Daily')
        fun = 'TIME_SERIES_DAILY'
        stock = input('Stock: ')
        ##Outputsize (OPT, only daily)
        outputsize = input('Outputsize - compact/full (default:compact): ') #OPT
    elif(fun==3):
        print('Function: Daily Adjusted')
        fun = 'TIME_SERIES_DAILY_ADJUSTED'
        stock = input('Stock: ')
        ##Outputsize (OPT, only daily)
        outputsize = input('Outputsize - compact/full (default:compact): ') #OPT
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
    
    print('----------------------------------------------------------------------------------------------------------')
    return fun, stock, interval, outputsize

def getUrl():
    
    #Basic Information
    ##Query Base (REQ)
    base = 'https://www.alphavantage.co/query?'

    print('=============================')
    print('Options:\n1) Intraday\n2) Daily\n3) Daily Adjusted (Not Implemented)\n4) Weekly')
    print('5) Weekly Adjusted (Not Implemented)\n6) Monthly\n7) Monthly Adjusted (Not Implemented)\n8) Batch Stock Quotes')
    
    ##Get function
    fun = False
    while (fun == False):
        print('----------------------------------------------------------------------------------------------------------')
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
    
    ##Symbol (REQ)
    if(fun==8):
        symbol = '&symbols='+stock
    else:
        symbol  = '&symbol='+stock

    ##Interval - Only INTRADAY (REQ)
    if(inter!=''):
        interval = '&interval='+inter+'min'
    else:
        interval=''

    ##Outputsize
    if(output!=''):
        outputsize = '&outputsize='+output
    else:
        outputsize=''
    print('----------------------------------------------------------------------------------------------------------')
    
    ##Datatype - CSV or Json (not used)
    datatype = '&datatype=csv'
    ##API Key (REQ)
    api = 'XDESS96825BHFYQE'
    api_key = '&apikey='+api
    
    url = base + function + symbol + interval+ outputsize + api_key + datatype
    
    print('URL = '+url)
    return url, fun


def graph_data (url, fun):
    #Graph configuration 
    fig = plt.figure()
    ax1 = plt.subplot2grid((1,1), (0,0))

    print('----------------------------------------------------------------------------------------------------------')
    #URL Decode
    print('Decoding source URL')
    source_code = urllib.request.urlopen(url).read().decode()
    #Array DATA
    stock_data = [] 
    #Dividir as linhas do API
    split_source = source_code.split('\n')

    #Recuperar as informações do arquivo CSV
    for each_line in split_source:
        split_line = each_line.split(',')
        if len(split_line) == 6:
            if 'timestamp' not in each_line:
                stock_data.append(each_line)
             
    #Transferindo os dados para as variáveis
                #date       > data específica
                #openp   > valor das ações ao abrir o dia
                #highp    > maior valor que as ações atingiu no dia
                #lowp      > menor valor que as ações atingiu no dia
                #closep  > valor que as ações fecharam
                #volume > a quantidade de ações movimentadas
    if(fun != 1):
        date, openp, highp, lowp, closep, volume = np.loadtxt(stock_data, delimiter= ',', unpack=True,
                                                              converters={0:bdate2num('%Y-%m-%d')})
    elif(fun==1):
        date, openp, highp, lowp, closep, volume = np.loadtxt(stock_data, delimiter= ',', unpack=True,
                                                              converters={0:bdate2num('%Y-%m-%d %H:%M:%S')})
    plt.plot_date(date, closep, '-')
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)
        
    ax1.grid(True) #, color='g', linestyle='-', linewidth=3)
    plt.subplots_adjust(left = .15, bottom = .15, right = .95, top = .95, wspace = .2, hspace = .2)
    plt.show()


#Main code
while(True):
    url, fun = getUrl()
    graph_data(url, fun)
