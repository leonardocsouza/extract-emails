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
from urlparse import urljoin
from collections import deque
from urlparse import urlparse

socket.setdefaulttimeout(10)

# Download page and return its contents
def get_page(url):
	try:
		print "Requesting url [%s]" % url
		f = urllib.urlopen(url)
		page = f.read()
		f.close()
		return page
	except:
		return ""
	return ""

# Return parsed page using BeautifulSoup
def parse_page(page):
	return BeautifulSoup(page)

# Extract and return all links found in a page
def get_all_valid_links(parsed_page, base_url, domain):	
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

# Extract and return all emails found in a block of text
def get_all_emails(page_contents):
	emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", page_contents, re.I)

	return emails

def crawl_site(seed, domain, max_pages=10):
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
	for item in set_values:
		print item

if __name__ == "__main__":
		import optparse
		__version__ = "0.1"
		USAGE   = "%prog [options] <url>"
		VERSION = "%prog v" + __version__
		def parse_options():
				"""parse_options() -> opts, args

				Parse any command-line options given returning both
				the parsed options and arguments.
				"""
				parser = optparse.OptionParser(usage=USAGE,version=VERSION)
				parser.add_option("-p", "--maxpages",action="store", type="int",
									  default=10, dest="maxpages",
									  help="Maximum number of pages to crawl")
				
				(opts, args) = parser.parse_args()
				if len(args) < 1:
					parser.print_help()
					raise SystemExit, 1
				return opts, args
		
		def main():
				opts, args = parse_options()
				domain = args[0]
				seed_url = "http://{}/".format(domain)

				#if url[-1] == '/':
				#    url = url[:len(url) - 1]
				maxpages = opts.maxpages
				
				crawled, emails_found = crawl_site(seed_url, domain, maxpages)
				
				print "URLs crawled:"
				print_set(crawled)
				print ""

				print "Found these email addresses:"
				print_set(emails_found)

		main()