from requests_html import HTMLSession
import requests_html
from bs4 import BeautifulSoup
import random
from file_reader import read_from_xlsx
import time
import pandas as pd
from pprint import pprint
from ProxySnatcher import getFreshProxies

"""INITIAL WORK"""
asins = read_from_xlsx('ASINs.xlsx')['ASIN/ISBN']
useragent_list= open('user_agents.txt','r',encoding='utf-8').read().splitlines()
proxies_list = open('http_proxies.txt','r',encoding='utf-8').read().splitlines()

items = [['span',{'id':'productTitle'}],['span',{'class':'a-icon-alt'}],['a',{'data-hook':'review-title'}]]
names = ['Title','Rating','Top Review']
CHUNK_SIZE=100


def getNewProxy():
	proxy = random.choice(proxies_list)
	proxies={'http':f'http://{proxy}'}
	return proxies
def getNewHeaders():
	useragent = random.choice(useragent_list)
	HEADERS={'user-agent':useragent}	
	return HEADERS
def checkResponse(r):
	if "To discuss automated access to Amazon data please contact" in r.html.text or "Sorry, we just need to make sure you're not a robot" in r.html.text or r.status_code != 200:
		return False
	return True	
def getItems(soup):
	result={}
	for i,n in zip(items,names):
		item = soup.find(*i)
		if item is not None:
			result[n]=item.get_text(strip=True)
	return result		





"""SCRAPING"""
def Scrape(s_index):
	getFreshProxies()
	session = HTMLSession()
	count=0
	data=[]
	
	for asin in asins[s_index:s_index+CHUNK_SIZE]:
		noOfTries=0
		succesful=False
		URL = f'https://www.amazon.com/dp/{asin}'
		while not succesful:
			try:
				response = session.get(URL,headers=getNewHeaders(),proxies=getNewProxy())
				response.html.render(timeout=10)
			except Exception as e:
				print(e)
				continue
			if checkResponse(response):
				soup = BeautifulSoup(response.html.html,features='lxml')
				count+=1
				dat = getItems(soup)
				
				print(dat,count)
				data.append(dat)
				if count%10==0:
					df= pd.DataFrame(data)
					df.to_csv("result1.csv",index=False)						
				succesful = True
			else:
				print("BAD RESPONSE")
				noOfTries+=1
				if noOfTries==20:
					print("NEED NEW FUEL")
					time.sleep(random.randint(100,200))
					getFreshProxies()
					print("STARTING")
					proxies_list = open('http_proxies.txt','r',encoding='utf-8').read().splitlines()
					try:
						print("closing response")
						response.close()
						time.sleep(10)
						print('closing session')
						response.session.close()
						time.sleep(10)
					except Exception as e:	
						print("ERROR WHILE CLOSING SESSIONS AND RESPONSE \n\n",e)
					session = HTMLSession()
					noOfTries=0
	response.close()
	response.session.close()

Scrape(0)



