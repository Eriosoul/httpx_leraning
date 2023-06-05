import os

import httpx
from selectolax.parser import HTMLParser
from dotenv import load_dotenv

def get_author(author, response):
    html = HTMLParser(response.text)
    viewstate = html.css_first("input#__VIEWSTATE").attributes['value']
    print(viewstate)
    options = html.css("select#author > option")
    for opt in options[1:]:
        formdata = {
            "author": author,
            "tag": opt.attributes.get("value"),
            "__VIEWSTATE": viewstate
        }
        yield formdata

def main():
    load_dotenv()
    url = os.getenv('URL')
    client = httpx.Client()
    data = client.get(str(url) + "search.aspx")
    for author in get_author(data.url, data):
        author_html = client.post(url + "filter.aspx", data=author)
        for tag in get_author(author['author'], author_html):
            quote_html = client.post(url + "filter.aspx", data=tag)
            print(quote_html.text)


if __name__ == '__main__':
    main()