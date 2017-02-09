#coding=utf-8

import requests
import hashlib 
import time
import urlparse
import json


headers = {
	'Host' : 'mp.weixin.qq.com',
    'Referer' : 'https://mp.weixin.qq.com/',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    "Origin" : "https://mp.weixin.qq.com"
}

apis = {
	"host" : "https://mp.weixin.qq.com",
	"login" : "https://mp.weixin.qq.com/cgi-bin/bizlogin?action=startlogin",
	"qrcode" : "https://mp.weixin.qq.com/cgi-bin/loginqrcode?action=getqrcode&param=4300",
	"loginqrcode" : "https://mp.weixin.qq.com/cgi-bin/loginqrcode?action=ask&token=&lang=zh_CN&f=json&ajax=1",
	"loginask" : "https://mp.weixin.qq.com/cgi-bin/loginqrcode?action=ask&token=&lang=zh_CN&f=json&ajax=1",
	"bizlogin" : "https://mp.weixin.qq.com/cgi-bin/bizlogin?action=login&lang=zh_CN"
}

def md5str(s):
	m2 = hashlib.md5()
	m2.update(s)
	return m2.hexdigest()

class WeixinMP(object):
	"""docstring for Weixin"""

	def __init__(self, email, pwd, name):
		
		self.name = name

		if self.tryoldcookies() == False:
			pwd = md5str(pwd)
			self.cookies = {}

			res = self.req(apis["host"])

			res = self.req(apis["login"], data={
					"username": email,
			        "pwd": pwd,
			        "imgcode": "",
			        "f": "json"
				});

			rej = res.json()
			if not "base_resp" in rej or rej["base_resp"]["ret"] != 0:
				print res.text
				raise Exception("username or password error")
				return 

			print "账号密码验证成功"

			res = self.req(apis["qrcode"])

			f = open("test.jpg", "wb")
			f.write(res.content)
			f.flush()

			print "等待扫码"
			while True:
				res = self.req(apis["loginask"])
				if res.json()["status"] == 1:
					print "登录成功"
					break
				elif res.json()["status"] == 4:
					print "已经扫码"
				else:
					print "等待扫码"

				time.sleep(1)

			print "开始验证"
			res = self.req(apis["bizlogin"], data={
					"lang" : "zh_CN",
					"f" : "json",
					"ajax" : 1
				})
			rej = res.json()

			if not "base_resp" in rej or rej["base_resp"]["ret"] != 0:
				raise Exception("systerm error " + rej["base_resp"]["err_msg"])
				return 

			self.token = self.url2token(rej["redirect_url"])
			print "验证成功,token:", self.token

	def url2token(self, url):
		ret = urlparse.urlparse(url)
		params = urlparse.parse_qs(ret.query, True)
		token = params["token"][0]
		return token

	def tryoldcookies(self):
		try:
			cookies = open("cookies.log", "r").read()
			self.cookies = json.loads(cookies)

			res = self.req(apis["host"])
			if res.text.encode("utf-8").find(self.name) != -1:
				self.token = self.url2token(res.url)
				print "获取token:", self.token
				return True

		except Exception, e:
			print e

		self.cookies = {}
		open("cookies.log", "w")
		return False

	def req(self, url, data=False):
		if data == False:
			res = requests.get(url, headers=headers, cookies=self.cookies)
		else:
			res = requests.post(url, data=data, headers=headers, cookies=self.cookies)
		
		cookies = res.cookies.items()
		if len(cookies) > 0:
			for item in cookies:
				self.cookies[item[0]] = item[1]

			f = open("cookies.log", "w")
			f.write(json.dumps(self.cookies))
			f.flush()

		return res

	def callapi(self, url, data=False):
		url = "%s&token=%s" % (url, self.token)
		res = self.req(url, data)
		return res

if __name__ == '__main__':
	a = WeixinMP("email", "password", "公众号名称")
	res = a.callapi("https://mp.weixin.qq.com/merchant/ad_host_report?lang=zh_CN&f=json")
	print res.text


