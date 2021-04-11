## Made By Hangeulkim

import sqlite3
import os
import openpyxl

if __name__=='__main__':
    
    filepath = "C:/data/db_to_exel"
    try:
        if not(os.path.isdir(filepath)):
            os.makedirs(filepath)
        except OSError as e:
            if e.errno != errno.EEXIST:
                 print("Failed to create directory!!!!!")
                raise

    file = filepath+"/data.db"
    wb = openpyxl.Workbook()

    con = sqlite3.connect(file)
    cur = con.cursor()
    
    
