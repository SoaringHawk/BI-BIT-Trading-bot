#from poloniex import poloniex
from binance.client import Client
import urllib, json
import pprint
from botcandlestick import BotCandlestick

class BotChart(object):
    def __init__(self, exchange, pair, period, backtest=True):
        self.pair = pair
        self.period = period

        self.startTime = 1491048000
        self.endTime = 1491591200

        self.data = []
		
        if (exchange == "poloniex"):
            self.conn = poloniex('key goes here','Secret goes here')
            
            if backtest:
                poloData = self.conn.api_query("returnChartData",{"currencyPair":self.pair,"start":self.startTime,"end":self.endTime,"period":self.period})
                for datum in poloData:
                    if (datum['open'] and datum['close'] and datum['high'] and datum['low']):
                        self.data.append(BotCandlestick(self.period,datum['open'],datum['close'],datum['high'],datum['low'],datum['weightedAverage']))

        if (exchange == "bittrex"):
            if backtest:
                url = "https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName="+self.pair+"&tickInterval="+self.period+"&_="+str(self.startTime)
                response = urllib.urlopen(url)
                rawdata = json.loads(response.read())

                self.data = rawdata["result"]
        if (exchange == "binance"):
            if backtest:
                APIkey = 'gcMugP0qdU5JBPoueFXgIY6I4gSEsDVwIb89ZC0oJzmDSgPVUW1gBlDiZmy9zHOl'
                Secretkey = 'F05pow8F5pxMyIBDEcj6Q3uWNf6CPLfJRDr3bCDrvnYpn7sYElayH3iGY0RiKyox'
                client = Client(APIkey, Secretkey)
                binandata = client.get_historical_klines(symbol=self.pair, interval=self.period, start_str="1 Jul, 2019", end_str="2 Jul, 2019")
                for datas in binandata:
                    if len(datas) != 0:
                        weightAve = (float(datas[4])+float(datas[2])+float(datas[3])/ float(3))
                        self.data.append(BotCandlestick(self.period,datas[1],datas[4],datas[2],datas[3], weightAve))



    def getPoints(self):
        return self.data

    def getCurrentPrice(self):
        #currentValues = self.conn.api_query("returnTicker")
        #lastPairPrice = {}
        #lastPairPrice = currentValues[self.pair]["last"]
        #return lastPairPrice
        APIkey = 'gcMugP0qdU5JBPoueFXgIY6I4gSEsDVwIb89ZC0oJzmDSgPVUW1gBlDiZmy9zHOl'
        Secretkey = 'F05pow8F5pxMyIBDEcj6Q3uWNf6CPLfJRDr3bCDrvnYpn7sYElayH3iGY0RiKyox'
        client = Client(APIkey, Secretkey)
        current = client.get_historical_klines(symbol="ETHBTC", interval='1m', start_str="1 minute ago UTC")
        Pairprice = current[-1][4]
        return Pairprice

