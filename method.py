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
import datetime
import time
global stopprogram
class AutoTrade(object):
    def __init__(self, JY_dict, ZYZS_dict):
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



        self.accountAPI = account.AccountAPI(JY_dict['api_key'].get(),
                                             JY_dict['secret_key'].get(),
                                             JY_dict['passphrase'].get(), False)

        self.swapAPI = swap.SwapAPI(JY_dict['api_key'].get(),
                                    JY_dict['secret_key'].get(),
                                    JY_dict['passphrase'].get(), False)

        self.ShortQuantity = JY_dict['ShortQuantity'].get()
        self.LongQuantity = JY_dict['LongQuantity'].get()
     #  ShortPrice = float(JY_dict['ShortPrice'].get())
      # LongPrice = float(JY_dict['LongPrice'].get())
        self.ShortPoint = int(JY_dict['ShortPoint'].get())
        self.LongPoint = int(JY_dict['LongPoint'].get())
        self.Step = float(JY_dict['Step'].get())
        self.Step2 = float(JY_dict['Step2'].get())
        self.CoinType = JY_dict['CoinType'].get()

        self.param_dict = JY_dict
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
    def trade(self):
        while True:
            self.take_JY()
            if self.JYflag == True:
                self.check_JY()
                if self.revokeFlag == True:
                    self.revoke_JY()
                    self.ShortDict = dict()
                    self.LongDict = dict()

    def long_trade(self):
        while True:
            self.long_take()
            self.long_check()
            if self.longRevoke == 'need':
                self.long_revoke()

    def long_take(self):
        if self.longTake == 'need':
            # while True:
            #     time.sleep(0.1)
            #     try:
            #         result = self.spotAPI.get_specific_ticker(self.CoinType + '-USDT')
            #         if result['instrument_id'] == self.CoinType + '-USDT':
            #             LongPrice = float(result['last'])
            #             break
            #         else:
            #             time.sleep(2)
            #             print("获取当前价格失败，再次获取")
            #     except BaseException as errmsg:
            #         print("获取当前价格失败，再次获取。错误信息："+errmsg)
            LongPrice = self.currentPrice
            for i in range(0, self.LongPoint):
                self.LongDict[LongPrice] = list()
                self.LongDict[LongPrice].append(-1)
                self.LongDict[LongPrice].append('NULL')
                LongPrice = round(LongPrice - LongPrice / self.Step, 2)
            self.longTake = 'noneed'
        for a in self.LongDict.keys():
            if self.LongDict[a][0] == -1:
                for i in range(3):
                    time.sleep(0.1)
                    try:
                        result = self.swapAPI.take_order(self.CoinType + '-USD-SWAP', type='1', price=str(a),
                                                         size=self.LongQuantity)
                        if result['result'] == 'true' and result['error_code'] == '0' and result['order_id'] != '-1':
                            self.LongDict[a][0] = 0
                            self.LongDict[a][1] = result['order_id']
                            logging.info("开多单成功,开单价格：" + str(a)+"开单数量：" +
                                         self.LongQuantity + " 订单id:"+result['order_id'])
                            break
                        else:
                            logging.info('开多单失败，重新开单。开单价格：'+str(a))
                            time.sleep(10)
                            continue
                    except BaseException as errmsg:
                        logging.info("开多单异常")
                        print(errmsg)
                        time.sleep(10)
        return

    def long_check(self):
        while True:
            time.sleep(0.1)
            try:
                result = self.swapAPI.get_specific_ticker(self.CoinType + '-USD-SWAP')
                if result['instrument_id'] == self.CoinType + '-USD-SWAP':
                    self.currentPrice = float(result['last'])
                    break
                else:
                    print("获取当前价格失败，再次获取")
            except BaseException as errmsg:
                print("获取当前价格失败，再次获取。错误信息："+errmsg)
        if self.currentPrice > max(self.LongDict.keys())+max(self.LongDict.keys())/self.Step:
            self.longRevoke = 'need'

        else:
            for a in self.LongDict.keys():
                if self.LongDict[a][0] == 0:
                    try:
                        result = self.swapAPI.get_order_info(self.CoinType + '-USD-SWAP', self.LongDict[a][1])
                        time.sleep(0.1)
                        if result['state'] == '2' and result['type'] == '1':
                            result = self.swapAPI.take_order(self.CoinType + '-USD-SWAP', type='3'
                                                    , price=str(a + a / self.Step2), size=self.LongQuantity)
                            if result['result'] == 'true':
                                self.LongDict[a][0] = 1
                                self.LongDict[a][1] = result['order_id']
                            time.sleep(0.1)
                    except BaseException as errmsg:
                        print('查询开多单失败:'+errmsg)
                if self.LongDict[a][0] == 1:
                    try:
                        result = self.swapAPI.get_order_info(self.CoinType + '-USD-SWAP', self.LongDict[a][1])
                        time.sleep(0.1)
                        if result['state'] == '2':
                            self.LongDict[a][0] = -1
                            self.LongDict[a][1] = 'NULL'
                    except BaseException as errmsg:
                        print('查询平多单失败：')
                        print(errmsg)

    def long_revoke(self):
        for a in self.LongDict.keys():
            if self.LongDict[a][0] == 0:
                try:
                    time.sleep(0.1)
                    result = self.swapAPI.get_order_info(self.CoinType + '-USD-SWAP', self.LongDict[a][1])
                    if result['result'] == 'true'and (result['state'] == '0' or result['state'] == '1'):
                        self.swapAPI.revoke_order(self.CoinType+'-USD-SWAP', order_id=self.LongDict[a][1])
                    elif result['result'] == 'true' and result['state'] == '2':
                        self.swapAPI.take_order(self.CoinType + '-USD-SWAP', type='3', price=str(a + a / self.Step2),
                                            size=self.LongQuantity)
                        time.sleep(0.1)
                except BaseException as errmsg:
                    print('撤单失败')
                    print(errmsg)
                    continue
        self.LongDict.clear()
        self.longTake = 'need'
        self.revokeFlag = 'noneed'

    def take_JY(self):
        if self.JYflag==False:
            result = self.swapAPI.get_specific_ticker(self.CoinType + '-USD-SWAP')
            currentPrice = float(result['last'])
            ShortPrice = currentPrice
            LongPrice = currentPrice
            for i in range(0, self.ShortPoint):
                ShortPrice = round(ShortPrice + ShortPrice / self.Step, 2)
                self.ShortDict[ShortPrice] = list()
                self.ShortDict[ShortPrice].append(-1)
                self.ShortDict[ShortPrice].append('NULL')
            for i in range(0, self.LongPoint):
                LongPrice = round(LongPrice - LongPrice / self.Step, 2)
                self.LongDict[LongPrice] = list()
                self.LongDict[LongPrice].append(-1)
                self.LongDict[LongPrice].append('NULL')
            for a in self.ShortDict.keys():
                time.sleep(0.1)
                try:
                    openflag = 0
                    result = self.swapAPI.get_order_list('XRP-USD-SWAP', state='0')
                    if result:
                        for b in result[0]['order_info']:
                            if b['type'] == '4':
                                closeprice = float(b['price'])
                                if abs(a - closeprice) < a / self.step:
                                    openflag = -1
                    if openflag == 0:
                        result = self.swapAPI.take_order(self.CoinType + '-USD-SWAP', type='2', price=str(a),
                                                         size=self.ShortQuantity)
                        time.sleep(0.1)
                        if result['result'] == 'true' and result['error_code']=='0' and result['order_id'] != '-1':
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
                time.sleep(0.1)
                try:
                    openflag = 0
                    result = self.swapAPI.get_order_list('XRP-USD-SWAP', state='0')
                    if result:
                        for b in result[0]['order_info']:
                            if b['type'] == '3':
                                closeprice = float(b['price'])
                                if abs(a - closeprice) < a / self.step:
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
                time.sleep(0.1)
                if result['state'] == '2':
                    self.revokeFlag = True
                    self.ShortDict[a][0] = 1
                    self.swapAPI.take_order(self.CoinType + '-USD-SWAP', type='4', price=str(a-a/self.Step2),
                                                 size=self.ShortQuantity)
                    time.sleep(0.1)

        for a in self.LongDict.keys():
            if self.LongDict[a][0] == 0:
                result = self.swapAPI.get_order_info(self.CoinType + '-USD-SWAP', self.LongDict[a][1])
                time.sleep(0.1)
                if result['state'] == '2':
                    self.revokeFlag = True
                    self.LongDict[a][0] = 1
                    self.swapAPI.take_order(self.CoinType + '-USD-SWAP', type='3', price=str(a + a / self.Step2),
                                            size=self.LongQuantity)
                    time.sleep(0.1)


    def revoke_JY(self):
        for a in self.ShortDict.keys():
            if self.ShortDict[a][0] == 0:
                result = self.swapAPI.revoke_order(self.CoinType+'-USD-SWAP', order_id=self.ShortDict[a][1])
                time.sleep(0.1)
                if result['result'] != 'true':
                    self.swapAPI.take_order(self.CoinType + '-USD-SWAP', type='4', price=str(a - a / self.Step2),
                                            size=self.ShortQuantity)
                    time.sleep(0.1)
        for a in self.LongDict.keys():
            if self.LongDict[a][0] == 0:
                result = self.swapAPI.revoke_order(self.CoinType+'-USD-SWAP', order_id=self.LongDict[a][1])
                time.sleep(0.1)
                if result['result'] != 'true':
                    self.swapAPI.take_order(self.CoinType + '-USD-SWAP', type='3', price=str(a + a / self.Step2),
                                            size=self.LongQuantity)
                    time.sleep(0.1)
        self.JYflag = False
        self.revokeFlag = False

    def get_timestamp(self):
        now = datetime.datetime.now()
        t = now.isoformat("T", "milliseconds")
        return t + "Z"

#
# class ZYZS(object):
#     def __init__(self):
#         api_key = "e475a6ff-3a83-4bce-8cc8-51b1108b5d23"
#         secret_key = "57944536044AD9587DC263C734A2B3A7"
#         passphrase = "rander360104456"
#         self.ZYZS_ShortPrice  = 20
#         self.ZYZS_LongPrice = 40
#         self.swapAPI = swap.SwapAPI(api_key, secret_key, passphrase, False)
#     def take_ZYZS(self):
#         if self.ZYZS_ShortState == -1:
#             short_algo_price = self.ZYZS_ShortPrice - self.ZYZS_ShortPrice / float(self.ZYZS_OpenShortProp)
#             result = self.swapAPI.take_order_algo(self.CoinType+'USD-SWAP', type=2, order_type=1,
#                                      size=self.ZYZS_ShortQuantity, trigger_price=str(self.ZYZS_ShortPrice),
#                                      algo_price=str(short_algo_price))
#             if result['data']['result'] == 'success':
#                 self.ZYZS_ShortState = 0
#         if self.ZYZS_LongState == -1:
#             long_algo_price = self.ZYZS_LongPrice + self.ZYZS_LongPrice / float(self.ZYZS_OpenLongProp)
#             result = self.swapAPI.take_order_algo(self.CoinType + 'USD-SWAP', type=1, order_type=1,
#                                      size=self.ZYZS_LongQuantity, trigger_price=str(self.ZYZS_LongPrice),
#                                      algo_price=str(long_algo_price))
#             if result['data']['result'] == 'success':
#                 self.ZYZS_LongState = 0

def start_trade(JY_dict, ZYZS_dict):
    autotrade = AutoTrade(JY_dict,ZYZS_dict)
    autotrade.trade()

def stop_stop():
    global stopprogram