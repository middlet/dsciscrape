#!/usr/bin/env python

import codecs
import BeautifulSoup as bs
import requests

def all_scrape(site, search):
	for i in range(0,100,10):
		url = '%s%s&start=%d' % (site, search, i)
		scrape(site, url)

def scrape(site, url):
	"""
	get all the urls on the page
	"""
	count = 0
	r = requests.get(url)
	soup = bs.BeautifulSoup(r.text)
	for link in soup.body.findAll(target='_blank'):
		l = link.get('href')
		if l.find('/rc/clk?')>=0:
			print site+l
			r = requests.get(str(site+l))
			f = codecs.open('./out/%05d.html'%count, 'w', 'utf8')
			f.write(r.text)
			f.close()
			count += 1


if __name__ == '__main__':
	all_scrape('http://www.indeed.co.uk/', 'jobs?q=Data+Scientist')
