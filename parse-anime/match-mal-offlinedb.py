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

# Manual match (use the offline database name)
manual_match = [
    {
        'mal_match': 'Tennis no Oujisama',
        'db_match': 'Tennis no Ouji-sama'
    },
    {
        'mal_match': 'Mukamuka Paradise',
        'db_match': 'Muka Muka Paradise'
    }
]

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

# Manual matching
for manual in manual_match:

    # find entry in mal list
    for mal in mal_anime:
        if manual['mal_match'] == mal['title']:
            break

    # find entry in offline db
    for anime in anime_db['data']:
        if manual['db_match'] == anime['title']:
            anime['mal_id'] = mal['id']

            try:
                anime['en'] = mal['en']
            except KeyError:
                pass

            matched_list['data'].append(anime)
            break

# Write to disk the matched titles
with open('matched-anime-list.json', 'w') as f:
    json.dump(matched_list, f, ensure_ascii=False, indent=2)

# Print out unmatched titles
print(f'Could not match the following, add manually (if wanted)\n: {unmatched_list}')
