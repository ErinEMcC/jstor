from bs4 import BeautifulSoup
import requests
import json
import time
import re


#list of dictionaries - each dictionary one article
jdaily_articles = []

#Ex. indv. article, practice use. Eventually want to scrape all articles
#start with oldest article: http://daily.jstor.org/maya-angelou-has-died/
url = 'http://daily.jstor.org/maya-angelou-has-died'

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

title = soup.find("h1", attrs = {"class": "entry-title single-title"}).text
if '\n' in title:
    art_title = title.replace ('\n' , ''). strip()


#create list for JSTOR citation(s) / article(s) acting as source
jstor_dois = []

#create variable for indv. Jstor citations - just the DOI suffix
art_source = soup.find_all("h3", attrs = {"class": "citation-title"})
for link in art_source:
    a_link = link.find("a")
    #add link(s) to jstor_links list
    text = a_link.get('href')
    doi = text.replace('http://www.jstor.org/stable/' , '')
    jstor_dois.append(doi)

#create list for titles of journals used as sources
journals_sourced = []

#Journal Name, Vol/Issue information
for title_source in soup.find_all('p', attrs = {"class": "citation-source"}):
    a_source = title_source.text
    #append journals to list
    journals_sourced.append(a_source)

#create list for and article's 'tag' variables
jdaily_tags = []

#find and create variable for 'tags'
for tag in soup.find_all("a", attrs = {"rel": "tag"}):
    a_tag = tag.string

    #append tag(s) to list
    jdaily_tags.append(a_tag)


#finding the "Next" link
n_link = soup.find("a",attrs = {"rel": "next"})

#create / define a dictionary of indv article's data
this_article = {}

#assigning data fields as dictionary keys, with the variables created above
this_article['date'] = art_date
this_article['jdaily_author'] = art_author
this_article['jdaily_title'] = art_title
this_article['sources'] = jstor_dois
this_article['tags'] = jdaily_tags
this_article['journals'] = journals_sourced
this_article ['publishers'] = "None listed"

#add the dictionary to the list created at top or return message
jdaily_articles.append(this_article)

print (this_article)

while n_link != None:
    url = n_link['href']
    a_article = requests.get(url)
    time.sleep(1)
    soup = BeautifulSoup(a_article.text, "html.parser")

    #creating, cleaning author variable
    art_author2 = soup.find('span', attrs = {"class": "entry-author"}).text
    if 'By' in art_author2:
        art_author = art_author2.replace('By' , '').strip()

    #creating other variables for article metadata
    art_date = soup.find("span", attrs = {"class": "entry-date"}).text
    
    title = soup.find("h1", attrs = {"class": "entry-title single-title"}).text
    if '\n' in title:
        art_title = title.replace ('\n' , ''). strip()

    #create list for JSTOR citation(s) / article(s) acting as source
    jstor_dois = []

    #create variable for indv. Jstor citations - just the DOI suffix
    art_source = soup.find_all("h3", attrs = {"class": "citation-title"})
    for link in art_source:
        a_link = link.find("a")
        #add link(s) to jstor_links list
        text = a_link.get('href')
        doi = text.replace('http://www.jstor.org/stable/' , '')
        jstor_dois.append(doi)
                
    #add doi(s) to jstor_dois list
    jstor_dois.append(doi)
        
    #create list for titles of journals used as sources
    journals_sourced = []
    
    #Journal Name, Vol/Issue information
    for title_source in soup.find_all('p', attrs = {"class": "citation-source"}):
        a_source = title_source.text
        #append journals to list
        journals_sourced.append(a_source)

       
    #create list for publishers of journals used as sources
    publishers_sourced = []
    
    #Publisher Statement
    for publisher_source in soup.find_all('p', attrs = {"class": "citation-source"}):
        a_pub = publisher_source.text

        #append journals to list
        publishers_sourced.append(a_pub)


    #create list for and article's 'tag' variables
    jdaily_tags = []

    #find and create variable for 'tags'
    for tag in soup.find_all("a", attrs = {"rel": "tag"}):
        a_tag = tag.string

        #append tag(s) to list
        jdaily_tags.append(a_tag)
    
    #find > create variable for next page link
    n_link = soup.find("a",attrs = {"rel": "next"})
    
    #create / define a dictionary of indv article's data
    this_article = {}

    #assigning data fields as dictionary keys, with the variables created above
    this_article['date'] = art_date
    this_article['jdaily_author'] = art_author
    this_article['jdaily_title'] = art_title
    this_article['sources'] = jstor_dois
    this_article['tags'] = jdaily_tags
    this_article['journals'] = journals_sourced
    this_article['publishers'] = publishers_sourced

    #add the dictionary to the list created at top or return message
    jdaily_articles.append(this_article)

    print(this_article)
    print("\n")

with open('scraped_jdaily.json', 'w') as f:
    f.write(json.dumps(jdaily_articles, indent=4))



