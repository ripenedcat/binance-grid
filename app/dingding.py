import requests,json

# windows
from app.authorization import dingding_token,api_secret,api_key, WECHAT_AGENTID,WECHAT_SECRET,WECHAT_ID
from app.BinanceAPI import BinanceAPI
from app.logger import Logger
# linux
# from app.authorization import dingding_token
logger = Logger().get()
class Message:

    def buy_limit_msg(self,coin, quantity, price,step):
        try:
            res = BinanceAPI(api_key,api_secret).buy_limit(coin, quantity, price)
            if res and res['orderId']:
                buy_info = f"成交：币种为：{coin}。买单价为：{price}。买单量为：{quantity}，仓位：{step}"
                self.wechat_warn(buy_info)
                return res
        except BaseException as e:
            error_info = f"Warn: 币种为：{coin},买单失败.api返回内容为:{res['msg']}"
            logger.error(error_info)
            logger.error("res = ", res)
            self.wechat_warn(error_info)


    def sell_limit_msg(self,coin, quantity, price,step):
        '''
        :param market:
        :param quantity: 数量
        :param rate: 价格
        :return:
        '''
        try:

            res = BinanceAPI(api_key,api_secret).sell_limit(coin, quantity, price)
            if res and res['orderId']:
                buy_info = f"成交：币种为：{coin}。卖单价为：{price}。卖单量为：{quantity}, 仓位：{step}"
                self.wechat_warn(buy_info)
                return res
        except BaseException as e:
            error_info = f"Warn: 币种为：{coin},卖单失败.api返回内容为:{res['msg']}"
            logger.error(error_info)
            logger.error("res = ",res)
            self.wechat_warn(error_info+str(res))

    def dingding_warn(self,text):
        headers = {'Content-Type': 'application/json;charset=utf-8'}
        api_url = "https://oapi.dingtalk.com/robot/send?access_token=%s" % dingding_token
        json_text = self._msg(text)
        requests.post(api_url, json.dumps(json_text), headers=headers).content

    def wechat_warn(self,text):
        get_token_url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=" + WECHAT_ID + "&corpsecret=" + WECHAT_SECRET
        ACCESS_TOKEN = json.loads(requests.get(get_token_url).text)["access_token"]
        send = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + ACCESS_TOKEN
        message = {
            "touser": "@all",
            "msgtype": "text",
            "agentid": WECHAT_AGENTID,
            "text": {
                "content": text
            },
            "safe": 0
        }
        requests.post(send, data=json.dumps(message))

    def _msg(self,text):
        json_text = {
            "msgtype": "text",
            "at": {
                "atMobiles": [
                    "11111"
                ],
                "isAtAll": False
            },
            "text": {
                "content": text
            }
        }
        return json_text

if __name__ == "__main__":
    msg = Message()
    print(msg.buy_limit_msg("EOSUSDT",4,2))