import okex.account_api as account
import okex.futures_api as future
import okex.lever_api as lever
import okex.spot_api as spot
import okex.swap_api as swap
import okex.lever_api as lever
import okex.index_api as index
import okex.option_api as option
import json
import logging
import threading
import datetime
import time
global stopprogram


class TradeThread(threading.Thread):
    def __init__(self, JY_dict, ZYZS_dict):
        try:
            threading.Thread.__init__(self)
            log_format = '%(asctime)s - %(levelname)s - %(message)s'
            # 初始化日志
            logging.basicConfig(filename='mylog-AutoTrade.json', filemode='a', format=log_format, level=logging.INFO)
            # vefyDict = dict()
            # vefyDict['api_key'] = list()
            # vefyDict['secret_key'] = list()
            # vefyDict['passphrase'] = list()
            #
            # vefyDict['api_key'].append('e475a6ff-3a83-4bce-8cc8-51b1108b5d23')
            # vefyDict['secret_key'].append('57944536044AD9587DC263C734A2B3A7')
            # vefyDict['passphrase'].append('rander360104456')
            #
            # vefyDict['api_key'].append('a75b5757-cb73-4957-ad5e-72fbc01e3899')
            # vefyDict['secret_key'].append('1CA488771AD910A70AA12A80A2E9DA32')
            # vefyDict['passphrase'].append('12345678')
            #
            # vefyDict['api_key'].append('6cc8cdef-61ad-4137-a402-0c1dae905cfe')
            # vefyDict['secret_key'].append('8EFC039D096B97619E9D4A558A5C5155')
            # vefyDict['passphrase'].append('12345678')

            self.lag = 0.5  #操作等待时延

            self._running = True

            self.accountAPI = account.AccountAPI(JY_dict['api_key'].get(),
                                                 JY_dict['secret_key'].get(),
                                                 JY_dict['passphrase'].get(), False)

            self.swapAPI = swap.SwapAPI(JY_dict['api_key'].get(),
                                        JY_dict['secret_key'].get(),
                                        JY_dict['passphrase'].get(), False)

            self.ShortQuantity = JY_dict['ShortQuantity'].get()
            self.LongQuantity = JY_dict['LongQuantity'].get()
          # ShortPrice = float(JY_dict['ShortPrice'].get())
          # LongPrice = float(JY_dict['LongPrice'].get())
            self.ShortPoint = int(JY_dict['ShortPoint'].get())
            self.LongPoint = int(JY_dict['LongPoint'].get())

            self.shortStep = float(JY_dict['shortStep'].get())
            self.shortStep2 = float(JY_dict['shortStep2'].get())
            self.longStep = float(JY_dict['longStep'].get())
            self.longStep2 = float(JY_dict['longStep2'].get())

            self.CoinType = JY_dict['CoinType'].get()

            self.param_dict = JY_dict
            result = self.swapAPI.get_order_list(self.CoinType+'-USD-SWAP', state='0')
            if result:
                for b in result[0]['order_info']:
                    if b['state'] == '0' or b['state'] == '1':
                        if b['type'] == '1' or b['type'] == '2':
                            self.swapAPI.revoke_order(self.CoinType + '-USD-SWAP', order_id=b['order_id'])
                            time.sleep(self.lag)

            result = self.swapAPI.get_specific_ticker(self.CoinType + '-USD-SWAP')
            if result['instrument_id'] == self.CoinType + '-USD-SWAP':
                self.currentPrice = float(result['last'])

            self.JYflag = False
            self.revokeFlag = False
            self.longTake = 'need'
            self.longRevoke = 'noneed'
            self.shortTake = 'need'
            self.shortRevoke = 'noneed'
            self.ShortDict = dict()
            self.LongDict = dict()
            self.shortClose = False
            self.longClose = False
        except BaseException as errorMsg:
            print(errorMsg)
            self._running = False

    def run(self):
        try:
            self.trade()
        except BaseException as errorMsg:
            self._running = False
            print(errorMsg)
            print("线程结束，重启线程")


    def trade(self):
        while True:
            self.take_JY()
            if self.JYflag == True:
                self.check_JY()
                if self.revokeFlag == True:
                    self.revoke_JY()
                    self.ShortDict = dict()
                    self.LongDict = dict()

    def take_JY(self):
        if self.JYflag==False:
            result = self.swapAPI.get_specific_ticker(self.CoinType + '-USD-SWAP')
            currentPrice = float(result['last'])
            ShortPrice = currentPrice
            LongPrice = currentPrice
            for i in range(0, self.ShortPoint):
                if self.longClose == False:
                    ShortPrice = round(ShortPrice + ShortPrice / self.shortStep, 2)
                else:
                    ShortPrice = round(ShortPrice + ShortPrice / self.shortStep2, 2)
                    self.longClose = False
                self.ShortDict[ShortPrice] = list()
                self.ShortDict[ShortPrice].append(-1)
                self.ShortDict[ShortPrice].append('NULL')
            for i in range(0, self.LongPoint):
                if self.shortClose == False:
                    LongPrice = round(LongPrice - LongPrice / self.longStep, 2)
                else:
                    LongPrice = round(LongPrice - LongPrice / self.longStep2, 2)
                    self.shortClose = False
                self.LongDict[LongPrice] = list()
                self.LongDict[LongPrice].append(-1)
                self.LongDict[LongPrice].append('NULL')
            for a in self.ShortDict.keys():
                time.sleep(self.lag)
                try:
                    openflag = 0
                    result = self.swapAPI.get_order_list(self.CoinType + '-USD-SWAP', state='0')
                    if result:
                        for b in result[0]['order_info']:
                            if b['type'] == '4':
                                closeprice = float(b['price'])
                                if abs(a - closeprice) < a / self.shortStep:
                                    openflag = -1
                    if openflag == 0:
                        result = self.swapAPI.take_order(self.CoinType + '-USD-SWAP', type='2', price=str(a),
                                                         size=self.ShortQuantity)
                        time.sleep(self.lag)
                        if result['result'] == 'true' and result['error_code'] == '0' and result['order_id'] != '-1':
                            self.ShortDict[a][0] = 0
                            self.ShortDict[a][1] = result['order_id']
                            logging.info("开空单成功,开单价格：" + str(a)+"开单数量：" +
                                         self.ShortQuantity + " 订单id:"+result['order_id'])
                        else:
                            logging.info('开空单失败，开单价格：'+str(a))
                except BaseException as errmsg:
                    logging.info("开空单异常:")
                    print(errmsg)
            for a in self.LongDict.keys():
                time.sleep(self.lag)
                try:
                    openflag = 0
                    result = self.swapAPI.get_order_list(self.CoinType + '-USD-SWAP', state='0')
                    if result:
                        for b in result[0]['order_info']:
                            if b['type'] == '3':
                                closeprice = float(b['price'])
                                if abs(a - closeprice) < a / self.longStep:
                                    openflag = -1

                    if openflag == 0:
                        result = self.swapAPI.take_order(self.CoinType + '-USD-SWAP', type='1', price=str(a),
                                                         size=self.LongQuantity)
                        if result['result'] == 'true' and result['error_code']=='0' and result['order_id'] != '-1':
                            self.LongDict[a][0] = 0
                            self.LongDict[a][1] = result['order_id']
                            logging.info("开多单成功,开单价格：" + str(a)+"开单数量：" +
                                         self.LongQuantity + " 订单id:"+result['order_id'])
                        else:
                            logging.info('开多单失败，开单价格：'+str(a))
                except BaseException as errmsg:
                    logging.info("开多单异常:")
                    print(errmsg)
            self.JYflag = True

    def check_JY(self):
        for a in self.ShortDict.keys():
            if self.ShortDict[a][0] == 0:
                result = self.swapAPI.get_order_info(self.CoinType+'-USD-SWAP', self.ShortDict[a][1])
                time.sleep(self.lag)
                if result['state'] == '2':
                    self.revokeFlag = True
                    self.shortClose = True
                    self.ShortDict[a][0] = 1
                    self.swapAPI.take_order(self.CoinType + '-USD-SWAP', type='4', price=str(a-a/self.shortStep2),
                                                 size=self.ShortQuantity)
                    time.sleep(self.lag)

        for a in self.LongDict.keys():
            if self.LongDict[a][0] == 0:
                result = self.swapAPI.get_order_info(self.CoinType + '-USD-SWAP', self.LongDict[a][1])
                time.sleep(self.lag)
                if result['state'] == '2':
                    self.revokeFlag = True
                    self.longClose = True
                    self.LongDict[a][0] = 1
                    self.swapAPI.take_order(self.CoinType + '-USD-SWAP', type='3', price=str(a + a / self.longStep2),
                                            size=self.LongQuantity)
                    time.sleep(self.lag)


    def revoke_JY(self):
        for a in self.ShortDict.keys():
            if self.ShortDict[a][0] == 0:
                result = self.swapAPI.revoke_order(self.CoinType+'-USD-SWAP', order_id=self.ShortDict[a][1])
                time.sleep(self.lag)
                if result['result'] != 'true':
                    self.swapAPI.take_order(self.CoinType + '-USD-SWAP', type='4', price=str(a - a / self.shortStep2),
                                            size=self.ShortQuantity)
                    time.sleep(self.lag)
        for a in self.LongDict.keys():
            if self.LongDict[a][0] == 0:
                result = self.swapAPI.revoke_order(self.CoinType+'-USD-SWAP', order_id=self.LongDict[a][1])
                time.sleep(self.lag)
                if result['result'] != 'true':
                    self.swapAPI.take_order(self.CoinType + '-USD-SWAP', type='3', price=str(a + a / self.longStep2),
                                            size=self.LongQuantity)
                    time.sleep(self.lag)
        self.JYflag = False
        self.revokeFlag = False

    def get_timestamp(self):
        now = datetime.datetime.now()
        t = now.isoformat("T", "milliseconds")
        return t + "Z"

def start_trade(JY_dict, ZYZS_dict):
    autotrade = TradeThread(JY_dict, ZYZS_dict)
    autotrade.start()
    # while True:
    #     time.sleep(100)
    #     try:
    #         if autotrade._running == False or autotrade.is_alive() == True:
    #             autotrade = TradeThread(JY_dict, ZYZS_dict)
    #             autotrade.start()
    #         else:
    #             print("线程运行正常")
    #     except BaseException as errorMsg:
    #         print("线程运行异常：")
    #         print(errorMsg)
    #         autotrade = TradeThread(JY_dict, ZYZS_dict)
    #         autotrade.start()

def stop_stop():
    global stopprogram