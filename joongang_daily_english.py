## Made By Hangeulkim

import sqlite3
import requests
from bs4 import BeautifulSoup
import re
import datetime
import time
import os
from multiprocessing import Pool,cpu_count,Queue
from collections import Counter
import traceback
from http.client import IncompleteRead as http_incompleteRead
from urllib3.exceptions import IncompleteRead as urllib3_incompleteRead


names = ["National_Politics","National_social_affairs","National_education","National_People",
         "Business_Econnomy","Business_Finanace","Business_Industry",
         "Business_Stock_Market"]


links = ["http://koreajoongangdaily.joins.com/news/list/List.aspx?gCat=030101",
         "http://koreajoongangdaily.joins.com/news/list/List.aspx?gCat=030201",
         "http://koreajoongangdaily.joins.com/news/list/List.aspx?gCat=030301",
         "http://koreajoongangdaily.joins.com/news/list/List.aspx?gCat=030401",
         "http://koreajoongangdaily.joins.com/news/list/List.aspx?gCat=050101",
         "http://koreajoongangdaily.joins.com/news/list/List.aspx?gCat=050201",
         "http://koreajoongangdaily.joins.com/news/list/List.aspx?gCat=050301",
         "http://koreajoongangdaily.joins.com/news/list/List.aspx?gCat=050401"]


filepath=""
year=""
month=""
day=""
con=sqlite3.connect("C:/Keyword_data/data.db")
cur=con.cursor()
titlenum=0


def get_links(title):
    if os.path.exists(filepath+"/complitment_getpages.txt"):
        return set()
   
    pages = set()
    links_get = set()

    int page=1
   

    r=requests.get(title+"&pgi="+str(page))
    r.encoding="UTF-8"
    html=r.text
    bsobject=BeautifulSoup(html,"lxml")


    numbers = bsobject.find('div',{"id":"paginate"}).find_all('a',{"class":"pg"})
    int max=0;
    for number in numbers:
        if(int(number.get_text()) > max):
            max = int(number.get_text())

    
    f_plus=open(filepath+"/complitment_getpages.txt","a")
    f_read=open(filepath+"/complitment_getpages.txt","r")
    delete_list=[]
    already_list=f_read.readlines()


    for page in range(1,max):
        r=requests.get(title+"&pgi="+str(page))
        r.encoding="UTF-8"
        html=r.text
        bsobject=BeautifulSoup(html,"lxml")

        
        
        


    f_read.close()
    f_plus.close()
    print("get_links end\n\n")
    return links_get


def get_content(link_get):
    #print("start get_content")
    
    text_get=""

    r=requests.get(link_get)
    r.encoding='UTF-8'
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

    #print("end get_content")
    return text


def get_text(bsobject,link):
    #print("start get_text")

    try:
        title=bsobject.find('meta',{'property' : "og:title"}).get('content')
        filetitle=re.sub('…|·|\\x1e',' ',title,0)
        filetitle=filetitle.replace('\\','')
        filetitle = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》’“”·]', ' ', filetitle,0,re.I|re.S)
        filetitle=re.sub('\n|\t',' ',filetitle,0)
        filetitle=re.sub(' +',' ',filetitle,0)
        filetitle=re.sub('/','-',filetitle,0)
        if len(filetitle)==0:
            tmp_time=datetime.datetime.strptime(bsobject.find('span',{'class' : "date"}).text,"%b %d,%Y")
            filetitle=tmp_time.strftime("%b %d,%Y")
        filetitle=filetitle.strip()
        

        news=str(bsobject.find('div',{'id' : "articleBody"}))
        news=re.sub('//.*\}','',news,0,re.I|re.S)
        news=news.replace(newscom,'')
        news=news.replace(string,'')
        news=re.sub('<br/>','\n',news,0,re.I|re.S)
        news=re.sub('<.+?>|▶.*|[a-zA-Z0-9+-_.]+@.*|\"|\'|◆|\a0|■|-|▲|©.*','',news,0,re.I|re.S)
        news=re.sub('\r','\n',news,0,re.I|re.S)
        news=re.sub('\(.+?\)|\[*\]|/|\[|\]|\=|◇|△|\(|;','',news,0,re.I|re.S)
        news=re.sub(' +|\t',' ',news,0,re.I|re.S)

        get_date=bsobject.find('span',{'class' : "date"}).text
        date=datetime.datetime.strptime(get_date, "%b %d,%Y")


        f=(filetitle+"\n\n"+news'\n\n'+link+'\n\n'+date)


        #print("end get_text")
        return [filetitle+" "+news,[filetitle,f]]

    except http_incompleteRead as e:
        raise http_incompleteRead

    except urllib3_incompleteRead as e:
        raise urllib3_incompleteRead
    
    except Exception as e:
        return [link,[str(traceback.format_exc().strip())+'\n'+link,link]]




def save_text(text):
    f=open(filepath+"/"+text[0]+".txt","w",encoding='UTF-8')
    f.write(text[1])
    f.close()


def get_data(text):
    

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
    pool = Pool(processes=cpu_count()*4)
    listkslist=set()

    print("이어서 데이터를 수집합니다.\n")

        
    cur.execute("CREATE TABLE IF NOT Exists data(Word text, Frequency integer, Date date, Year text, Month text, Day text, Area text);")

    if os.path.isfile("C:/Keyword_data/error.txt"):
        os.remove("C:/Keyword_data/error.txt")

    while True:
        titlenum=0
        startdate=start_time.strftime('%Y%m%d')
        year=startdate[:4]
        month=startdate[4:6]
        day=startdate[6:8]

        for titles in links:
            time_flag=False
            filepath="C:/Keyword_data/"+year+"/"+month+"/"+day+"/"+names[titlenum]

            try:
                if not(os.path.isdir(filepath)):
                    os.makedirs(filepath)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    print("Failed to create directory!!!!!")
                    raise

            
            try:
                linkslist=get_links(titles)


                alltext=[]
                alltext+=pool.map(get_content,linkslist)
                alldata=Counter()

            
                for text in alltext:
                    if text == None:
                        continue
                    save_text(text[1])
                    alldata+=get_data(text[0])

            except requests.exceptions.ConnectionError as e:
                time.sleep(600)
                os.remove(filepath+"/complitment.txt")
                titlenum-=1
                continue


            except http_incompleteRead as e:
                time.sleep(600)
                os.remove(filepath+"/complitment.txt")
                titlenum-=1
                continue

            except urllib3_incompleteRead as e:
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

                
                f=open("C:/Keyword_data/error.txt",'a')
                f.write(str(traceback.format_exc()))
                f.write("\n\n\n"+startdate+"\n\n\n"+names[titlenum]+"\n\n\n\n\n")
                f.close()
                titlenum+=1
                continue
            


            save_sql(dict(alldata))

            con.commit()
            titlenum+=1


                
    #chg_to_txt()
    cur.close()
    con.close()
    

