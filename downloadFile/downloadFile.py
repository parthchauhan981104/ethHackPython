#!/usr/bin/python2

import requests


def download(url):
    get_request = requests.get(url)
    file_name = url.split("/")[-1]

    with open(file_name, "wb") as file:
        file.write(get_request.content)


download("https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_1280.jpg")
