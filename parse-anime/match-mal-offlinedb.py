import json

# From get-mal.py
f = open('mal.json')
mal_anime = json.load(f)

# File from https://github.com/manami-project/anime-offline-database
f = open('anime-offline-database.json')
anime_db = json.load(f)

# Setup
matched_list = {'data': []}
unmatched_list = []

# Match the title from the MAL API to the offline DB
for mal in mal_anime:
    found = False

    for anime in anime_db['data']:
        if anime['title'] == mal['title']:
            anime['mal_id'] = mal['id']

            try:
                anime['en'] = mal['en']
            except KeyError:
                pass
            
            matched_list['data'].append(anime)
            found = True
            break

    # Create an list of unmatched titles
    if found == False:
        unmatched_list.append(mal['title'])

# Write to disk the matched titles
with open('matched-anime-list.json', 'w') as f:
    json.dump(matched_list, f, ensure_ascii=False, indent=2)

# Print out unmatched titles
print(f'Could not match the following, add manually (if wanted)\n: {unmatched_list}')
