## Made By Hangeulkim

import sqlite3
import os
import datetime
from dateutil import relativedelta

con=sqlite3.connect("C:/data/data.db")
cur=con.cursor()

filepath=""
start_time=""
end_time=""
year=""
month=""
day=""

names = ["경제_금융","경제_증권","경제_산업-재계","경제_중기-벤처","경제_부동산","경제_글로벌-경제",
         "경제_생활경제","경제_경제-일반","정치_국방-외교","정치_행정"]

def chg_to_txt():
    filepath="C:/data/"
    f2=open(filepath+"word_list.txt","w",encoding='UTF-8')
    cur.execute("select Word, SUM(Frequency) FROM data group by Word Order by SUM(Frequency) DESC")
    rows=cur.fetchall()

    cur.execute("select Word FROM data group by Word Order by Word")
    rows=cur.fetchall()
    for row in rows:
        f2.write(row[0]+'\n')

        
    cur.execute("select year from data group by year order by Year")
    years=cur.fetchall()
    for year in years:
        cur.execute("select Month from data where year=? group by Month order by Month",year)
        months=cur.fetchall()
        
        for month in months:
            cur.execute("select day from data where year=(?) and month=(?) group by day order by day",(year[0],month[0]))
            days=cur.fetchall()
            
            for day in days:
                
                filepath="C:/data/"+str(year[0])+"/"+str(month[0])+"/"+str(day[0])
                f=open(filepath+"/data_dic.txt","w",encoding='UTF-8')
                cur.execute("select Word, SUM(Frequency) FROM data where year=(?) and month=(?) and day=(?) group by Word Order by SUM(Frequency) DESC",(year[0],month[0],day[0]))
                rows=cur.fetchall()
                f.write(str(year[0])+str(month[0])+str(day[0])+'\n\n')
                for row in rows:
                    f.write(row[0]+"  :  "+str(row[1])+"\n")

            filepath="C:/data/"+str(year[0])+"/"+str(month[0])
            f=open(filepath+"/data_dic.txt","w",encoding='UTF-8')
            cur.execute("select Word, SUM(Frequency) FROM data where year=(?) and month=(?) group by Word Order by SUM(Frequency) DESC",(year[0],month[0]))
            rows=cur.fetchall()
            f.write(str(year[0])+str(month[0])+'\n\n')
            for row in rows:
                f.write(row[0]+"  :  "+str(row[1])+"\n")

        filepath="C:/data/"+str(year[0])
        f=open(filepath+"/data_dic.txt","w",encoding='UTF-8')
        cur.execute("select Word, SUM(Frequency) FROM data where year=(?) group by Word Order by SUM(Frequency) DESC",(year))
        rows=cur.fetchall()
        f.write(str(year[0])+'\n\n')
        for row in rows:
            f.write(row[0]+"  :  "+str(row[1])+"\n")


def save_all():
    ye_flag=0
    me_flag=0

    
    ##year
    tmp_start_year=datetime.datetime.strptime(start_time.strftime("%Y")+"0101","%Y%m%d")
    tmp_end_year=datetime.datetime.strptime(tmp_start_year.strftime("%Y")+"1231","%Y%m%d")

    f=open(real_filepath+"/Year.txt","w",encoding="UTF-8")
    while True:
        
        if tmp_start_year < start_time:
            start_year=start_time
        elif tmp_start_year > end_time:
            break
        else:
            start_year=tmp_start_year


        if tmp_end_year > end_time:
            end_year=end_time
            ye_flag=1
        else:
            end_year=tmp_end_year


        cur.execute("select Word, SUM(Frequency) From data where date>=(?) and date<=(?) group by Word Order by Sum(Frequency) Desc",(int(start_year.strftime("%Y%m%d")),int(end_year.strftime("%Y%m%d"))))
        rows=cur.fetchall()
        f.write(start_year.strftime("%Y")+"\n\n")
        for row in rows:
            f.write(row[0]+"  :  "+str(row[1])+"\n")
        f.write("\n\n\n\n\n\n\n\n")
        
        if ye_flag>0:
            break

        
        tmp_start_year+=relativedelta.relativedelta(years=1)
        tmp_end_year+=relativedelta.relativedelta(years=1)
        
    f.close()

    
    ##month
    tmp_start_month=datetime.datetime.strptime(start_time.strftime("%Y%m")+"01","%Y%m%d")
    tmp_end_month=tmp_start_month+relativedelta.relativedelta(months=1)-datetime.timedelta(days=1)

    f=open(real_filepath+"/Month.txt","w",encoding="UTF-8")
    while True:
        
        if tmp_start_month < start_time:
            start_month=start_time
        elif tmp_start_month > end_time:
            break
        else:
            start_month=tmp_start_month


        if tmp_end_month > end_time:
            end_month=end_time
            me_flag=1
        else:
            end_month=tmp_end_month


        cur.execute("select Word, SUM(Frequency) From data where date>=(?) and date<=(?) group by Word Order by Sum(Frequency) Desc",(int(start_month.strftime("%Y%m%d")),int(end_month.strftime("%Y%m%d"))))
        rows=cur.fetchall()
        f.write(start_month.strftime("%Y%m")+"\n\n")
        for row in rows:
            f.write(row[0]+"  :  "+str(row[1])+"\n")
        f.write("\n\n\n\n\n\n\n\n")
        
        if me_flag>0:
            break

        
        tmp_start_month+=relativedelta.relativedelta(months=1)
        tmp_end_month+=relativedelta.relativedelta(months=1)
        
    f.close()

    
    ##day
    tmp_day=start_time

    f=open(real_filepath+"/Day.txt","w",encoding="UTF-8")
    while True:

        if tmp_day > end_time:
            break


        cur.execute("select Word, SUM(Frequency) From data where date>=(?) and date<=(?) group by Word Order by Sum(Frequency) Desc",(int(tmp_day.strftime("%Y%m%d")),int(tmp_day.strftime("%Y%m%d"))))
        rows=cur.fetchall()
        f.write(tmp_day.strftime("%Y%m%d")+"\n\n")
        for row in rows:
            f.write(row[0]+"  :  "+str(row[1])+"\n")
        f.write("\n\n\n\n\n\n\n\n")
        
    
        tmp_day+=datetime.timedelta(days=1)
        
    f.close()



def save_some(title):
    ye_flag=0
    me_flag=0

    
    ##year
    tmp_start_year=datetime.datetime.strptime(start_time.strftime("%Y")+"0101","%Y%m%d")
    tmp_end_year=datetime.datetime.strptime(tmp_start_year.strftime("%Y")+"1231","%Y%m%d")

    tmp_filepath=real_filepath+"/"+title
    
    try:
        if not(os.path.isdir(tmp_filepath)):
            os.makedirs(tmp_filepath)
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory!!!!!")
            raise
    
    f=open(tmp_filepath+"/Year.txt","w",encoding="UTF-8")
    while True:
        
        if tmp_start_year < start_time:
            start_year=start_time
        elif tmp_start_year > end_time:
            break
        else:
            start_year=tmp_start_year


        if tmp_end_year > end_time:
            end_year=end_time
            ye_flag=1
        else:
            end_year=tmp_end_year


        cur.execute("select Word, SUM(Frequency) From data where date>=(?) and date<=(?) and Area=(?) group by Word Order by Sum(Frequency) Desc",(int(start_year.strftime("%Y%m%d")),int(end_year.strftime("%Y%m%d")),title))
        rows=cur.fetchall()
        f.write(start_year.strftime("%Y")+"\n\n")
        for row in rows:
            f.write(row[0]+"  :  "+str(row[1])+"\n")
        f.write("\n\n\n\n\n\n\n\n")
        
        if ye_flag>0:
            break

        
        tmp_start_year+=relativedelta.relativedelta(years=1)
        tmp_end_year+=relativedelta.relativedelta(years=1)
        
    f.close()

    
    ##month
    tmp_start_month=datetime.datetime.strptime(start_time.strftime("%Y%m")+"01","%Y%m%d")
    tmp_end_month=tmp_start_month+relativedelta.relativedelta(months=1)-datetime.timedelta(days=1)

    f=open(tmp_filepath+"/Month.txt","w",encoding="UTF-8")
    while True:
        
        if tmp_start_month < start_time:
            start_month=start_time
        elif tmp_start_month > end_time:
            break
        else:
            start_month=tmp_start_month


        if tmp_end_month > end_time:
            end_month=end_time
            me_flag=1
        else:
            end_month=tmp_end_month


        cur.execute("select Word, SUM(Frequency) From data where date>=(?) and date<=(?) and Area=(?) group by Word Order by Sum(Frequency) Desc",(int(start_month.strftime("%Y%m%d")),int(end_month.strftime("%Y%m%d")),title))
        rows=cur.fetchall()
        f.write(start_month.strftime("%Y%m")+"\n\n")
        for row in rows:
            f.write(row[0]+"  :  "+str(row[1])+"\n")
        f.write("\n\n\n\n\n\n\n\n")
        
        if me_flag>0:
            break

        
        tmp_start_month+=relativedelta.relativedelta(months=1)
        tmp_end_month+=relativedelta.relativedelta(months=1)
        
    f.close()

    
    ##day
    tmp_day=start_time

    f=open(tmp_filepath+"/Day.txt","w",encoding="UTF-8")
    while True:

        if tmp_day > end_time:
            break


        cur.execute("select Word, SUM(Frequency) From data where date>=(?) and date<=(?) and Area=(?) group by Word Order by Sum(Frequency) Desc",(int(tmp_day.strftime("%Y%m%d")),int(tmp_day.strftime("%Y%m%d")),title))
        rows=cur.fetchall()
        f.write(tmp_day.strftime("%Y%m%d")+"\n\n")
        for row in rows:
            f.write(row[0]+"  :  "+str(row[1])+"\n")
        f.write("\n\n\n\n\n\n\n\n")
        
    
        tmp_day+=datetime.timedelta(days=1)
        
    f.close()



if __name__=='__main__':
    chg_to_txt()

    filepath="C:/data/추출"
    try:
        if not(os.path.isdir(filepath)):
            os.makedirs(filepath)
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory!!!!!")
            raise

    start_time=datetime.datetime.strptime(input("시작 날짜 (년월일)\nex:)20190311 : "),"%Y%m%d")
    end_time=datetime.datetime.strptime(input("종료 날짜 (년월일)\nex:)20190315 : "),"%Y%m%d")


    if(start_time > end_time):#시작날짜가 작도록만듬 start~end로 조
        start_time, end_time = end_time, start_time

    real_filepath=filepath+"/"+start_time.strftime('%Y%m%d')+"_"+end_time.strftime('%Y%m%d')
    try:
        if not(os.path.isdir(real_filepath)):
            os.makedirs(real_filepath)
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory!!!!!")
            raise


    while True:
        titlenum=int(input("0 : 전체\n1 : 경제_금융\n2 : 경제_증권\n3 : 경제_산업-재계\n4 : 경제_증기-벤처\n5 : 경제_부동산\n6 : 경제_글로벌-경제\n7 : 경제_생활경제\n8 : 경제_경제-일반\n9 : 정치_국방-외교\n10 : 정치_행정\n11 : 종료\n12 : 날짜 변경\n메뉴 선택 : "))
        print("\n\n\n")
        if(titlenum==11):
            break
        elif(titlenum==0):
            save_all()
        elif(titlenum==12):
            start_time=datetime.datetime.strptime(input("시작 날짜 (년월일)\nex:)20190311 : "),"%Y%m%d")
            end_time=datetime.datetime.strptime(input("종료 날짜 (년월일)\nex:)20190315 : "),"%Y%m%d")


            if(start_time > end_time):#시작날짜가 작도록만듬 start~end로 조
                start_time, end_time = end_time, start_time


            real_filepath=filepath+"/"+start_time.strftime('%Y%m%d')+"_"+end_time.strftime('%Y%m%d')


            try:
                if not(os.path.isdir(real_filepath)):
                    os.makedirs(real_filepath)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    print("Failed to create directory!!!!!")
                    raise
        else:
            save_some(names[titlenum-1])

            
    cur.close()
    con.close()
    
