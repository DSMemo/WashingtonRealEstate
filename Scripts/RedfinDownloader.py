import pandas as pd
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from time import sleep
from random import randint
import os

def get_url(url):
	# Need to provide user agent or Redfin is unhappy
	headers = {
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
	}

	try:
		with closing(get(url, stream=True, headers=headers)) as resp:
			return resp.content
	except RequestException:
		return None


def get_zip_list():
	# Grabs the zip codes from the csv and turn them into a list
	zip_codes = pd.read_csv(os.getcwd()+'/DATA/zip.csv', usecols=['Zip Code'], skiprows=[732])
	zip_codes = zip_codes.ix[:, 0].tolist()
	return zip_codes


def dlink_scraper(zip_code):
	try:
		raw_html = get_url('https://www.redfin.com/zipcode/' + zip_code)
		html = BeautifulSoup(raw_html, 'html.parser')
		download_link = html.find('a', attrs={'class': 'downloadLink'})
		download_link = 'https://www.redfin.com/' + download_link.get('href')
		return download_link
	except:
		print('Couldn\'t get a download link for some reason!')
		return None


def downloader():
	zip_codes = get_zip_list()
	headers = {
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
	}
	for i in range(0, len(zip_codes)):
		try:
			url = dlink_scraper(str(zip_codes[i]))
			r = get(url, headers=headers)

			# This puts all the csvs into one file. It creates the file for the first loop and then appends
			# The header row is 383 characters long so I trim that when appending.
			if i == 0:
				with open(os.getcwd()+'/DATA/RedfinRealEstateData.csv', 'wb') as f:
					f.write(r.content)
			else:
				with open(os.getcwd()+'/DATA/RedfinRealEstateData.csv', 'ab') as f:
					f.write(r.content[383:])

			# Sleeps to not be mean to Redfin, sleeps a long time because extra nice, random so it doesn't seem like a robot
			sleep(randint(45, 75))
		except:
			print("This is Python at its finest. Everything in a try/except block." )


downloader()
