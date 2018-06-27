#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pdb
import time
# import exchangeConnection.bitex.bitexService
# import exchangeConnection.pro.proService
import utils.helper as uh
import json
#############
from OkcoinSpotAPI import OKCoinSpot
from OkcoinFutureAPI import OKCoinFuture
from config import *

#现货API
okcoinSpot = OKCoinSpot(okcoinRESTURL,apikey,secretkey)

#期货API
okcoinFuture = OKCoinFuture(okcoinRESTURL,apikey,secretkey)

#############

# 包装一个不同市场的统一接口 方便同一套套利

class Market:
    def __init__(self, market_name="okex"):
        self.market_name = market_name
        self.curs = ['insur', 'eth', 'usdt', 'btc']

    def market_detail(self, base_cur, quote_cur):
        """
        获取市场盘口信息
        :param base_cur:
        :param quote_cur:
        :return:
        """
        if self.market_name == "okex":
            if (base_cur in self.curs) and (quote_cur in self.curs) and (base_cur != quote_cur):
                try:
                    tk = okcoinSpot.ticker(base_cur+'_'+quote_cur)
                    # print(tk)
                    if type(tk) ==str:
                        tk = json.loads(tk)
                    if 'ticker' in tk.keys():
                        return tk['ticker']
                except:
                    return None
            else:
                return None
        else:
            return None

    def account_available(self, cur_name):
        """
        获取某个currency的可用量
        :param cur_name:
        :param cur_market_name:
        :return:
        注意: free 和 freezed 代表了不同的资产种类. 可用余额只考虑free
        """
        if self.market_name == "okex":
            userinfo = okcoinSpot.userinfo()
            if type(userinfo) == str:
                userinfo = json.loads(userinfo)
            try:
                if userinfo["result"]:
                    return float(userinfo['info']['funds']['free'][cur_name])
                else:
                    return None
            except KeyError:
                return None

    def buy(self, cur_market_name, price, amount):
        '''
        注意最小交易金额的限制
        '''
        # print("buy", cur_market_name, price, amount)
        if self.market_name == "okex":
            base_cur, quote_cur = cur_market_name.split("_")
            try:
                order_result = okcoinSpot.trade(cur_market_name,'buy',str(price),str(amount))
                if type(order_result) == str:
                    order_result = json.loads(order_result)
                return order_result
            except:
                return None

    def sell(self, cur_market_name, price, amount):
        # print("sell", cur_market_name, price, amount)
        if self.market_name == "okex":
            base_cur, quote_cur = cur_market_name.split("_")
            try:
                order_result = okcoinSpot.trade(cur_market_name,'sell',str(price),str(amount))
                if type(order_result) == str:
                    order_result = json.loads(order_result)
                return order_result
            except:
                return None

    def buy_market(self, cur_market_name, amount):
        """
        市价买
        :param cur_market_name: 货币对的名称
        :param amount: 买的总价
        :return:
        """
        # print("buy_market:", cur_market_name, amount)
        if self.market_name == "okex":
            base_cur, quote_cur = cur_market_name.split("_")
            try:
                order_result = okcoinSpot.trade(cur_market_name,'buy_market', str(amount))
                if type(order_result) == str:
                    order_result = json.loads(order_result)
                return order_result
            except:
                return None


    def sell_market(self, cur_market_name, amount):
        """
        市价卖
        :param cur_market_name: 货币对的名称
        :param amount: 卖的数量
        :return:
        """
        # print("sell_market:", cur_market_name, amount)
        if self.market_name == "okex":
            base_cur, quote_cur = cur_market_name.split("_")
            try:
                order_result = okcoinSpot.trade(cur_market_name,'sell_market', str(amount))
                if type(order_result) == str:
                    order_result = json.loads(order_result)
                return order_result
            except:
                return None


    def order_normal(self, order_result, cur_market_name):
        """
        是否成功下单
        :param order_result: 下单返回结果
        :param cur_market_name: 货币对名称
        :return:
        """
        if self.market_name == "okex":
            base_cur, quote_cur = cur_market_name.split("_")
            try:
                if order_result.get('result') == True:
                    return True
                else:
                    return False
            except:
                # maybe key error
                return False


    def get_order_processed_amount(self, order_result, cur_market_name):
        '''
        获取交易订单对应的交易货币数目
        '''
        # print("get_order_processed_amount:", order_result, cur_market_name)
        if self.market_name == "okex":
            base_cur, quote_cur = cur_market_name.split("_")
            try:
                if order_result['result'] == True:
                    order_id = order_result['order_id']
                    order_info = okcoinSpot.orderinfo(cur_market_name,str(order_id))
                    if type(order_info) ==str:
                        order_info = json.loads(order_info)
                    return order_info['orders'][0]['deal_amount']
                else:
                    return None
            except:
                return None


    def cancel_order(self, order_result, cur_market_name):
        if self.market_name == "okex":
            base_cur, quote_cur = cur_market_name.split("_")
            try:
                orderid = order_result.get("order_id")
                cancel_result = okcoinSpot.cancelOrder(cur_market_name, str(orderid))
                if type(cancel_result) == str:
                    cancel_result = json.loads(cancel_result)
                return cancel_result
            except:
                return None


    def get_order_status(self, order_result, cur_market_name):
        # print("get_order_status:", order_result, cur_market_name)
        if self.market_name == "okex":
            base_cur, quote_cur = cur_market_name.split("_")
            try:
                order_id = order_result.get("order_id")
                order_info = okcoinSpot.orderinfo(cur_market_name,str(order_id))
                if type(order_info) ==str:
                    order_info = json.loads(order_info)
                if order_info['result'] == True:
                    return order_info['orders'][0]['status']
                else:
                    return None
            except:
                return None


# test
if __name__ == "__main__":
    okex = Market()
    # print(okex.market_detail("eth", "usdt"))
    # print(okex.market_detail("insur", "usdt"))
    # print(okex.market_detail("insur", "eth"))
    # print(okex.account_available('insur'))
    # print(okex.account_available('eth'))
    # print(okex.account_available('usdt'))
    # print(okex.account_available('btc'))
    # r1 = okex.buy('insur_usdt', '0.0029','20')
    # r2 = okex.sell('insur_usdt', '0.0029','20')
    # print(r1)
    # print(r2)
    # r3 = okex.buy_market('insur_usdt','20')
    # r4 = okex.sell_market('insur_usdt','20')
    # print(r3)
    # print(r4)
    # r5 = okex.order_normal(r1,'insur_usdt')
    # r6 = okex.get_order_processed_amount(r1,'insur_usdt')
    # r7 = okex.cancel_order(r1,'insur_usdt')
    # r8 = okex.get_order_status(r1,'insur_usdt')
    # print(r5)
    # print(r6)
    # print(r7)
    # print(r8)
    # base_cur, mid_cur, quote_cur = 'insur', 'usdt', 'eth'
    base_cur, mid_cur, quote_cur = 'insur', 'usdt', 'eth'
    # mid_cur = 'usdt'
    # quote_cur = 'eth'
    while True:
        # insur_eth
        # insur_usdt
        # eth_usdt
        base_quote = okex.market_detail(base_cur, quote_cur)
        base_mid = okex.market_detail(base_cur, mid_cur)
        quote_mid = okex.market_detail(quote_cur, mid_cur)
        print("*"*50)
        print("base_quote => {} | sell: {} | buy: {}".format(base_cur+'/'+quote_cur, base_quote['sell'], base_quote['buy']))
        print("base_mid => {} | sell: {} | buy: {}".format(base_cur+'/'+mid_cur, base_mid['sell'], base_mid['buy']))
        print("quote_mid => {} | sell: {} | buy: {}".format(quote_cur+'/'+mid_cur, quote_mid['sell'], quote_mid['buy']))
        # 计算正循环套利
        print("="*50)
        print("positive cycle: {}".format(( float(base_mid['buy']) /float(quote_mid['sell']) - float(base_quote['sell']))/float(base_quote['sell'])))
        print("negative cycle: {}".format((float(base_quote['buy']) - float(base_mid['sell'])/float(quote_mid['buy']) )/float(base_quote['sell'])))
        # base_mid_price_buy_1 / quote_mid_price_sell_1 - market_price_sell_1)/market_price_sell_1
        # market_price_buy_1 - base_mid_price_sell_1 / quote_mid_price_buy_1)/market_price_buy_1
        time.sleep(0.5)
        pass
    pdb.set_trace()

# print(exchangeConnection.pro.proService.ProServiceAPIKey().get_depth("ethcny").get("tick"))
# print("以太币账户：",exchangeConnection.bitex.bitexService.BitexServiceAPIKey(key_index="CNY_1").get_spot_acct_info())
# print("以太币可用", okex.account_available("cny", "eth_cny"))
# print(exchangeConnection.okex.okexService.getAccountInfo("cny", "get_account_info"))
# print(exchangeConnection.pro.proService.ProServiceAPIKey(key_index="CNY_1").get_spot_acct_info())
# result = exchangeConnection.okex.okexService.buy(2, 320.90, 0.4, None, None, "cny", "buy")
# print(result)
# {'result': 'success', 'id': 4491600137}
# result = exchangeConnection.okex.okexService.cancelOrder(1,4491600137, "cny", "cancel_order")
# print(result)
# print(exchangeConnection.okex.okexService.getOrderInfo(1, result.get("id"), "cny", "order_info"))
# {'id': 4491348833, 'type': 1, 'order_price': '20000.00', 'order_amount': '0.0020', 'processed_price': '19997.98', 'processed_amount': '0.0020', 'vot': '39.99', 'fee': '0.0000', 'total': '39.99', 'status': 2}

# result = exchangeConnection.okex.okexService.buyMarket(1, 2000, None, None, "cny", "buy_market")
# print(result)
# 买入eth
# result = exchangeConnection.bitex.bitexService.BitexServiceAPIKey(
#                         key_index="CNY_1").order("ethcny", 4000, 0.01, 'buy-limit')
# print("买入eth", result)  # {'status': 'ok', 'data': '2705107'}
# result = {'status': 'ok', 'data': '2706194'}
# print(exchangeConnection.bitex.bitexService.BitexServiceAPIKey(key_index="CNY_1").get_order_info(result.get("data")))
# print("eth order:", exchangeConnection.bitex.bitexService.BitexServiceAPIKey(key_index="CNY_1").get_active_orders("ethcny"))
# print("eth cancel order:", exchangeConnection.bitex.bitexService.BitexServiceAPIKey(key_index="CNY_1").cancel_order("2705970"))
# result = exchangeConnection.bitex.bitexService.BitexServiceAPIKey(
#                         key_index="CNY_1").order("ethcny", 11.0, 0.01, 'buy-market')
# print(result)

#pro
# print(exchangeConnection.pro.proService.ProServiceAPIKey(key_index="CNY_1").get_spot_acct_info())
# print(exchangeConnection.pro.proService.ProServiceAPIKey(key_index="CNY_1")\
#                         .order("ethbtc", 1.001, 0.01, 'buy-limit'))
# order_result = {'status': 'ok', 'data': '51'}
# print(exchangeConnection.pro.proService.ProServiceAPIKey(key_index="CNY_1")\
#                         .get_order_info(order_result.get("data")).get("data").get("field-amount"))
# print(exchangeConnection.pro.proService.ProServiceAPIKey(key_index="CNY_1").cancel_order(order_result.get("data")))
# order_result = {'status': 'ok', 'data': '3075505'}
# print(exchangeConnection.bitex.bitexService.BitexServiceAPIKey(
#                         key_index="CNY_1").get_order_info(order_result.get("data")).get("data"))
