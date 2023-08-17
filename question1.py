import requests
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path


page = requests.get('https://www.reddit.com/r/programming/')

soup = BeautifulSoup(page.content, 'html.parser')
posts = soup('shreddit-post')

data = list()
for post in posts[:3]:
    title   = post.find(slot = 'title').text.strip()
    upvotes = post.get('score')
    if upvotes is None:
        upvotes = 0
    link    = post.a['href']
    data.append([title, upvotes, link])

df = pd.DataFrame(data, columns=["Título", "Up Votes", "Link"])

df.index += 1
df.to_csv(Path.cwd() / "Postagens do subreddit programming.csv")