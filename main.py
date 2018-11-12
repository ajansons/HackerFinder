import argparse
import requests
from hacker_finder import HackerFinder
from telem_manager import TelemManager
from api import Api

parser = argparse.ArgumentParser(prog='hackerfinder', description='Find suspicious kills in PUBG game data.Find suspicious kills in PUBG games using data from the developer API.')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-f', '--file', dest='filename', type=argparse.FileType(),
                    help='analyse a telemetry data JSON file', metavar='FILE')
group.add_argument('-m', '--match', dest='match_id', metavar='MATCH_ID',
                    help='retrieve and analyse a single match')
group.add_argument('-r', '--random', dest='random', action='store_true',
                    help='retrieve and analyse a random sample of matches. Requires an API key (-k)')
group.add_argument('-p', '--player', dest='player_name', metavar='PLAYER_NAME',
                    help='retrieve and analyse the matches of a player. Requires an API key (-k)')
parser.add_argument('-k', '--key', dest='api_key', metavar='API_KEY',
                    help='set the API key that\'ll be used to authenticate with the developer API')
args = parser.parse_args()

def analyse_match(telem):
    finder = HackerFinder(telem)
    suspicious_assaults = finder.find_suspcious_assaults()
    if suspicious_assaults:
        print('Match ID: %s\n%s' % (telem.get_match_id(), '=' * 50))
        for assault in suspicious_assaults:
            print(finder.summarise_assault(assault))

def analyse_matches(match_ids):
    for match_id in match_ids:
        try:
            data = api.get_telem_data_by_match_id(match_id)
            telem = TelemManager(data)
            analyse_match(telem)
        except requests.exceptions.ContentDecodingError:
            pass # Sometimes the compression resp header is wrong

def analyse_file(filename):
    telem = TelemManager(file=filename)
    analyse_match(telem)

def analyse_match_by_id(match_id):
    data = Api().get_telem_data_by_match_id(match_id)
    telem = TelemManager(data)
    analyse_match(telem)

def analyse_random_matches(api_key):
    api = Api(api_key)
    match_ids = api.get_sample_match_ids()
    anallyse_matches(match_ids)

if args.filename is not None:
    analyse_file(args.filename)
elif args.match_id is not None:
    analyse_match_by_id(args.match_id)
elif args.random:
    if (args.api_key is None):
        parser.error('Anlysing random matches requires the API key to be set, use the --key argument.')
    else:
        analyse_random_matches(args.api_key)
elif args.player_name is not None:
    if (args.api_key is None):
        parser.error('Looking up matches by player name requires the API key to be set, use the --key argument.')
    api = Api(args.api_key)
    match_ids = api.get_match_ids_by_player(args.player_name)
    analyse_matches(match_ids)
else:
    # This shouldn't happen
    raise RuntimeError
