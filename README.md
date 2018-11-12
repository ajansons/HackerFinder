# HackerFinder 🔎

Find suspicious kills in PUBG games using data from the developer API.

## Usage
```
hackerfinder [-h] (-f FILE | -m MATCH_ID | -r | -p PLAYER_NAME) [-k API_KEY]

optional arguments:
  -h, --help                   show this help message and exit
  -f, --file FILE              analyse a telemetry data JSON file
  -m, --match MATCH_ID         retrieve and analyse a single match
  -r, --random                 retrieve and analyse a random sample of matches. Requires API key (-k)
  -p, --player PLAYER_NAME     retrieve and analyse the matches of a player. Requires API key (-k)
  -k, --key API_KEY            set the API key that'll be used to authenticate with the developer API
```