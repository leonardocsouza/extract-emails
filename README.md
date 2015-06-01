# extract-emails
Python script to extract emails when given a specific domain

## Installing required libraries
Install all necessary libraries using
```
> pip install -r requirements.txt
```

## Usage
Call the script specifying the domain you want to crawl, 
and an optional parameter _--maxpages <number>_ indicating the maximum amount of pages to be crawled (default: 10).
Example:
```
> python extract_emails.py www.atlassian.com --maxpages 30
```

## Optional parameters
* maxpages - indicates the maximum amount of pages to be crawled (default: 10)
