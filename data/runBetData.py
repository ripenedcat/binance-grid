import os,json
from app.logger import Logger
import sys
# linux
logger = Logger().get()


class RunBetData:

    def __init__(self,coin_type):
        self.data_path = os.getcwd()+"/data/data_"+coin_type+".json"

    def _get_json_data(self):
        '''读取json文件'''
        tmp_json = {}
        with open(self.data_path, 'r') as f:
            tmp_json = json.load(f)
            f.close()
        return tmp_json


    def _modify_json_data(self,data):
        '''修改json文件'''
        with open(self.data_path, "w") as f:
            f.write(json.dumps(data, indent=4))
        f.close()


    ####------下面为输出函数--------####

    def get_buy_price(self):
        data_json = self._get_json_data()
        return data_json["runBet"]["next_buy_price"]


    def get_sell_price(self):
        data_json = self._get_json_data()
        return data_json["runBet"]["grid_sell_price"]

    def get_cointype(self):
        data_json = self._get_json_data()
        return data_json["config"]["cointype"]

    def get_quantity(self,exchange_method=True):
        '''
        :param exchange: True 代表买入，取买入的仓位 False：代表卖出，取卖出应该的仓位
        :return:
        '''

        data_json = self._get_json_data()
        cur_step = data_json["runBet"]["step"] if exchange_method else data_json["runBet"]["step"] - 1 # 买入与卖出操作对应的仓位不同
        quantity_arr = data_json["config"]["quantity"]

        quantity = None
        if cur_step < len(quantity_arr): # 当前仓位 > 设置的仓位 取最后一位
            quantity = quantity_arr[0] if cur_step == 0 else quantity_arr[cur_step]
        else:
            quantity = quantity_arr[-1]
        return quantity

    def get_step(self):
        data_json = self._get_json_data()
        return data_json["runBet"]["step"]

    # 买入后，修改 补仓价格 和 网格平仓价格以及步数
    def modify_price(self, deal_price,step):
        logger.info(f'start adjusting price')
        data_json = self._get_json_data()
        data_json["runBet"]["next_buy_price"] = round(deal_price * (1 - data_json["config"]["double_throw_ratio"] / 100), 6) # 保留2位小数
        data_json["runBet"]["grid_sell_price"] = round(deal_price * (1 + data_json["config"]["profit_ratio"] / 100), 6)
        data_json["runBet"]["step"] = step
        self._modify_json_data(data_json)
        logger.info(f'modified buy price is: {data_json["runBet"]["next_buy_price"]}. monified sell price is: {data_json["runBet"]["grid_sell_price"]}. step is {data_json["runBet"]["step"]}')



if __name__ == "__main__":
    instance = RunBetData()
    # print(instance.modify_price(8.87,instance.get_step()-1))
    print(instance.get_quantity(False))
