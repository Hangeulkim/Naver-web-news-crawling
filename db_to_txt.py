## Made By Hangeulkim

import sqlite3
import requests
from bs4 import BeautifulSoup
import re
import datetime
import time
import os
from soynlp.noun import LRNounExtractor_v2
from multiprocessing import Pool,cpu_count,Queue
from collections import Counter
import traceback

year=""
month=""
day=""
con=sqlite3.connect("E:/data/data.db")
cur=con.cursor()
titlenum=0

def save_text(filepath, content):
    
    f=open(filepath+"/complitment.txt","w",encoding='UTF-8')
    f.write(content)
    f.close()
    
    
    
if __name__=='__main__':
    cur.execute("select * from data where title = 'complitment.txt'")
    for row in cur:
        filepath="E:\\data\\"+row[0]+"\\"+row[1]+"\\"+row[2]+"\\"+row[3]
        try:
            if not(os.path.isdir(filepath)):
                os.makedirs(filepath)
        except OSError as e:
            if e.errno != errno.EEXIST:
                print("Failed to create directory!!!!!")
                raise
        save_text(filepath,row[5])
    cur.execute("delete from data where title = 'complitment.txt'")
    con.commit()
                
    cur.close()
    con.close()
    

