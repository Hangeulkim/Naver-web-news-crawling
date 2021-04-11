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
con=sqlite3.connect("E:/data/data.db")
cur=con.cursor()
titlenum=0


def get_links(title):
    print("start get_links"+'\n'+startdate+'\n'+names[titlenum])
    
    pages = set()
    links_get = set()

    if os.path.exists(filepath+"/complitment.txt"):
        f_read=open(filepath+"/complitment.txt","r")
   

    pagenum=1
    
    while True:
        pages.add(title+"&date="+startdate+"&page="+str(pagenum))
        r=requests.get(title+"&date="+startdate+"&page="+str(pagenum))
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
        r=requests.get(page)
        r.encoding='euc-kr'
        html=r.text
        bsobject=BeautifulSoup(html,"lxml")
        for link in bsobject.find('div',{'class' : "list_body newsflash_body"}).find_all('a'):
            links_get.add(link.get('href'))

    f_plus=open(filepath+"/complitment.txt","a")
    f_read=open(filepath+"/complitment.txt","r")
    delete_list=[]
    already_list=f_read.readlines()

    for link in links_get:
        if link+'\n' not in already_list:
            f_plus.write(link+"\n")
        else:
            delete_list+=[link]
            
    
    for del_mem in delete_list:
        links_get.remove(del_mem)

    f_read.close()
    f_plus.close()
    print("get_links end\n\n")
    return links_get


def get_content(link_get):
##    print("start get_content")
    

    r=requests.get(link_get)
    r.encoding='EUC-KR'
    html=r.text
    bsobject=BeautifulSoup(html,"lxml")

    if bsobject.find('meta',{'property':"og:url"}) == None:
        return None
    if "http://news.naver.com/" not in str(bsobject.find('meta',{'property':"og:url"}).get('content')):
        return None
    if bsobject.find('h1',{'class' : "error_title"}) != None:
        return None

    text=get_text(bsobject,link_get)
    text[0] = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》’“”]', ' ', text[0])
    text[0]=re.sub('\r|\n|\'|\"',' ',text[0],0,re.I|re.S)
    text[0]=re.sub(' +'," ",text[0],0,re.I|re.S)

    time.sleep(3)

##    print("end get_content")
##    return text
    if text != None:
        save_text(text)


def get_text(bsobject,link):
    #print("start get_text")

    try:
        title=bsobject.find('meta',{'property' : "og:title"}).get('content')
        filetitle=re.sub('…|·|\\x1e',' ',title,0)
        filetitle=filetitle.replace('\\','')
        filetitle = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》’“”·]', ' ', filetitle,0,re.I|re.S)
        filetitle=re.sub('단독|Hot Line|fnRASSI|e공시|ET투자뉴스|I 리포트','',filetitle)
        filetitle=re.sub('\n|\t',' ',filetitle,0)
        filetitle=re.sub(' +',' ',filetitle,0)
        filetitle=re.sub('/','-',filetitle,0)
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
        news=news.replace(newscom,'')
        news=news.replace(string,'')
        news=re.sub('<br/>','\n',news,0,re.I|re.S)
        news=re.sub('<.+?>|▶.*|[a-zA-Z0-9+-_.]+@.*|\"|\'|◆|\a0|■|-|▲|©.*','',news,0,re.I|re.S)
        news=re.sub('\r','\n',news,0,re.I|re.S)
        news=re.sub('\(.+?\)|\[*\]|/|\[|\]|\=|◇|△|\(|;','',news,0,re.I|re.S)
        news=re.sub(' +|\t',' ',news,0,re.I|re.S)

        get_time=bsobject.find('span',{'class' : "t11"}).text


        f=(filetitle+news+'\n\n\n'+newscom+'\n\n'+stringsub+'\n\n'+link+'\n\n'+get_time)


        #print("end get_text")
        return [filetitle+" "+news,[filetitle,f]]

    except http_incompleteRead:
        raise http_incompleteRead

    except urllib3_incompleteRead:
        raise urllib3_incompleteRead
    
    except Exception:
        return [link,[str(traceback.format_exc().strip())+'\n'+link,link]]




def save_text(text):
    f=open(filepath+"/"+text[0]+".txt","w",encoding='UTF-8')
    f.write(text[1])
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
    delli=[]
    for word, val in alldata.items():
        if(int(val)<30):
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
    start_time=datetime.datetime.strptime(input("시작 날짜 (년월일)\nex:)20190311 : "),"%Y%m%d")
    end_time=datetime.datetime.strptime(input("종료 날짜 (년월일)\nex:)20190315 : "),"%Y%m%d")


    if(start_time > end_time):#시작날짜가 작도록만듬 start~end로 조
        start_time, end_time = end_time, start_time

        
    #cur.execute("CREATE TABLE IF NOT Exists data(Word text, Frequency integer, Date date, Year text, Month text, Day text, Area text);")

    if os.path.isfile("E:/data/error.txt"):
        os.remove("E:/data/error.txt")

    while True:
        titlenum=0
        startdate=start_time.strftime('%Y%m%d')
        year=startdate[:4]
        month=startdate[4:6]
        day=startdate[6:8]

        for titles in links:
            time_flag=False
            filepath="E:/data/"+year+"/"+month+"/"+day+"/"+names[titlenum]

            if not(os.path.isdir(filepath)):
                os.makedirs(filepath)

            
            try:
                linkslist=get_links(titles)
##                pool.map(get_content,linkslist)
##                alltext=[]
##                alltext+=pool.map(get_content,linkslist)
##                alldata=Counter()
##
##            
##                for text in alltext:
##                    if text == None:
##                        continue
##                    save_text(text[1])
##                    alldata+=get_data(text[0])

            except requests.exceptions.ConnectionError:
                time.sleep(600)
                os.remove(filepath+"/complitment.txt")
                titlenum-=1
                continue


            except http_incompleteRead:
                time.sleep(600)
                os.remove(filepath+"/complitment.txt")
                titlenum-=1
                continue

            except urllib3_incompleteRead:
                time.sleep(600)
                os.remove(filepath+"/complitment.txt")
                titlenum-=1
                continue
                
            except Exception as e:
                print(type(e))
                print(e.args)
                print(e)

                traceback.print_exc()
                
                print('\n\n\n\n'+names[titlenum]+'\n\n\n\n')
                os.remove(filepath+"/complitment.txt")

                
                f=open("E:/data/error.txt",'a')
                f.write(str(traceback.format_exc()))
                f.write("\n\n\n"+startdate+"\n\n\n"+names[titlenum]+"\n\n\n\n\n")
                f.close()
                titlenum+=1
                continue
            


##            save_sql(dict(alldata))
##
##            con.commit()
            titlenum+=1


        start_time+=datetime.timedelta(days=1)
        if(start_time>end_time):
            break
                
##    chg_to_txt()
##    cur.close()
##    con.close()
    print("--- %s seconds ---" %(time.time() - starttime))
    

