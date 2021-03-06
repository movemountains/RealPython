'''
Task description:
=================
- Write a script that grabs the full HTML from the page
http://www.realpython.com/practice/profiles.html
- Parse out a list of all the links on the page using Beautiful Soup by
looking for HTML tags with the name "a" and retrieving the value taken on
by the "href" attribute of each tag
- Get the HTML from each of the pages in the list by adding the full path
to the file name, and display the text (without HTML tags) on each page
using Beautiful Soup's get_text() method
'''

from bs4 import BeautifulSoup
from urllib2 import urlopen

base_url = "http://www.realpython.com/practice/"
addr = base_url + "profiles.html"
html_page = urlopen(addr)
html_text = html_page.read()
parsed_text = BeautifulSoup(html_text)

for link in parsed_text.find_all("a"):
    link_addr = base_url + link["href"]
    link_page = urlopen(link_addr)
    link_text = link_page.read()
    parsed_link = BeautifulSoup(link_text)
    print parsed_link.get_text().replace("\n\n\n", "")
