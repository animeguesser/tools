# Get-MAL
Using the MyAnimeList API, we will want to get the top relevant animes. This will help us parse down a list that is smaller in size and since we we most likely be choosing more popular animes.
We query the MyAnimeList API for the top animes and top movies. We will try to request the top 5000 animes and the top 250 movies based on the MAL rating. After further parsing, this should be
a sufficent list for our needs.

Upon completion of the script, it will output a file `mal.json` that can be used in the next python script.

## Running
You must use your MyAnimeList API as an environment variable under the key `MAL_CLIENT_ID`.

Example in linux:
```
export MAL_CLIENT_ID='abc1234'
```

You can then run the script as a normal python script and it will product an output file in JSON for you.

# Match MAL offline db
Using the anime database list from: https://github.com/manami-project/anime-offline-database, this python script will match the animes from the top MyAnimeList ratings to items within the offline database.We want to use the offline database as it contains synonyms that animes could be called instead of their titles. 

For example, the anime "Your Name" is actually titled "Kimi no Na wa."; but unless you specificallyknow that it is using the romanji name rather than the English name, you'll never be able to find the anime in our list. Because of this, we want to be able to search through the synonyms as well as the the titles to match our animes. We will **always** use the title to verify the submission on guesses, but we want users to be able to put in other titles they may have heard before.

You will need both the `mal.json` file from the `get-mal.py` script and the aboved mention `anime-offline-database.json` script. Once ran, it will produce a new file: `matched-animed-list.json`. It will also print to console any animes that we not found in the offline database (maybe due to different title names) and you have the option to add those manually.

# Anime list parser
Using the previous scripts, you will need to have the `matched-anime-list.json` file in order to use this parser. Since there are a lot of animes that have multiple seasons or similar names to what we want to select, we need to make several lists of items we **do not** wish to be in the final list. For example, we do not want both "Kaguya-sama wa Kokurasetai: Ultra Romantic" (Which is Season 3) and 
"Kaguya-sama wa Kokurasetai? Tensai-tachi no Renai Zunousen" (which is Season 2) in our search results. This makes it confusing for the end user as there are several animes with the same name but we only match to one exact one. This list isn't perfect and should be constantly updated and filter to make search results better.

As there are not a lot of relevant fields, it will strip the non-relevant fields such as `tags` or `picture`. It will also parse out anything that isn't a `TV` show or a `Movie`. 
This means that it will not have anything such as `OVAs` or `Specials`. We also strip any `synonyms` of any lines that have unicode characters as we do not support any unicode for our titles.

Doing this parsing, we can keep our needed information to a minimal. The file size reduction is over 10x!

This script will output two different files: `parsed-anime-list.json` and `parsed-anime-list-mini.json`. The `mini` version will be smaller in size but without formatting, ideal for our use case.
The larger version with indentation will be better for readability.

## Running
First, you will need to download the offline database from: https://github.com/manami-project/anime-offline-database

```
wget https://github.com/manami-project/anime-offline-database/raw/master/anime-offline-database.json
```

Assuming you have `python` installed, you will need to install `pandas`.

```
pip install pandas
```

Now you can run the python script and it will parse and output two files.
```
python ./parse-anime.py
```