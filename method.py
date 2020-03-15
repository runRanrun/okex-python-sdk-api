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

class AutoTrade(object):
    def __init__(self, JY_dict, ZYZS_dict):
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        # 初始化日志
        logging.basicConfig(filename='mylog-AutoTrade.json', filemode='a', format=log_format, level=logging.INFO)
        api_key = "e475a6ff-3a83-4bce-8cc8-51b1108b5d23"
        secret_key = "57944536044AD9587DC263C734A2B3A7"
        passphrase = "rander360104456"
        self.accountAPI = account.AccountAPI(api_key, secret_key, passphrase, False)

        self.swapAPI = swap.SwapAPI(api_key, secret_key, passphrase, False)
        self.ShortQuantity = JY_dict['ShortQuantity'].get()
        self.LongQuantity = JY_dict['LongQuantity'].get()
        ShortPrice = float(JY_dict['ShortPrice'].get())
        LongPrice = float(JY_dict['LongPrice'].get())
        ShortPoint = int(JY_dict['ShortPoint'].get())
        LongPoint = int(JY_dict['LongPoint'].get())
        self.Step = float(JY_dict['Step'].get())
        self.CoinType = JY_dict['CoinType'].get()

        self.param_dict = JY_dict
        

        self.ZYZS_ShortPrice = float(ZYZS_dict['ShortPrice'].get())
        self.ZYZS_ShortQuantity = ZYZS_dict['ShortQuantity'].get()
        self.ZYZS_OpenShortProp = float(ZYZS_dict['OpenShortProp'].get())
        self.ZYZS_CloseShortNormProp = ZYZS_dict['CloseShortNormProp'].get()
        self.ZYZS_CloseShortQuickProp = ZYZS_dict['CloseShortQuickProp'].get()
        self.ZYZS_WaveAdjust = float(ZYZS_dict['WaveAdjust'].get())
        self.ZYZS_CloseLag = ZYZS_dict['CloseLag'].get()


        self.ZYZS_LongPrice = float(ZYZS_dict['LongPrice'].get())
        self.ZYZS_LongQuantity = ZYZS_dict['LongQuantity'].get()
        self.ZYZS_OpenLongProp = float(ZYZS_dict['OpenLongProp'].get())
        self.ZYZS_CloseLongNormProp = ZYZS_dict['CloseLongNormProp'].get()
        self.ZYZS_Clososition = ZYZS_dict['AddPosition'].get()
        self.ZYZS_QuickCloseTrigger = ZYZS_dict['QuickCloseTrigger'].get()


        self.ShortDict = dict()
        self.LongDict = dict()
        self.ZYZS_ShortState = -1
        self.ZYZS_LongState = -1
        for i in range(0, ShortPoint):
            ShortPrice = round(ShortPrice + ShortPrice / self.Step, 2)
            self.ShortDict[ShortPrice] = list()
            self.ShortDict[ShortPrice].append(-1)
            self.ShortDict[ShortPrice].append('NULL')
        for i in range(0, LongPoint):
            LongPrice = round(LongPrice - LongPrice / self.Step, 2)
            self.LongDict[LongPrice] = list()
            self.LongDict[LongPrice].append(-1)
            self.LongDict[LongPrice].append('NULL')
    def trade(self):
        while True:
            self.take_JY()
            self.check_JY()
            self.take_ZYZS()
            self.checke_ZYZS

    def take_JY(self):
        try:
            result = spot.get_specific_ticker(self.CoinType + '-USDT')

            CurrentPrice = float(result['last'])
            for i in int(self.ShortQuantity):

            OrderRecord = dict()


            for a in self.ShortDict.keys():
                if self.ShortDict[a][0]== -1:
                    result = self.swapAPI.take_order(self.CoinType + '-USD-SWAP', type='2', price=str(a),
                                                    size=self.ShortQuantity)
                    if result['result'] == 'true' and result['error_code']=='0' and result['order_id'] != '-1':
                        self.ShortDict[a][0] = 0
                        self.ShortDict[a][1] = result['order_id']
                if self.ShortDict[a][0]=='1':
                    result = self.swapAPI.take_order(self.CoinType + '-USD-SWAP', type='4', price=str(a - a/self.Step),
                                                     size=self.ShortQuantity)
                    if result['result'] == 'true' and result['error_code'] == '0' and result['order_id'] != '-1':
                        self.ShortDict[a][0] = 2
                        self.ShortDict[a][1] = result['order_id']

            for a in self.LongDict.keys():
                if self.LongDict[a][0] == -1:
                    result = self.swapAPI.take_order(self.CoinType + '-USD-SWAP', type='1', price=str(a),
                                                 size=self.LongQuantity)
                    if result['result'] == 'true' and result['error_code'] == '0' and result['order_id'] != '-1':
                        self.LongDict[a][0] = 0
                        self.LongDict[a][1] = result['order_id']
                if self.LongDict[a][0] == '1':
                    result = self.swapAPI.take_order(self.CoinType + '-USD-SWAP', type='3', price=str(a + a/self.Step),
                                                 size=self.LongQuantity)
                    if result['result'] == 'true' and result['error_code'] == '0' and result['order_id'] != '-1':
                        self.LongDict[a][0] = 2
                        self.LongDict[a][1] = result['order_id']

        except BaseException as errmsg:
            logging.info("开单错误:" + errmsg)

    def check_JY(self):
        for a in self.ShortDict.keys():
            if self.ShortDict[a][0] == 0 :
                result = self.swapAPI.get_order_info(self.CoinType+'-USD-SWAP',self.ShortDict[a][1])
                if result['state'] == '2':
                    self.ShortDict[a][0] = 1
            elif self.ShortDict[a][0] == 2:
                result = self.swapAPI.get_order_info(self.CoinType + '-USD-SWAP', self.ShortDict[a][1])
                if result['state'] == '2':
                    self.ShortDict[a][0] = -1

        for a in self.LongDict.keys():
            if self.LongDict[a][0] == 0:
                result = self.swapAPI.get_order_info(self.CoinType + '-USD-SWAP', self.LongDict[a][1])
                if result['state'] == '2':
                    self.LongDict[a][0] = 1
            elif self.ShortDict[a][0] == 2:
                result = self.swapAPI.get_order_info(self.CoinType + '-USD-SWAP', self.LongDict[a][1])
                if result['state'] == '2':
                    self.LongDict[a][0] = -1
    def take_ZYZS(self):
        if self.ZYZS_ShortState == -1:
            short_algo_price = self.ZYZS_ShortPrice - self.ZYZS_ShortPrice / float(self.ZYZS_OpenShortProp)
            result = self.swapAPI.take_order_algo(self.CoinType+'USD-SWAP', type=2, order_type=1,
                                     size=self.ZYZS_ShortQuantity, trigger_price=str(self.ZYZS_ShortPrice),
                                     algo_price=str(short_algo_price))
            if result['data']['result'] == 'success':

                self.ZYZS_ShortState = 0
        if self.ZYZS_LongState == -1:
            long_algo_price = self.ZYZS_LongPrice + self.ZYZS_LongPrice / float(self.ZYZS_OpenLongProp)
            result = self.swapAPI.take_order_algo(self.CoinType + 'USD-SWAP', type=1, order_type=1,
                                     size=self.ZYZS_LongQuantity, trigger_price=str(self.ZYZS_LongPrice),
                                     algo_price=str(long_algo_price))
            if result['data']['result'] == 'success':
                self.ZYZS_LongState = 0

    def check_ZYZS(self):
        if self.ZYZS_ShortState == 0:
            self.swapAPI.get_order_algos(self.CoinType + '-USD-SWAP', order_type=1,s)


    def get_timestamp(self):
        now = datetime.datetime.now()
        t = now.isoformat("T", "milliseconds")
        return t + "Z"


class ZYZS()
def start_trade(JY_dict, ZYZS_dict):
    autotrade = AutoTrade(JY_dict,ZYZS_dict )
    autotrade.trade()