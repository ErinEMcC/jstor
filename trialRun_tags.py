from bs4 import BeautifulSoup
import requests

#Ex. indv. article, practice use. Eventually want to scrape all articles
url = 'http://daily.jstor.org/deforestation-lead-drought/'

a_article = requests.get (url)
if a_article.status_code != 200:
    print ("There was an error with", url)

#url's complete html
article_html = a_article.text

#soup parsing
soup = BeautifulSoup (article_html, "html.parser")

#create list for and article's 'tag' variables
jdaily_tags = []

#find and create variable for 'tags'
for tag in soup.find_all("a", attrs = {"rel": "tag"}):
    a_tag = tag.string

    #append tag(s) to list
    jdaily_tags.append(a_tag)

print (jdaily_tags)
