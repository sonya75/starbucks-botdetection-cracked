from sensordata import BotDetector
import requests
import time
import random
def login(email,password):
	sess=requests.session()
	prox=None
	d=sess.get('https://www.starbucks.com/account/signin?ReturnUrl=%2F',headers={"Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36","Sec-Fetch-User":"?1","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3","Sec-Fetch-Site":"none","Sec-Fetch-Mode":"navigate"},proxies={"https":prox})
	d.raise_for_status()
	x=BotDetector()
	x.headernameprefix="X-DQ7Hy5L1-"
	x.processrawscript(d.content)
	time.sleep(float(random.randint(5000,8000))/1000)
	x.generateevents()
	headers=x.getheaders()
	headers.update({"Origin":"https://www.starbucks.com","Accept":"application/json","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36","X-NewRelic-ID":"VQUHVlNSARACUFRWDgADVA==","Sec-Fetch-Site":"same-origin","Sec-Fetch-Mode":"cors","Referer":"https://www.starbucks.com/account/signin?ReturnUrl=%2F"})
	d=sess.post("https://www.starbucks.com/bff/account/signin",json={"username":email,"password":password,"rememberMe":True,"market":"US","reputation":{"deviceFingerprint":""}},headers=headers,proxies={"https":prox})
	d.raise_for_status()
	return sess