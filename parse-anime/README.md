# Anime list parser
Using the anime database list from: https://github.com/manami-project/anime-offline-database, this python script will parse and shorten the anime list to only ones needed for this project.

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