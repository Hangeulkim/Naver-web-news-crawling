from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
from io import open
from urllib.request import urlopen
import os
import logging
import re

# 다음 코드는 라이브러리에서 PDF 파일을 읽을 시 사용하는 전형적인 코드 형태이므로, 필요할 때 활용하면 됨
def read_pdf_file(pdfFile):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)

    process_pdf(rsrcmgr, device, pdfFile)
    device.close()

    content = retstr.getvalue()
    retstr.close()
    return content



path_dir="C:/data/pdfs"
txt_dir="C:/data/변환"
if __name__=='__main__':
    try:
        if not(os.path.isdir(path_dir)):
            os.makedirs(path_dir)
        if not(os.path.isdir(txt_dir)):
            os.makedirs(txt_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory!!!!!")
            raise

    file_list=os.listdir(path_dir)
    file_list.sort()

    logging.propagate = False 
    logging.getLogger().setLevel(logging.ERROR)
    
    for item in file_list:
        print(item)
        # pdf_file = urlopen("http://pythonscraping.com/pages/warandpeace/chapter1.pdf")  # 웹에 있는 pdf 파일을 읽을 수 있음
        pdf_file = open(path_dir+"/"+str(item), "rb")                                       # 로컬 PC에 있는 pdf 파일도 읽을 수 있음
        contents = read_pdf_file(pdf_file)
        contents = re.sub("",'',contents)
        f=open(txt_dir+"/"+item+".txt","w",encoding="utf-8")
        f.write(contents)
        pdf_file.close()
        f.close()
        
