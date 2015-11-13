from bs4 import BeautifulSoup
import requests

jdaily_articles = []

#Ex. indv. article, practice use. Eventually want to scrape all articles
url = 'http://daily.jstor.org/deforestation-lead-drought/'

a_article = requests.get (url)
if a_article.status_code != 200:
    print ("There was an error with", url)

#url's complete html
article_html = a_article.text

#soup parsing
soup = BeautifulSoup (article_html, "html.parser")

#creating, cleaning author variable
art_author2 = soup.find('span', attrs = {"class": "entry-author"}).text
if 'By' in art_author2:
    art_author = art_author2.replace('By' , '').strip()
    
#creating other variables for article metadata
art_date = soup.find("span", attrs = {"class": "entry-date"}).text
art_title = soup.find("h1", attrs = {"class": "entry-title single-title"}).text

#create list for JSTOR citation(s) / article(s) acting as source
jstor_links = []

#create variable for indv. Jstor citations
art_source = soup.find_all("h3", attrs = {"class": "citation-title"})
for link in art_source:
    a_link = link.find("a")
    #add link(s) to jstor_links list
    jstor_links.append(a_link.get('href'))
    
#create a variable for the actual text of an article (could be one or many paragraphs)
art_frame = soup.find_all ("div", attrs = {"class": "single-box clearfix entry-content"})
for text in art_frame:
    art_text = text.find_all("p")

#finding the "Next" link
n_link = soup.find("a",attrs = {"rel": "next"})

#create / define a dictionary of indv article's data
this_article = {}

#assigning data fields as dictionary keys, with the variables created above
this_article['date'] = art_date
this_article['author'] = art_author
this_article['title'] = art_title
this_article['sources'] = jstor_links
this_article['text'] = art_text

print (this_article)
print ("\n")

#add the dictionary to the list created at top or return message
#jdaily_articles.append(this_article)

while n_link != None:
    url = n_link['href']
    a_article = requests.get(url)
    soup = BeautifulSoup(a_article.text, "html.parser")

    #creating, cleaning author variable
    art_author2 = soup.find('span', attrs = {"class": "entry-author"}).text
    if 'By' in art_author2:
        art_author = art_author2.replace('By' , '').strip()

    #creating other variables for article metadata    
    art_date = soup.find("span", attrs = {"class": "entry-date"}).text
    art_title = soup.find("h1", attrs = {"class": "entry-title single-title"}).text

    #create variable for JSTOR citation (article acting as source)
    jstor_links = []
    art_source = soup.find_all("h3", attrs = {"class": "citation-title"})
    for link in art_source:
        a_link = link.find("a")
        #add link(s) to jstor_links list
        jstor_links.append(a_link.get('href'))

    #create a variable for the actual text of an article (could be one or many paragraphs)
    art_frame = soup.find_all ("div", attrs = {"class": "single-box clearfix entry-content"})
    for text in art_frame:
        art_text = text.find_all("p")

    n_link = soup.find("a",attrs = {"rel": "next"})

    #create / define a dictionary of indv article's data
    this_article = {}

    #assigning data fields as dictionary keys, with the variables created above
    this_article['date'] = art_date
    this_article['author'] = art_author
    this_article['title'] = art_title
    this_article['sources'] = jstor_links
    this_article['text'] = art_text

    print (this_article)
    print ("\n")
    




