#!/usr/bin/env python
# discover urls in the domain by extract the href link in the content and crawl recursively to get all urls

import requests
import re
import urllib.parse

target_url = "http://dl.roozdl.com/roozdl/"
target_links = []


def extract_links_from(url):
    response = requests.get(url)
    return re.findall('(?:href=")(.*?)"', str(response.content))  # OR response.content.decode(errors="ignore")


def crawl(url):
    href_links = extract_links_from(url)

    for link in href_links:
        link = urllib.parse.urljoin(url, link)  # if relative link, convert to full url

        if "#" in link:  # after # - not real separate links but dynamic JS content on same page
            link = link.split("#")[0]

        if target_url in link and link not in target_links:  # to avoid repeating the same url
            target_links.append(link)
            print("[+]urls --->", link)
            crawl(link)  # recursively crawling


crawl(target_url)
