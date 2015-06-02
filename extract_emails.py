'''
Start with seed
Fetch page
Extract all links and add to queue
Extract all emails and add to list the ones not previously found
Pop next link from queue and fetch page if not previously crawled
Extract links
Extract emails
'''
import urllib
import socket
from bs4 import BeautifulSoup
import re
from urlparse import urljoin, urlparse
from collections import deque
import argparse

socket.setdefaulttimeout(10)

def get_page(url):
	"""
	Download page and return its contents 
	"""
	try:
		#print "Requesting url [%s]" % url
		f = urllib.urlopen(url)
		page = f.read()
		f.close()
		return page
	except:
		return ""
	return ""

def parse_page(page):
	"""
	Return parsed page using BeautifulSoup
	"""
	return BeautifulSoup(page)

def get_all_valid_links(parsed_page, base_url, domain):	
	"""
	Extract and return all links found in a page
	"""
	links = set()

	# Find all links
	for anchor in parsed_page.find_all('a'):
		anchor_link = anchor.get('href')

		# Only proceed if href was found in anchor tag
		if anchor_link:
			# Uses urljoin to take care of turning
			# relative URLs into absolute ones
			absolute_link = urljoin(base_url, anchor_link)

			parsed_uri = urlparse(absolute_link)
			anchor_netloc = parsed_uri.netloc

			# Only add to list links from same domain
			if anchor_netloc == domain:
				links.add(absolute_link)

	return links

def get_all_emails(page_contents):
	"""
	Extract and return all emails found in a block of text
	"""
	emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", page_contents, re.I)

	return emails

def crawl_site(seed, domain, max_pages=10):
	"""
	Crawl and process pages starting with the seed url
	"""
	to_crawl = deque([seed])
	crawled = set()
	emails_found = set()

	while len(to_crawl) and (len(crawled) < max_pages):
		url = to_crawl.popleft()
		crawled.add(url)
		
		content = get_page(url)

		if content:
			# Parse page
			parsed_page = parse_page(content)

			# Extract all emails from page contents and add to list of emails found
			emails_found.update(get_all_emails(parsed_page.get_text()))

			# Extract valid links and append to crawling queue
			page_links = get_all_valid_links(parsed_page, url, domain)

			for link in page_links:
				# Only add links that have not been seen yet
				if (not link in crawled) and (not link in to_crawl):
					to_crawl.append(link)
	
	return (crawled, emails_found)

def print_set(set_values):
	"""
	Print each item on a set/list
	"""
	for item in set_values:
		print item

if __name__ == "__main__":
	def parse_options():
		"""
		Parse command line options
		"""
		parser = argparse.ArgumentParser()
		parser.add_argument("domain",
		                    help="domain to be crawled")
		parser.add_argument("-m", "--maxpages", action="store", type=int,
		                    default=10, help="maximum number of pages to crawl")
		parser.add_argument("-v", "--verbose", action="store_true",
		                    help="increase output verbosity", default=False)
		args = parser.parse_args()
		
		return args
		
	def main():
		args = parse_options()
		domain = args.domain
		seed_url = "http://{}/".format(domain)
		maxpages = args.maxpages
		
		crawled, emails_found = crawl_site(seed_url, domain, maxpages)
		
		if args.verbose:
			print "URLs crawled:"
			print_set(crawled)
			print ""

		print "Found these email addresses:"
		print_set(emails_found)

	main()