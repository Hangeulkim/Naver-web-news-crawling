from soynlp.noun import LRNounExtractor_v2
import re
from bs4 import BeautifulSoup
import requests
import collections 
import time
import datetime
import os
from multiprocessing import Queue,Pool


names = ["경제_금융","경제_증권","경제_산업-재계","경제_중기-벤처","경제_부동산","경제_글로벌-경제",
         "경제_생활경제","경제_경제-일반","정치_국방-외교","정치_행정"]


links = ["https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=101&sid2=259",
         "https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=101&sid2=258",
         "https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=101&sid2=261",
         "https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=101&sid2=771",
         "https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=101&sid2=260",
         "https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=101&sid2=262",
         "https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=101&sid2=310",
         "https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=101&sid2=263",
         "https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=100&sid2=267",
         "https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=100&sid2=266"]


startdate=""
filepath=""
year=""
month=""
day=""
con=sqlite3.connect("E:/data/data.db")
cur=con.cursor()
titlenum=0




##print(bsobject.prettify(formatter='html'))


'''
for link in links:
    where=link.find('sid2')
    print(link[where+5:where+7])
'''

'''
r=requests.get("https://news.naver.com/main/read.nhn?mode=LS2D&mid=shm&sid1=101&sid2=259&oid=008&aid=0004186498")
r.encoding='euc-kr'
html=r.text
bsobject=BeautifulSoup(html,"html.parser")
    
title=bsobject.find('meta',{'property' : "og:title"}).get('content')
filetitle=re.sub('…|·',' ',title,0)
filetitle=re.sub('\[|\]|\(|\)|\'|\"|\?',' ',filetitle,0,re.I|re.S)
filetitle=re.sub(' +',' ',filetitle,0)
filetitle=" "+filetitle
if filetitle[0]==" ":
    filetitle=filetitle[1:]

newscom=bsobject.find('meta',{'property' : "me2:category1"}).get('content')

whos=bsobject.find('div',{'id' : "articleBodyContents"}).text
who=whos.rfind("기자")
string=whos[who-4:who+2]
stringsub=re.sub('\/| |\n|\r','',string,0)

news=str(bsobject.find('div',{'id' : "articleBodyContents"}))
news=re.sub('//.*\}','',news,0,re.I|re.S)
news=news.replace(newscom,'')
news=news.replace(string,'')
news=re.sub('<br/>','\n',news,0,re.I|re.S)
news=re.sub('<.+?>|▶.*|[a-zA-Z0-9+-_.]+@.*','',news,0,re.I|re.S)
news=re.sub('\r','\n',news,0,re.I|re.S)
news=re.sub('\(.+?\)|\[*\]|/|\[|\]|\=|◇|△|\(|','',news,0,re.I|re.S)
news=re.sub(' +|\t',' ',news,0,re.I|re.S)


print(filetitle)

'''
##text=bsobject.find('div',{'class' : 'art_txt'}).text
##title=str(bsobject.find('title').text)
##title=re.sub('\[.+?\]|Mk.*-|\(.+?\)|\'|\"','',title,0,re.I|re.S)
##title=re.sub('\r|\n',' ',title,0,re.I|re.S)
##text=bsobject.find('div',{'class' : 'art_txt'}).text
##text=re.sub('\[.+?\]|ⓒ.*|◆|google.*;|<.*>|window.*|Copy.*', '', text, 0, re.I|re.S)
##text=re.sub('\r|\n',' ',text,0,re.I|re.S)
##text+=" "+title
##text=re.sub(' +'," ",text,0,re.I|re.S)
##
##noun_extractor = LRNounExtractor_v2(verbose=True, extract_compound=True)
##nouns = noun_extractor.train_extract(text.split(' '))
##li=[]
##for word, val in nouns.items():
##    print(val)
##    if(int(val[0]) < 3):
##        li+=[word]
##for word in li:
##    del nouns[word]
##odnouns=sorted(nouns.items(),key=lambda k: k[1][0], reverse=True)
##for word in odnouns:
##    print("%s : %d" %(word[0], word[1][0]))
'''
    num=0
    while True:#매일경제
        cnt=0
        r = requests.get('http://news.mk.co.kr/newsList.php?sc=30000016&page='+str(num))
        r.encoding='EUC-KR'
        html =r.text
        bsobject = BeautifulSoup(html, "html.parser")

        for title in bsobject.find_all('dd', {'class' : "desc"}):
            checktimetext=title.find('span',{'class' : "date"}).text
            
            checktime=datetime.datetime.strptime(checktimetext,"%Y.%m.%d %H:%M")
            if(checktime<endtime):
                continue
            else:
                cnt+=1
                link = title.select('a')[0].get('href')
            pages.append(link)
        if(cnt==0):
            break
        num+=1
        

    num=0
    while True:#중앙일보 산업
        cnt=0
        r = requests.get('https://news.joins.com/money/indusrty/list/'+str(num))
        r.encoding = 'utf-8'
        html = r.text
        bsobject = BeautifulSoup(html, "html.parser")

        for title in bsobject.find_all('span', {'class' : "thumb"}):
            checktimetext=title.find(
    '''
    