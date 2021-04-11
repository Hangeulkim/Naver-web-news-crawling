import sqlite3
import os

filepath="E:\data"
conn=sqlite3.connect("E:/data/data.db")
cur=conn.cursor()


if __name__=='__main__':
    cur.execute("CREATE TABLE IF NOT Exists data(Year text, Month text, Day text, Area text, Title text, Contents text);")
    years=os.listdir(filepath)
    for year in years:
        print(year)
        year_dir=filepath+"\\"+year
        months=os.listdir(year_dir)
        for month in months:
            print(month)
            month_dir=year_dir+"\\"+month
            days=os.listdir(month_dir)
            for day in days:
                print(day)
                day_dir=month_dir+"\\"+day
                areas=os.listdir(day_dir)
                for area in areas:
                    
                    area_dir=day_dir+"\\"+area
                    titles=os.listdir(area_dir)
                    for title in titles:
                        fpath=area_dir+"\\"+title
                        f=open(fpath,"r",encoding='UTF8',errors='ignore')

                        cur.execute("INSERT INTO DATA VALUES(?,?,?,?,?,?)",(year,month,day,area,title,f.read()))
                        
                        f.close()
                        os.remove(fpath)
                    os.rmdir(area_dir)
                os.rmdir(day_dir)
            os.rmdir(month_dir)
            conn.commit()
        os.rmdir(year_dir)
       
                
    #chg_to_txt()
    conn.close()
    
