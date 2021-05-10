# 数字货币量化交易-网格策略

---

### 介绍
参考项目地址： https://github.com/hengxuZ/spot-trend-grid

去掉了趋势判断，因为一直报错

修改成bat传参模式，可以运行多个交易对

去掉了dingding提醒改用微信提醒

加了logger

增加定投追跌次数限制，默认3次，可调

### 使用方法
1. 默认币安API，因为网格手续费巨大， 而币安手续费最低
2. /app/authorization/py 文件中加入自己的币安api，参考# https://www.binance.com/restapipub.html
3. /app/authorization/py 文件中加入自己的企业微信api，参考# https://zhuanlan.zhihu.com/p/56806164
4. 修改/start.py中的max_steps = 3可以修改定投追跌次数
5. bat文件中修改python start.py XRPDOWNUSDT 最后的XRPDOWNUSDT位自己想要交易的交易对
6. 修改第五步后确保/data目录下存在data_XRPDOWNUSDT.json文件，文件名与币种对应
7. 其他参考原项目说明
