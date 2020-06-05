# coding: utf-8
# Author: Zandra Nilsson

from bottle import route, run, template, request, static_file, redirect, error
import json

def get_articles():
    '''
    Läser in json-filen, alternativt skapar den ifall den inte finns.
    '''
    
    try:
        my_file = open("artiklar.json", "r")
        articles = json.loads(my_file.read())
        my_file.close()
        
        return articles

    except FileNotFoundError and ValueError:
        my_file = open("artiklar.json", "w")
        articles = []
        my_file.write(json.dumps(articles))
        my_file.close()
        
        return articles

@route("/")
def list_articles():
    """
    This is the home page, which shows a list of links to all articles
    in the wiki.
    """

    return template("index", articles=get_articles())

@route('/update', method="POST")
def update_article():
    """
    Receives page title and contents from a form, and creates/updates a
    text file for that page.
    """

    article = {}
    article["title"] = getattr(request.forms, "title")
    article["text"] = getattr(request.forms, "article")
    article["id"] = request.forms.get("id")

    articles = get_articles()

    if article["title"] == "" and article["text"] == "":
        return template("fel")

    elif article["id"] == "":
        highest_id = 0
        for a in articles:
            if int(a["id"]) > highest_id:
                highest_id = int(a["id"])
                
        article["id"] = highest_id + 1
        articles.append(article)
        my_file = open("artiklar.json", "w")
        my_file.write(json.dumps(articles, indent=4))
        my_file.close()

        redirect ("/wiki/" + article["title"])

    else:
        article_id = int(article["id"])
        for i in articles:
            if article_id == i["id"]:
                articles.remove(i)
                article["id"] = article_id

        articles.append(article)
        my_file = open("artiklar.json", "w")
        my_file.write(json.dumps(articles, indent=4))
        my_file.close()

        redirect ("/wiki/" + article["title"])

@route('/delete', method="POST")
def delete_article():

    article = getattr(request.forms, "titel")

    articles = get_articles()

    for i in articles:
        if article == i["title"]:
            articles.remove(i)
    my_file = open("artiklar.json", "w")
    my_file.write(json.dumps(articles, indent=4))
    my_file.close()

    redirect ("/")
    
@route('/edit/<pagename>')
def edit_form(pagename):
    """
    Shows a form which allows the user to input a title and content
    for an article. This form should be sent via POST to /update/.
    """

    articles = get_articles()

    edit_article = None
    for article in articles:
        if article["title"] == pagename:
            edit_article = article

    if edit_article == None:
        return template("skapa-artikel")

    else:
        return template("edit", article=edit_article)
    

@route('/wiki/<pagename>')
def show_article(pagename):
    """Displays a single article (loaded from a text file).
    Om artikeln inte finns så visas en fel-sida upp istället.
    """

    articles = get_articles()

    found_article = None
    for article in articles:
        if article["title"] == pagename:
            replace = article["text"].replace("\r\n", "<br>")
            found_article = article
    
    if found_article == None:
        return template("article-not-found")
        
    else:
        return template("wiki", article=found_article, replace=replace)

@route("/about")
def about():
    '''Visar upp sidan "Om"'''

    return template("about")

@error(404)
def error404(error):
    '''Handles the error 404: File not found'''

    return template("error")

@route("/static/<filename>")
def static_files(filename):
    '''Handles the routes to our static files'''
    
    return static_file(filename, root="static")

run(host='localhost', port=8081, debug=True, reloader=True)
