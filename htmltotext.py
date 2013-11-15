#!/usr/bin/env python

"""
recurse the html directory and extract the parts of the job of interest
"""

import os
import sys

import BeautifulSoup

def process(fname):
    """
    return a string with all the useless html removed
    """
    # get data
    f = open(fname)
    text = f.read()
    f.close()
    # parse replacing entities
    soup = BeautifulSoup.BeautifulSoup(text, convertEntities=BeautifulSoup.BeautifulStoneSoup.HTML_ENTITIES)

    otext = ''
    if soup.find(id='vacancyMain'):
        ad = soup.find(id='vacancyMain')
        for si in ad.findAll('div', {'class':'infoBox1'}):
            si.extract()
        for si in ad.findAll(id='vacPlacedBy'):
            si.extract()
        for si in ad.findAll('a'):
            si.extract()
        otext = ad.text
    else:
        ad = soup.find(id='lineage-container')
        comment = u' market_dscrpn OR job_dscrpn comes here '
        try:
            for ai in ad.findAll('p'):
                # remove all comments
                comments = ai.findAll(text=lambda text:isinstance(text, BeautifulSoup.Comment))
                for ci in comments:
                    ci.extract()
                # remove <br />
                for item in ai.contents:
                    if str(item)!='<br />':
                        otext += str(item)+"\n"
        except:
            print 'error :', fname
    #
    return otext.strip()



def save_text(text, fname):
    """
    save the results of the conversion to a text file
    """
    if len(text)==0:
        return

    if not os.path.isdir('./text'):
        os.mkdir('./text')

    ofname = './text/%s' % fname[:-5]

    # dont overwrite if the file exists
    if os.path.isfile(ofname):
        return

    f = open(ofname, 'w')
    f.write(text)
    f.close()



def convert(dname):
    """
    convert an html file used by jobsite to a text description of the job
    """
    for fi in os.listdir(dname):
        print fi
        fname = '%s/%s' % (dname, fi)
        text = process(fname)
        save_text(text, fi)



if __name__ == '__main__':
    convert('./html')

