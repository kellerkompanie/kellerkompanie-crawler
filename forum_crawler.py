#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import json
import re
import uuid
from urllib.request import urlopen
import sys

import dateparser

FORUM_URL = "http://kellerkompanie.com/forum"
NEWS_SUBFORUM_ID = 3
MISSIONS_SUBFORUM_ID = 5

DONATION_KEYWORDS = ["spende", "paypal", "finanz"]


def get_urls(subforum_id):
    html = urlopen(FORUM_URL + "/viewforum.php?f=" + str(subforum_id)).read().decode('utf-8').replace("&amp;", "&")

    pattern_announcements = re.compile(r"""<ul class="topiclist topics">([\s\S]*?)</ul>""")
    announcement_html = pattern_announcements.findall(html)[0]  # 0 = announcements, 1 = normal posts

    posts_pattern = re.compile(
        r"""href=(["']\.)(/viewtopic\.php\?f=""" + str(subforum_id) + """&t=([0-9]*)&sid=.*?)(["'])""")
    post_urls = []
    for match in posts_pattern.findall(announcement_html):
        post_urls.append(FORUM_URL + match[1])

    return post_urls


def get_posts(urls):
    posts = []
    for post_url in urls:
        html = urlopen(post_url).read().decode('utf-8').replace("&amp;", "&")

        pattern_title = re.compile(r"""(<h3 class="first"><a href=)(["'])(#p[0-9]*)\2>(.*)(</a></h3>)""")
        post_title = pattern_title.findall(html)[0][3]

        pattern_content = re.compile(r"""<div class="content">(.*)</div>""")
        post_content = pattern_content.findall(html)[0].replace("<br />", " ")
        post_content = re.sub(' +', ' ', post_content)
        post_content = re.sub(r"""</?span(.*?)>""", '', post_content)
        post_content = re.sub(r"""</?a(.*?)>""", '', post_content)
        post_content = re.sub(r"""</?img(.*?)>""", '', post_content)
        post_content = re.sub(r"""</?ul>""", '', post_content)
        post_content = re.sub(r"""<!--(.*?)-->""", '', post_content)
        post_content = re.sub(r"""&quot;""", '"', post_content)

        pattern_author = re.compile(r"""<p class="author">([\s\S]*?</p>)""")
        author_html = pattern_author.findall(html)[0]
        pattern_date = re.compile(r"""&raquo; (.*?)</p>""")
        date_html = pattern_date.findall(author_html)[0]
        post_date = dateparser.parse(date_html)

        posts.append([post_url, post_title, post_content, post_date])
    return posts


class JSONNews(dict):
    def __init__(self, type, title, content, url, timestamp):
        dict.__init__(self, uuid=str(uuid.uuid4()), newsType=type, title=title, content=content, weblink=url,
                      timestamp=timestamp)
        self.uuid = str(uuid.uuid4())
        self.newsType = type
        self.title = title
        self.content = content
        self.weblink = url
        self.timestamp = timestamp


def unix_time_millis(dt):
    return (dt - datetime.datetime.utcfromtimestamp(0)).total_seconds() * 1000.0


def main():
    if len(sys.argv) != 2:
        print('ERROR: specify filename as parameter')
        return

    fname = sys.argv[1]

    news_urls = get_urls(NEWS_SUBFORUM_ID)
    mission_urls = get_urls(MISSIONS_SUBFORUM_ID)

    news_posts = get_posts(news_urls)
    mission_posts = get_posts(mission_urls)

    print("crawled", len(news_posts), "news posts")
    print("crawled", len(mission_posts), "mission posts")

    news_list = list()
    for url, title, content, date in news_posts + mission_posts:
        type = "NEWS"
        if any(keyword in title for keyword in DONATION_KEYWORDS) or any(
                keyword in content for keyword in DONATION_KEYWORDS):
            type = "DONATION"
        timestamp = unix_time_millis(date)
        news = JSONNews(type, title, content, url, timestamp)
        news_list.append(news)

    with open(fname, 'w') as outfile:
        json.dump(news_list, outfile, indent=4)


if __name__ == "__main__":
    main()
