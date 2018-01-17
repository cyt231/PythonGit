import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import urllib
import numpy as np
import datetime as dt
import matplotlib.ticker as mticker
from matplotlib.finance import candlestick_ohlc

def bdate2num(fmt, encoding='utf-8'):
    str_converter = mdates.strpdate2num(fmt)
    def bconverter(b):
        s = b.decode(encoding)
        return str_converter(s)
    return bconverter

def graph_data (stock, api):

    #Informações basicas
    base = 'https://www.alphavantage.co/query?' #Base da Query

    #Data type do API Alphavantage - Tipo (valores temporais)
    temp = input('Temporal Resolution: ')
    print('=====================')
    size = ''
    if temp == '2':
        print('Daily')
        function = 'function=TIME_SERIES_DAILY'
    elif temp == '3':
        print('Weekly')
        function = 'function=TIME_SERIES_WEEKLY'
    elif temp =='4':
        print('Monthly')
        function = 'function=TIME_SERIES_MONTHLY'
    else:
        print(type(temp))
        print("Error: "+temp)
    print('=====================')
        
    #Stock - ticket do stock
    symbol = '&symbol='+stock

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
    x = 0
    y = len(date)
    new_list = []
    while x < y:
        append_line = date[x], openp[x], highp[x], lowp[x], closep[x], volume[x]
        new_list.append(append_line)
        x +=1
        
    candlestick_ohlc(ax1, new_list, width=.6, colorup='g', colordown='r')
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)

    
    if(temp != '1'):
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
    elif(temp=='1'):
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y - %H:%M:%S '))
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
    ax1.grid(True) #, color='g', linestyle='-', linewidth=3)
    plt.subplots_adjust(left = .15, bottom = .15, right = .95, top = .95, wspace = .2, hspace = .2)
    plt.show()

api = 'XDESS96825BHFYQE'
while(True):
    stock = input('Stock to plot: ')
    graph_data(stock,api)
