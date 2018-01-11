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
    if(fun==1):
        print('Function: Intraday') 
        fun = 'TIME_SERIES_INTRADAY'        #REQ - value for query
        stock = input('Stock: ')                          #REQ - stock value (ticket)
        ##Interval
        print('-----------------------------------------------------')
        interval = input('Interval (1, 5, 15, 30, 60 min): ') #REQ (time)
        ##Outputsize (OPT)
        print('-----------------------------------------------------')
        outputsize = input('Outputsize - compact/full (default:compact): ')
        print('-----------------------------------------------------')
        
    elif(fun==2):
        print('Function: Daily')
        fun = 'TIME_SERIES_DAILY'
        stock = input('Stock: ')
    elif(fun==3):
        print('Function: Daily Adjusted')
        fun = 'TIME_SERIES_DAILY_ADJUSTED'
        stock = input('Stock: ')
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
    return fun, stock, interval

def graph_data ():
    
    #Basic Information
    ##Query Base (REQ)
    base = 'https://www.alphavantage.co/query?'

    print('=============================')
    print('Options:\n1) Intraday\n2) Daily\n3) Daily Adjusted (Not Implemented)\n4) Weekly')
    print('5) Weekly Adjusted (Not Implemented)\n6) Monthly\n7) Monthly Adjusted (Not Implemented)\n8) Batch Stock Quotes')
    
    ##Get function
    fun = True
    while (fun == True):
        fun = input('\nSelect the function: ')
        fun = int(fun)
        print (type(fun))
        if (fun == 3):
            print(fun ,' isn\'t a valid operation (yet)')
            fun=True
        elif(fun ==5):
            print(fun , ' isn\'t a valid operation (yet)')
            fun=True
        elif(fun==7):
            print(fun ,' isn\'t a valid operation (yet)')
            fun=True
        
    fun, stock, interval = getFunction(fun)
    print(fun, '>>>', stock)
    
    ##Function (REQ)
    function = '&function='+fun
    print(function)
    
    ##Symbol (REQ)
    symbol = '&symbol='+stock
    print(symbol)

    ##Interval - Only INTRADAY (REQ)
    interval = '&interval='+inter
    
        #Datatype - CSV or Json (not used)
    datatype = '&datatype='+data
        #API Key (REQ)
    api = 'XDESS96825BHFYQE'

    
    #Intraday
    #Daily
    #Daily Adjusted
    #Weekly
    #Weekly Adjusted
    #Monthly
    #Monthly Adjusted
    #Batch Stock Quotes

    #Configuração do gráfico em Grid
    fig = plt.figure()
    ax1 = plt.subplot2grid((1,1), (0,0))

    #Exibir informações
    print('Currently pulling: ', stock)   
    url = base+function+symbol+size+'&outputsize=full&apikey='+api+'&datatype=csv'
    print('URL: '+ url + '\n>> Decodificando URL')
    
    #URL Decode - decodificando o URL
    source_code = urllib.request.urlopen(url).read().decode()
    stock_data = [] #Array DATA
    split_source = source_code.split('\n') #Dividir as linhas do API

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

    if(temp != '1'):
        date, openp, highp, lowp, closep, volume = np.loadtxt(stock_data, delimiter= ',', unpack=True,
                                                              converters={0:bdate2num('%Y-%m-%d')})
    elif(temp=='1'):
        date, openp, highp, lowp, closep, volume = np.loadtxt(stock_data, delimiter= ',', unpack=True,
                                                              converters={0:bdate2num('%Y-%m-%d %H:%M:%S')})
    plt.plot_date(date, closep, '-')
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)
        
    ax1.grid(True) #, color='g', linestyle='-', linewidth=3)
    plt.subplots_adjust(left = .15, bottom = .15, right = .95, top = .95, wspace = .2, hspace = .2)
    plt.show()


while(True):
    graph_data()
