# -*- coding: utf-8 -*-
from app.BinanceAPI import BinanceAPI
from app.authorization import api_key,api_secret
from data.runBetData import RunBetData
from app.dingding import Message
import time
from app.logger import Logger
from data.calcIndex import CalcIndex
import sys
import traceback

binan = BinanceAPI(api_key,api_secret)

msg = Message()
logger = Logger().get()


max_steps = 3

class Run_Main():

    def __init__(self):
        logger.info("start running")
        self.coin_type = runbet.get_cointype()  # 交易币种
        pass


    def loop_run(self):
        while True:
            try:
                cur_market_price = binan.get_ticker_price(runbet.get_cointype()) # 当前交易对市价
                grid_buy_price = runbet.get_buy_price()  # 当前网格买入价格
                grid_sell_price = runbet.get_sell_price() # 当前网格卖出价格
                quantity = runbet.get_quantity()   # 买入量
                step = runbet.get_step() # 当前步数

                right_size = len(str(cur_market_price).split(".")[1])


                if grid_buy_price >= cur_market_price and max_steps<=3:   # 是否满足买入价
                #if grid_buy_price >= cur_market_price and step<=3 and index.calcAngle(self.coin_type,"5m",False,right_size):   # 是否满足买入价
                    res = msg.buy_limit_msg(self.coin_type, quantity, grid_buy_price,runbet.get_step()+1)
                    if res and res['orderId']: # 挂单成功
                        buy_info = f"Warn: {runbet.get_cointype()}. buy at: {grid_buy_price}. quatity: {quantity}"
                        logger.info(buy_info)
                        runbet.modify_price(grid_buy_price, step+1) #修改data.json中价格、当前步数
                        time.sleep(20) # 挂单后，停止运行1分钟


                elif grid_sell_price < cur_market_price:  # 是否满足卖出价
                #elif grid_sell_price < cur_market_price and index.calcAngle(self.coin_type,"5m",True,right_size):  # 是否满足卖出价
                    if step==0: # setp=0 防止踏空，跟随价格上涨
                        runbet.modify_price(grid_sell_price,step)
                    else:
                        res = msg.sell_limit_msg(self.coin_type, runbet.get_quantity(False), grid_sell_price,runbet.get_step()-1)
                        if res and res['orderId']:
                            buy_info = f"Warn: {runbet.get_cointype()}. sell at: {grid_sell_price}. quatity: {runbet.get_quantity(False)}"
                            logger.info(buy_info)
                            runbet.modify_price(grid_sell_price, step - 1)
                            time.sleep(20)  # 挂单后，停止运行1分钟

                else:
                    logger.info(f"current price of {runbet.get_cointype()}: {cur_market_price}. no match, continue")
                    logger.info(f"grid value is {grid_buy_price} - {grid_sell_price}, step is {runbet.get_step()}")
            except Exception as e:
                logger.error(traceback.format_exc())
                continue

if __name__ == "__main__":
    coin = None
    if len(sys.argv)>1:
        coin = sys.argv[1]
    if not coin: coin = "XRPUSDT"
    runbet = RunBetData(coin)
    index = CalcIndex(coin)
    instance = Run_Main()
    try:
        instance.loop_run()
    except Exception as e:
        logger.info("program exit")
        logger.error(traceback.format_exc())
        error_info = f"Warn: {instance.coin_type} service stop, error message: {str(e)}"
        msg.wechat_warn(error_info)

# 调试看报错运行下面，正式运行用上面       
# if __name__ == "__main__":       
    # instance = Run_Main()    
    # instance.loop_run()
