import json
import pandas as pd

# File from https://github.com/manami-project/anime-offline-database
f = open('anime-offline-database.json')

# List of items to remove
remove_anime = [
    # Other seasons
    "Initial D Fifth Stage",
    "Initial D Final Stage",
    "Initial D Fourth Stage",
    "Initial D Second Stage",
    "Initial D Third Stage",
    "Shin Gekijouban Initial D",
    "New Initial D Movie: Legend 1 - Kakusei",
    "New Initial D Movie: Legend 2 - Tousou",
    "New Initial D Movie: Legend 3 - Mugen",
    "Tottoko Hamtaro (2012)",
    "Tottoko Hamtaro Dechu",
    "Tottoko Hamtarou Hai!",
    "Tottoko Hamtarou Movie 1: Ham-Ham Land Daibouken",
    "Tottoko Hamtarou Movie 2: Ham-Ham Hamuuja! Maboroshi no Princess",
    "Tottoko Hamtarou Movie 3: Ham Ham Grand Prix Aurora Tani no Kiseki - Ribon-chan Kiki Ippatsu!",
    "Tottoko Hamtarou Movie 4: Hamtaro to Fushigi no Oni no Emon Tou",
    "Tottoko Hamtarou: Hamu Hamu Paradichu!",
    "Boruto: Naruto the Movie",
    "Naruto (Shinsaku Anime)",
    "Naruto SD: Rock Lee no Seishun Full-Power Ninden",
    "Naruto Soyokazeden Movie: Naruto to Mashin to Mitsu no Onegai Dattebayo!!",
    "Naruto: Honoo no Chuunin Shiken! Naruto vs. Konohamaru!!",
    ".hack\/\/Roots",
    ".hack\/\/Tasogare no Udewa Densetsu",
    ".hack\/\/The Movie: Sekai no Mukou ni",
    # Similar synonyms 
    "Shi Er Shengxiao: Fuxing Gao Zhao Zhu Xiao Ba",
    "Fuxing Ba Jie",
]

other_seasons = [
    "Season 0",
    "Season 2",
    "Season 3",
    "Season 4",
    "Season 5",
    "Season 6",
    "Season 7",
    "Season 8",
    "Season 9",
    "Season 10",
    "Season 11",
    "Season 12",
    "Season 13",
    "Season 14",
    "Season 15",
    "Season 16",
    "Season 17",
    "Season 18",
    "Season 19",
    "Season 20",
    "season 2",
    "season 3",
    "season 4",
    "season 5",
    "season 6",
    "season 7",
    "season 8",
    "season 9",
    "2nd Season",
    "3rd Season",
    "4th Season",
    "5th Season",
    "6th Season",
    "7th Season",
    "8th Season",
    "9th Season",
    "10th Season",
    "11th Season",
    "Second Season",
    "Third Season",
    "Season II",
    "Season III",
    "Season Two",
    "Part 2",
    "Naruto Movie"
]

data = json.load(f)
parsed = [] # list of parsed names

for i in data['data']:

    # Only keep movies or TV shows
    if i['type'] == 'MOVIE' or i['type'] == 'TV':

        skip_loop = False

        if i['title'] in remove_anime:
            continue

        for seasons in other_seasons:
            if seasons in i['title']:
                skip_loop = True
                break

        if skip_loop == True:
            continue

        toss_based_on_synonym = False

        # Only keep synonyms that don't have unicode in them
        new_synonyms = []
        for j in i['synonyms']:

            for seasons in other_seasons:
                if seasons in j:
                    toss_based_on_synonym = True
                    break
            
            if toss_based_on_synonym == True:
                break

            if j.isascii():
                new_synonyms.append(j)

        if toss_based_on_synonym == True:
            continue

        i['synonyms'] = new_synonyms
        parsed.append(i)


# Convert to dataframe for further parsing
df = pd.DataFrame(parsed)
df = df.drop(['sources', 'status', 'picture', 'thumbnail', 'relations', 'tags', 'episodes', 'animeSeason'], axis=1) # remove columns

# Outputs
df.reset_index().to_json(r'parsed-anime-list.json', orient='records', indent=2)
df.reset_index().to_json(r'parsed-anime-list-mini.json', orient='records')
