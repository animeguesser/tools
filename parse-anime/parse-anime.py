import json
import pandas as pd

# File from https://github.com/manami-project/anime-offline-database
f = open('anime-offline-database.json')

# Skip entries if these match exactly
remove_anime = [
    # Other seasons
    "Initial D Fifth Stage",
    "Initial D Final Stage",
    "Initial D Fourth Stage",
    "Initial D Second Stage",
    "Initial D Third Stage",
    "Tottoko Hamtaro (2012)",
    "Tottoko Hamtaro Dechu",
    "Tottoko Hamtarou Hai!",
    "Tottoko Hamtarou: Hamu Hamu Paradichu!",
    "Naruto (Shinsaku Anime)",
    "Naruto SD: Rock Lee no Seishun Full-Power Ninden",
    ".hack\/\/Roots",
    ".hack\/\/Tasogare no Udewa Densetsu",
    ".hack\/\/The Movie: Sekai no Mukou ni",
    "Akira (Shin Anime)",
    "Eureka Seven AO",
    "Escaflowne",
    "Psycho-Pass RE:Start",
    "Psycho-Pass 3",
    "Gundam Seed Destiny HD Remaster",
    "Gundam: G no Reconguista",
    "Kidou Senshi Gundam SEED Destiny",
    "Kidou Senshi Gundam: Tekketsu no Orphans - Tokubetsu-hen",
    "Mobile Suit Gundam 00: 10th Anniversary Project",
    "Mobile Suit Gundam Seed HD Remaster",
    "Mobile Suit Gundam UC2",
    "Mobile Suit SD Gundam The Movie: Musha Knight Commando: SD Gundam Scramble",
    "Space Gundam V",
    "Gundam Build Fighters",

    # Similar synonyms 
    "Shi Er Shengxiao: Fuxing Gao Zhao Zhu Xiao Ba",
    "Fuxing Ba Jie",
]

# Skip enteries if it contains 'Season xx'
skip_seasons_entries = [
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
    "Part 3",
    "Part 4",
    "Part 5",
    "Part 6",
]

# Skip these entries if it's a movie AND contains one of these
skip_movie_entries = [
    "Detective Conan",
    "Naruto",
    "Psycho-Pass",
    "Girls & Panzer",
    "Eureka Seven",
    "Hamtarou",
    "Initial D",
    "Gundam"
]

data = json.load(f)
parsed = [] # list of parsed names

for i in data['data']:

    # Only keep movies or TV shows
    if i['type'] == 'MOVIE' or i['type'] == 'TV':

        skip_loop = False

        # Remove extra unwanted entries if it's in the title
        if i['title'] in remove_anime:
            continue

        # Remove unwanted if it's in the seasons
        for seasons in skip_seasons_entries:
            if seasons in i['title']:
                skip_loop = True
                break

        if skip_loop == True:
            continue

        toss_based_on_synonym = False

        # Cycle through the synonymns
        new_synonyms = []
        for j in i['synonyms']:

            # Remove extra unwanted enteries if it's in the synonym
            for seasons in skip_seasons_entries:
                if seasons in j:
                    toss_based_on_synonym = True
                    break
            
            # Remove unwanted entries if it's a synonym AND a movie
            if i['type'] == 'MOVIE':
                for movies in skip_movie_entries:
                    if movies in j:
                        toss_based_on_synonym = True
                        break
            
            if toss_based_on_synonym == True:
                break

            # Only keep synonyms that don't have unicode in them
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
