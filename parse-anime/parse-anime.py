import json
import pandas as pd

# File from https://github.com/manami-project/anime-offline-database
f = open('anime-offline-database.json')

data = json.load(f)
parsed = [] # list of parsed names

for i in data['data']:

    # Only keep movies or TV shows
    if i['type'] == 'MOVIE' or i['type'] == 'TV':

        # Only keep synonyms that don't have unicode in them
        new_synonyms = []
        for j in i['synonyms']:
            if j.isascii():
                new_synonyms.append(j)

        i['synonyms'] = new_synonyms
        parsed.append(i)


# Convert to dataframe for further parsing
df = pd.DataFrame(parsed)
df = df.drop(['sources', 'status', 'picture', 'thumbnail', 'relations', 'tags', 'episodes', 'animeSeason'], axis=1) # remove columns

# Outputs
df.reset_index().to_json(r'parsed-anime-list.json', orient='records', indent=2)
df.reset_index().to_json(r'parsed-anime-list-mini.json', orient='records')
