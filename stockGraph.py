import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import urllib
import numpy as np
import datetime as dt

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# bdate2num - function to convert the raw info to a usable
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def bdate2num(fmt, encoding='utf-8'):
    str_converter = mdates.strpdate2num(fmt)
    def bconverter(b):
        s = b.decode(encoding)
        return str_converter(s)
    return bconverter

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Get Function - function to prepare the query for alphavantage API
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  
def getFunction(fun):
    outputsize= ''
    interval= ''
    ### Function = 1 ### INTRADAY ###
    if(fun==1):
        print ('>>> Function: INTRADAY <<<')
        ##Stock - REQ
        stock = input('>>Stock: ')
        fun = 'TIME_SERIES_INTRADAY'
        title = 'Intraday - '+stock+' - '
        ##Interval - REQ
        print(120 *'-')
        valid = 0
        while not valid:
            try:
                interval = input ( '>>Interval (1, 5, 15, 30, 60 min): ')
                if( interval == '1'):
                    valid = 1
                elif( interval == '5'):
                    valid = 1
                elif( interval == '15'):
                    valid = 1
                elif( interval == '30'):
                    valid = 1
                elif( interval == '60'):
                    valid = 1
                else:
                    print('Input %s is not a valid value.' %interval)
                    print(type(interval))
            except ValueError as e:
                print ("Input %s is not a valid integer." % e.args[0].split(": ")[1])
        print(120*'-')
        ##Outputsize - OPT - Daily Only
        valid = 0
        while not valid:
            outputsize = input('>>Outputsize (compact or full): ')
            if(outputsize == 'compact'):
                valid = 1
            elif( outputsize == 'full'):
                valid = 1
            elif( outputsize == ''):
                valid = 1
            else:
                print('Invalid %s is not a valid value.' % outputsize)
        title = title + 'Outputsize: ' 
        if( outputsize != ''):
            title = title + outputsize
        else:
            title = title + 'Default(compact)'
            
    ### Function = 2 ### DAILY ###
    elif(fun==2):
        print('Function: Daily')
        fun = 'TIME_SERIES_DAILY'
        title = 'Daily - '
        stock = input('>>Stock: ')
        title = title + stock + ' - '
        ##Outputsize - OPT - Daily Only
        valid = 0
        while not valid:
            outputsize = input('>>Outputsize (compact or full): ')
            if(outputsize == 'compact'):
                valid = 1
            elif( outputsize == 'full'):
                valid = 1
            elif( outputsize == ''):
                valid = 1
            else:
                print('Invalid %s is not a valid value.' % outputsize)
        title = title + 'Outputsize: ' 
        if( outputsize != ''):
            title = title + outputsize
        else:
            title = title + 'Default(compact)'
    elif(fun==3):
        print('Function: Daily Adjusted')
        fun = 'TIME_SERIES_DAILY_ADJUSTED'
        title = 'Daily Adjusted - '
        stock = input('>>Stock: ')
        title = title + stock + ' - '
        ##Outputsize - OPT - Daily Only
        valid = 0
        while not valid:
            outputsize = input('>>Outputsize (compact or full): ')
            if(outputsize == 'compact'):
                valid = 1
            elif( outputsize == 'full'):
                valid = 1
            elif( outputsize == ''):
                valid = 1
            else:
                print('Invalid %s is not a valid value.' % outputsize)
        title = title + 'Outputsize: ' 
        if( outputsize != ''):
            title = title + outputsize
        else:
            title = title + 'Default(compact)'
    elif(fun==4):
        print('Function: Weekly')
        fun ='TIME_SERIES_WEEKLY'
        title = 'Weekly - '
        stock = input('>>Stock: ')
        title = title + stock
        ylabel = 'Time - Weekly'
    elif(fun==5):
        print('Function: Weekly Adjusted')
        fun = 'TIME_SERIES_WEEKLY_ADJUSTED'
        title = 'Weekly Adjusted - '
        stock = input('Stock: ')
        title = title + stock
        ylabel = 'Time - Weekly Adjusted'
    elif(fun==6):
        print('Function: Monthly')
        fun = 'TIME_SERIES_MONTHLY'
        title = 'Monthly - '
        stock = input('Stock: ')
        title = title + stock
        ylabel = 'Time - Monthly'
    elif(fun==7):
        print('Function: Monthly Adjusted')
        fun = 'TIME_SERIES_MONTHLY_ADJUSTED'
        title = 'Monthly Adjusted - '
        stock = input('Stock: ')
        title = title + stock
        ylabel = 'Time - Monthly Adjusted'
    elif(fun==8):
        print('Batch Stock Quotes')
        fun = 'BATCH_STOCK_QUOTES'
        title = 'Batch Stock Quotes'
        a= []
        prompt = '>'
        print('Stocks: ')
        line = input(prompt)
        while line:
            a.append(line)
            line = input(prompt)
        stock = ','.join(str(e) for e in a)
        title = title + stock
        
    
    print('----------------------------------------------------------------------------------------------------------')
    return fun, stock, interval, outputsize, title

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Get URL (url generator for alphavantage API)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def getUrl():
    #Basic Information
    ##Query Base (REQ)
    base = 'https://www.alphavantage.co/query?'
    print(60 * '=')
    print('Options:\n1) Intraday\n2) Daily\n3) Daily Adjusted (Not Implemented)\n4) Weekly')
    print('5) Weekly Adjusted (Not Implemented)\n6) Monthly\n7) Monthly Adjusted (Not Implemented)\n8) Batch Stock Quotes')
    
    ##Get function
    valid = 0
    while not valid:
        try:
            fun = int (input('>>Selec the function: '))
            if (fun == 3):
                print('Function: ', fun ,' isn\'t a valid operation (yet)')
                fun=False
            elif(fun ==5):
                print('Function: ',fun , ' isn\'t a valid operation (yet)')
                fun=False
            elif(fun==7):
                print('Function: ',fun ,' isn\'t a valid operation (yet)')
                fun=False
            else:
                valid = 1
        except ValueError as e:
                print ("'%s' is not a valid integer." % e.args[0].split(": ")[1])

    print(60 * '=')              
    aux, stock, inter, output, head = getFunction(fun)
        
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
    title = head
    print('URL = '+url)
    return url, fun, title


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Graph plot
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def graph_data (url, fun, title):
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

    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('Value')
    ax1.grid(True) #, color='g', linestyle='-', linewidth=3)
    plt.subplots_adjust(left = .15, bottom = .15, right = .95, top = .95, wspace = .2, hspace = .2)
    plt.show()

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Código Principal
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
while(True):
    url, fun, title = getUrl()
    graph_data(url, fun, title)
