#!/usr/bin/python3
"""
    Reddit API query
"""
import requests
after = None


def count_worrds(subreddit, word_list):
    """ I will insert this doc later """
    my_list = recurse(subreddit)
    my_dict = {}

    if my_list:
        for word in word_list:
            my_dict[word] = 0

        for title in my_list:
            title_split = title.split(" ")

            for iter in title_split:
                for iter_split in word_list:
                    if iter.lower() == iter_split.lower():
                        my_dict[iter_split] += 1

        for key, val in sorted(my_dict.items(),  key=lambda x: x[1],
                               reverse=True):
            if val != 0:
                print("{}: {}".format(key, val))


def recurse(subreddit, hot_list=[]):
    """ I will also insert this doc later """
    global after
    headers = {'User-Agent': 'ledbag123'}
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    parameters = {'after': after}
    response = requests.get(url, headers=headers, allow_redirects=False,
                            params=parameters)
    if response.status_code == 200:
        prox = response.json().get('data').get('after')

        if prox is not None:
            after = prox
            recurse(subreddit, hot_list)
        list_titles = response.json().get('data').get('children')

        for title_ in list_titles:
            hot_list.append(title_.get('data').get('title'))
        return hot_list
    else:
        return None
