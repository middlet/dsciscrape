#!/usr/bin/env python

import codecs
import xml.etree.ElementTree as ET
import requests
import sqlite3
import os.path

from datetime import datetime

def create_new_db(dbname):
    """
    create a database if required
    """
    if os.path.isfile(dbname):
        return
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute('''create table jobs (id integer primary key, pub_date timestamp, title string, link string, unique(pub_date, title, link))''')
    conn.close()

def download_ad(link, pubdate):
    """
    get the job ad from the link
    """
    r = requests.get(link)
    if r.status_code!=200:
        print 'cannot download'
        return
    html = r.text

    if not os.path.isdir('./html'):
        os.mkdir('./html')

    fname = './html/%s' % pubdate.strftime('%Y%m%d%H%M%S.html')
    if os.path.isfile(fname):
        print 'file exists :', fname
        return

    f = codecs.open(fname, 'w', 'utf8')
    f.write(html)
    f.close()




def find_new_jobs(dbname):
    """
    grab the rss feed and see if there are any new jobs in there
    """
    create_new_db(dbname)
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    url = "http://www.jobsite.co.uk/cgi-bin/advsearch?rss_feed=1&skill_include=&quot;data%20scientist&quot;&job_title_include=%22data%20scientist%22&daysback=50&scc=UK"
    r = requests.get(url)
    rss = r.text
    root = ET.fromstring(rss)
    for ei in root.findall('./channel/item'):
        title = ei.find('title').text
        link = ei.find('link').text
        pubdate = datetime.strptime(ei.find('pubDate').text, '%a, %d %b %Y %H:%M:%S %Z')
        c.execute("insert or ignore into jobs values(NULL, ?, ?, ?)", (pubdate, title, link))
        download_ad(link, pubdate)
    conn.commit()
    conn.close()






if __name__ == '__main__':
    find_new_jobs('./jobs.sq3')

