from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import csv


def get_url(url):
	try:
		with closing(get(url, stream=True)) as resp:
			return resp.content
	except RequestException:
		return None


def get_zip():
	outfile = open('zip.csv', 'w', newline='')
	writer = csv.writer(outfile)

	url = 'https://www.zipcodestogo.com/Washington/'
	raw_html = get_url(url)
	html = BeautifulSoup(raw_html, 'html.parser')
	table = html.find('table')

# The zip code site uses a nested table, if you search only the upper table you get the contents twice over
	inner_table = table.find('table')

	row_list = []

	for i in inner_table.findAll('tr'):

		# This if statement gets rid of the table title

		if i.has_attr('bgcolor'):
			None
		else:
			cell_list = []
			for cell in i.findAll('td'):
				text = cell.text
				cell_list.append(text)
			row_list.append(cell_list)

	for item in row_list:
		writer.writerow(item)


get_zip()