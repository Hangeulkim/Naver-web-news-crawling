## Made By Hangeulkim

import sqlite3
import requests
from bs4 import BeautifulSoup
import re
import datetime
import time
import os
from soynlp.noun import LRNounExtractor_v2
from multiprocessing import Pool,cpu_count
from collections import Counter
import traceback
from http.client import IncompleteRead as http_incompleteRead
from urllib3.exceptions import IncompleteRead as urllib3_incompleteRead


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
con=sqlite3.connect("data.db",isolation_level=None)
cur=con.cursor()
titlenum=0
headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36" }
err_dict=[]

def get_links(title):
    global filepath
    
    print("start get_links"+'\n'+startdate+'\n'+names[titlenum])
    
    pages = set()
    links_get = set()

    if not os.path.exists(filepath+"/save.txt"):
        f_read=open(filepath+"/save.txt","w")
        f_read.close()

    
    pagenum=1
    
    while True:
        pages.add(title+"&date="+startdate+"&page="+str(pagenum))
        r=requests.get(title+"&date="+startdate+"&page="+str(pagenum),headers=headers)
        r.encoding='euc-kr'
        html=r.text
        bsobject=BeautifulSoup(html,"lxml")
        
        pflag=0    
        for link in bsobject.find('div',{'class' : "paging"}).find_all('a',{'class' : "nclicks(fls.page)"}):
            pages.add("https://news.naver.com/main/list.nhn"+link.get('href'))
            for class_ in link.get('class'):
                if class_ == 'next':
                    pflag+=1
                    
        if(pflag==0):
            break
        else:
            pagenum+=10
   
    for page in pages:
        r=requests.get(page,headers=headers)
        r.encoding='euc-kr'
        html=r.text
        bsobject=BeautifulSoup(html,"lxml")
        for link in bsobject.find('div',{'class' : "list_body newsflash_body"}).find_all('a'):
            links_get.add(link.get('href'))

    f_read=open(filepath+"/save.txt","r")
    delete_list=[]
    already_list=f_read.readlines()

    for link in links_get:
        if link+'\n' in already_list:
            delete_list+=[link]
            
            
    
    for del_mem in delete_list:
        links_get.remove(del_mem)

    f_read.close()
    print("get_links end\n\n")
    return links_get

def re_run_error(where,title):
    print("start err_links"+'\n'+where)
    
    pages = set()
    links_get = set()

    f_read=open(where+"/error.txt","r")
    links_get=f_read.readlines()
    f_read.close()
    os.remove(where+"/error.txt","r")
    return links_get

    

def get_content(link_get):
##    print("start get_content")
    

    r=requests.get(link_get,headers=headers)
    r.encoding='EUC-KR'
    html=r.text
    bsobject=BeautifulSoup(html,"lxml")
    
    if bsobject.find('meta',{'property':"og:url"}) == None:
        print('url error')
        print(link_get)
        return None
    if "news.naver.com" not in str(bsobject.find('meta',{'property':"og:url"}).get('content')):
        print(str(bsobject.find('meta',{'property':"og:url"}).get('content')))
        print('content error')
        print(link_get)
        return None
    if bsobject.find('h1',{'class' : "error_title"}) != None:
        print('error title')
        print(link_get)
        return None

    text=get_text(bsobject,link_get)

    time.sleep(3)

##    print("end get_content")
    return text


def get_text(bsobject,link):
    global cur
    #print("start get_text")

    try:
        title=bsobject.find('meta',{'property' : "og:title"}).get('content')
        filetitle=re.sub('…|·|\\x1e',' ',title,0)
        filetitle=filetitle.replace('\\','')
        filetitle=re.sub('\<|\>|\(|\)|\[|\]','\n',filetitle,0,re.I|re.S)
        filetitle=re.sub('\r','\n',filetitle,0,re.I|re.S)
        filetitle=re.sub(' +|\t',' ',filetitle,0,re.I|re.S)
        filetitle=re.sub('[^A-Za-z0-9가-힣]| |\n', '', filetitle)
        filetitle=re.sub('단독|Hot Line|fnRASSI|e공시|ET투자뉴스|I 리포트','',filetitle)
        if len(filetitle)==0:
            tmp_time=datetime.datetime.strptime(bsobject.find('span',{'class' : "t11"}).text,"%Y-%m-%d %H:%M")
            filetitle=tmp_time.strftime("%Y-%m-%d %H-%M")
        filetitle=filetitle.strip()
        

        newscom=bsobject.find('meta',{'property' : "me2:category1"}).get('content')
    

        whos=str(bsobject.find('div',{'id' : "articleBodyContents"}))
        who=whos.rfind("기자")
        string=whos[who-4:who+2]
        stringsub=re.sub('\/| |\n|\r|\.|\>|\]','',string,0)

        news=str(bsobject.find('div',{'id' : "articleBodyContents"}))
        news=re.sub('//.*\}','',news,0,re.I|re.S)
        news=news.replace('<br/>','\n')
        news=news.replace(newscom,'')
        news=news.replace(string,'')
        news=re.sub('<.*>|\(.*\)|\[.*\]','\n',news,0,re.I|re.S)
        news=re.sub('\r','\n',news,0,re.I|re.S)
        news=re.sub(' +|\t',' ',news,0,re.I|re.S)
        news=re.sub('[^A-Za-z0-9가-힣]| |\n', '', news)
        
        

        get_time=bsobject.find('span',{'class' : "t11"}).text


        f=(filetitle+news+'\n\n\n'+newscom+'\n\n'+stringsub+'\n\n'+link+'\n\n'+get_time)


        #print("end get_text")
        cur.execute("INSERT INTO NEWS VALUES(?,?,?,?,?,?,?)",(filetitle,startdate,year,month,day,names[titlenum],news))
        return [filetitle+" "+news,[filetitle,f]]
    
    except Exception:
        raise Exception




def save_text(text):
    f=open(filepath+"/"+text[1][0]+".txt","w",encoding='UTF-8')
    f.write(text[1][1])
    f.close()


def get_data(text):
    delli=['등','것','위','대','뒤','오','통','또','수','말','더','못','새','인','있','점','올','많','때','측','기자','종목','수익률','https']
    noun_extractor = LRNounExtractor_v2(verbose=False)
    nouns = noun_extractor.train_extract(text.split(' '))
    nouns_data=Counter()

    for word in delli:
        if(word in nouns):
            del nouns[word]
        else:
            continue

    
    for word,data in nouns.items():
        nouns_data+=Counter({word:int(data[0])})

    return nouns_data
        

def save_sql(alldata):
    global cur
    delli=[]
    for word, val in alldata.items():
        if(int(val)<10):
            delli+=[word]


    for word in delli:
        del alldata[word]

            
    odnouns=sorted(alldata.items(),key=lambda k: k[1], reverse=True)
    year=str(startdate)[:4]
    month=str(startdate)[4:6]
    day=str(startdate)[6:8]
    
    for word in odnouns:
        cur.execute("INSERT INTO DATA VALUES(?,?,?,?,?,?,?)",(word[0],int(word[1]),startdate,year,month,day,names[titlenum]))

    
    
    
if __name__=='__main__':
    starttime=time.time()
    pool = Pool(processes=cpu_count()*2)
    listkslist=set()
    start_time=datetime.datetime.strptime("20120101","%Y%m%d")
    end_time=datetime.datetime.now()


    if(start_time > end_time):#시작날짜가 작도록만듬 start~end로 조
        start_time, end_time = end_time, start_time

        
    cur.execute("CREATE TABLE IF NOT Exists data(Word text, Frequency integer, Date date, Year text, Month text, Day text, Area text);")
    cur.execute("CREATE TABLE IF NOT Exists News(Title text, Date date, Year text, Month text, Day text, Area text,Cont text);")

    if os.path.isfile("error.txt"):
        os.remove("error.txt")

    while True:
        titlenum=0
        startdate=start_time.strftime('%Y%m%d')
        year=startdate[:4]
        month=startdate[4:6]
        day=startdate[6:8]

        

        for titles in range(len(links)):
            titlenum=titles
            con=sqlite3.connect("data.db",isolation_level=None)
            cur=con.cursor()
            time_flag=False
            filepath="data/"+year+"/"+month+"/"+day+"/"+names[titlenum]

            if not(os.path.isdir(filepath)):
                os.makedirs(filepath)

            
            try:
                linkslist=get_links(links[titles])
                pool.map(get_content,linkslist)
                alltext=[]
                alltext+=pool.map(get_content,linkslist)
                alldata=Counter()
                
                for text in alltext:
                    if text == None:
                        continue
                    save_text(text)
                    alldata+=get_data(text[0])
                    
                    f=open(filepath+"/save.txt","w")
                    
                for link in linkslist:
                    f.write(link+"\n")
                f.close()
                
                save_sql(dict(alldata))
                con.close()

                
            except Exception as e:
                print(e.args)
                print(e)

                traceback.print_exc()

                f=open("error.txt",'a')
                f.write(str(traceback.format_exc()))
                f.write("\n\n\n"+startdate+"\n\n\n"+names[titlenum]+"\n\n\n\n\n")
                f.close()
                titles-=1
                con.close()
                time.sleep(300)
                continue
            


        start_time+=datetime.timedelta(days=1)
        if(start_time>end_time):
            break
        
    
    print("--- %s seconds ---" %(time.time() - starttime))
    

