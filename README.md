# scrapy

## Needed Python Packages (pip install package)
1. pymongo
2. scrapy-deltafetch
3. scrapy-magicfields
4. scrapy-mongodb

## Needed Applications for testing server 
1. Berkeley DB "For DeltaFetch"
2. MongoDB "For crawl data"
3. docker.io

## Docker Image for Splash "Ajax crawl"
docker run -p 8050:8050 scrapinghub/splash &
