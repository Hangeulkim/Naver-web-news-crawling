# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 11:34:14 2020

@author: Hangeulkim
"""

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
startdate=""
filepath=""
year=""
month=""
day=""
con=sqlite3.connect("E:/data/data.db")
cur=con.cursor()

if __name__ == '__main__':
    