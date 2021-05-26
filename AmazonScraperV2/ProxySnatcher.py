from requests_html import HTMLSession
import requests_html
from bs4 import BeautifulSoup


def getFreshProxies():
	succesful=False
	session = HTMLSession()
	URL = 'https://sslproxies.org/'
	while not succesful:
		try:
			response = session.get(URL,headers=None,proxies=None)
			succesful=True
		except Exceptiona as e:
			succesful =False	
			print(e)
			continue
	#print(response.html.raw_html)
	soup = BeautifulSoup(response.html.raw_html,features='lxml')
	table = soup.find('tbody')
	proxies = table.findAll('tr')
	proxies = [f'{x.td.get_text()}:{x.td.next_sibling.get_text()}' for x in proxies]
	file = open('http_proxies.txt','w',encoding='utf-8')
	file.write('\n'.join(proxies))
	file.close()
	#response.html.render(timeout=10)
#getFreshProxies()	