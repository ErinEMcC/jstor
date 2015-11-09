from bs4 import BeautifulSoup
import requests

#Ex. indv. article, practice use. Eventually want to scrape all articles
url = 'http://daily.jstor.org/visual-literacy-in-the-age-of-open-content/'

a_article = requests.get (url)

if a_article.status_code != 200:
    print ("There was an error with", url)

#url's complete html
article_html = a_article.text

#soup parsing
soup = BeautifulSoup (article_html, "html.parser")

#creating variables for each article to be scraped
art_author = soup.find('span', attrs = {"class": "entry-author"}).text
art_date = soup.find("span", attrs = {"class": "entry-date"}).text
art_title = soup.find("h1", attrs = {"class": "entry-title single-title"}).text

print ('\n')

#create variable for JSTOR citation (article acting as source)
art_source = soup.find_all("h3", attrs = {"class": "citation-title"})
for link in art_source:
    a_link = link.find("a")

    print (a_link.get('href'))

print ('\n')
print (art_author, art_date, art_title)
print ('\n')

#create a variable for the actual text of an article (could be one or many paragraphs)
art_frame = soup.find_all ("div", attrs = {"class": "single-box clearfix entry-content"})
for text in art_frame:
    art_text = text.find_all("p")

    print (art_text)
    print ('\n')

#finding the "Next" link
n_link = soup.find("a",attrs = {"rel": "next"})
print (n_link.get('href'))

#while n_link == true
#url2 = n_link.get('href')
#b_article = requests.get(url2)



