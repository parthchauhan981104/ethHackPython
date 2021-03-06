#!/usr/bin/python

import requests
import re
import urllib.parse

target_url = "http://192.168.44.101"
target_links = []


def extract_links_from(url):
    response = requests.get(url)
    return re.findall('(?:href=")(.*?)"', str(response.content))  # OR response.content.decode(errors="ignore")


href_links = extract_links_from(target_url)

for link in href_links:
    link = urllib.parse.urljoin(target_url, link)  # if relative link, convert to full url

    if "#" in link:  # after # - not real separate links but dynamic JS content on same page
        link = link.split("#")[0]

    if target_url in link and link not in target_links:  # to avoid repeating the same url
        target_links.append(link)
        print(link)
