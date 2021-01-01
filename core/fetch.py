
import time
import requests


def fetch(url, i=0):
    try:
        return requests.get(url)
    except:
        print(f'[retry][{i}] {url}')
        time.sleep(5)
        if i < 3:
            return fetch(url, i+1)
        else:
            print(f'[fetch failed] {url}')
