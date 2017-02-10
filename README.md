# WeixinMP

## 用python实现的一个公众号后台登录程序

### 代码地址
	
[https://github.com/zengkv/WeixinMP](https://github.com/zengkv/WeixinMP)

### 使用示例

``` python
	# 调用WeixinMP类生成一个实例，该实例保留登录状态
	# WeixinMP提供callapi方法，该方法负责请求公众号后台url，拉取到对应公众号的后台数据
	# 本示例为登录公众号并且拉取广点通数据
	a = WeixinMP("email", "password", "公众号名称")
	res = a.callapi("https://mp.weixin.qq.com/merchant/ad_host_report?lang=zh_CN&f=json")
	print res.text
```

### 实现简介

模拟 https://mp.weixin.qq.com 前端页面进行http请求，保存下请求中的cookie
并且下载登录所需的二维码文件为test.jpg，管理员或者申请者用微信扫描此二维码实现登录。
登录的cookie保存至cookies.log文件，后续若该cookie未过期则使用此cookie进行数据拉取，若过期则重复登录步骤。
具体参看代码。
