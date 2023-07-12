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
    ".hack//Roots",
    ".hack//Tasogare no Udewa Densetsu",
    ".hack//The Movie: Sekai no Mukou ni",
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
    "Bleach: Sennen Kessen-hen",
    "BLEACH: Sennen Kessen-hen 3rd Cour",
    "BLEACH: Sennen Kessen-hen 4th Cour",
    "Bocchi the Rock! Movie",
    "Jujutsu Kaisen 0 Movie",
    "Dragon Ball GT",
    "Dragon Ball Kai",
    "Dragon Ball Kai (2014)",
    "Shingeki! Kyojin Chuugakkou",
    "Meitantei Conan: Zero no Tea Time",
    "Meitantei Conan: Hannin no Hanzawa-san",
    "Mashin Eiyuuden Wataru 2",
    "One Piece: Mugiwara no Ichimi \u2013 Minna e \u201cTearai, Suimin o!\u201d Kodomo-tachi Ouen SP",
    "Gintama.: Porori-hen",
    "Gintama.: Shirogane no Tamashii-hen",
    "Hunter x Hunter (2011)",
    "Huoyan Shan Lixian Ji",
    "Huyao Xiao Hongniang Movie: Xia Sha",
    "Fullmetal Alchemist",
    "Fushigi Dagashiya: Zenitendou Movie - Tsuri Taiyaki",
    "Mirai Shounen Conan 2: Taiga Daibouken",
    "MIRROR",
    "Pokemon Housoukyoku",
    "Pokemon (2019)",
    "Sword Art Online Alternative: Gun Gale Online",
    "Sword Art Online II",
    "Sword Art Online: Alicization",
    "Sylvanian Families: Freya no Happy Diary",
    "Sylvanian Families: Mini Story",
    "Kino no Tabi: The Beautiful World - The Animated Series",
    "Kanon",
    "Clannad Movie",
    "Toaru Majutsu no Index Movie: Endymion no Kiseki",
    "Toaru Majutsu no Index II",
    "Ano Hi Mita Hana no Namae wo Bokutachi wa Mada Shiranai. Movie",
    "Cowboy Bebop: Tengoku no Tobira",
    "Suzumiya Haruhi no Shoushitsu",
    "Koukaku Kidoutai Nyuumon Arise",
    "Koukaku Kidoutai Arise: Alternative Architecture",
    "Koukaku Kidoutai: Stand Alone Complex - Tachikoma na Hibi (TV)",
    "Koukaku Kidoutai: Stand Alone Complex 2nd GIG",
    "Yu\u2606Gi\u2606Oh! 5D's",
    "Yu\u2606Gi\u2606Oh! Arc-V",
    "Yu\u2606Gi\u2606Oh! (Movie)",
    "Yu\u2606Gi\u2606Oh! Duel Monsters ALEX",
    "Yu\u2606Gi\u2606Oh! Go Rush!",
    "Yu\u2606Gi\u2606Oh! Go Rush!!",
    "Yu\u2606Gi\u2606Oh! Sevens",
    "Yu\u2606Gi\u2606Oh! VRAINS",
    "Yu\u2606Gi\u2606Oh! Zexal",
    "Yu\u2606Gi\u2606Oh! Zexal Second",
    "InuYasha: Kanketsu-hen",
    "Lupin the Third: Mine Fujiko to Iu Onna",
    "Hidan no Aria AA",
    "Higashi no Eden: Air Communication",
    "Higurashi no Naku Koro ni Gou",
    "Higurashi no Naku Koro ni Sotsu",
    "Himawari!!",
    "Zutto Mae kara Suki deshita. Kokuhaku Jikkou Iinkai",
    "Fairy Tail: 100 Years Quest",
    "Hong Mao Lan Tu MTV",
    "Fate\/stay night: Unlimited Blade Works",
    "Fate\/Zero",
    "Fate\/Zero Cafe",
    
    # Similar synonyms 
    "Shi Er Shengxiao: Fuxing Gao Zhao Zhu Xiao Ba",
    "Fuxing Ba Jie",
    "Onigiri",
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
    "Gundam",
    "Kimetsu no Yaiba",
    "Boku no Hero Academia",
    "Bleach",
    "Dragon Ball",
    "Attack on Titan",
    "Code Geass",
    "Made in Abyss",
    "One Piece",
    "JoJo's Bizarre Adventure",
    "YuYu Hakusho",
    "Haikyu!!",
    "Gintama",
    "Hunter x Hunter",
    "Fullmetal Alchemist",
    "Mirai Shounen Conan",
    "Pokemon",
    "Pororo",
    "Power Battle Watch Car",
    "Precure",
    "Sword Art Online",
    "Sylvanian Families",
    "Kino no Tabi",
    "Gekijouban",
    "Ginga Tetsudou",
    "GHOST IN THE SHELL",
    "Ghost in the Shell",
    "Yu\u2606Gi\u2606Oh!",
    "InuYasha",
    "Lupin III",
    "Hibike! Euphonium",
    "Himitsu no Akko-chan",
    "Himitsukessha Taka no Tsume",
    "Hinomaru Hatanosuke"
]

# Skip these entries if it's a TV and contains one of these:
skip_tv_entries = [
    "Huo Xing Wa",
    "Huoli Shaonian Wang",
    "Huoxing Wa",
    "Pocket Monsters XY",
    "Pororo",
    "Hime Chen",
    "Himitsu no Akko-chan",
    "Himitsukessha Taka no Tsume"
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

data = json.load(f)
parsed = [] # list of parsed names

for i in data['data']:

    # Only keep movies or TV shows
    if i['type'] == 'MOVIE' or i['type'] == 'TV':

        skip_loop = False

        # Remove extra unwanted entries if it's in the title
        if i['title'] in remove_anime:
            continue
        
        # Remove unwanted entries if it's in the title AND a movie
        if i['type'] == 'MOVIE':
            for movies in skip_movie_entries:
                if movies in i['title']:
                    skip_loop = True
                    break

        if skip_loop == True:
            continue

        # Remove unwanted entries if it's in the title AND a TV
        if i['type'] == 'TV':
            for tv in skip_tv_entries:
                if tv in i['title']:
                    skip_loop = True
                    break
        
        if skip_loop == True:
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
