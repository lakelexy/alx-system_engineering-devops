#!/usr/bin/python3
"""
    Reddit API query
"""
import requests


def count_words(subreddit, word_list, after=None, counts=None):
    """
       recursive function that queries the Reddit API, parses the title
       of all hot articles, and prints a sorted count of given keywords
       (case-insensitive, delimited by spaces. Javascript should count
       as javascript, but java should not).
    """
    if counts is None:
        counts = {}
    if after is None:
        url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    else:
        url = f"https://www.reddit.com/r/{subreddit}/hot.json?after={after}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        for item in data["data"]["children"]:
            title = item["data"]["title"].lower()
            for word in word_list:
                if " " + word.lower() + " " in title:
                    if word.lower() in counts:
                        counts[word.lower()] += 1
                    else:
                        counts[word.lower()] = 1
        after = data["data"]["after"]
        if after is not None:
            count_words(subreddit, word_list, after, counts)
        else:
            sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
            for word, count in sorted_counts:
                print(f"{word}: {count}")
    else:
        print("Error:", response.status_code)
