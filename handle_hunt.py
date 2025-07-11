# -*- coding: utf-8 -*-
"""Handle Hunt.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1gO2d97tPLg84Ba0NOeLrc_jW0Rrp_C8-
"""

!pip install beautifulsoup4==4.8.2 certifi==2019.11.28 chardet==3.0.4 idna==2.8 pyfiglet==0.8.post1 requests==2.22.0 soupsieve==1.9.5 termcolor==1.1.0 urllib3==1.25.7 pandas

import requests
import pandas as pd
import sys
import random
from termcolor import colored
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool
from pyfiglet import figlet_format
import json
import time
import urllib.request

def banner(text, ch='=', length=78):
    spaced_text = ' %s ' % text
    banner = spaced_text.center(length, ch)
    print(banner)

def FindPresence(user_taken):
    start_time = time.time()

    wiki_link = 'https://en.wikipedia.org/wiki/List_of_HTTP_status_codes'
    uname = user_taken
    width = 20  # to pretty print
    global counter
    counter = 0  # to count no of success
    page = requests.get(wiki_link)
    soup = BeautifulSoup(page.content, 'html.parser')
    user_agent = ('Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130'
                  ' Mobile Safari/537.36')
    headers = {'user-agent': user_agent}

    def get_website_membership(site):
        def print_fail():
            print(site.rjust(width), ':', colored(state.ljust(width//2), 'red'), '(Status:', msg, ')')

        def print_success():
            print(site.rjust(width), ':', colored(state.ljust(width//2), 'green'), '(Status:', msg, ')')

        url = websites[site]
        global counter
        state = "FAIL"
        msg = '--exception--'

        if not url[:1] == 'h':
            link = 'https://'+uname+url
        else:
            link = url+uname

        try:
            if site == 'Youtube' or 'Twitter':
                response = requests.get(link)
            else:
                response = requests.get(link, headers=headers)
            tag = soup.find(id=response.status_code)
            msg = tag.find_parent('dt').text
            response.raise_for_status()

        except Exception:
            print_fail()

        else:
            res_soup = BeautifulSoup(response.content, 'html.parser')
            if site == 'Pastebin':
                if len(res_soup.find_all('h1')) == 0:
                    msg = 'broken URL'
                    print_fail()
                else:
                    state = 'SUCCESS'
                    counter += 1
                    print_success()
                    print(colored("\t\tLink to profile {}".format(link), 'red', 'on_cyan', attrs=['bold', 'dark', 'underline']))
            if site == 'LinkedIn':
                if len(res_soup.find_all('h1')) == 0:
                    msg = 'broken URL'
                    print_fail()
                else:
                    state = 'SUCCESS'
                    counter += 1
                    print_success()
                    print(colored("\t\tLink to profile {}".format(link), 'red', 'on_cyan', attrs=['bold', 'dark', 'underline']))
            elif site == 'Wordpress':
                if 'doesn’t exist' or 'blocked' in res_soup:
                    msg = 'broken URL'
                    print_fail()
                else:
                    state = 'SUCCESS'
                    counter += 1
                    print_success()
                    print(colored("\t\tLink to profile {}".format(link), 'red', 'on_cyan', attrs=['bold', 'dark', 'underline']))

            elif site == 'GitLab':
                if 'Sign in' in res_soup.title.text:
                    msg = 'broken URL'
                    print_fail()
                else:
                    state = 'SUCCESS'
                    counter += 1
                    print_success()
                    print(colored("\t\tLink to profile {}".format(link), 'red', 'on_cyan', attrs=['bold', 'dark', 'underline']))
            elif site == 'HackerNews':
                if 'No such user.' in res_soup:
                    msg = 'No Such User!'
                    print_fail()
                else:
                    state = 'SUCCESS'
                    counter += 1
                    print_success()
                    print(colored("\t\tLink to profile {}".format(link), 'red', 'on_cyan', attrs=['bold', 'dark', 'underline']))
            elif site == 'ProductHunt':
                if 'Page Not Found' in res_soup.text:
                    msg = 'No Such User!'
                    print_fail()
                else:
                    state = 'SUCCESS'
                    counter += 1
                    print_success()
                    print(colored("\t\tLink to profile {}".format(link), 'red', 'on_cyan', attrs=['bold', 'dark', 'underline']))
            else:
                state = 'SUCCESS'
                counter += 1
                print_success()
                print(colored("\t\tLink to profile {}".format(link), 'red', 'on_cyan', attrs=['bold', 'dark', 'underline']))

    websites = {
        'LinkedIn': 'https://www.linkedin.com/in/',
        'Facebook': 'https://www.facebook.com/',
        'Twitter': 'https://twitter.com/',
        'Instagram': 'https://www.instagram.com/',
        'Youtube': 'https://www.youtube.com/user/',
        'Reddit': 'https://www.reddit.com/user/',
        'ProductHunt': 'https://www.producthunt.com/@',
        'PInterest': 'https://www.pinterest.com/',
        'Flickr': 'https://www.flickr.com/people/',
        'Vimeo': 'https://vimeo.com/',
        'Soundcloud': 'https://soundcloud.com/',
        'Disqus': 'https://disqus.com/',
        'Medium': 'https://medium.com/@',
        'AboutMe': 'https://about.me/',
        'Imgur': 'https://imgur.com/user/',
        'Flipboard': 'https://flipboard.com/',
        'Slideshare': 'https://slideshare.net/',
        'Spotify': 'https://open.spotify.com/user/',
        'Scribd': 'https://www.scribd.com/',
        'Patreon': 'https://www.patreon.com/',
        'BitBucket': 'https://bitbucket.org/',
        'GitLab': 'https://gitlab.com/',
        'Github': 'https://www.github.com/',
        'GoodReads': 'https://www.goodreads.com/',
        'Instructable': 'https://www.instructables.com/member/',
        'CodeAcademy': 'https://www.codecademy.com/',
        'Gravatar': 'https://en.gravatar.com/',
        'Pastebin': 'https://pastebin.com/u/',
        'FourSquare': 'https://foursquare.com/',
        'TripAdvisor': 'https://tripadvisor.com/members/',
        'Wikipedia': 'https://www.wikipedia.org/wiki/User:',
        'HackerNews': 'https://news.ycombinator.com/user?id=',
        'CodeMentor': 'https://www.codementor.io/',
        'Trip': 'https://www.trip.skyscanner.com/user/',
        'Blogger': '.blogspot.com',
        'Wordpress': '.wordpress.com',
        'Tumbler': '.tumblr.com',
        'Deviantart': '.deviantart.com"',
        'LiveJournel': '.livejournal.com',
        'Slack': '.slack.com',
    }

    p = ThreadPool(10)
    p.map(get_website_membership, list(websites.keys()))
    n_websites = len(list(websites.keys()))
    print('Summary: User {} has membership in {}/{} websites'.format(uname, counter, n_websites))
    print(f"Completed {len(websites)} queries in {time.time() - start_time:.2f}s")

    return counter

def main():
    ascii_banner = figlet_format('Presence of Social Media Handle')
    print(ascii_banner)

    banner_text = "A platform Where A User can Find the Online Presence of Social Media Handle on Internet"
    banner(banner_text)

    username = input("Enter username to search: ")
    if username:
        FindPresence(username)
    else:
        print("No username provided. Exiting...")
        sys.exit(0)


    banner('completed')

if __name__ == '__main__':
    main()