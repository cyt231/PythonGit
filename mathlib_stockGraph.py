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

def graph_data (stock, api, tipo):

    #Informações basicas
    base = 'https://www.alphavantage.co/query?' #Base da Query

    #Data type do API Alphavantage - Tipo (valores temporais)
    if tipo == '1':
        function = 'function=TIME_SERIES_INTRADAY'
    elif tipo == '2':
        function = 'function=TIME_SERIES_DAILY'
    elif tipo == '3':
        function = 'function=TIME_SERIES_WEEKLY'
    elif tipo =='4':
        function = 'function=TIME_SERIES_MONTHLY'
    else:
        print(type(tipo))
        print("Error: "+tipo)
        
        
    #Stock - ticket do stock
    symbol = '&symbol='+stock

    #Configuração do gráfico em Grid
    fig = plt.figure()
    ax1 = plt.subplot2grid((1,1), (0,0))

    #Exibir informações
    print('Currently pulling: ', stock)   
    url = base+function+symbol+'&outputsize=full&&apikey='+api+'&datatype=csv'
    print('URL: ', url)

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
    date, openp, highp, lowp, closep, volume = np.loadtxt(stock_data, delimiter= ',', unpack=True,converters={0:bdate2num('%Y-%m-%d')})

    plt.plot_date(date, closep, '-')
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)
        
    ax1.grid(True) #, color='g', linestyle='-', linewidth=3)
    plt.subplots_adjust(left = .15, bottom = .15, right = .95, top = .95, wspace = .2, hspace = .2)
    plt.show()

api = 'XDESS96825BHFYQE'
while(True):
    stock = input('Stock to plot: ')
    tipo = input('Temporal: ')
    graph_data(stock,api,tipo)
