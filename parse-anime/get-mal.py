import requests
import time
import json
import os
# Setup
CLIENT_ID = os.getenv('MAL_CLIENT_ID')
offset = 0
anime_list = []

# Get list of TV animes using MAL API
while offset < 5000:

    # Can only get 500 at a time
    url = f'https://api.myanimelist.net/v2/anime/ranking?ranking_type=tv&fields=id,title,alternative_titles&limit=500&offset={offset}'
    resp = requests.get(url, headers={
        'X-MAL-CLIENT-ID': CLIENT_ID
    })
    anime = resp.json()

    # Add into our list
    for node in anime['data']:
        anime_list.append({'title': node['node']['title'], 'id': node['node']['id'], 'en': node['node']['alternative_titles']['en']})

    # Start at the next 500
    offset = offset + 500

    # Let's not spam the MAL API
    time.sleep(1)

# Get the list of movie animes using MAL API
offset = 0
while offset < 250:
    
    # Limit to 250 entries at a time
    url = f'https://api.myanimelist.net/v2/anime/ranking?ranking_type=movie&fields=id,title,alternative_titles&limit=250&offset={offset}'
    resp = requests.get(url, headers={
        'X-MAL-CLIENT-ID': CLIENT_ID
    })
    anime = resp.json()

    # Add into our list
    for node in anime['data']:
        anime_list.append({'title': node['node']['title'], 'id': node['node']['id'], 'en': node['node']['alternative_titles']['en']})

    # Start at the next 250
    offset = offset + 250

    # Let's not spam the MAL API
    time.sleep(1)
    
# Write to disk
with open('mal.json', 'w') as f:
    json.dump(anime_list, f, ensure_ascii=False, indent=4)