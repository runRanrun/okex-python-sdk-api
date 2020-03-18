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
        self.spotAPI = spot.SpotAPI(api_key, secret_key, passphrase, False)
        self.ShortQuantity = JY_dict['ShortQuantity'].get()
        self.LongQuantity = JY_dict['LongQuantity'].get()
     #   ShortPrice = float(JY_dict['ShortPrice'].get())
      #  LongPrice = float(JY_dict['LongPrice'].get())
        self.ShortPoint = int(JY_dict['ShortPoint'].get())
        self.LongPoint = int(JY_dict['LongPoint'].get())
        self.Step = float(JY_dict['Step'].get())
        self.CoinType = JY_dict['CoinType'].get()

        self.param_dict = JY_dict
        

        # self.ZYZS_ShortPrice = float(ZYZS_dict['ShortPrice'].get())
        # self.ZYZS_ShortQuantity = ZYZS_dict['ShortQuantity'].get()
        # self.ZYZS_OpenShortProp = float(ZYZS_dict['OpenShortProp'].get())
        # self.ZYZS_CloseShortNormProp = ZYZS_dict['CloseShortNormProp'].get()
        # self.ZYZS_CloseShortQuickProp = ZYZS_dict['CloseShortQuickProp'].get()
        # self.ZYZS_WaveAdjust = float(ZYZS_dict['WaveAdjust'].get())
        # self.ZYZS_CloseLag = ZYZS_dict['CloseLag'].get()
        #
        #
        # self.ZYZS_LongPrice = float(ZYZS_dict['LongPrice'].get())
        # self.ZYZS_LongQuantity = ZYZS_dict['LongQuantity'].get()
        # self.ZYZS_OpenLongProp = float(ZYZS_dict['OpenLongProp'].get())
        # self.ZYZS_CloseLongNormProp = ZYZS_dict['CloseLongNormProp'].get()
        # self.ZYZS_Clososition = ZYZS_dict['AddPosition'].get()
        # self.ZYZS_QuickCloseTrigger = ZYZS_dict['QuickCloseTrigger'].get()

        self.JYflag = False
        self.revokeFlag = False
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
    def take_JY(self):
        if self.JYflag==False:
            result = self.spotAPI.get_specific_ticker(self.CoinType + '-USDT')
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
                tmprice = currentPrice+(i+1)*currentPrice/self.Step
                time.sleep(0.1)
                try:
                    result = self.swapAPI.take_order(self.CoinType + '-USD-SWAP', type='2', price=str(tmprice),
                                                     size=self.ShortQuantity)
                    time.sleep(0.1)
                    if result['result'] == 'true' and result['error_code']=='0' and result['order_id'] != '-1':
                        self.ShortDict[a][0] = 0
                        self.ShortDict[a][1] = result['order_id']
                        logging.info("开空单成功,开单价格：" + str(tmprice)+"开单数量：" +
                                     self.ShortQuantity + " 订单id:"+result['order_id'])

                    else:
                        logging.info('开空单失败，开单价格：'+str(tmprice))
                except BaseException as errmsg:
                    logging.info("开空单异常:" + errmsg)
            for a in self.LongDict.keys():
                time.sleep(0.1)
                try:
                    result = self.swapAPI.take_order(self.CoinType + '-USD-SWAP', type='1', price=str(a),
                                                     size=self.LongQuantity)
                    if result['result'] == 'true' and result['error_code']=='0' and result['order_id'] != '-1':
                        self.LongDict[a][0] = 0
                        self.LongDict[a][1] = result['order_id']
                        logging.info("开多单成功,开单价格：" + str(tmprice)+"开单数量：" +
                                     self.LongQuantity + " 订单id:"+result['order_id'])
                    else:
                        logging.info('开多单失败，开单价格：'+str(tmprice))
                except BaseException as errmsg:
                    logging.info("开多单异常:" + errmsg)
            self.JYflag = True


    def check_JY(self):
        for a in self.ShortDict.keys():
            if self.ShortDict[a][0] == 0:
                result = self.swapAPI.get_order_info(self.CoinType+'-USD-SWAP', self.ShortDict[a][1])
                time.sleep(0.1)
                if result['state'] == '2':
                    self.revokeFlag = True
                    self.ShortDict[a][0] = 1
                    self.swapAPI.take_order(self.CoinType + '-USD-SWAP', type='4', price=str(a-a/self.Step),
                                                 size=self.ShortQuantity)
                    time.sleep(0.1)
        for a in self.LongDict.keys():
            if self.LongDict[a][0] == 0:
                result = self.swapAPI.get_order_info(self.CoinType + '-USD-SWAP', self.LongDict[a][1])
                time.sleep(0.1)
                if result['state'] == '2':
                    self.revokeFlag = True
                    self.LongDict[a][0] = 1
                    self.swapAPI.take_order(self.CoinType + '-USD-SWAP', type='3', price=str(a + a / self.Step),
                                            size=self.LongQuantity)
                    time.sleep(0.1)

    def revoke_JY(self):
        for a in self.ShortDict.keys():
            if self.ShortDict[a][0] == 0:
                result = self.swapAPI.revoke_order(self.CoinType+'-USD-SWAP', order_id=self.ShortDict[a][1])
                time.sleep(0.1)
                if result['result'] == False:
                    self.swapAPI.take_order(self.CoinType + '-USD-SWAP', type='4', price=str(a - a / self.Step),
                                            size=self.ShortQuantity)
                    time.sleep(0.1)
        for a in self.LongDict.keys():
            if self.LongDict[a][0] == 0:
                result = self.swapAPI.revoke_order(self.CoinType+'-USD-SWAP', order_id=self.LongDict[a][1])
                time.sleep(0.1)
                if result['result'] == False:
                    self.swapAPI.take_order(self.CoinType + '-USD-SWAP', type='3', price=str(a + a / self.Step),
                                            size=self.LongQuantity)
                    time.sleep(0.1)
        self.JYflag = False

    def get_timestamp(self):
        now = datetime.datetime.now()
        t = now.isoformat("T", "milliseconds")
        return t + "Z"


class ZYZS(object):
    def __init__(self):
        api_key = "e475a6ff-3a83-4bce-8cc8-51b1108b5d23"
        secret_key = "57944536044AD9587DC263C734A2B3A7"
        passphrase = "rander360104456"
        self.ZYZS_ShortPrice  = 20
        self.ZYZS_LongPrice = 40
        self.swapAPI = swap.SwapAPI(api_key, secret_key, passphrase, False)
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

def start_trade(JY_dict, ZYZS_dict):
    autotrade = AutoTrade(JY_dict,ZYZS_dict )
    autotrade.trade()