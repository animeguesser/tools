# Tools and functions

This repo contains tools and functions that are apart of the animeguess project.

## parse-anime
A python script that will parse an anime list from: https://github.com/manami-project/anime-offline-database into a format that the animeguesser project can use.

More information can be found within the [parse-anime](./parse-anime) folder.

## daily-s3-move
A python script that is deployed into AWS Lambda that will nightly move files from the private future days S3 bucket into the present available S3 bucket.