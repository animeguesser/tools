import requests
import time
import json
import os
import argparse

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--mal", type=str, required=True)
args = parser.parse_args()

# Setup
CLIENT_ID = args.mal
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
    time.sleep(0.5)

# Get the list of movie animes using MAL API
offset = 0
while offset < 1000:
    
    # Limit to 250 entries at a time
    url = f'https://api.myanimelist.net/v2/anime/ranking?ranking_type=movie&fields=id,title,alternative_titles&limit=500&offset={offset}'
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
    time.sleep(0.5)

# Get the list of ova animes using MAL API
offset = 0
while offset < 500:
    
    # Limit to 250 entries at a time
    url = f'https://api.myanimelist.net/v2/anime/ranking?ranking_type=ova&fields=id,title,alternative_titles&limit=500&offset={offset}'
    resp = requests.get(url, headers={
        'X-MAL-CLIENT-ID': CLIENT_ID
    })
    anime = resp.json()

    # Add into our list
    for node in anime['data']:
        anime_list.append({'title': node['node']['title'], 'id': node['node']['id'], 'en': node['node']['alternative_titles']['en']})

    # Start at the next 250
    offset = offset + 500

    # Let's not spam the MAL API
    time.sleep(0.5)

# Write to disk
with open('mal.json', 'w') as f:
    json.dump(anime_list, f, ensure_ascii=False, indent=4)